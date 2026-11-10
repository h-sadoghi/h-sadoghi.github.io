"""Stage linked course notebook downloads that Jekyll excludes by default.

This utility runs after all Jupyter Books have been staged into _site and before
link checking and deployment. It does not execute any notebook.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from shutil import copy2
from urllib.parse import unquote, urlsplit

COURSES = ("data-engineering", "image-processing")


class NotebookLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if key in {"href", "src"} and val and ".ipynb" in val:
                self.urls.add(val)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--site-dir", type=Path, default=Path("_site"))
    args = parser.parse_args()
    repo = args.repo.resolve()
    site = args.site_dir if args.site_dir.is_absolute() else repo / args.site_dir
    site = site.resolve()
    if not site.is_dir():
        raise SystemExit("ERROR: The built _site directory does not exist.")
    copied = 0
    verified = 0
    for course in COURSES:
        source = repo / "assets" / "downloads" / "courses" / course
        if not source.is_dir():
            raise SystemExit(f"ERROR: course download source missing: {source}")
        for notebook in sorted(source.rglob("*.ipynb")):
            if notebook.is_symlink():
                raise SystemExit(f"ERROR: symlinked notebook rejected: {notebook}")
            destination = site / notebook.relative_to(repo)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.is_file() or destination.stat().st_size != notebook.stat().st_size:
                copy2(notebook, destination)
                copied += 1
            if not destination.is_file() or destination.stat().st_size != notebook.stat().st_size:
                raise SystemExit(f"ERROR: notebook staging failed: {destination}")
            verified += 1

    linked = set()
    for course in COURSES:
        html_dir = site / "teaching" / course / "book"
        for page in html_dir.rglob("*.html") if html_dir.is_dir() else []:
            finder = NotebookLinks()
            finder.feed(page.read_text(encoding="utf-8", errors="replace"))
            for url in finder.urls:
                p = urlsplit(url)
                prefix = f"/assets/downloads/courses/{course}/"
                if p.path.startswith(prefix) and p.path.lower().endswith(".ipynb"):
                    linked.add(unquote(p.path))
    missing = [p for p in sorted(linked) if not (site / p.lstrip("/")).is_file()]
    if missing:
        raise SystemExit("ERROR: Missing linked notebook(s):\n" + "\n".join(missing))
    print(f"PASS: {verified} source notebooks checked; {copied} copied into _site; {len(linked)} distinct links verified.")


if __name__ == "__main__":
    main()
