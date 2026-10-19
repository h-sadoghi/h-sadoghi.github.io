from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from pybtex.database import parse_string
from ruamel.yaml import YAML

from .bibliography import validate_bibliography
from .frontmatter import split_front_matter


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict:
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings}


LOCAL_ASSET_PATTERNS = [
    re.compile(r"!?\[[^\]]*\]\(\s*<?(?P<path>/?assets/[^)>\s]+)", re.I),
    re.compile(r"\b(?:src|href)=[\"'](?P<path>/?assets/[^\"'#?]+)", re.I),
    re.compile(r"\bpath=[\"'](?P<path>assets/[^\"']+)", re.I),
]


class Validator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    def validate_markdown(
        self,
        relative_path: str,
        text: str,
        virtual_files: set[str] | None = None,
        *,
        require_frontmatter: bool = True,
        require_title: bool = True,
    ) -> ValidationResult:
        result = ValidationResult()
        virtual_files = virtual_files or set()
        try:
            metadata, body, has_frontmatter = split_front_matter(text)
        except Exception as exc:
            result.errors.append(str(exc))
            return result
        if not has_frontmatter and require_frontmatter:
            result.errors.append("فایل مقصد باید front matter داشته باشد.")
            return result
        if has_frontmatter and require_title and not metadata.get("title"):
            result.errors.append("فیلد title لازم است.")
        permalink = str(metadata.get("permalink") or "")
        if permalink and not permalink.startswith("/"):
            result.errors.append("permalink باید با / شروع شود.")
        if permalink and not permalink.endswith("/") and "." not in permalink.rsplit("/", 1)[-1]:
            result.errors.append("permalink پوشه‌ای باید با / پایان یابد.")
        if metadata.get("published") is False:
            result.warnings.append("این محتوا draft است و با published: false ذخیره می‌شود.")
        for pattern in LOCAL_ASSET_PATTERNS:
            for match in pattern.finditer(body):
                raw = match.group("path").split("?", 1)[0].split("#", 1)[0]
                relative = raw.lstrip("/").replace("%20", " ")
                if "{{" in relative or "{%" in relative:
                    continue
                if relative not in virtual_files and not (self.repo_root / relative).is_file():
                    result.errors.append(f"فایل محلی ارجاع‌شده وجود ندارد: {raw}")
        return result

    def duplicate_permalinks(self, proposed_path: str = "", proposed_text: str = "") -> list[str]:
        seen: dict[str, str] = {}
        issues: list[str] = []
        files = list((self.repo_root / "_pages").rglob("*.md")) + list((self.repo_root / "_posts").rglob("*.md")) + list((self.repo_root / "_projects").rglob("*.md"))
        for path in files:
            relative = path.relative_to(self.repo_root).as_posix()
            text = proposed_text if relative == proposed_path else path.read_text(encoding="utf-8-sig")
            try:
                metadata, _, _ = split_front_matter(text)
            except Exception:
                continue
            permalink = str(metadata.get("permalink") or "").strip()
            if not permalink:
                continue
            key = permalink.rstrip("/").casefold() or "/"
            if key in seen and seen[key] != relative:
                issues.append(f"permalink تکراری: {permalink} در {seen[key]} و {relative}")
            seen[key] = relative
        if proposed_path and proposed_path not in {p.relative_to(self.repo_root).as_posix() for p in files}:
            try:
                metadata, _, _ = split_front_matter(proposed_text)
                permalink = str(metadata.get("permalink") or "").strip()
                key = permalink.rstrip("/").casefold()
                if key and key in seen:
                    issues.append(f"permalink تکراری: {permalink} با {seen[key]}")
            except Exception:
                pass
        return sorted(set(issues))

    def validate_bibtex(self, text: str) -> ValidationResult:
        result = ValidationResult()
        try:
            parse_string(text, "bibtex")
            result.errors.extend(validate_bibliography(text))
        except Exception as exc:
            result.errors.append(str(exc))
        return result

    def validate_yaml(self, text: str) -> ValidationResult:
        result = ValidationResult()
        try:
            YAML(typ="safe").load(text)
        except Exception as exc:
            result.errors.append(f"YAML نامعتبر است: {exc}")
        return result

    def validate_site_quick(self) -> ValidationResult:
        result = ValidationResult()
        fragment_paths: set[str] = {"_pages/about_einstein.md"}
        profiles = self.repo_root / "_pages" / "profiles.md"
        if profiles.exists():
            try:
                metadata, _, _ = split_front_matter(profiles.read_text(encoding="utf-8-sig"))
                for profile in metadata.get("profiles", []):
                    if isinstance(profile, dict) and profile.get("content"):
                        fragment_paths.add(f"_pages/{profile['content']}")
            except Exception as exc:
                result.errors.append(f"_pages/profiles.md: {exc}")
        for folder in ("_pages", "_posts", "_projects", "_news"):
            for path in (self.repo_root / folder).rglob("*.md"):
                relative = path.relative_to(self.repo_root).as_posix()
                check = self.validate_markdown(
                    relative,
                    path.read_text(encoding="utf-8-sig"),
                    require_frontmatter=relative not in fragment_paths,
                    require_title=False,
                )
                result.errors.extend(f"{relative}: {item}" for item in check.errors)
                result.warnings.extend(f"{relative}: {item}" for item in check.warnings)
        result.errors.extend(self.duplicate_permalinks())
        bib = self.repo_root / "_bibliography" / "papers.bib"
        if bib.exists():
            check = self.validate_bibtex(bib.read_text(encoding="utf-8-sig"))
            result.errors.extend(f"_bibliography/papers.bib: {item}" for item in check.errors)
        result.errors = sorted(set(result.errors))
        result.warnings = sorted(set(result.warnings))
        return result
