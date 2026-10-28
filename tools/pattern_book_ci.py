#!/usr/bin/env python3
"""Compile Pattern Recognition using native Jupyter Book v1, and stage AFTER Jekyll.

CI must call this immediately before the existing Pages publication action.
"""
import argparse
import functools
import hashlib
import http.server
import pathlib
import shutil
import subprocess
import sys
import tempfile
import webbrowser

DEFAULT_REPO = pathlib.Path(__file__).resolve().parent.parent
SOURCE_REL = pathlib.Path('courses/pattern-recognition/book')
SITE_REL = pathlib.Path('teaching/pattern-recognition/book')


def cli_path(repo):
    for cli in [repo / '.venv-jupyterbook/Scripts/jupyter-book.exe',
                repo / '.venv-jupyterbook/bin/jupyter-book']:
        if cli.is_file(): return str(cli)
    return shutil.which('jupyter-book')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def build(repo, stage=True, preview=False):
    src = repo / SOURCE_REL
    if not (src / '_toc.yml').is_file():
        raise ValueError('Pattern Recognition book is not installed.')
    cli = cli_path(repo)
    if not cli:
        raise ValueError('Jupyter Book v1 CLI not found. Run SETUP_JUPYTERBOOK.cmd once.')
    print('[1/2] Clean old Jupyter Book output...', flush=True)
    subprocess.run([cli, 'clean', str(src), '--all'], cwd=repo, check=True)
    print('[2/2] Build with the original Jupyter Book compiler...', flush=True)
    subprocess.run([cli, 'build', str(src)], cwd=repo, check=True)
    html = src / '_build/html'
    if not (html / 'index.html').is_file() or not (html / '_static').is_dir():
        raise ValueError('Build is missing HTML index or Sphinx Book Theme assets.')
    if stage:
        site = repo / '_site'
        if not (site / 'index.html').is_file():
            raise ValueError('Jekyll _site/index.html missing. Build Jekyll BEFORE staging.')
        target = site / SITE_REL
        if target.exists():
            raise ValueError('Target site book already exists; refusing to replace: ' + str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=str(target.parent), prefix='.pr-stage-') as tmp:
            work = pathlib.Path(tmp) / 'book'
            shutil.copytree(html, work)
            files = {p.relative_to(html).as_posix(): p for p in html.rglob('*') if p.is_file()}
            copied = {p.relative_to(work).as_posix(): p for p in work.rglob('*') if p.is_file()}
            if files.keys() != copied.keys():
                raise ValueError('Copied file set differs from source.')
            for key, orig in files.items():
                if sha(orig) != sha(copied[key]):
                    raise ValueError('Copied file digest mismatch: ' + key)
            work.rename(target)
        (site / '.nojekyll').touch(exist_ok=True)
        print('SUCCESS: Staged', len(files), 'unmodified HTML/assets files into', target)
    else:
        print('SUCCESS: Book HTML created:', html)
    if preview:
        port = 4102
        url = 'http://127.0.0.1:{}/'.format(port)
        print('PREVIEW READY:', url, flush=True)
        print('Use Ctrl+C to stop.', flush=True)
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(html))
        with http.server.ThreadingHTTPServer(('127.0.0.1', port), handler) as server:
            webbrowser.open(url)
            try: server.serve_forever()
            except KeyboardInterrupt: pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=pathlib.Path, default=DEFAULT_REPO)
    p.add_argument('--no-stage', action='store_true')
    p.add_argument('--preview', action='store_true')
    args = p.parse_args()
    try:
        build(args.repo.resolve(), stage=not args.no_stage, preview=args.preview)
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('ERROR:', exc, file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
