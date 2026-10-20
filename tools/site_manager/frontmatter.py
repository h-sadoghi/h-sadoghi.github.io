from __future__ import annotations

from io import StringIO
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from .utils import SiteManagerError


def _yaml() -> YAML:
    parser = YAML(typ="rt")
    parser.preserve_quotes = True
    parser.allow_duplicate_keys = False
    parser.width = 1000
    return parser


def split_front_matter(text: str) -> tuple[CommentedMap, str, bool]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return CommentedMap(), normalized, False
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise SiteManagerError("پایان front matter با --- پیدا نشد.")
    raw = normalized[4:end]
    try:
        data = _yaml().load(raw) or CommentedMap()
    except Exception as exc:  # ruamel provides the exact line in its message
        raise SiteManagerError(f"YAML front matter نامعتبر است: {exc}") from exc
    if not isinstance(data, dict):
        raise SiteManagerError("front matter باید یک نگاشت YAML باشد.")
    return data, normalized[end + 5 :], True


def render_front_matter(data: dict[str, Any], body: str) -> str:
    stream = StringIO()
    _yaml().dump(data, stream)
    clean_body = body.replace("\r\n", "\n").lstrip("\n")
    return f"---\n{stream.getvalue()}---\n\n{clean_body.rstrip()}\n"
