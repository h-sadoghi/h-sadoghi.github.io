from __future__ import annotations

import subprocess
from pathlib import Path

from ruamel.yaml import YAML

from tools.jupyterbook_manager.manager import BookManager


REPO = Path(__file__).resolve().parents[3]


def test_real_book_is_valid_and_inside_main_repository() -> None:
    manager = BookManager(REPO)
    report = manager.validate("image-processing")
    assert report.ok, report.errors
    book_root = manager.book("image-processing")["root"]
    top = Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=book_root, text=True).strip()
    ).resolve()
    assert top == REPO.resolve()
    assert not list(book_root.rglob(".git"))
    assert not (REPO / ".gitmodules").exists()


def test_jekyll_excludes_raw_book_and_keeps_existing_urls() -> None:
    config = YAML(typ="safe").load((REPO / "_config.yml").read_text(encoding="utf-8"))
    assert "courses/" in config["exclude"]
    pages = {
        "image-processing.md": "/teaching/image-processing/",
        "image-processing-gonzalez.md": "/teaching/image-processing/gonzalez/",
        "image-processing-student-work.md": "/teaching/image-processing/student-work/",
    }
    for filename, url in pages.items():
        text = (REPO / "_pages/courses" / filename).read_text(encoding="utf-8")
        assert f"permalink: {url}" in text
    home = (REPO / "_pages/courses/image-processing.md").read_text(encoding="utf-8")
    assert "/teaching/image-processing/book/" in home


def test_deploy_build_order_and_single_artifact() -> None:
    workflow = (REPO / ".github/workflows/deploy.yml").read_text(encoding="utf-8")
    jekyll = workflow.index("bundle exec jekyll build")
    purge = workflow.index("purgecss -c purgecss.config.js")
    book = workflow.index("build --book image-processing --clean")
    stage = workflow.index("stage --book image-processing --site-dir _site")
    deploy = workflow.index("folder: _site")
    assert jekyll < purge < book < stage < deploy
    assert workflow.count("JamesIves/github-pages-deploy-action") == 1
    assert "if: github.event_name != 'pull_request'" in workflow


def test_notebooks_are_off_in_book_config() -> None:
    config = YAML(typ="safe").load(
        (REPO / "courses/image-processing/book/_config.yml").read_text(encoding="utf-8")
    )
    assert config["execute"]["execute_notebooks"] == "off"
