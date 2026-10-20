from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    (tmp_path / "_config.yml").write_text("permalink: /blog/:year/:title/\n", encoding="utf-8")
    for folder in ("_pages/resources", "_posts", "_projects", "_news", "_bibliography", "_data", "assets/content"):
        (tmp_path / folder).mkdir(parents=True, exist_ok=True)
    (tmp_path / "_data" / "legacy_resources.yml").write_text("[]\n", encoding="utf-8")
    (tmp_path / "_pages" / "existing.md").write_text(
        "---\nlayout: page\ntitle: Existing Page\npermalink: /existing/\npublished: true\n---\n\n"
        "Math $x^2$ and {% include figure.liquid path=\"assets/img/old.png\" %}.\n\n```python\nprint('ok')\n```\n",
        encoding="utf-8",
    )
    (tmp_path / "assets" / "img").mkdir(parents=True)
    (tmp_path / "assets" / "img" / "old.png").write_bytes(b"old-image")
    (tmp_path / "_bibliography" / "papers.bib").write_text(
        "@article{known2024,\n  title={Known Work},\n  author={Author, A},\n  year={2024},\n  doi={10.1000/known}\n}\n",
        encoding="utf-8",
    )
    return tmp_path
