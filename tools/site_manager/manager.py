from __future__ import annotations

import difflib
import json
import shutil
import time
import uuid
from dataclasses import asdict, dataclass, field
from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .assets import AssetInput, prepare_assets, rewrite_asset_links
from .bibliography import duplicate_messages
from .frontmatter import render_front_matter, split_front_matter
from .importer import import_markdown
from .inspector import RepositoryInspector
from .routes import RouteMap
from .utils import SiteManagerError, atomic_write, contained_path, file_sha256, safe_slug
from .validator import ValidationResult, Validator


@dataclass
class FileChange:
    path: str
    action: str
    content: bytes
    before_sha256: str | None
    diff: str = ""

    def public(self) -> dict:
        data = asdict(self)
        data.pop("content")
        data["size"] = len(self.content)
        return data


@dataclass
class ChangePlan:
    token: str
    operation: str
    route: str
    target_path: str
    proposed_url: str
    front_matter: dict[str, Any]
    changes: list[FileChange]
    validation: ValidationResult
    conflicts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def public(self) -> dict:
        return {
            "token": self.token,
            "operation": self.operation,
            "route": self.route,
            "target_path": self.target_path,
            "proposed_url": self.proposed_url,
            "front_matter": dict(self.front_matter),
            "changes": [change.public() for change in self.changes],
            "validation": self.validation.as_dict(),
            "conflicts": self.conflicts,
            "warnings": self.warnings,
        }


class SiteManager:
    """Small API used by the web UI and optional batch workflows."""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        if not (self.repo_root / "_config.yml").is_file() or not (self.repo_root / ".git").exists():
            raise SiteManagerError("مسیر انتخاب‌شده مخزن Jekyll مورد انتظار نیست.")
        self.routes = RouteMap(self.repo_root)
        self.inspector = RepositoryInspector(self.repo_root)
        self.validator = Validator(self.repo_root)
        self._plans: dict[str, ChangePlan] = {}
        site_config = YAML(typ="safe").load((self.repo_root / "_config.yml").read_text(encoding="utf-8-sig")) or {}
        self.default_author = " ".join(
            str(site_config.get(key) or "").strip() for key in ("first_name", "middle_name", "last_name")
        ).strip()

    def route_choices(self) -> list[dict[str, str]]:
        choices = [
            {
                "name": name,
                "label": str(route.get("label_fa", name)),
                "content_type": str(route.get("content_type", "")),
                "warning": str(route.get("warning_fa", "")),
            }
            for name, route in self.routes.routes.items()
        ]
        for course in self.courses():
            choices.insert(
                1,
                {
                    "name": f"course:{course['id']}",
                    "label": f"درس / {course['title']}",
                    "content_type": "teaching_note",
                    "warning": "",
                    "chapters": course.get("chapters", []),
                },
            )
        return choices

    def courses(self) -> list[dict[str, Any]]:
        path = self.repo_root / "_data" / "teaching_courses.yml"
        if not path.is_file():
            return []
        data = YAML(typ="safe").load(path.read_text(encoding="utf-8-sig")) or []
        if not isinstance(data, list):
            raise SiteManagerError("ساختار _data/teaching_courses.yml باید یک فهرست باشد.")
        return [dict(item) for item in data if isinstance(item, dict)]

    def read_content(self, relative_path: str) -> dict[str, Any]:
        target = contained_path(self.repo_root, relative_path)
        if not target.is_file() or target.suffix.lower() != ".md":
            raise SiteManagerError("فایل Markdown انتخاب‌شده پیدا نشد.")
        metadata, body, has_frontmatter = split_front_matter(target.read_text(encoding="utf-8-sig"))
        tags = metadata.get("tags", [])
        if isinstance(tags, list):
            tags = ", ".join(str(tag) for tag in tags)
        published = metadata.get("published")
        return {
            "path": relative_path,
            "title": str(metadata.get("title") or target.stem),
            "author": str(metadata.get("author") or ""),
            "date": str(metadata.get("date") or ""),
            "description": str(metadata.get("description") or ""),
            "tags": str(tags or ""),
            "lang": str(metadata.get("lang") or ""),
            "published": published,
            "published_label": "پیش‌نویس" if published is False else "آمادهٔ انتشار",
            "body": body,
            "has_frontmatter": has_frontmatter,
            "permalink": str(metadata.get("permalink") or ""),
        }

    def browse(self, query: str = "", content_type: str = "") -> list[dict]:
        return self.inspector.search(query, content_type)

    def _diff(self, path: str, before: bytes, after: bytes) -> str:
        old = before.decode("utf-8", errors="replace").splitlines(keepends=True)
        new = after.decode("utf-8", errors="replace").splitlines(keepends=True)
        return "".join(difflib.unified_diff(old, new, fromfile=f"a/{path}", tofile=f"b/{path}"))

    def _metadata(self, route: dict, fields: dict[str, Any], imported: CommentedMap) -> CommentedMap:
        metadata = imported
        for key, value in route.get("defaults", {}).items():
            if key not in metadata:
                metadata[key] = value
        values = {
            "title": str(fields.get("title") or metadata.get("title") or "").strip(),
            "permalink": route["url"],
        }
        if "author" not in metadata and not str(fields.get("author") or "").strip() and self.default_author:
            values["author"] = self.default_author
        optional = ("author", "date", "description", "tags", "lang")
        for key in optional:
            value = fields.get(key)
            if value not in (None, "", []):
                if key == "tags" and isinstance(value, str):
                    value = [tag.strip() for tag in value.split(",") if tag.strip()]
                values[key] = value
        if route.get("content_type") == "post" and "date" not in values:
            values["date"] = route["date"]
        values["published"] = str(fields.get("status") or "ready") != "draft"
        for key, value in values.items():
            if value != "":
                metadata[key] = value
        return metadata

    def preview_add(self, route_name: str, fields: dict[str, Any], markdown: str = "", assets: list[AssetInput] | None = None) -> ChangePlan:
        if route_name == "publication":
            route = self.routes.resolve(route_name, fields)
            return self._preview_publication(route_name, route, str(fields.get("bibtex") or markdown))
        imported_content = import_markdown(markdown)
        imported, body = imported_content.metadata, imported_content.body
        resolved_fields = dict(fields)
        for key in ("title", "date"):
            if not str(resolved_fields.get(key) or "").strip() and imported.get(key) not in (None, ""):
                resolved_fields[key] = str(imported[key])
        route = self._resolve_content_route(route_name, resolved_fields)
        if not str(resolved_fields.get("date") or "").strip() and route.get("date"):
            resolved_fields["date"] = route["date"]
        for required in route.get("required", []):
            if not str(resolved_fields.get(required) or "").strip():
                raise SiteManagerError(f"فیلد لازم خالی است: {required}")
        metadata = self._metadata(route, resolved_fields, imported)
        route["published"] = metadata.get("published") is not False
        asset_files, rewrites = prepare_assets(
            self.routes.config["image_asset_root"],
            self.routes.config["document_asset_root"],
            route["slug"],
            assets or [],
        )
        body = rewrite_asset_links(body, rewrites)
        rendered = render_front_matter(metadata, body)
        target: Path = route["target"]
        relative = route["relative_target"]
        conflicts: list[str] = []
        if target.exists():
            conflicts.append(f"فایل مقصد از قبل وجود دارد: {relative}")
        proposed_title = str(metadata.get("title") or "").casefold()
        for item in self.inspector.inventory():
            if proposed_title and item.title.casefold() == proposed_title:
                conflicts.append(f"عنوان مشابه موجود است: {item.path}")
        virtual = set(asset_files)
        validation = self.validator.validate_markdown(relative, rendered, virtual)
        validation.errors.extend(self.validator.duplicate_permalinks(relative, rendered))
        changes = [self._change(relative, rendered.encode("utf-8"))]
        for asset_path, data in asset_files.items():
            if contained_path(self.repo_root, asset_path).exists():
                conflicts.append(f"فایل رسانه‌ای از قبل وجود دارد: {asset_path}")
            changes.append(self._change(asset_path, data))
        if route.get("index_group"):
            index_change, index_conflicts = self._resource_index_change(route, str(metadata.get("title") or ""))
            changes.append(index_change)
            conflicts.extend(index_conflicts)
        plan = ChangePlan(
            token=uuid.uuid4().hex,
            operation="add",
            route=route_name,
            target_path=relative,
            proposed_url=route["url"],
            front_matter=metadata,
            changes=changes,
            validation=validation,
            conflicts=sorted(set(conflicts)),
            warnings=[route["warning_fa"]] if route.get("warning_fa") else [],
        )
        self._plans[plan.token] = plan
        return plan

    def _resolve_content_route(self, route_name: str, fields: dict[str, Any]) -> dict[str, Any]:
        if not route_name.startswith("course:"):
            return self.routes.resolve(route_name, fields)
        course_id = route_name.partition(":")[2]
        course = next((item for item in self.courses() if str(item.get("id")) == course_id), None)
        if course is None:
            raise SiteManagerError("درس انتخاب‌شده دیگر وجود ندارد؛ صفحه را تازه‌سازی کنید.")
        title = str(fields.get("title") or "").strip()
        slug = safe_slug(str(fields.get("slug") or title))
        relative = f"_pages/resources/teaching-{course_id}-{slug}.md"
        chapter_id = str(fields.get("chapter") or "").strip()
        chapter = next((item for item in course.get("chapters", []) if str(item.get("id")) == chapter_id), None)
        defaults: dict[str, Any] = {
            "layout": "legacy_page",
            "nav": False,
            "resource_group": "Teaching",
            "course": str(course.get("title") or course_id),
            "course_id": course_id,
        }
        if chapter:
            defaults["chapter"] = str(chapter.get("title") or chapter_id)
            defaults["chapter_id"] = chapter_id
        return {
            "label_fa": f"درس / {course.get('title', course_id)}",
            "content_type": "teaching_note",
            "target": contained_path(self.repo_root, relative),
            "relative_target": relative,
            "slug": slug,
            "url": f"/resources/teaching-{course_id}-{slug}/",
            "defaults": defaults,
            "index_group": str(course.get("title") or "Teaching"),
            "required": ["title"],
            "warning_fa": "",
        }

    def preview_course(self, fields: dict[str, Any], assets: list[AssetInput] | None = None) -> ChangePlan:
        title = str(fields.get("title") or "").strip()
        if not title:
            raise SiteManagerError("عنوان درس را وارد کنید.")
        slug = safe_slug(str(fields.get("slug") or title))
        description = str(fields.get("description") or "").strip()
        chapter_titles = [line.strip() for line in str(fields.get("chapters") or "").splitlines() if line.strip()]
        chapters = [{"id": safe_slug(value), "title": value} for value in chapter_titles]
        if len({item["id"] for item in chapters}) != len(chapters):
            raise SiteManagerError("دو فصل نام یکسان دارند؛ نام فصل‌ها را متمایز کنید.")
        existing_courses = self.courses()
        conflicts: list[str] = []
        course_url = f"/teaching/{slug}/"
        for course in existing_courses:
            if str(course.get("id", "")).casefold() == slug.casefold():
                conflicts.append("درسی با این نام یا شناسه از قبل وجود دارد.")
            if str(course.get("title", "")).casefold() == title.casefold():
                conflicts.append("درسی با این عنوان از قبل وجود دارد.")
            if str(course.get("url", course.get("permalink", ""))).rstrip("/").casefold() == course_url.rstrip("/").casefold():
                conflicts.append("نشانی این درس از قبل در فهرست Teaching وجود دارد.")
        course_assets = assets or []
        if len(course_assets) > 1:
            raise SiteManagerError("برای تصویر اصلی درس فقط یک فایل انتخاب کنید.")
        if course_assets and Path(course_assets[0].name).suffix.casefold() == ".pdf":
            raise SiteManagerError("تصویر اصلی درس باید فایل تصویری باشد؛ PDF پذیرفته نیست.")
        asset_files, _ = prepare_assets("assets/img/courses", "assets/img/courses", slug, course_assets)
        image_path = f"/{next(iter(asset_files))}" if asset_files else "/assets/img/courses/default-course.svg"
        next_order = max((int(course.get("order", 0)) for course in existing_courses), default=0) + 1
        published = str(fields.get("status") or "ready") != "draft"
        course_item = CommentedMap(
            id=slug,
            title=title,
            description=description,
            image=image_path,
            url=course_url,
            order=next_order,
            link_type="internal",
            chapters=chapters,
            published=published,
        )
        yaml = YAML(typ="rt")
        yaml.preserve_quotes = True
        yaml.width = 1000
        stream = StringIO()
        yaml.dump([*existing_courses, course_item], stream)
        data_text = stream.getvalue()
        data_validation = self.validator.validate_yaml(data_text)
        metadata = CommentedMap(
            layout="page",
            title=title,
            permalink=course_url,
            nav=False,
            course_id=slug,
            published=published,
        )
        if description:
            metadata["description"] = description
        body = "{% include teaching_course_materials.liquid course_id=page.course_id %}\n"
        page_text = render_front_matter(metadata, body)
        page_path = f"_pages/courses/{slug}.md"
        page_validation = self.validator.validate_markdown(page_path, page_text)
        page_validation.errors.extend(data_validation.errors)
        page_validation.warnings.extend(data_validation.warnings)
        page_validation.errors.extend(self.validator.duplicate_permalinks(page_path, page_text))
        changes = [
            self._change("_data/teaching_courses.yml", data_text.encode("utf-8")),
            self._change(page_path, page_text.encode("utf-8")),
        ]
        for asset_path, data in asset_files.items():
            if contained_path(self.repo_root, asset_path).exists():
                conflicts.append(f"فایل تصویر درس از قبل وجود دارد: {asset_path}")
            changes.append(self._change(asset_path, data))
        for change in changes:
            if change.action == "create":
                continue
            if change.path.endswith(f"/{slug}.md"):
                conflicts.append(f"صفحهٔ درس از قبل وجود دارد: {change.path}")
        plan = ChangePlan(
            token=uuid.uuid4().hex,
            operation="course",
            route=f"course:{slug}",
            target_path=page_path,
            proposed_url=course_url,
            front_matter=metadata,
            changes=changes,
            validation=page_validation,
            conflicts=sorted(set(conflicts)),
        )
        self._plans[plan.token] = plan
        return plan

    def _resource_index_change(self, route: dict[str, Any], title: str) -> tuple[FileChange, list[str]]:
        relative = "_data/legacy_resources.yml"
        target = contained_path(self.repo_root, relative)
        existing_text = target.read_text(encoding="utf-8-sig")
        yaml = YAML(typ="rt")
        yaml.preserve_quotes = True
        yaml.width = 1000
        data = yaml.load(existing_text) or []
        conflicts: list[str] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            if str(item.get("destination_path", "")).casefold() == route["relative_target"].casefold():
                conflicts.append(f"مسیر در فهرست منابع موجود است: {route['relative_target']}")
            if str(item.get("destination_url", "")).rstrip("/").casefold() == route["url"].rstrip("/").casefold():
                conflicts.append(f"URL در فهرست منابع موجود است: {route['url']}")
        new_item = CommentedMap(
            source_path=f"local-authoring/{Path(route['relative_target']).name}",
            destination_path=route["relative_target"],
            destination_url=route["url"],
            title=title,
            group=route["index_group"],
            mode="local_authored",
            published=bool(route.get("published", True)),
        )
        if route.get("defaults", {}).get("course_id"):
            new_item["course_id"] = route["defaults"]["course_id"]
        if route.get("defaults", {}).get("chapter_id"):
            new_item["chapter_id"] = route["defaults"]["chapter_id"]
        stream = StringIO()
        yaml.dump([new_item], stream)
        updated_text = f"{existing_text.rstrip()}\n{stream.getvalue()}" if data else stream.getvalue()
        YAML(typ="safe").load(updated_text)
        return self._change(relative, updated_text.encode("utf-8")), conflicts

    def _preview_publication(self, route_name: str, route: dict, candidate: str) -> ChangePlan:
        target: Path = route["target"]
        existing = target.read_text(encoding="utf-8-sig")
        candidate = candidate.strip()
        conflicts = duplicate_messages(existing, candidate)
        after = f"{existing.rstrip()}\n\n{candidate}\n"
        validation = self.validator.validate_bibtex(after)
        relative = target.relative_to(self.repo_root).as_posix()
        change = self._change(relative, after.encode("utf-8"))
        plan = ChangePlan(uuid.uuid4().hex, "add", route_name, relative, "/publications/", {}, [change], validation, conflicts)
        self._plans[plan.token] = plan
        return plan

    def preview_edit(self, relative_path: str, fields: dict[str, Any], markdown: str | None = None, assets: list[AssetInput] | None = None) -> ChangePlan:
        target = contained_path(self.repo_root, relative_path)
        if not target.is_file() or target.suffix.lower() != ".md":
            raise SiteManagerError("فقط فایل Markdown موجود در مخزن قابل ویرایش است.")
        existing_text = target.read_text(encoding="utf-8-sig")
        metadata, old_body, has_frontmatter = split_front_matter(existing_text)
        body = old_body if markdown is None else split_front_matter(markdown)[1]
        if not has_frontmatter and any(fields.get(key) for key in ("title", "author", "date", "description", "tags", "status", "lang")):
            raise SiteManagerError("این فایل یک fragment بدون front matter است؛ در ویرایش عادی فقط متن آن را تغییر دهید.")
        original_permalink = metadata.get("permalink")
        for key in ("title", "author", "date", "description", "lang"):
            if fields.get(key) not in (None, ""):
                metadata[key] = fields[key]
        if fields.get("tags") not in (None, ""):
            metadata["tags"] = [tag.strip() for tag in str(fields["tags"]).split(",") if tag.strip()]
        if fields.get("status"):
            metadata["published"] = fields["status"] != "draft"
        # Existing permalink is deliberately immutable in an ordinary edit.
        if original_permalink is not None:
            metadata["permalink"] = original_permalink
        slug = target.stem
        asset_files, rewrites = prepare_assets(
            self.routes.config["image_asset_root"],
            self.routes.config["document_asset_root"],
            slug,
            assets or [],
        )
        body = rewrite_asset_links(body, rewrites)
        rendered = render_front_matter(metadata, body) if has_frontmatter else f"{body.rstrip()}\n"
        validation = self.validator.validate_markdown(relative_path, rendered, set(asset_files), require_frontmatter=has_frontmatter, require_title=has_frontmatter)
        validation.errors.extend(self.validator.duplicate_permalinks(relative_path, rendered))
        changes = [self._change(relative_path, rendered.encode("utf-8"))]
        conflicts: list[str] = []
        for asset_path, data in asset_files.items():
            if contained_path(self.repo_root, asset_path).exists():
                conflicts.append(f"فایل رسانه‌ای از قبل وجود دارد: {asset_path}")
            changes.append(self._change(asset_path, data))
        plan = ChangePlan(uuid.uuid4().hex, "edit", "existing", relative_path, str(metadata.get("permalink") or ""), metadata, changes, validation, conflicts)
        self._plans[plan.token] = plan
        return plan

    def _change(self, relative: str, content: bytes) -> FileChange:
        target = contained_path(self.repo_root, relative)
        before = target.read_bytes() if target.exists() else b""
        return FileChange(
            path=relative,
            action="modify" if target.exists() else "create",
            content=content,
            before_sha256=file_sha256(target),
            diff=self._diff(relative, before, content) if target.suffix.lower() in {".md", ".bib", ".yml", ".yaml"} else "",
        )

    def add(self, plan_or_token: ChangePlan | str, confirm: bool = False) -> dict:
        return self._apply(plan_or_token, confirm)

    def edit(self, plan_or_token: ChangePlan | str, confirm: bool = False) -> dict:
        return self._apply(plan_or_token, confirm)

    def _apply(self, plan_or_token: ChangePlan | str, confirm: bool) -> dict:
        plan = self._plans.get(plan_or_token) if isinstance(plan_or_token, str) else plan_or_token
        if plan is None:
            raise SiteManagerError("پیش‌نمایش منقضی یا ناشناخته است؛ دوباره Preview بگیرید.")
        if not confirm:
            raise SiteManagerError("نوشتن فقط پس از تأیید صریح مجاز است.")
        if plan.validation.errors or plan.conflicts:
            raise SiteManagerError("تا رفع خطاها و تعارض‌ها نوشتن انجام نمی‌شود.")
        if time.time() - plan.created_at > 3600:
            raise SiteManagerError("پیش‌نمایش بیش از یک ساعت عمر دارد؛ دوباره آن را بسازید.")
        for change in plan.changes:
            current = file_sha256(contained_path(self.repo_root, change.path))
            if current != change.before_sha256:
                raise SiteManagerError(f"فایل پس از Preview تغییر کرده است: {change.path}")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_root = contained_path(self.repo_root, self.routes.config["backup_root"]) / f"{timestamp}-{plan.token[:8]}"
        backup_root.mkdir(parents=True, exist_ok=False)
        manifest: list[dict[str, Any]] = []
        written: list[FileChange] = []
        try:
            for change in plan.changes:
                target = contained_path(self.repo_root, change.path)
                if target.exists():
                    backup = backup_root / change.path
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, backup)
                atomic_write(target, change.content)
                written.append(change)
                manifest.append({"path": change.path, "action": change.action, "before_sha256": change.before_sha256, "after_sha256": file_sha256(target)})
            (backup_root / "operation.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            rollback_errors: list[str] = []
            for change in reversed(written):
                target = contained_path(self.repo_root, change.path)
                backup = backup_root / change.path
                try:
                    if change.before_sha256 is None:
                        target.unlink(missing_ok=True)
                    else:
                        shutil.copy2(backup, target)
                except OSError as rollback_exc:
                    rollback_errors.append(f"{change.path}: {rollback_exc}")
            detail = f" جزئیات بازگردانی: {'; '.join(rollback_errors)}" if rollback_errors else ""
            raise SiteManagerError(f"ذخیره کامل نشد و تغییرات نوشته‌شده بازگردانده شدند: {exc}.{detail}") from exc
        del self._plans[plan.token]
        return {"ok": True, "changed_files": [item["path"] for item in manifest], "backup": str(backup_root.relative_to(self.repo_root)), "validation": self.validate(changed_only=[item["path"] for item in manifest]).as_dict()}

    def validate(self, changed_only: list[str] | None = None) -> ValidationResult:
        if not changed_only:
            return self.validator.validate_site_quick()
        result = ValidationResult()
        for relative in changed_only:
            path = contained_path(self.repo_root, relative)
            if path.suffix.lower() == ".md":
                check = self.validator.validate_markdown(relative, path.read_text(encoding="utf-8-sig"))
            elif path.suffix.lower() == ".bib":
                check = self.validator.validate_bibtex(path.read_text(encoding="utf-8-sig"))
            elif path.suffix.lower() in {".yml", ".yaml"}:
                check = self.validator.validate_yaml(path.read_text(encoding="utf-8-sig"))
            else:
                continue
            result.errors.extend(check.errors)
            result.warnings.extend(check.warnings)
        return result
