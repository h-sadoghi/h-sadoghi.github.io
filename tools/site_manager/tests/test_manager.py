from __future__ import annotations

from pathlib import Path
from io import BytesIO
import zipfile

import pytest
from ruamel.yaml import YAML

from tools.site_manager import SiteManager
from tools.site_manager.assets import AssetInput
from tools.site_manager.frontmatter import split_front_matter
from tools.site_manager.utils import SiteManagerError
import tools.site_manager.manager as manager_module


def zip_bytes(entries: dict[str, bytes]) -> bytes:
    stream = BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    return stream.getvalue()


def seed_image_processing(repo: Path) -> None:
    (repo / "_data" / "teaching_courses.yml").write_text(
        "- id: image-processing\n"
        "  title: Image Processing\n"
        "  url: /teaching/image-processing/\n"
        "  link_type: internal\n",
        encoding="utf-8",
    )
    (repo / "_data" / "teaching_packages.yml").write_text(
        "- id: gonzalez\n"
        "  course_id: image-processing\n"
        "  title: Gonzalez — جزوه‌ها و فایل‌های آموزشی\n"
        "  chapters: []\n",
        encoding="utf-8",
    )
    (repo / "_data" / "teaching_student_works.yml").write_text("[]\n", encoding="utf-8")


def test_preview_persian_markdown_with_two_images_is_read_only(repo: Path) -> None:
    manager = SiteManager(repo)
    before = sorted(path.relative_to(repo) for path in repo.rglob("*"))
    body = "# تبدیل فوریه\n\n![اول](first image.png)\n\n![دوم](second.png)\n"
    plan = manager.preview_add(
        "teaching_signals",
        {"title": "تبدیل فوریه گسسته", "author": "دانشجو", "status": "draft"},
        body,
        [AssetInput("first image.png", b"\x89PNG\r\n\x1a\none"), AssetInput("second.png", b"\x89PNG\r\n\x1a\ntwo")],
    )
    after = sorted(path.relative_to(repo) for path in repo.rglob("*"))
    assert before == after
    assert plan.validation.ok
    assert not plan.conflicts
    assert plan.target_path == "_pages/resources/teaching-signals-تبدیل-فوریه-گسسته.md"
    text = plan.changes[0].content.decode()
    assert "/assets/img/content/تبدیل-فوریه-گسسته/first-image.png" in text
    assert "/assets/img/content/تبدیل-فوریه-گسسته/second.png" in text
    assert any(change.path == "_data/legacy_resources.yml" for change in plan.changes)


def test_imported_frontmatter_can_supply_title(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add(
        "resource",
        {"status": "draft"},
        "---\ntitle: عنوان واردشده\n---\n\nمتن\n",
    )
    assert plan.target_path.endswith("resource-عنوان-واردشده.md")


def test_apply_requires_confirmation_and_creates_backup_manifest(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add("project", {"title": "Safe Project", "status": "ready"}, "Project body")
    with pytest.raises(SiteManagerError, match="تأیید"):
        manager.add(plan)
    result = manager.add(plan, confirm=True)
    target = repo / "_projects" / "safe-project.md"
    assert target.is_file()
    assert result["validation"]["ok"]
    assert (repo / result["backup"] / "operation.json").is_file()


def test_draft_is_not_published(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add("resource", {"title": "Draft Item", "status": "draft"}, "Draft")
    metadata, _, _ = split_front_matter(plan.changes[0].content.decode())
    assert metadata["published"] is False
    assert any("draft" in warning for warning in plan.validation.warnings)


def test_draft_post_uses_date_filename_and_stays_unpublished(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add(
        "blog_post",
        {"title": "Draft Post", "date": "2026-10-19", "status": "draft"},
        "Post body",
    )
    assert plan.target_path == "_posts/2026-10-19-draft-post.md"
    metadata, _, _ = split_front_matter(plan.changes[0].content.decode())
    assert metadata["published"] is False


def test_new_post_gets_today_when_custom_date_is_hidden(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add("blog_post", {"title": "Automatic date"}, "Post body")
    metadata, _, _ = split_front_matter(plan.changes[0].content.decode())
    assert metadata["date"]
    assert metadata["published"] is True


def test_duplicate_title_is_reported(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add("resource", {"title": "Existing Page", "status": "ready"}, "Another")
    assert any("عنوان مشابه" in conflict for conflict in plan.conflicts)
    with pytest.raises(SiteManagerError):
        manager.add(plan, confirm=True)


def test_edit_preserves_permalink_code_math_and_liquid(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_edit("_pages/existing.md", {"title": "عنوان تازه", "status": "ready"})
    text = plan.changes[0].content.decode()
    metadata, body, _ = split_front_matter(text)
    assert metadata["permalink"] == "/existing/"
    assert metadata["title"] == "عنوان تازه"
    assert "$x^2$" in body
    assert "{% include figure.liquid" in body
    assert "```python" in body


def test_edit_fragment_preserves_absence_of_frontmatter(repo: Path) -> None:
    fragment = repo / "_pages" / "person.md"
    fragment.write_text("# Person\n\nOriginal body.\n", encoding="utf-8")
    manager = SiteManager(repo)
    plan = manager.preview_edit("_pages/person.md", {}, "# Person\n\nUpdated body.\n")
    text = plan.changes[0].content.decode()
    assert not text.startswith("---")
    assert "Updated body" in text


def test_publication_duplicate_doi_and_key_are_blocked(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add(
        "publication",
        {"bibtex": "@article{known2024, title={Other}, year={2025}, doi={https://doi.org/10.1000/known}}"},
    )
    assert any("کلید BibTeX تکراری" in item for item in plan.conflicts)
    assert any("DOI تکراری" in item for item in plan.conflicts)


def test_new_publication_is_valid(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_add(
        "publication",
        {"bibtex": "@article{new2025, title={A New Work}, author={Author, B}, year={2025}, doi={10.1000/new}}"},
    )
    assert plan.validation.ok
    assert not plan.conflicts


def test_unknown_route_is_refused(repo: Path) -> None:
    manager = SiteManager(repo)
    with pytest.raises(SiteManagerError, match="ناشناخته"):
        manager.preview_add("made-up", {"title": "No"}, "")


def test_fake_image_is_refused(repo: Path) -> None:
    manager = SiteManager(repo)
    with pytest.raises(SiteManagerError, match="سازگار نیست"):
        manager.preview_add("resource", {"title": "Unsafe", "status": "draft"}, "", [AssetInput("fake.png", b"not-png")])


def test_edit_refuses_path_outside_repo(repo: Path) -> None:
    manager = SiteManager(repo)
    with pytest.raises(SiteManagerError, match="خارج از مخزن"):
        manager.preview_edit("../outside.md", {"title": "No"})


def test_new_course_creates_data_and_page_then_accepts_material(repo: Path) -> None:
    manager = SiteManager(repo)
    before = sorted(path.relative_to(repo) for path in repo.rglob("*"))
    plan = manager.preview_course(
        {
            "title": "Image Processing",
            "description": "Course materials.",
            "chapters": "Introduction\nExercises",
            "status": "draft",
        }
    )
    assert plan.validation.ok
    assert not plan.conflicts
    assert plan.target_path == "_pages/courses/image-processing.md"
    assert before == sorted(path.relative_to(repo) for path in repo.rglob("*"))
    course_data = YAML(typ="safe").load(plan.changes[0].content.decode())[0]
    assert course_data["image"] == "/assets/img/courses/default-course.svg"
    assert course_data["url"] == "/teaching/image-processing/"
    assert course_data["order"] == 1
    assert course_data["link_type"] == "internal"
    _, course_body, _ = split_front_matter(plan.changes[1].content.decode())
    assert "Course materials." not in course_body
    manager.add(plan, confirm=True)
    assert (repo / "_data" / "teaching_courses.yml").is_file()
    assert (repo / "_pages" / "courses" / "image-processing.md").is_file()
    assert any(choice["name"] == "course:image-processing" for choice in manager.route_choices())

    material = manager.preview_add(
        "course:image-processing",
        {"title": "First lesson", "chapter": "introduction", "status": "draft"},
        "# First lesson\n",
    )
    assert material.validation.ok
    assert material.target_path == "_pages/resources/teaching-image-processing-first-lesson.md"
    metadata, _, _ = split_front_matter(material.changes[0].content.decode())
    assert metadata["course_id"] == "image-processing"
    assert metadata["chapter_id"] == "introduction"

    duplicate = manager.preview_course({"title": "Image Processing", "status": "draft"})
    assert duplicate.conflicts


def test_new_course_stores_selected_image_in_same_change_plan(repo: Path) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_course(
        {"title": "Computer Vision", "description": "Visual computing.", "status": "draft"},
        [AssetInput("course cover.jpg", b"\xff\xd8\xffcourse-image")],
    )
    assert plan.validation.ok
    assert not plan.conflicts
    assert len(plan.changes) == 3
    assert plan.changes[2].path == "assets/img/courses/computer-vision/course-cover.jpg"
    data = YAML(typ="safe").load(plan.changes[0].content.decode())[0]
    assert data["image"] == "/assets/img/courses/computer-vision/course-cover.jpg"
    assert data["published"] is False
    assert not (repo / "_pages" / "courses" / "computer-vision.md").exists()


def test_course_save_rolls_back_when_one_file_cannot_be_written(repo: Path, monkeypatch) -> None:
    manager = SiteManager(repo)
    plan = manager.preview_course({"title": "Rollback Course", "status": "draft"})
    real_atomic_write = manager_module.atomic_write
    calls = 0

    def fail_second_write(path: Path, data: bytes) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated write failure")
        real_atomic_write(path, data)

    monkeypatch.setattr(manager_module, "atomic_write", fail_second_write)
    with pytest.raises(SiteManagerError, match="بازگردانده شدند"):
        manager.add(plan, confirm=True)
    assert not (repo / "_data" / "teaching_courses.yml").exists()
    assert not (repo / "_pages" / "courses" / "rollback-course.md").exists()


def test_read_content_exposes_existing_values_without_changing_them(repo: Path) -> None:
    manager = SiteManager(repo)
    item = manager.read_content("_pages/existing.md")
    assert item["title"] == "Existing Page"
    assert item["published"] is True
    assert "$x^2$" in item["body"]
    plan = manager.preview_edit("_pages/existing.md", {}, item["body"])
    metadata, _, _ = split_front_matter(plan.changes[0].content.decode())
    assert metadata["published"] is True


def test_course_package_is_atomic_and_updates_existing_course_collection(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    archive = AssetInput("Gonzalez Chapter 1.zip", zip_bytes({"chapter-1/notes.txt": b"sample"}))
    pdf = AssetInput("chapter 1.pdf", b"%PDF-1.4\n%%EOF\n")

    plan = manager.preview_course_package(
        {
            "course_id": "image-processing",
            "collection_id": "gonzalez",
            "chapter_number": "1",
            "chapter_title": "Digital Image Fundamentals",
            "summary": "Sampling, quantization, and image representation.",
        },
        archive,
        pdf,
    )

    assert plan.validation.ok
    assert not plan.conflicts
    assert plan.target_path == "assets/downloads/courses/image-processing/gonzalez/chapter-01/chapter-01.zip"
    assert [change.path for change in plan.changes] == [
        "_data/teaching_packages.yml",
        "assets/downloads/courses/image-processing/gonzalez/chapter-01/chapter-01.zip",
        "assets/downloads/courses/image-processing/gonzalez/chapter-01/chapter-01.pdf",
    ]
    manager.add(plan, confirm=True)
    data = YAML(typ="safe").load((repo / "_data" / "teaching_packages.yml").read_text(encoding="utf-8"))
    chapter = data[0]["chapters"][0]
    assert chapter["number"] == 1
    assert chapter["summary"] == "Sampling, quantization, and image representation."
    assert chapter["published"] is True
    assert chapter["zip_url"].endswith("/chapter-01.zip")
    assert chapter["pdf_url"].endswith("/chapter-01.pdf")
    assert (repo / chapter["zip_url"].lstrip("/")).read_bytes() == archive.data


def test_course_package_replacement_requires_explicit_choice_and_is_backed_up(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    fields = {
        "course_id": "image-processing",
        "collection_id": "gonzalez",
        "chapter_number": "2",
        "chapter_title": "Image Enhancement",
    }
    first = manager.preview_course_package(fields, AssetInput("first.zip", zip_bytes({"first.txt": b"v1"})))
    manager.add(first, confirm=True)

    blocked = manager.preview_course_package(fields, AssetInput("second.zip", zip_bytes({"second.txt": b"v2"})))
    assert any("جایگزینی" in conflict for conflict in blocked.conflicts)
    with pytest.raises(SiteManagerError, match="تعارض"):
        manager.add(blocked, confirm=True)

    replacement = manager.preview_course_package(
        {**fields, "replace": "yes"}, AssetInput("second.zip", zip_bytes({"second.txt": b"v2"}))
    )
    result = manager.add(replacement, confirm=True)
    zip_path = repo / "assets/downloads/courses/image-processing/gonzalez/chapter-02/chapter-02.zip"
    backup = repo / result["backup"] / zip_path.relative_to(repo)
    assert zip_path.read_bytes() != backup.read_bytes()
    assert zipfile.ZipFile(zip_path).namelist() == ["second.txt"]


def test_course_package_rejects_unsafe_zip_member(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    with pytest.raises(SiteManagerError, match="مسیر داخلی ZIP ایمن نیست"):
        manager.preview_course_package(
            {
                "course_id": "image-processing",
                "collection_id": "gonzalez",
                "chapter_number": "3",
                "chapter_title": "Unsafe",
            },
            AssetInput("unsafe.zip", zip_bytes({"../outside.txt": b"no"})),
        )


def test_course_package_does_not_create_duplicate_course(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    plan = manager.preview_course_package(
        {
            "course_id": "image-processing",
            "collection_id": "gonzalez",
            "chapter_number": "4",
            "chapter_title": "Restoration",
        },
        AssetInput("chapter.zip", zip_bytes({"readme.txt": b"ok"})),
    )
    assert all(change.path != "_data/teaching_courses.yml" for change in plan.changes)
    assert all(not change.path.startswith("_pages/courses/") for change in plan.changes)


def test_student_work_requires_owner_approval(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    with pytest.raises(SiteManagerError, match="تأیید صریح"):
        manager.preview_student_work(
            {"course_id": "image-processing", "title": "Edge detector", "summary": "A sample project."},
            AssetInput("project.zip", zip_bytes({"README.md": b"sample"})),
        )


def test_student_work_is_atomic_publication_and_duplicates_are_blocked(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    archive = AssetInput("project.zip", zip_bytes({"src/main.py": b"print('ok')"}))
    fields = {
        "course_id": "image-processing",
        "title": "Edge Detector",
        "summary": "A reproducible edge-detection exercise.",
        "students": "Student A",
        "term": "Fall 2026",
        "owner_approved": "yes",
    }
    plan = manager.preview_student_work(fields, archive, AssetInput("report.pdf", b"%PDF-1.4\n%%EOF\n"))
    assert plan.validation.ok
    assert not plan.conflicts
    assert plan.operation == "student_work"
    assert plan.proposed_url == "/teaching/image-processing/student-work/#edge-detector"
    manager.add(plan, confirm=True)
    data = YAML(typ="safe").load((repo / "_data" / "teaching_student_works.yml").read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["published"] is True
    assert data[0]["students"] == "Student A"
    assert (repo / data[0]["zip_url"].lstrip("/")).read_bytes() == archive.data

    duplicate = manager.preview_student_work(fields, archive)
    assert duplicate.conflicts
    with pytest.raises(SiteManagerError, match="تعارض"):
        manager.add(duplicate, confirm=True)


def test_existing_course_cover_is_replaced_without_creating_course(repo: Path) -> None:
    seed_image_processing(repo)
    manager = SiteManager(repo)
    plan = manager.preview_course_cover(
        {"course_id": "image-processing"},
        AssetInput("image processing.jpg", b"\xff\xd8\xffcourse-cover"),
    )
    assert plan.validation.ok
    assert not plan.conflicts
    assert [change.path for change in plan.changes] == [
        "_data/teaching_courses.yml",
        "assets/img/courses/image-processing/image-processing.jpg",
    ]
    data = YAML(typ="safe").load(plan.changes[0].content.decode("utf-8"))
    assert len(data) == 1
    assert data[0]["image"] == "/assets/img/courses/image-processing/image-processing.jpg"
    assert all(not change.path.startswith("_pages/courses/") for change in plan.changes)
