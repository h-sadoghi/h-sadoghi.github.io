#!/usr/bin/env python3
"""Stage only Data Mining public downloads after Jekyll/Jupyter Book build.

This intentionally copies from tracked repository assets into generated _site.
No changes to Markdown sources, TOC, CSS, or other courses.
"""
from __future__ import annotations
import argparse
import re
import shutil
from pathlib import Path

PUBLIC_SUBPATH = Path('assets/downloads/courses/data-mining/course-notes')
LINK_RE = re.compile(r'href="(/assets/downloads/courses/data-mining/course-notes/[^"]+)"')


def stage(repo: Path, site: Path) -> None:
    source = repo / PUBLIC_SUBPATH
    destination = site / PUBLIC_SUBPATH
    if not source.is_dir():
        raise SystemExit(f'Missing repository downloads directory: {source}')
    if not site.is_dir():
        raise SystemExit(f'Not a generated site directory: {site}')
    copied = 0
    unchanged = 0
    for src in sorted(source.rglob('*')):
        if not src.is_file():
            continue
        rel = src.relative_to(source)
        dst = destination / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_file() and src.stat().st_size == dst.stat().st_size and src.read_bytes() == dst.read_bytes():
            unchanged += 1
            continue
        shutil.copy2(src, dst)
        copied += 1
    print(f'Data Mining staged: {copied} new/updated, {unchanged} unchanged.')
    checked = 0
    missing = []
    for md in sorted((repo/'courses/data-mining/book/course-notes').glob('chapter-*.md')):
        content=md.read_text(encoding='utf-8')
        for link in LINK_RE.findall(content):
            checked += 1
            target=site / link.lstrip('/')
            if not target.is_file() or target.stat().st_size == 0:
                missing.append(link)
    if missing:
        for link in sorted(set(missing)):
            print(f'MISSING DOWNLOAD TARGET: {link}')
        raise SystemExit(f'ERROR: {len(set(missing))} downloadable targets missing after stage')
    print(f'Data Mining download link targets verified: {checked} references.')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,default=Path.cwd())
    ap.add_argument('--site-dir',type=Path,default=Path('_site'))
    args=ap.parse_args()
    repo=args.repo.resolve()
    site=args.site_dir
    if not site.is_absolute():site=repo/site
    stage(repo,site.resolve())

if __name__ == '__main__':main()
