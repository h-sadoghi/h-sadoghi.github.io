from __future__ import annotations

import hashlib
import io
import re
import stat
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .assets import AssetInput
from .utils import SiteManagerError


# GitHub warns for files larger than 50 MiB and blocks regular Git files larger
# than 100 MiB. Staying at the warning boundary keeps GitHub Desktop usable.
MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024
MAX_ZIP_ENTRIES = 5_000
MAX_ZIP_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_COMPRESSION_RATIO = 500


@dataclass(frozen=True)
class ValidatedDownload:
    size: int
    sha256: str


def _validate_upload_name(name: str, suffix: str) -> None:
    normalized = unicodedata.normalize("NFKC", name or "").strip()
    if not normalized or Path(normalized).suffix.casefold() != suffix:
        raise SiteManagerError(f"پسوند فایل باید {suffix} باشد.")
    if any(ord(character) < 32 for character in normalized):
        raise SiteManagerError("نام فایل دارای نویسهٔ کنترلی غیرمجاز است.")
    if "/" in normalized or "\\" in normalized:
        raise SiteManagerError("نام فایل نباید شامل مسیر یا نام پوشه باشد.")


def _validate_size(asset: AssetInput) -> None:
    if not asset.data:
        raise SiteManagerError(f"فایل خالی است: {asset.name}")
    if len(asset.data) > MAX_DOWNLOAD_BYTES:
        raise SiteManagerError(
            f"حجم فایل {asset.name} بیش از ۵۰ مگابایت است. "
            "GitHub از ۵۰ مگابایت هشدار می‌دهد و فایل‌های بیش از ۱۰۰ مگابایت را نمی‌پذیرد؛ "
            "فایل را کوچک یا به چند بخش تقسیم کنید."
        )


def validate_pdf(asset: AssetInput) -> ValidatedDownload:
    _validate_upload_name(asset.name, ".pdf")
    _validate_size(asset)
    if not asset.data.startswith(b"%PDF-"):
        raise SiteManagerError("محتوای PDF با پسوند فایل سازگار نیست.")
    return ValidatedDownload(len(asset.data), hashlib.sha256(asset.data).hexdigest())


def validate_zip(asset: AssetInput) -> ValidatedDownload:
    _validate_upload_name(asset.name, ".zip")
    _validate_size(asset)
    if not asset.data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
        raise SiteManagerError("محتوای ZIP با پسوند فایل سازگار نیست.")

    try:
        archive = zipfile.ZipFile(io.BytesIO(asset.data))
        entries = archive.infolist()
    except (zipfile.BadZipFile, OSError) as exc:
        raise SiteManagerError("فایل ZIP معتبر یا قابل خواندن نیست.") from exc

    if len(entries) > MAX_ZIP_ENTRIES:
        raise SiteManagerError(f"ZIP بیش از {MAX_ZIP_ENTRIES:,} ورودی دارد و پذیرفته نمی‌شود.")

    total_uncompressed = 0
    seen: set[str] = set()
    for entry in entries:
        name = unicodedata.normalize("NFKC", entry.filename)
        if not name or "\x00" in name or any(ord(character) < 32 for character in name):
            raise SiteManagerError("ZIP دارای نام داخلی خالی یا نویسهٔ کنترلی است.")
        if "\\" in name or name.startswith("/") or re.match(r"^[A-Za-z]:", name):
            raise SiteManagerError(f"مسیر داخلی ZIP ایمن نیست: {entry.filename}")
        parts = PurePosixPath(name).parts
        if any(part in {"", ".", ".."} for part in parts):
            raise SiteManagerError(f"مسیر داخلی ZIP ایمن نیست: {entry.filename}")
        key = name.rstrip("/").casefold()
        if key in seen:
            raise SiteManagerError(f"نام داخلی تکراری در ZIP وجود دارد: {entry.filename}")
        seen.add(key)
        if entry.flag_bits & 0x1:
            raise SiteManagerError(f"فایل رمزگذاری‌شده داخل ZIP مجاز نیست: {entry.filename}")
        mode = (entry.external_attr >> 16) & 0xFFFF
        if stat.S_ISLNK(mode):
            raise SiteManagerError(f"پیوند نمادین داخل ZIP مجاز نیست: {entry.filename}")
        total_uncompressed += entry.file_size
        if total_uncompressed > MAX_ZIP_UNCOMPRESSED_BYTES:
            raise SiteManagerError("حجم بازشدهٔ ZIP بیش از ۵۱۲ مگابایت است و احتمال ZIP bomb وجود دارد.")
        if entry.file_size and (
            entry.compress_size == 0 or entry.file_size / entry.compress_size > MAX_COMPRESSION_RATIO
        ):
            raise SiteManagerError(f"نسبت فشرده‌سازی ورودی {entry.filename} غیرعادی و ناامن است.")

    archive.close()
    return ValidatedDownload(len(asset.data), hashlib.sha256(asset.data).hexdigest())


def display_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"
