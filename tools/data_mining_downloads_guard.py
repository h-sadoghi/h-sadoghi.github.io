#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract guard for Data Mining chapter downloadable assets.

Three modes:
  --check: fail immediately if a chapter Markdown href points to absent/empty repo asset.
  --sync --inbox <CHAPTERS>: first copy only linked files from ChapterNN/downloads,
                            then check all chapter download hrefs.
The site build continues to use tools/stage_data_mining_downloads.py unchanged.
This file intentionally does not modify any chapter Markdown, Jupyter Book, or site config.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote

BOOK = Path('courses/data-mining/book/course-notes')
PUBLIC = Path('assets/downloads/courses/data-mining/course-notes')
HREF = re.compile(r'''href\s*=\s*["'](/assets/downloads/courses/data-mining/course-notes/chapter-\d{2}/[^"']+)["']''', re.I)
CHAPTER = re.compile(r'^chapter-(\d{2})\.md$', re.I)
ALLOWED_SUFFIXES = {'.pdf', '.zip', '.ipynb', '.py', '.csv', '.json', '.md', '.txt', '.tex', '.html', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.xlsx', '.npy', '.npz', '.parquet'}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def list_links(repo: Path) -> list[tuple[Path, Path, str]]:
    chapter_folder = repo / BOOK
    if not chapter_folder.is_dir():
        raise RuntimeError('Data Mining chapter folder not found: ' + str(chapter_folder))
    rows = []
    for md in sorted(chapter_folder.glob('chapter-*.md')):
        if not CHAPTER.fullmatch(md.name):
            continue
        content = md.read_text(encoding='utf-8-sig')
        for href in HREF.findall(content):
            path = unquote(href.split('?', 1)[0].split('#', 1)[0].lstrip('/'))
            rel = Path(path)
            if '..' in rel.parts or rel.is_absolute() or not rel.is_relative_to(PUBLIC):
                raise RuntimeError('Unsafe download URL in '+md.name+': '+href)
            parts = rel.relative_to(PUBLIC).parts
            if len(parts) != 2 or parts[0] != md.stem or not parts[-1] or parts[-1].startswith('.'):
                raise RuntimeError('Download chapter/path mismatch in '+md.name+': '+href)
            if Path(parts[-1]).suffix.lower() not in ALLOWED_SUFFIXES:
                raise RuntimeError('Unexpected downloadable extension in '+md.name+': '+href)
            rows.append((md, repo / rel, href))
    return rows


def atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.data-mining-guard-', dir=str(target.parent))
    tmp = Path(temp)
    try:
        with os.fdopen(fd, 'wb') as dst, source.open('rb') as src:
            shutil.copyfileobj(src, dst)
            dst.flush()
            os.fsync(dst.fileno())
        os.replace(tmp, target)
    finally:
        tmp.unlink(missing_ok=True)


def verify(rows: list[tuple[Path, Path, str]], repo: Path) -> None:
    missing = [(md, dst, href) for md, dst, href in rows if not dst.is_file() or dst.stat().st_size == 0]
    if missing:
        for md, _, href in missing:
            print('[MISSING BEFORE BUILD] ' + md.name + ': ' + href, flush=True)
        raise RuntimeError(f'{len(missing)} missing Data Mining download(s) in Git checkout. '
                           'Run the corrected local One-Click launcher and commit its new assets.')
    print(f'[OK] {len(rows)} Data Mining public download references exist in the Git working tree.', flush=True)


def sync(repo: Path, inbox: Path, rows: list[tuple[Path, Path, str]]) -> None:
    if not inbox.is_dir():
        raise RuntimeError('Chapter Inbox directory missing: '+str(inbox))
    # All required source files must be present *before* any write.
    edits: dict[Path, Path] = {}
    absent: list[str] = []
    for md, dst, href in rows:
        number = md.stem.split('-')[-1]
        chapter = inbox / ('Chapter' + number)
        src = chapter / 'downloads' / dst.name
        if src.is_file() and not src.is_symlink() and src.stat().st_size > 0:
            if not dst.is_file() or sha256(src) != sha256(dst):
                edits[dst] = src
        elif not dst.is_file() or dst.stat().st_size == 0:
            absent.append(href + ' (expected in ' + str(src) + ')')
    if absent:
        for item in absent:
            print('[MISSING IN REPO AND INBOX] '+item, flush=True)
        raise RuntimeError('No files changed. Restore the original ChapterNN/downloads folder or install the bundled chapter repair.')

    # We only create/update tracked-site assets linked by the chapter.
    snapshots: dict[Path, bytes | None] = {}
    try:
        for dest, src in sorted(edits.items(), key=lambda x: str(x[0])):
            if dest.is_symlink() or any(p.is_symlink() for p in dest.parents if p != repo.parent):
                raise RuntimeError('Unsafe symlink destination: '+str(dest))
            snapshots[dest] = dest.read_bytes() if dest.is_file() else None
            atomic_copy(src, dest)
        verify(rows, repo)
    except Exception:
        for dest, old in reversed(list(snapshots.items())):
            if old is None:
                dest.unlink(missing_ok=True)
            else:
                fd, temp = tempfile.mkstemp(prefix='.data-mining-rollback-', dir=str(dest.parent))
                with os.fdopen(fd, 'wb') as f:
                    f.write(old)
                os.replace(temp, dest)
        raise
    print(f'[OK] Data Mining One-Click download sync: {len(edits)} asset(s) created/updated.', flush=True)
    if edits:
        print('[IMPORTANT] In GitHub Desktop COMMIT AND PUSH the added/updated chapter download files.', flush=True)
        for dest in sorted(edits):
            print('   + '+dest.relative_to(repo).as_posix(), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--sync', action='store_true')
    parser.add_argument('--inbox', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not (repo / '.git').exists():
        print('[STOP] Not a Git repository/worktree: '+str(repo), file=sys.stderr)
        return 2
    try:
        rows = list_links(repo)
        if args.sync:
            if not args.inbox:
                raise RuntimeError('--sync requires --inbox pointing to the CHAPTERS folder')
            sync(repo, args.inbox.resolve(), rows)
        else:
            verify(rows, repo)
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print('[STOP] '+str(exc), file=sys.stderr, flush=True)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
