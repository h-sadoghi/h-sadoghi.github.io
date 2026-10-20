from __future__ import annotations

import hashlib
import os
import re
import unicodedata
from pathlib import Path


class SiteManagerError(ValueError):
    """A user-facing validation or safety error."""


def safe_slug(value: str) -> str:
    value = unicodedata.normalize("NFKC", (value or "").strip()).casefold()
    value = re.sub(r"[^\w\-\s]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_]+", "-", value).strip("-. ")
    if not value:
        raise SiteManagerError("عنوان یا slug برای ساخت نام فایل کافی نیست.")
    if value.upper() in {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1"}:
        value = f"item-{value}"
    return value[:100].rstrip("-.")


def safe_filename(value: str) -> str:
    original = Path(value).name
    stem = safe_slug(Path(original).stem)
    suffix = Path(original).suffix.lower()
    suffix = suffix if re.fullmatch(r"\.[a-z0-9]{1,10}", suffix) else ""
    return f"{stem}{suffix}"


def contained_path(root: Path, relative: str | Path) -> Path:
    root = root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise SiteManagerError(f"مسیر خارج از مخزن مجاز نیست: {relative}") from exc
    return candidate


def file_sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.site-manager-{os.getpid()}.tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)
