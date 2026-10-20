from __future__ import annotations

from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from .utils import SiteManagerError, contained_path, safe_slug


class RouteMap:
    def __init__(self, repo_root: Path, config_path: Path | None = None):
        self.repo_root = repo_root.resolve()
        self.config_path = config_path or Path(__file__).with_name("content_routes.yml")
        with self.config_path.open("r", encoding="utf-8") as handle:
            config = YAML(typ="safe").load(handle)
        if not isinstance(config, dict) or config.get("version") != 1:
            raise SiteManagerError("نسخهٔ content_routes.yml پشتیبانی نمی‌شود.")
        self.config = config
        self.routes: dict[str, dict[str, Any]] = config.get("routes", {})

    def get(self, name: str) -> dict[str, Any]:
        if name not in self.routes:
            raise SiteManagerError(f"مسیر ناشناخته است و حدس زده نمی‌شود: {name}")
        return deepcopy(self.routes[name])

    def resolve(self, name: str, fields: dict[str, Any]) -> dict[str, Any]:
        route = self.get(name)
        if route.get("mode") == "bibtex":
            route["target"] = contained_path(self.repo_root, route["destination"])
            route["url"] = "/publications/"
            return route

        title = str(fields.get("title") or "").strip()
        slug = safe_slug(str(fields.get("slug") or title))
        date_value = str(fields.get("date") or date.today().isoformat())
        try:
            parsed_date = date.fromisoformat(date_value)
        except ValueError as exc:
            raise SiteManagerError("تاریخ باید به صورت YYYY-MM-DD باشد.") from exc
        values = {"slug": slug, "date": parsed_date.isoformat(), "year": parsed_date.year}
        filename = route["filename"].format(**values)
        relative = Path(route["destination"]) / filename
        route.update(
            slug=slug,
            date=parsed_date.isoformat(),
            target=contained_path(self.repo_root, relative),
            relative_target=relative.as_posix(),
            url=route["permalink"].format(**values),
        )
        return route
