from __future__ import annotations

from dataclasses import dataclass

from ruamel.yaml.comments import CommentedMap

from .frontmatter import split_front_matter


@dataclass
class ImportedMarkdown:
    metadata: CommentedMap
    body: str
    had_frontmatter: bool


def import_markdown(text: str) -> ImportedMarkdown:
    """Import UTF-8 Markdown without altering its body, Liquid, math or code."""
    metadata, body, had_frontmatter = split_front_matter(text or "")
    return ImportedMarkdown(metadata, body, had_frontmatter)
