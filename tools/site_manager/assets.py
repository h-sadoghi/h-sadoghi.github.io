from __future__ import annotations

import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path

from .utils import SiteManagerError, safe_filename


ALLOWED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tif", ".tiff", ".pdf"
}


def _matches_type(suffix: str, data: bytes) -> bool:
    if suffix == ".png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return data.startswith(b"\xff\xd8\xff")
    if suffix == ".gif":
        return data.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".webp":
        return len(data) >= 12 and data.startswith(b"RIFF") and data[8:12] == b"WEBP"
    if suffix in {".tif", ".tiff"}:
        return data.startswith((b"II*\x00", b"MM\x00*"))
    if suffix == ".pdf":
        return data.startswith(b"%PDF-")
    if suffix == ".svg":
        head = data[:4096].decode("utf-8-sig", errors="ignore").casefold()
        return "<svg" in head
    return False


@dataclass(frozen=True)
class AssetInput:
    name: str
    data: bytes
    source: str = "user-selected"


def prepare_assets(image_root: str, document_root: str, slug: str, assets: list[AssetInput]) -> tuple[dict[str, bytes], dict[str, str]]:
    files: dict[str, bytes] = {}
    rewrites: dict[str, str] = {}
    used: set[str] = set()
    for item in assets:
        suffix = Path(item.name).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise SiteManagerError(f"نوع فایل پشتیبانی نمی‌شود: {item.name}")
        if not item.data:
            raise SiteManagerError(f"فایل خالی است: {item.name}")
        if len(item.data) > 32 * 1024 * 1024:
            raise SiteManagerError(f"حجم یک فایل بیش از ۳۲ مگابایت است: {item.name}")
        if not _matches_type(suffix, item.data):
            raise SiteManagerError(f"محتوای فایل با پسوند آن سازگار نیست: {item.name}")
        name = safe_filename(item.name)
        stem, ext = Path(name).stem, Path(name).suffix
        candidate = name
        serial = 2
        while candidate.casefold() in used:
            candidate = f"{stem}-{serial}{ext}"
            serial += 1
        used.add(candidate.casefold())
        asset_root = document_root if suffix == ".pdf" else image_root
        relative = f"{asset_root.rstrip('/')}/{slug}/{candidate}"
        files[relative] = item.data
        web_path = f"/{relative}"
        rewrites[item.name.replace("\\", "/")] = web_path
        rewrites[Path(item.name).name] = web_path
        mime, _ = mimetypes.guess_type(candidate)
        if mime is None:
            raise SiteManagerError(f"نوع MIME قابل تشخیص نیست: {item.name}")
    return files, rewrites


def rewrite_asset_links(markdown: str, rewrites: dict[str, str]) -> str:
    result = markdown
    for original, replacement in sorted(rewrites.items(), key=lambda pair: len(pair[0]), reverse=True):
        escaped = re.escape(original)
        # Markdown image/link targets, including optional angle brackets and titles.
        result = re.sub(
            rf"(?P<prefix>!?\[[^\]]*\]\(\s*<?)(?:[^)>]*/)?{escaped}(?P<suffix>>?(?:\s+[\"'][^\"']*[\"'])?\s*\))",
            lambda match: f"{match.group('prefix')}{replacement}{match.group('suffix')}",
            result,
            flags=re.IGNORECASE,
        )
        # Existing Liquid figure paths.
        result = re.sub(
            rf"(?P<prefix>\bpath\s*=\s*[\"'])(?:[^\"']*/)?{escaped}(?P<suffix>[\"'])",
            lambda match: f"{match.group('prefix')}{replacement.lstrip('/')}{match.group('suffix')}",
            result,
            flags=re.IGNORECASE,
        )
    return result
