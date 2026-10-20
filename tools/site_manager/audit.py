from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from ruamel.yaml import YAML

from .frontmatter import split_front_matter
from .inspector import RepositoryInspector


def preferred_category(path: str, content_type: str, profile_fragments: set[str], resource_groups: dict[str, str]) -> str:
    if content_type in {"post", "news"}:
        return "News / Blog"
    if content_type == "project" or path.endswith(("publications.md", "projects.md", "research_topics.md", "repositories.md")):
        return "Research"
    if path in profile_fragments or path.endswith(("profiles.md", "student_research.md", "laboratory_gallery.md")):
        return "People & Students"
    if path.startswith("_pages/resources/presentation-") or path.endswith("presentations.md"):
        return "Library"
    if path.startswith("_pages/resources/teaching-") or path.endswith("teaching.md"):
        return "Teaching"
    if content_type == "resource":
        group = resource_groups.get(path, "")
        if group in {"Engineering projects", "Health research concepts", "Research artifacts", "Research toolkit"}:
            return "Research"
        if group in {"Circuits and electronics", "Pattern recognition and machine learning", "Data engineering and AI education"}:
            return "Teaching"
        return "Library"
    if path.endswith("resources.md"):
        return "Library"
    return "Home / About / CV / Contact"


def write_inventory(repo_root: Path, output: Path) -> int:
    inspector = RepositoryInspector(repo_root)
    items = inspector.inventory()
    title_counts = Counter(item.title.casefold() for item in items if item.title)
    profile_fragments: set[str] = set()
    profile_index = repo_root / "_pages" / "profiles.md"
    if profile_index.exists():
        metadata, _, _ = split_front_matter(profile_index.read_text(encoding="utf-8-sig"))
        profile_fragments = {
            f"_pages/{profile['content']}"
            for profile in metadata.get("profiles", [])
            if isinstance(profile, dict) and profile.get("content")
        }
    resource_groups: dict[str, str] = {}
    resource_index = repo_root / "_data" / "legacy_resources.yml"
    if resource_index.exists():
        for item in YAML(typ="safe").load(resource_index.read_text(encoding="utf-8-sig")) or []:
            if isinstance(item, dict) and item.get("destination_path"):
                resource_groups[str(item["destination_path"])] = str(item.get("group", ""))
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "path", "content_type", "title", "permalink", "has_frontmatter", "nav",
                "nav_order", "preferred_category", "duplicate_title_count", "parse_error",
            ],
        )
        writer.writeheader()
        for item in items:
            path = repo_root / item.path
            metadata, _, has_frontmatter = split_front_matter(path.read_text(encoding="utf-8-sig"))
            writer.writerow(
                {
                    "path": item.path,
                    "content_type": item.content_type,
                    "title": item.title,
                    "permalink": item.permalink,
                    "has_frontmatter": str(has_frontmatter).lower(),
                    "nav": metadata.get("nav", ""),
                    "nav_order": metadata.get("nav_order", ""),
                    "preferred_category": preferred_category(item.path, item.content_type, profile_fragments, resource_groups),
                    "duplicate_title_count": title_counts[item.title.casefold()] if item.title else 0,
                    "parse_error": item.parse_error,
                }
            )
    return len(items)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the site-manager information architecture inventory")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--output", default="SITE_INFORMATION_ARCHITECTURE_INVENTORY.csv")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    output = (repo / args.output).resolve()
    print(f"Wrote {write_inventory(repo, output)} records to {output}")


if __name__ == "__main__":
    main()
