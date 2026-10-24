from __future__ import annotations

import json
import zipfile
from pathlib import Path

import nbformat
import pytest

from tools.jupyterbook_manager.manager import BookManager, ManagerError


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "مخزن دارای فاصله"
    (root / ".git").mkdir(parents=True)
    tool = root / "tools/jupyterbook_manager"
    tool.mkdir(parents=True)
    tool.joinpath("books.yml").write_text(
        "version: 1\nbooks:\n  - id: image-processing\n    title: Image Processing\n"
        "    source: courses/image-processing/book\n"
        "    public_path: /teaching/image-processing/book/\n"
        "    jekyll_destination: _site/teaching/image-processing/book\n",
        encoding="utf-8",
    )
    book = root / "courses/image-processing/book"
    (book / "gonzalez").mkdir(parents=True)
    (book / "student-work").mkdir()
    (book / "_config.yml").write_text(
        'title: Test\nexecute:\n  execute_notebooks: "off"\n', encoding="utf-8"
    )
    (book / "_toc.yml").write_text(
        "format: jb-book\nroot: index\nchapters:\n  - file: gonzalez/index\n  - file: student-work/index\n",
        encoding="utf-8",
    )
    (book / "index.md").write_text("# کتاب فارسی\n\n## English heading\n", encoding="utf-8")
    (book / "gonzalez/index.md").write_text("# Gonzalez\n", encoding="utf-8")
    (book / "student-work/index.md").write_text("# Student Work\n", encoding="utf-8")
    return root


def test_validate_and_tree(repo: Path) -> None:
    manager = BookManager(repo)
    report = manager.validate("image-processing")
    assert report.ok, report.errors
    assert [row[1] for row in manager.tree("image-processing")] == [
        "index",
        "gonzalez/index",
        "student-work/index",
    ]


def test_add_markdown_is_dry_run_then_atomic(repo: Path, tmp_path: Path) -> None:
    source = tmp_path / "فصل اول.md"
    source.write_text("# فصل اول\n\nرابطه $x^2$.\n", encoding="utf-8")
    manager = BookManager(repo)
    plan = manager.plan_add(
        "image-processing",
        source,
        "gonzalez/chapter-01.md",
        "gonzalez/index",
        title="فصل اول",
        description="توضیح کوتاه",
    )
    assert not (repo / "courses/image-processing/book/gonzalez/chapter-01.md").exists()
    assert "gonzalez/chapter-01" in plan.diff
    backup = manager.apply(plan)
    assert backup.is_dir()
    assert (repo / "courses/image-processing/book/gonzalez/chapter-01.md").is_file()
    metadata = (repo / "courses/image-processing/book/_content.yml").read_text(encoding="utf-8")
    assert "توضیح کوتاه" in metadata
    assert manager.validate("image-processing").ok
    with pytest.raises(ManagerError, match="از قبل"):
        manager.plan_add("image-processing", source, "gonzalez/chapter-01.md", "gonzalez/index")


def test_notebook_is_validated_but_never_executed(repo: Path, tmp_path: Path) -> None:
    marker = tmp_path / "must-not-exist.txt"
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell("# Notebook فارسی"),
            nbformat.v4.new_code_cell(f"open({str(marker)!r}, 'w').write('executed')", execution_count=None),
        ]
    )
    source = tmp_path / "sample.ipynb"
    nbformat.write(notebook, source)
    manager = BookManager(repo)
    plan = manager.plan_add("image-processing", source, "student-work/sample.ipynb", "student-work/index")
    manager.apply(plan)
    assert not marker.exists()
    assert manager.validate("image-processing").ok
    with pytest.raises(ManagerError, match="آگاهانه"):
        manager.execute_copy("image-processing", "student-work/sample", "NO")


def test_apply_detects_change_after_preview(repo: Path, tmp_path: Path) -> None:
    source = tmp_path / "chapter.md"
    source.write_text("# Chapter\n", encoding="utf-8")
    manager = BookManager(repo)
    plan = manager.plan_add("image-processing", source, "gonzalez/chapter.md", "gonzalez/index")
    toc = repo / "courses/image-processing/book/_toc.yml"
    toc.write_text(toc.read_text(encoding="utf-8") + "\n# concurrent change\n", encoding="utf-8")
    with pytest.raises(ManagerError, match="پس از Preview تغییر"):
        manager.apply(plan)


def test_rejects_traversal_and_invalid_execution_mode(repo: Path, tmp_path: Path) -> None:
    source = tmp_path / "test.md"
    source.write_text("# Test\n", encoding="utf-8")
    manager = BookManager(repo)
    with pytest.raises(ManagerError, match="ایمن نیست"):
        manager.plan_add("image-processing", source, "../escape.md")
    config = repo / "courses/image-processing/book/_config.yml"
    config.write_text("execute:\n  execute_notebooks: force\n", encoding="utf-8")
    assert any("off" in item for item in manager.validate("image-processing").errors)


def test_safe_zip_asset_and_stage(repo: Path, tmp_path: Path) -> None:
    archive = tmp_path / "lesson.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("notes/readme.txt", "safe")
    manager = BookManager(repo)
    plan = manager.plan_asset("image-processing", archive, "gonzalez/index", "فایل فصل")
    assert "/assets/downloads/courses/image-processing/jupyter-book/" in plan.diff
    manager.apply(plan)
    assert manager.validate("image-processing").ok

    output = repo / "courses/image-processing/book/_build/html"
    (output / "_static").mkdir(parents=True)
    (output / "index.html").write_text("book", encoding="utf-8")
    (output / "_static/webpack-macros.html").write_text("{{ pathto('x') }}", encoding="utf-8")
    site = repo / "_site"
    site.mkdir()
    destination = manager.stage("image-processing", site)
    assert (destination / "index.html").read_text(encoding="utf-8") == "book"
    assert not (destination / "_static/webpack-macros.html").exists()


def test_rejects_zip_traversal(repo: Path, tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("../escape.txt", "unsafe")
    manager = BookManager(repo)
    with pytest.raises(ManagerError, match="ایمن نیست"):
        manager.plan_asset("image-processing", archive, "gonzalez/index")


def test_registry_and_book_are_in_one_repository(repo: Path) -> None:
    manager = BookManager(repo)
    book = manager.book("image-processing")
    assert repo.resolve() in book["root"].parents
    assert not list(book["root"].rglob(".git"))
    assert json.loads(json.dumps(manager.books()))[0]["id"] == "image-processing"
