from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .frontmatter import split_front_matter


@dataclass
class ContentItem:
    path: str
    content_type: str
    title: str
    permalink: str
    parse_error: str = ""


class RepositoryInspector:
    ROOTS = {
        "_pages": "page",
        "_posts": "post",
        "_projects": "project",
        "_news": "news",
    }

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    def inventory(self) -> list[ContentItem]:
        items: list[ContentItem] = []
        for folder, content_type in self.ROOTS.items():
            root = self.repo_root / folder
            if not root.exists():
                continue
            for path in sorted(root.rglob("*.md")):
                relative = path.relative_to(self.repo_root).as_posix()
                try:
                    metadata, _, _ = split_front_matter(path.read_text(encoding="utf-8-sig"))
                    title = str(metadata.get("title") or path.stem)
                    permalink = str(metadata.get("permalink") or "")
                    kind = "resource" if relative.startswith("_pages/resources/") else content_type
                    items.append(ContentItem(relative, kind, title, permalink))
                except Exception as exc:
                    items.append(ContentItem(relative, content_type, path.stem, "", str(exc)))
        return items

    def search(self, query: str = "", content_type: str = "") -> list[dict]:
        needle = query.casefold().strip()
        matches = []
        for item in self.inventory():
            if content_type and item.content_type != content_type:
                continue
            haystack = f"{item.path} {item.title} {item.permalink}".casefold()
            if not needle or needle in haystack:
                matches.append(asdict(item))
        return matches
