#!/usr/bin/env python3
"""Validate/stage ONLY packages installed by the universal course publisher.
Does not scan unrelated legacy course download links. Standard library only.
"""
from __future__ import annotations
import argparse,json,shutil,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    grp=p.add_mutually_exclusive_group(required=True)
    grp.add_argument('--check',action='store_true')
    grp.add_argument('--site-dir',type=Path)
    a=p.parse_args();repo=a.repo.resolve()
    manifest=repo/'tools/course_package_manifest.json'
    if not manifest.is_file():
        print('[UNIVERSAL] No published course package manifest; nothing to stage.');return 0
    data=json.loads(manifest.read_text('utf8'))
    if data.get('schema_version')!=1 or not isinstance(data.get('packages'),list):
        print('[STOP] Invalid universal publisher manifest',file=sys.stderr);return 2
    count=0;missing=[]
    for entry in data['packages']:
        md=Path(entry['markdown'])
        if md.is_absolute() or '..' in md.parts or not (repo/md).is_file():
            missing.append(str(md));continue
        text=(repo/md).read_text('utf-8-sig')
        for s in entry['downloads']:
            rel=Path(s)
            if rel.is_absolute() or '..' in rel.parts or not rel.as_posix().startswith('assets/downloads/courses/'):
                missing.append('unsafe: '+s);continue
            src=repo/rel
            if not src.is_file() or src.stat().st_size==0 or ('/'+rel.as_posix()) not in text:
                missing.append(str(rel));continue
            if a.site_dir:
                site=a.site_dir if a.site_dir.is_absolute() else repo/a.site_dir
                dst=site/rel;dst.parent.mkdir(parents=True,exist_ok=True)
                if not dst.is_file() or dst.stat().st_size!=src.stat().st_size or src.read_bytes()!=dst.read_bytes():shutil.copy2(src,dst)
                if not dst.is_file() or dst.stat().st_size==0:missing.append('site:'+str(rel))
            count+=1
    if missing:
        print('[STOP] Universal published assets missing:',*missing,sep='\n  ',file=sys.stderr);return 2
    print(f'[UNIVERSAL OK] {len(data["packages"])} registered package(s), {count} public downloads '+('verified in checkout.' if a.check else 'staged in site.'))
    return 0
if __name__=='__main__':raise SystemExit(main())
