from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

from tools.site_manager.frontmatter import split_front_matter


REPO_ROOT = Path(__file__).parents[3]


def page(path: str) -> tuple[dict, str]:
    metadata, body, present = split_front_matter((REPO_ROOT / path).read_text(encoding="utf-8-sig"))
    assert present
    return dict(metadata), body


def test_image_processing_uses_three_stable_pages() -> None:
    home_meta, home = page("_pages/courses/image-processing.md")
    gonzalez_meta, gonzalez = page("_pages/courses/image-processing-gonzalez.md")
    student_meta, student = page("_pages/courses/image-processing-student-work.md")

    assert home_meta["permalink"] == "/teaching/image-processing/"
    assert gonzalez_meta["permalink"] == "/teaching/image-processing/gonzalez/"
    assert student_meta["permalink"] == "/teaching/image-processing/student-work/"
    assert home.count("/teaching/image-processing/gonzalez/") == 1
    assert home.count("/teaching/image-processing/student-work/") == 1
    assert "teaching_course_materials.liquid" not in home
    assert 'view="packages"' in gonzalez
    assert 'view="student_work"' in student


def test_image_processing_keeps_one_course_record_and_local_cover() -> None:
    courses = YAML(typ="safe").load((REPO_ROOT / "_data" / "teaching_courses.yml").read_text(encoding="utf-8-sig"))
    matches = [item for item in courses if item.get("id") == "image-processing"]
    assert len(matches) == 1
    image = str(matches[0]["image"])
    assert image.startswith("/assets/img/")
    assert (REPO_ROOT / image.lstrip("/")).is_file()


def test_student_work_registry_starts_without_sample_content() -> None:
    works = YAML(typ="safe").load((REPO_ROOT / "_data" / "teaching_student_works.yml").read_text(encoding="utf-8-sig")) or []
    assert isinstance(works, list)
    assert works == []
