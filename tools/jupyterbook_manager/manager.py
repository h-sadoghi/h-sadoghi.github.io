from __future__ import annotations

import difflib
import filecmp
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unicodedata
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import nbformat
from ruamel.yaml import YAML

from tools.site_manager.assets import AssetInput, prepare_assets
from tools.site_manager.course_packages import validate_pdf, validate_zip
from tools.site_manager.utils import SiteManagerError, safe_filename


MAX_ASSET_BYTES = 50 * 1024 * 1024
ALLOWED_ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".zip"}
CONTENT_SUFFIXES = {".md", ".ipynb"}


class ManagerError(RuntimeError):
    """A safe, user-facing manager failure."""


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class Change:
    path: Path
    content: bytes
    before_sha256: str | None = field(init=False)

    def __post_init__(self) -> None:
        self.before_sha256 = hashlib.sha256(self.path.read_bytes()).hexdigest() if self.path.exists() else None


@dataclass
class Plan:
    summary: str
    changes: list[Change]
    diff: str
    warnings: list[str] = field(default_factory=list)


def _yaml() -> YAML:
    parser = YAML(typ="rt")
    parser.preserve_quotes = True
    parser.width = 1000
    parser.indent(mapping=2, sequence=4, offset=2)
    return parser


def _slug(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"[^\w._-]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"-{2,}", "-", value).strip("-.")
    if not value or value in {".", ".."}:
        raise ManagerError("نام فایل یا شناسهٔ امن قابل تولید نیست.")
    if value.upper() in {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1"}:
        value = f"item-{value}"
    return value


def _safe_relative(value: str) -> PurePosixPath:
    normalized = unicodedata.normalize("NFKC", value).replace("\\", "/").strip()
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ManagerError(f"مسیر نسبی ایمن نیست: {value}")
    if re.match(r"^[A-Za-z]:", normalized):
        raise ManagerError(f"مسیر درایو در این قسمت مجاز نیست: {value}")
    return path


def _inside(root: Path, relative: str | PurePosixPath) -> Path:
    root = root.resolve()
    candidate = (root / Path(str(relative))).resolve()
    if candidate != root and root not in candidate.parents:
        raise ManagerError(f"مسیر از محدودهٔ مجاز خارج می‌شود: {relative}")
    return candidate


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def _text_diff(path: Path, before: bytes, after: bytes) -> str:
    try:
        old = before.decode("utf-8").splitlines(keepends=True)
        new = after.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return f"Binary file: {path.as_posix()} ({len(before)} -> {len(after)} bytes)\n"
    return "".join(
        difflib.unified_diff(old, new, fromfile=f"a/{path.as_posix()}", tofile=f"b/{path.as_posix()}")
    )


class BookManager:
    def __init__(self, repo_root: Path, registry: Path | None = None):
        self.repo_root = repo_root.resolve()
        self.registry_path = (registry or self.repo_root / "tools/jupyterbook_manager/books.yml").resolve()
        if not (self.repo_root / ".git").exists():
            raise ManagerError(f"ریشهٔ Git پیدا نشد: {self.repo_root}")
        if not self.registry_path.is_file():
            raise ManagerError(f"فهرست کتاب‌ها پیدا نشد: {self.registry_path}")
        self.registry = _yaml().load(self.registry_path.read_text(encoding="utf-8")) or {}

    def books(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.registry.get("books", [])]

    def book(self, book_id: str) -> dict[str, Any]:
        matches = [item for item in self.books() if str(item.get("id")) == book_id]
        if len(matches) != 1:
            raise ManagerError(f"کتاب ناشناخته یا تکراری است: {book_id}")
        result = matches[0]
        source_rel = _safe_relative(str(result["source"]))
        result["root"] = _inside(self.repo_root, source_rel)
        return result

    def load_toc(self, book_id: str) -> tuple[dict[str, Any], Path]:
        book = self.book(book_id)
        toc_path = book["root"] / "_toc.yml"
        if not toc_path.is_file():
            raise ManagerError(f"فایل _toc.yml پیدا نشد: {toc_path}")
        data = _yaml().load(toc_path.read_text(encoding="utf-8")) or {}
        return data, toc_path

    @staticmethod
    def _entries(toc: dict[str, Any]) -> Iterable[dict[str, Any]]:
        def walk(items: Any) -> Iterable[dict[str, Any]]:
            if not isinstance(items, list):
                return
            for item in items:
                if isinstance(item, dict):
                    yield item
                    yield from walk(item.get("sections"))

        root = toc.get("root")
        if root:
            yield {"file": root, "_root": True}
        yield from walk(toc.get("chapters"))
        yield from walk(toc.get("parts"))

    @staticmethod
    def _content_ref(value: str) -> str:
        path = PurePosixPath(value)
        return path.with_suffix("").as_posix() if path.suffix.lower() in CONTENT_SUFFIXES else path.as_posix()

    @staticmethod
    def _resolve_content(book_root: Path, ref: str) -> Path | None:
        safe = _safe_relative(ref)
        candidates = [_inside(book_root, safe)]
        if safe.suffix.lower() not in CONTENT_SUFFIXES:
            candidates = [_inside(book_root, f"{safe}.md"), _inside(book_root, f"{safe}.ipynb")]
        found = [item for item in candidates if item.is_file()]
        if len(found) > 1:
            raise ManagerError(f"برای یک ورودی TOC هم Markdown و هم Notebook وجود دارد: {ref}")
        return found[0] if found else None

    def tree(self, book_id: str) -> list[tuple[int, str, str]]:
        toc, _ = self.load_toc(book_id)
        rows: list[tuple[int, str, str]] = []

        def walk(items: Any, depth: int) -> None:
            for item in items or []:
                if not isinstance(item, dict):
                    continue
                rows.append((depth, str(item.get("file", "")), str(item.get("title", ""))))
                walk(item.get("sections"), depth + 1)

        rows.append((0, str(toc.get("root", "")), "صفحهٔ اصلی"))
        walk(toc.get("chapters"), 1)
        for part in toc.get("parts") or []:
            rows.append((1, "", str(part.get("caption", "بخش"))))
            walk(part.get("chapters"), 2)
        return rows

    def validate(self, book_id: str) -> ValidationReport:
        report = ValidationReport()
        book = self.book(book_id)
        book_root: Path = book["root"]
        config_path = book_root / "_config.yml"
        if not config_path.is_file():
            report.errors.append("_config.yml کتاب وجود ندارد.")
        else:
            config = _yaml().load(config_path.read_text(encoding="utf-8")) or {}
            mode = str((config.get("execute") or {}).get("execute_notebooks", "")).lower()
            if mode != "off":
                report.errors.append("execute.execute_notebooks باید برای Build عادی روی off باشد.")
        try:
            toc, _ = self.load_toc(book_id)
        except Exception as exc:
            report.errors.append(str(exc))
            return report
        if toc.get("format") != "jb-book":
            report.errors.append("format در _toc.yml باید jb-book باشد.")
        refs: set[str] = set()
        for entry in self._entries(toc):
            ref = str(entry.get("file", "")).strip()
            if not ref:
                report.errors.append("یک ورودی TOC بدون file پیدا شد.")
                continue
            try:
                normalized = self._content_ref(str(_safe_relative(ref))).casefold()
            except ManagerError as exc:
                report.errors.append(str(exc))
                continue
            if normalized in refs:
                report.errors.append(f"ورودی تکراری در TOC: {ref}")
                continue
            refs.add(normalized)
            try:
                content = self._resolve_content(book_root, ref)
            except ManagerError as exc:
                report.errors.append(str(exc))
                continue
            if content is None:
                report.errors.append(f"فایل TOC پیدا نشد: {ref}")
                continue
            if content.is_symlink():
                report.errors.append(f"پیوند نمادین به‌عنوان محتوا مجاز نیست: {content}")
                continue
            report.files.append(content.relative_to(self.repo_root).as_posix())
            self._validate_content_links(book_root, content, report)
        metadata_path = book_root / "_content.yml"
        if metadata_path.is_file():
            metadata = _yaml().load(metadata_path.read_text(encoding="utf-8")) or {}
            metadata_refs: set[str] = set()
            for item in metadata.get("items", []) or []:
                if not isinstance(item, dict):
                    report.errors.append("یک رکورد نامعتبر در _content.yml پیدا شد.")
                    continue
                ref = self._content_ref(str(item.get("file", ""))).casefold()
                if not ref or ref in metadata_refs:
                    report.errors.append(f"رکورد تکراری یا خالی در _content.yml: {ref}")
                metadata_refs.add(ref)
                if ref not in refs:
                    report.warnings.append(f"متادیتا برای فایل خارج از TOC ثبت شده است: {ref}")
        nested = [p for p in book_root.rglob(".git") if p != self.repo_root / ".git"]
        if nested:
            report.errors.extend(f"مخزن Git تو در تو مجاز نیست: {p}" for p in nested)
        return report

    def _validate_content_links(self, book_root: Path, path: Path, report: ValidationReport) -> None:
        if path.suffix.lower() == ".ipynb":
            try:
                notebook = nbformat.read(path, as_version=4)
                nbformat.validate(notebook)
                texts = [cell.source for cell in notebook.cells if cell.cell_type == "markdown"]
            except Exception as exc:
                report.errors.append(f"Notebook نامعتبر است ({path.name}): {exc}")
                return
        else:
            texts = [path.read_text(encoding="utf-8")]
        for text in texts:
            for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)", text):
                target = target.strip("<>")
                if not target or target.startswith(("http://", "https://", "mailto:", "#", "data:")):
                    continue
                clean = target.split("#", 1)[0].split("?", 1)[0]
                if not clean:
                    continue
                try:
                    if clean.startswith("/"):
                        candidate = _inside(self.repo_root, _safe_relative(clean.lstrip("/")))
                    else:
                        candidate = (path.parent / clean).resolve()
                        if book_root.resolve() not in candidate.parents and candidate != book_root.resolve():
                            raise ManagerError(f"لینک نسبی از سورس کتاب خارج می‌شود: {target}")
                    if not candidate.exists() and Path(clean).suffix:
                        report.errors.append(f"هدف لینک پیدا نشد در {path.name}: {target}")
                except ManagerError as exc:
                    report.errors.append(str(exc))

    def plan_add(
        self,
        book_id: str,
        source: Path,
        destination: str | None = None,
        parent: str | None = None,
        position: int | None = None,
        title: str | None = None,
        description: str | None = None,
    ) -> Plan:
        book = self.book(book_id)
        book_root: Path = book["root"]
        source = source.resolve()
        if not source.is_file() or source.is_symlink() or source.suffix.lower() not in CONTENT_SUFFIXES:
            raise ManagerError("فقط فایل واقعی .md یا .ipynb قابل افزودن است.")
        if source.suffix.lower() == ".ipynb":
            notebook = nbformat.read(source, as_version=4)
            nbformat.validate(notebook)
        else:
            source.read_text(encoding="utf-8")
        if destination:
            dest_rel = _safe_relative(destination)
            if dest_rel.suffix.lower() not in CONTENT_SUFFIXES:
                dest_rel = dest_rel.with_suffix(source.suffix.lower())
        else:
            dest_rel = PurePosixPath("chapters") / f"{_slug(source.stem)}{source.suffix.lower()}"
        if dest_rel.suffix.lower() != source.suffix.lower():
            raise ManagerError("پسوند مقصد باید با فایل ورودی یکسان باشد.")
        destination_path = _inside(book_root, dest_rel)
        if destination_path.exists():
            raise ManagerError(f"فایل مقصد از قبل وجود دارد: {dest_rel}")

        toc, toc_path = self.load_toc(book_id)
        ref = self._content_ref(dest_rel.as_posix())
        existing = {self._content_ref(str(item.get("file", ""))).casefold() for item in self._entries(toc)}
        if ref.casefold() in existing:
            raise ManagerError(f"این ورودی از قبل در TOC وجود دارد: {ref}")
        entry: dict[str, Any] = {"file": ref}
        if title:
            entry["title"] = title.strip()
        container = toc.setdefault("chapters", [])
        if parent and parent != "root":
            parent_ref = self._content_ref(parent).casefold()
            matches = [item for item in self._entries(toc) if self._content_ref(str(item.get("file", ""))).casefold() == parent_ref]
            if len(matches) != 1 or matches[0].get("_root"):
                raise ManagerError(f"فصل والد یکتا پیدا نشد: {parent}")
            container = matches[0].setdefault("sections", [])
        index = len(container) if position is None else position - 1
        if index < 0 or index > len(container):
            raise ManagerError("موقعیت خارج از محدوده است.")
        container.insert(index, entry)
        from io import StringIO

        stream = StringIO()
        _yaml().dump(toc, stream)
        toc_bytes = stream.getvalue().encode("utf-8")
        metadata_path = book_root / "_content.yml"
        metadata = _yaml().load(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else None
        metadata = metadata or {"version": 1, "items": []}
        metadata_items = metadata.setdefault("items", [])
        if any(self._content_ref(str(item.get("file", ""))).casefold() == ref.casefold() for item in metadata_items):
            raise ManagerError(f"متادیتای این فایل از قبل ثبت شده است: {ref}")
        metadata_item: dict[str, Any] = {"file": ref}
        if title:
            metadata_item["title"] = title.strip()
        if description:
            metadata_item["description"] = description.strip()
        metadata_items.append(metadata_item)
        metadata_stream = StringIO()
        _yaml().dump(metadata, metadata_stream)
        metadata_bytes = metadata_stream.getvalue().encode("utf-8")
        before = toc_path.read_bytes()
        relative_toc = toc_path.relative_to(self.repo_root)
        diff = _text_diff(relative_toc, before, toc_bytes)
        diff += _text_diff(
            metadata_path.relative_to(self.repo_root),
            metadata_path.read_bytes() if metadata_path.exists() else b"",
            metadata_bytes,
        )
        diff += f"\nNew file: {destination_path.relative_to(self.repo_root).as_posix()} ({source.stat().st_size} bytes)\n"
        return Plan(
            summary=f"افزودن {dest_rel.as_posix()} به کتاب {book_id}",
            changes=[
                Change(toc_path, toc_bytes),
                Change(metadata_path, metadata_bytes),
                Change(destination_path, source.read_bytes()),
            ],
            diff=diff,
            warnings=["Notebook فقط اعتبارسنجی می‌شود و اجرا نخواهد شد."] if source.suffix.lower() == ".ipynb" else [],
        )

    def plan_move(self, book_id: str, ref: str, position: int, title: str | None = None) -> Plan:
        toc, toc_path = self.load_toc(book_id)
        wanted = self._content_ref(ref).casefold()
        found: list[tuple[list[Any], int, dict[str, Any]]] = []

        def scan(items: Any) -> None:
            if not isinstance(items, list):
                return
            for index, item in enumerate(items):
                if isinstance(item, dict):
                    if self._content_ref(str(item.get("file", ""))).casefold() == wanted:
                        found.append((items, index, item))
                    scan(item.get("sections"))

        scan(toc.get("chapters"))
        for part in toc.get("parts") or []:
            scan(part.get("chapters"))
        if len(found) != 1:
            raise ManagerError(f"ورودی یکتا پیدا نشد: {ref}")
        container, old_index, entry = found[0]
        if position < 1 or position > len(container):
            raise ManagerError("موقعیت خارج از محدودهٔ همان بخش است.")
        container.pop(old_index)
        container.insert(position - 1, entry)
        if title is not None:
            if title.strip():
                entry["title"] = title.strip()
            else:
                entry.pop("title", None)
        from io import StringIO

        stream = StringIO()
        _yaml().dump(toc, stream)
        after = stream.getvalue().encode("utf-8")
        changes = [Change(toc_path, after)]
        diff = _text_diff(toc_path.relative_to(self.repo_root), toc_path.read_bytes(), after)
        metadata_path = self.book(book_id)["root"] / "_content.yml"
        if metadata_path.is_file() and title is not None:
            metadata = _yaml().load(metadata_path.read_text(encoding="utf-8")) or {}
            for item in metadata.get("items", []) or []:
                if isinstance(item, dict) and self._content_ref(str(item.get("file", ""))).casefold() == wanted:
                    if title.strip():
                        item["title"] = title.strip()
                    else:
                        item.pop("title", None)
            metadata_stream = StringIO()
            _yaml().dump(metadata, metadata_stream)
            metadata_after = metadata_stream.getvalue().encode("utf-8")
            changes.append(Change(metadata_path, metadata_after))
            diff += _text_diff(
                metadata_path.relative_to(self.repo_root), metadata_path.read_bytes(), metadata_after
            )
        return Plan(
            summary=f"تغییر ترتیب/عنوان {ref}",
            changes=changes,
            diff=diff,
        )

    def plan_asset(self, book_id: str, source: Path, page_ref: str, label: str | None = None) -> Plan:
        book = self.book(book_id)
        book_root: Path = book["root"]
        source = source.resolve()
        if not source.is_file() or source.is_symlink():
            raise ManagerError("فایل همراه معتبر نیست.")
        suffix = source.suffix.lower()
        if suffix not in ALLOWED_ASSET_SUFFIXES:
            raise ManagerError(f"نوع فایل مجاز نیست: {suffix}")
        size = source.stat().st_size
        if size == 0 or size > MAX_ASSET_BYTES:
            raise ManagerError("فایل باید غیرخالی و حداکثر ۵۰ مگابایت باشد.")
        safe_name = safe_filename(source.name)
        page = self._resolve_content(book_root, page_ref)
        if page is None:
            raise ManagerError(f"صفحهٔ مقصد پیدا نشد: {page_ref}")
        if page.suffix.lower() != ".md":
            raise ManagerError("افزودن خودکار لینک فعلاً فقط برای صفحهٔ Markdown انجام می‌شود.")
        if suffix in {".zip", ".pdf"}:
            try:
                uploaded = AssetInput(source.name, source.read_bytes())
                validate_zip(uploaded) if suffix == ".zip" else validate_pdf(uploaded)
            except SiteManagerError as exc:
                raise ManagerError(str(exc)) from exc
            course_id = _slug(str(book.get("course_id") or book_id))
            destination = self.repo_root / "assets/downloads/courses" / course_id / "jupyter-book" / _slug(page.stem) / safe_name
            link = "/" + destination.relative_to(self.repo_root).as_posix()
        else:
            try:
                prepare_assets("images", "documents", _slug(page.stem), [AssetInput(source.name, source.read_bytes())])
            except SiteManagerError as exc:
                raise ManagerError(str(exc)) from exc
            destination = book_root / "_images" / _slug(page.stem) / safe_name
            link = Path(os.path.relpath(destination, page.parent)).as_posix()
        if destination.exists():
            raise ManagerError(f"فایل مقصد از قبل وجود دارد: {destination.relative_to(self.repo_root)}")
        old = page.read_text(encoding="utf-8")
        title = label.strip() if label else source.stem
        markdown = f"![{title}]({link})" if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"} else f"[{title}]({link})"
        if link in old:
            raise ManagerError("این فایل از قبل در صفحه لینک شده است.")
        after = f"{old.rstrip()}\n\n{markdown}\n".encode("utf-8")
        relative_page = page.relative_to(self.repo_root)
        diff = _text_diff(relative_page, page.read_bytes(), after)
        diff += f"\nNew file: {destination.relative_to(self.repo_root).as_posix()} ({size} bytes)\n"
        return Plan(
            summary=f"افزودن فایل همراه به {page_ref}",
            changes=[Change(page, after), Change(destination, source.read_bytes())],
            diff=diff,
            warnings=["ZIP فقط اعتبارسنجی می‌شود و هرگز استخراج یا اجرا نمی‌شود."] if suffix == ".zip" else [],
        )

    def apply(self, plan: Plan) -> Path:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        digest = hashlib.sha256(plan.diff.encode("utf-8")).hexdigest()[:8]
        backup = self.repo_root / ".jupyterbook-manager-backups" / f"{timestamp}-{digest}"
        backup.mkdir(parents=True, exist_ok=False)
        manifest: list[dict[str, Any]] = []
        written: list[tuple[Path, Path | None]] = []
        try:
            for change in plan.changes:
                resolved = change.path.resolve()
                allowed = self.repo_root == resolved or self.repo_root in resolved.parents
                if not allowed or resolved.is_symlink():
                    raise ManagerError(f"نوشتن در این مسیر مجاز نیست: {change.path}")
                old_hash = hashlib.sha256(resolved.read_bytes()).hexdigest() if resolved.exists() else None
                if old_hash != change.before_sha256:
                    raise ManagerError(f"فایل پس از Preview تغییر کرده است؛ دوباره Preview بگیرید: {change.path}")
                backup_file: Path | None = None
                if resolved.exists():
                    backup_file = backup / resolved.relative_to(self.repo_root)
                    backup_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(resolved, backup_file)
                _atomic_write(resolved, change.content)
                written.append((resolved, backup_file))
                manifest.append(
                    {
                        "path": resolved.relative_to(self.repo_root).as_posix(),
                        "before_sha256": old_hash,
                        "after_sha256": hashlib.sha256(change.content).hexdigest(),
                    }
                )
            (backup / "operation.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            for target, saved in reversed(written):
                if saved is None:
                    target.unlink(missing_ok=True)
                elif saved.exists():
                    shutil.copy2(saved, target)
            raise
        return backup

    def build(self, book_id: str, clean: bool = False) -> Path:
        report = self.validate(book_id)
        if not report.ok:
            raise ManagerError("اعتبارسنجی کتاب شکست خورد:\n- " + "\n- ".join(report.errors))
        book = self.book(book_id)
        book_root: Path = book["root"]
        executable = self.repo_root / ".venv-jupyterbook/Scripts/jupyter-book.exe"
        if not executable.is_file():
            executable = Path(shutil.which("jupyter-book") or "")
        if not executable.is_file():
            raise ManagerError("Jupyter Book در محیط اختصاصی پیدا نشد؛ ابتدا SETUP_JUPYTERBOOK.cmd را اجرا کنید.")
        if clean:
            subprocess.run([str(executable), "clean", str(book_root), "--all"], cwd=self.repo_root, check=True)
        command = [str(executable), "build", str(book_root)]
        subprocess.run(command, cwd=self.repo_root, check=True)
        output = book_root / "_build/html"
        if not (output / "index.html").is_file() or not (output / "_static").is_dir():
            raise ManagerError("خروجی Build کامل نیست؛ index.html یا _static پیدا نشد.")
        return output

    def execute_copy(self, book_id: str, ref: str, acknowledgement: str) -> Path:
        if acknowledgement != "EXECUTE":
            raise ManagerError(
                "اجرای کد فقط آگاهانه مجاز است. برای تأیید خطر دسترسی کد به رایانه، "
                "--acknowledge-risk EXECUTE را وارد کنید."
            )
        book = self.book(book_id)
        source = self._resolve_content(book["root"], ref)
        if source is None or source.suffix.lower() != ".ipynb" or source.is_symlink():
            raise ManagerError("فقط یک Notebook موجود در کتاب قابل اجرای صریح است.")
        notebook = nbformat.read(source, as_version=4)
        nbformat.validate(notebook)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        work = self.repo_root / ".jupyterbook-manager-runtime/executed" / timestamp
        work.mkdir(parents=True, exist_ok=False)
        copied = work / source.name
        shutil.copy2(source, copied)
        python = self.repo_root / ".venv-jupyterbook/Scripts/python.exe"
        if not python.is_file():
            raise ManagerError("محیط اختصاصی Jupyter Book پیدا نشد.")
        subprocess.run(
            [
                str(python),
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--ExecutePreprocessor.timeout=600",
                "--output",
                "executed.ipynb",
                copied.name,
            ],
            cwd=work,
            check=True,
        )
        result = work / "executed.ipynb"
        if not result.is_file():
            raise ManagerError("نسخهٔ اجرایی Notebook ساخته نشد.")
        return result

    def stage(self, book_id: str, site_dir: Path) -> Path:
        book = self.book(book_id)
        source: Path = book["root"] / "_build/html"
        if not (source / "index.html").is_file():
            raise ManagerError("ابتدا کتاب را Build کنید؛ index.html خروجی پیدا نشد.")
        site_dir = site_dir.resolve()
        if not site_dir.is_dir():
            raise ManagerError("خروجی Jekyll وجود ندارد؛ Jekyll باید قبل از Stage اجرا شود.")
        public_path = _safe_relative(str(book["public_path"]).strip("/"))
        destination = _inside(site_dir, public_path)
        if destination.exists():
            shutil.rmtree(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
        if not (destination / "index.html").is_file() or not (destination / "_static").is_dir():
            raise ManagerError("Stage کتاب کامل نشد.")
        source_files = sorted(path.relative_to(source) for path in source.rglob("*") if path.is_file())
        destination_files = sorted(path.relative_to(destination) for path in destination.rglob("*") if path.is_file())
        if source_files != destination_files or any(
            not filecmp.cmp(source / relative, destination / relative, shallow=False) for relative in source_files
        ):
            raise ManagerError("Stage کتاب دست‌نخورده کپی نشد؛ فهرست یا محتوای فایل‌های مقصد متفاوت است.")
        return destination

    def preview(self, book_id: str, port: int = 4100, open_browser: bool = True) -> str:
        output = self.build(book_id)
        if not self._port_free(port):
            raise ManagerError(f"پورت {port} در حال استفاده است. Preview کتاب از 4100 استفاده می‌کند تا با 4000 و 8765 تداخل نداشته باشد.")
        runtime = self.repo_root / ".jupyterbook-manager-runtime"
        runtime.mkdir(exist_ok=True)
        state = runtime / "preview.json"
        if state.exists():
            old = json.loads(state.read_text(encoding="utf-8"))
            if self._pid_running(int(old.get("pid", 0))):
                raise ManagerError(f"Preview قبلی با PID {old['pid']} هنوز فعال است؛ ابتدا دستور stop را اجرا کنید.")
            state.unlink(missing_ok=True)
        python = self.repo_root / ".venv-jupyterbook/Scripts/python.exe"
        if not python.is_file():
            raise ManagerError("Python محیط Jupyter Book پیدا نشد.")
        flags = 0
        kwargs: dict[str, Any] = {}
        if os.name == "nt":
            flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        else:
            kwargs["start_new_session"] = True
        log_path = runtime / "preview.log"
        log = log_path.open("ab")
        process = subprocess.Popen(
            [str(python), "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", str(output)],
            cwd=self.repo_root,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            creationflags=flags,
            **kwargs,
        )
        log.close()
        state.write_text(json.dumps({"pid": process.pid, "port": port, "book": book_id, "started": time.time()}, indent=2), encoding="utf-8")
        deadline = time.time() + 10
        while time.time() < deadline:
            if not self._port_free(port):
                break
            time.sleep(0.2)
        else:
            raise ManagerError(f"سرور Preview شروع نشد؛ لاگ: {log_path}")
        url = f"http://127.0.0.1:{port}/"
        if open_browser:
            webbrowser.open(url)
        return url

    def stop_preview(self) -> str:
        state = self.repo_root / ".jupyterbook-manager-runtime/preview.json"
        if not state.is_file():
            return "Preview فعالی ثبت نشده است."
        data = json.loads(state.read_text(encoding="utf-8"))
        pid = int(data.get("pid", 0))
        if self._pid_running(pid):
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False, capture_output=True)
            else:
                os.killpg(pid, 15)
        state.unlink(missing_ok=True)
        return f"Preview با PID {pid} متوقف شد."

    @staticmethod
    def _port_free(port: int) -> bool:
        with socket.socket() as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return True
            except OSError:
                return False

    @staticmethod
    def _pid_running(pid: int) -> bool:
        if pid <= 0:
            return False
        if os.name == "nt":
            result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"], capture_output=True, text=True)
            return result.returncode == 0 and f'"{pid}"' in result.stdout
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def find_repo(start: Path) -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=start, capture_output=True, text=True)
    if result.returncode != 0:
        raise ManagerError("این مسیر داخل مخزن Git اصلی نیست.")
    return Path(result.stdout.strip()).resolve()
