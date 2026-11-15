#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone, standard-library Data Mining ZIP publisher.

The *repository*, not an external ChatGPT patch or Inbox launcher, owns this tool.
Input is one chapter ZIP (or an extracted ChapterNN directory). It validates
references before writing, syncs linked downloads into the Git checkout,
updates chapter text/images/TOC for new chapters, and stages only its changes.
It NEVER commits or pushes. Chapter updates require explicit opt-in.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime

BOOK = Path('courses/data-mining/book')
COURSE_NOTES = BOOK / 'course-notes'
PUBLIC = Path('assets/downloads/courses/data-mining/course-notes')
NUMBER = re.compile(r'^chapter(\d{2})\.md$', re.I)
CHAPTER_DIR = re.compile(r'^Chapter(\d{2})$', re.I)
CHAPTER_ZIP = re.compile(r'^(?:DataMining_)?Chapter(\d{2})(?:_.*)?$', re.I)
IMAGE_RE = re.compile(r'^\s*```\{figure\}\s+(\S+)', re.M)
MD_IMAGE_RE = re.compile(r'!\[[^\]]*\]\(([^\s)]+)')
HTML_IMAGE_RE = re.compile(r'<img\s[^>]*src=["\']([^"\']+)["\']', re.I)
HREF = re.compile(r'''href\s*=\s*["'](/assets/downloads/courses/data-mining/course-notes/chapter-\d{2}/[^"']+)["']''', re.I)
MAX_SINGLE = 80 * 1024 * 1024
MAX_TOTAL = 250 * 1024 * 1024

class PublishError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(cond: bool, why: str) -> None:
    if not cond:
        raise PublishError(why)


def safe_name(name: str) -> str:
    p = Path(name.replace('\\', '/'))
    require(name and not name.startswith(('/', '\\')) and not re.match(r'^[a-zA-Z]:', name)
            and all(q not in ('', '.', '..') for q in p.parts) and '\x00' not in name,
            'Unsafe filename in chapter package: ' + name)
    return '/'.join(p.parts)


def read_package(source: Path) -> dict[str, bytes]:
    require(source.exists(), 'Chapter package not found: ' + str(source))
    rows: dict[str, bytes] = {}
    total = 0
    if source.is_file():
        require(zipfile.is_zipfile(source), 'Chapter input must be a ZIP or extracted ChapterNN directory')
        with zipfile.ZipFile(source) as z:
            entries = [v for v in z.infolist() if not v.is_dir()]
            for info in entries:
                name = safe_name(info.filename)
                require(not ((info.external_attr >> 16) & 0o170000) == 0o120000,
                        'ZIP contains a symlink: ' + name)
                require(info.file_size <= MAX_SINGLE, 'Oversized chapter file: ' + name)
                total += info.file_size
                require(total <= MAX_TOTAL, 'Chapter ZIP uncompressed payload is too large')
                require(name not in rows, 'Duplicate filename: ' + name)
                rows[name] = z.read(info)
    else:
        require(source.is_dir(), 'Not a directory: ' + str(source))
        for p in sorted(source.rglob('*')):
            if p.is_symlink():
                raise PublishError('Chapter directory contains symlink: ' + str(p))
            if p.is_file():
                name = safe_name(p.relative_to(source).as_posix())
                require(p.stat().st_size <= MAX_SINGLE, 'Oversized chapter file: ' + name)
                total += p.stat().st_size
                require(total <= MAX_TOTAL, 'Chapter source directory too large')
                rows[name] = p.read_bytes()
    # Allow one enclosing ChapterNN folder (older ZIP variants).
    if 'chapter_meta.json' not in rows:
        prefixes = {x.split('/')[0] for x in rows}
        if len(prefixes) == 1 and CHAPTER_DIR.fullmatch(next(iter(prefixes))):
            rows = {p.split('/', 1)[1]: b for p, b in rows.items()}
    require('chapter_meta.json' in rows, 'Missing chapter_meta.json in ZIP root')
    return rows


def load_chapter(files: dict[str, bytes]):
    try:
        meta = json.loads(files['chapter_meta.json'].decode('utf-8-sig'))
    except (ValueError, UnicodeDecodeError) as exc:
        raise PublishError('Invalid chapter_meta.json: ' + str(exc)) from exc
    require(str(meta.get('course_id')) == 'data-mining', 'Wrong course_id: expected data-mining')
    num = int(meta.get('chapter_number', -1))
    require(1 <= num <= 99, 'Invalid chapter_number')
    s = f'{num:02d}'
    entry = str(meta.get('entry', ''))
    require(entry == f'chapter{s}.md', f'Entry must be chapter{s}.md, found {entry}')
    require(entry in files, 'Missing Markdown entry: ' + entry)
    expected = (COURSE_NOTES / f'chapter-{s}.md').as_posix()
    require(str(meta.get('destination_path')) == expected, 'destination_path must be ' + expected)
    try:
        markdown = files[entry].decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise PublishError('Chapter Markdown must be UTF-8') from exc
    require(markdown.lstrip().startswith('# '), 'Chapter Markdown must have an H1 heading')
    links = HREF.findall(markdown)
    require(len(links) > 0, 'No public download links found in chapter Markdown')
    linked: dict[str, bytes] = {}
    for href in links:
        # URL query/hash forbidden for local strict contract.
        require('?' not in href and '#' not in href and '%' not in href, 'Nonliteral download path: '+href)
        basename = href.split('/')[-1]
        require(basename and basename not in ('.', '..') and '/' not in basename, 'Invalid download: '+href)
        require(href == ('/' + (PUBLIC / f'chapter-{s}' / basename).as_posix()), 'Download URL chapter mismatch: '+href)
        key = 'downloads/' + basename
        require(key in files and bool(files[key]), 'Missing required download in ZIP: '+key)
        require(key not in linked or linked[key] == files[key], 'Conflicting download '+key)
        linked[key] = files[key]
        if basename.lower().endswith('.pdf'):
            require(files[key].startswith(b'%PDF-'), 'Invalid PDF: '+key)
        if basename.lower().endswith('.zip'):
            require(zipfile.is_zipfile(io.BytesIO(files[key])), 'Invalid inner ZIP: '+key)
        if basename.lower().endswith(('.ipynb', '.json')):
            try:
                json.loads(files[key].decode('utf-8-sig'))
            except (ValueError, UnicodeDecodeError) as exc:
                raise PublishError('Invalid JSON/Notebook: '+key) from exc
        if basename.lower().endswith('.py'):
            try:
                compile(files[key].decode('utf8'), key, 'exec')
            except (SyntaxError, UnicodeDecodeError) as exc:
                raise PublishError('Invalid Python code: '+key) from exc
    declared = meta.get('downloads', [])
    require(isinstance(declared, list) and all(isinstance(x, str) for x in declared), 'Metadata downloads must be a list')
    for key in linked:
        require(key in declared, 'Linked download missing from metadata: '+key)
    images = meta.get('images', [])
    require(isinstance(images, list) and bool(images), 'Metadata must list chapter images')
    for filename in images:
        require(isinstance(filename, str) and re.fullmatch(r'images/[\w.-]+\.(?:png|jpg|jpeg|webp|svg|gif)', filename, re.I) is not None,
                'Unsafe or unsupported image name: '+str(filename))
        require(filename in files and bool(files[filename]), 'Missing image: '+filename)
        if filename.lower().endswith('.png'):
            require(files[filename].startswith(b'\x89PNG\r\n\x1a\n'), 'Invalid PNG: '+filename)
    refs = IMAGE_RE.findall(markdown) + MD_IMAGE_RE.findall(markdown) + HTML_IMAGE_RE.findall(markdown)
    for url in refs:
        # Chapter fixtures may already have a canonical target path.
        relative = url
        prefix = f'chapter-{s}-assets/'
        if relative.startswith(prefix):
            relative = relative[len(prefix):]
        require(relative in images, 'Referenced MyST/Markdown image missing from declared images: '+url)
    require(bool(refs), 'No image references found in chapter')
    # Normalize image URLs in Markdown once, within known syntactic contexts.
    def canon(match):
        src = match.group(2)
        if src.startswith(f'chapter-{s}-assets/'):
            return match.group(0)
        return match.group(1) + f'chapter-{s}-assets/' + src
    markdown = re.sub(r'(^\s*```\{figure\}\s+)(images/[\w.-]+)', canon, markdown, flags=re.M)
    markdown = re.sub(r'(!\[[^\]]*\]\()(images/[\w.-]+)', canon, markdown)
    markdown = re.sub(r'(<img\s[^>]*src=["\'])(images/[\w.-]+)', canon, markdown, flags=re.I)
    return s, meta, markdown.encode('utf8'), linked, images


def update_toc(existing: bytes, number: str, title: str) -> bytes:
    raw = existing.decode('utf-8-sig')
    if re.search(r'^\s+- file: course-notes/chapter-'+number+r'\s*$', raw, re.M):
        return existing
    candidates = list(re.finditer(r'(?m)^([ \t]*)- file: course-notes/chapter-(\d{2})[ \t]*\n(?:[ \t]+title:.*\n)?', raw))
    require(candidates, 'Unrecognized _toc.yml; refusing to edit it')
    last = candidates[-1]
    indent = last.group(1)
    nums = [int(m.group(2)) for m in candidates]
    require(int(number) > max(nums), 'Refusing to insert an out-of-order chapter in TOC')
    require(title and '\n' not in title, 'Chapter title invalid')
    quote = json.dumps(title, ensure_ascii=False)
    insert = f'{indent}- file: course-notes/chapter-{number}\n{indent}  title: {quote}\n'
    return (raw[:last.end()] + insert + raw[last.end():]).encode('utf8')


def public_links_ok(repo: Path) -> int:
    count = 0
    for md in sorted((repo / COURSE_NOTES).glob('chapter-*.md')):
        content = md.read_text(encoding='utf-8-sig')
        for url in HREF.findall(content):
            rel = url.lstrip('/')
            require('..' not in Path(rel).parts, 'Unsafe URL: '+url)
            target = repo / rel
            require(target.is_file() and target.stat().st_size > 0, '[MISSING BEFORE COMMIT] '+url+' in '+md.name)
            count += 1
    return count


def git_binary() -> str | None:
    x = shutil.which('git')
    if x:
        return x
    if os.name == 'nt':
        paths = [Path(r'C:\Program Files\Git\cmd\git.exe')]
        app = Path(os.environ.get('LOCALAPPDATA', r'C:\Users\Public\AppData\Local')) / 'GitHubDesktop'
        paths += sorted(app.glob('app-*/resources/app/git/cmd/git.exe'), reverse=True)
        for p in paths:
            if p.is_file():
                return str(p)
    return None


def git(repo: Path, exe: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([exe, '-C', str(repo), *args], capture_output=True, text=True,
                          encoding='utf-8', errors='replace', check=check)


def publish(repo: Path, files: dict[str, bytes], *, allow_update: bool = False,
            do_stage: bool = True, dry_run: bool = False, do_commit: bool = False, do_build: bool = False) -> list[Path]:
    require((repo / '.git').exists(), 'Not a Git checkout: '+str(repo))
    require((repo / BOOK / '_toc.yml').is_file(), 'Data Mining TOC missing')
    s, meta, md, downloads, images = load_chapter(files)
    existing = repo / COURSE_NOTES / f'chapter-{s}.md'
    toc = repo / BOOK / '_toc.yml'
    proposed: dict[Path, bytes] = {}
    if not existing.is_file():
        proposed[existing] = md
        for image in images:
            proposed[repo / COURSE_NOTES / f'chapter-{s}-assets' / image] = files[image]
        proposed[toc] = update_toc(toc.read_bytes(), s, str(meta.get('title', f'Chapter {s}')))
    elif allow_update and meta.get('update_existing') is True:
        proposed[existing] = md
        for image in images:
            proposed[repo / COURSE_NOTES / f'chapter-{s}-assets' / image] = files[image]
    else:
        print(f'[KEEP] Chapter {s} already in the book: text and images preserved.')
        # For a published chapter, verify existing referenced images.
        existing_text = existing.read_text(encoding='utf-8-sig')
        for url in IMAGE_RE.findall(existing_text):
            if url.startswith(f'chapter-{s}-assets/images/'):
                require((existing.parent / url).is_file(), 'Image missing from existing chapter: '+url)
    for key, data in downloads.items():
        dest = repo / PUBLIC / f'chapter-{s}' / key.removeprefix('downloads/')
        if not dest.is_file() or allow_update:
            proposed[dest] = data
        elif dest.read_bytes() != data:
            raise PublishError('Existing downloadable file differs; no overwrite without --allow-update: '+str(dest))
    edits = {p: data for p, data in proposed.items() if not p.is_file() or p.read_bytes() != data}
    for p in edits:
        require(p.is_relative_to(repo) and not p.is_symlink(), 'Unsafe target: '+str(p))
    print(f'[PREFLIGHT OK] Chapter {s}: {len(images)} images, {len(downloads)} public downloads, {len(edits)} changes.')
    for p in sorted(edits):
        print('   +', p.relative_to(repo).as_posix())
    if dry_run:
        return list(edits)
    require(not do_commit or do_stage, 'Cannot commit with --no-stage')
    exe = git_binary() if do_stage else None
    if do_stage:
        require(exe is not None, 'Git executable not found; files not changed. Install Git or use --no-stage.')
        require(git(repo, exe, 'rev-parse', '--is-inside-work-tree').stdout.strip() == 'true', 'Invalid Git worktree')
        # The critical correction: stage ALL linked downloads, including files that
        # already have correct bytes on disk but are untracked / not in a commit.
        rels = sorted(set([p.relative_to(repo).as_posix() for p in edits] +
                          [(PUBLIC / f'chapter-{s}' / k.removeprefix('downloads/')).as_posix() for k in downloads]))
        # An earlier failed attempt may already have correct files staged.
        # Re-running this one-click command must be safe and idempotent.
        # Existing different binary contents were already rejected above.
    # Back up existing changed content outside the repository so Git never sees backups.
    backup_parent = repo.parent / '_COURSE_INBOX' / '_BACKUPS'
    backup = backup_parent / ('DM_ONECLICK_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    saved = {}
    try:
        for p, data in edits.items():
            old = p.read_bytes() if p.is_file() else None
            saved[p] = old
            if old is not None:
                rel = p.relative_to(repo)
                dest = backup / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(old)
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(p.suffix+'.dm-write')
            require(not tmp.exists(), 'Temporary write path already exists: '+str(tmp))
            try:
                tmp.write_bytes(data)
                os.replace(tmp, p)
            finally:
                tmp.unlink(missing_ok=True)
        n = public_links_ok(repo)
        print(f'[REFERENCES OK] {n} linked downloads found on disk.')
        if do_stage:
            git(repo, exe, 'add', '--', *rels)
            for rel in rels:
                tracked = git(repo, exe, 'ls-files', '--error-unmatch', '--', rel, check=False)
                require(tracked.returncode == 0, 'Git index did not record: '+rel)
                staged_sha = git(repo, exe, 'rev-parse', ':' + rel).stdout.strip()
                disk_sha = git(repo, exe, 'hash-object', rel).stdout.strip()
                require(staged_sha == disk_sha, 'Git stage differs from chapter bytes: ' + rel)
            print(f'[GIT INDEX OK] {len(rels)} chapter paths verified in Git index (including unchanged on disk).')
            if do_build:
                for cmd in ('validate', 'build'):
                    args = [sys.executable, '-m', 'tools.jupyterbook_manager', '--repo', str(repo), cmd, '--book', 'data-mining']
                    if cmd == 'build':
                        args.append('--clean')
                    print('[LOCAL BOOK '+cmd.upper()+'] '+ ' '.join(args), flush=True)
                    proc = subprocess.run(args, cwd=repo, check=False)
                    require(proc.returncode == 0, 'Jupyter Book '+cmd+' failed locally. No commit was created.')
                print('[LOCAL BOOK BUILD OK]')
            if do_commit:
                print(f'[READY TO COMMIT] Chapter {s}; only these {len(rels)} paths, no other worktree files.')
                approval = input('Type COMMIT to create a local Git commit (NO PUSH): ').strip()
                require(approval == 'COMMIT', 'Commit not approved. Files are staged, but NOT committed or pushed.')
                changed_stage = git(repo, exe, 'diff', '--cached', '--name-only', '--', *rels).stdout.strip()
                if changed_stage:
                    git(repo, exe, 'commit', '--only', '-m', f'Data Mining chapter {s}: complete content and downloads', '--', *rels)
                else:
                    print('[GIT] No changes need committing; assets are already in the latest commit.')
                for rel in rels:
                    obj = git(repo, exe, 'rev-parse', 'HEAD:' + rel, check=False)
                    require(obj.returncode == 0, 'HEAD commit does not include required asset: '+rel)
                    disk = git(repo, exe, 'hash-object', rel).stdout.strip()
                    require(obj.stdout.strip() == disk, 'HEAD content differs from required asset: '+rel)
                print('[COMMIT VERIFIED] Every chapter download is now recorded in HEAD; Push only after this message.')
        if edits:
            print(f'[BACKUP] Previous versions: {backup}' if backup.exists() else '[BACKUP] No existing files replaced.')
        print('[SUCCESS] All linked downloads verified in working tree and Git index. ' + ('Local commit verified. PUSH is still manual.' if do_commit else 'COMMIT and PUSH are still required.'))
        return list(edits)
    except Exception:
        if do_stage and edits and exe:
            rels = [p.relative_to(repo).as_posix() for p in edits]
            git(repo, exe, 'reset', '--quiet', '--', *rels, check=False)
        for p, old in reversed(list(saved.items())):
            if old is None:
                p.unlink(missing_ok=True)
            else:
                p.write_bytes(old)
        print('[ROLLBACK] Restored all changed chapter files.', file=sys.stderr)
        raise



def pending_from_inbox(repo: Path, inbox: Path) -> Path | None:
    require(inbox.is_dir(), 'Inbox directory not found: '+str(inbox))
    paths = []
    for p in inbox.iterdir():
        if p.is_dir() and CHAPTER_DIR.fullmatch(p.name):
            paths.append((int(CHAPTER_DIR.fullmatch(p.name).group(1)), p))
        elif p.is_file() and p.suffix.lower() == '.zip' and CHAPTER_ZIP.fullmatch(p.stem):
            paths.append((int(CHAPTER_ZIP.fullmatch(p.stem).group(1)), p))
    paths.sort(key=lambda x:(x[0], x[1].is_file()))
    require(bool(paths), 'No ChapterNN folder or ChapterNN.zip in Inbox: '+str(inbox))
    exe = git_binary()
    require(exe is not None, 'Git executable not found: cannot verify committed downloads')
    for n, p in paths:
        md = repo / COURSE_NOTES / f'chapter-{n:02d}.md'
        if not md.is_file():
            return p
        for href in HREF.findall(md.read_text(encoding='utf-8-sig')):
            path = href.lstrip('/')
            file = repo / path
            if not file.is_file() or file.stat().st_size == 0:
                return p
            committed = git(repo, exe, 'cat-file', '-e', 'HEAD:'+path, check=False)
            if committed.returncode != 0:
                return p
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Independent Data Mining chapter publisher')
    parser.add_argument('--repo', type=Path, required=True)
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument('--source', type=Path, help='ChapterNN ZIP or extracted folder')
    sources.add_argument('--inbox', type=Path, help='Auto-select earliest unpublished ChapterNN ZIP/folder in Inbox')
    parser.add_argument('--validate-only', action='store_true', help='Validate ZIP contract; no writes')
    parser.add_argument('--dry-run', action='store_true', help='Show exact changes; no writes')
    parser.add_argument('--no-stage', action='store_true', help='Do not run git add (for offline QA)')
    parser.add_argument('--allow-update', action='store_true', help='Update existing chapter only if metadata allows')
    parser.add_argument('--commit', action='store_true', help='Ask for COMMIT approval; commit ONLY this chapter and its public assets, then verify HEAD')
    parser.add_argument('--build', action='store_true', help='Validate and build local Jupyter Book before commit (requires book environment)')
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve()
        source = args.source.resolve() if args.source else pending_from_inbox(repo, args.inbox.resolve())
        if source is None:
            print('[UP TO DATE] No unpublished chapters or missing downloads in this Inbox.')
            return 0
        print('[CHAPTER PACKAGE] '+str(source))
        files = read_package(source)
        s, meta, md, downloads, images = load_chapter(files)
        if args.validate_only:
            print(f'[VALIDATED] Chapter {s}: {len(images)} images, {len(downloads)} public downloads; correct ZIP contract.')
            return 0
        publish(repo, files, allow_update=args.allow_update,
                do_stage=not args.no_stage, dry_run=args.dry_run, do_commit=args.commit, do_build=args.build)
        return 0
    except (OSError, ValueError, PublishError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        print('[STOP] ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
