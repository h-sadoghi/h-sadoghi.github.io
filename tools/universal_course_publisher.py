#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Universal chapter/Markdown publisher for *registered* Jupyter Book courses.

Standard library only; no Git push, no credential access, no arbitrary shell from ZIP.
Contract: root chapter_meta.json + entry Markdown + images/ + downloads/.
Also accepts raw Markdown with --course <registered-id>.
Explicit COMMIT stages and commits only affected paths, verifying HEAD afterwards.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

class PublishError(RuntimeError):pass

def must(ok,why):
    if not ok:raise PublishError(why)

def safe_rel(s):
    must(isinstance(s,str) and s and not s.startswith(('/', '\\')) and not re.match(r'^[A-Za-z]:',s),f'Unsafe path: {s}')
    must('\\' not in s and '\x00' not in s,'Use POSIX relative paths without backslashes')
    p=PurePosixPath(s)
    must(all(x not in ('','.','..') for x in p.parts) and len(p.parts)>0 and p.as_posix()==s,f'Unsafe relative path: {s}')
    return Path(*p.parts)

def inside(repo,rel):
    target=repo/rel
    must(target.resolve().is_relative_to(repo.resolve()),f'Target escapes repository: {rel}')
    return target

def git_exe():
    x=shutil.which('git')
    if x:return x
    if os.name=='nt':
        ps=[Path(r'C:\Program Files\Git\cmd\git.exe')]
        app=Path(os.environ.get('LOCALAPPDATA',r'C:\Users\Public\AppData\Local'))/'GitHubDesktop'
        ps+=sorted(app.glob('app-*/resources/app/git/cmd/git.exe'),reverse=True)
        for p in ps:
            if p.is_file():return str(p)
    raise PublishError('Git not found. Install Git/GitHub Desktop, and restart CMD.')

def git(repo,*a,check=True):
    p=subprocess.run([git_exe(),'-C',str(repo),*a],capture_output=True,text=True,encoding='utf8',errors='replace')
    if check and p.returncode:raise PublishError(f'Git {a[0]} failed: {p.stderr.strip()[:500]}')
    return p

def sha(b):return hashlib.sha256(b).hexdigest()

def registry(repo):
    path=repo/'tools/jupyterbook_manager/books.yml'
    must(path.is_file(),'Jupyter Book registry missing: tools/jupyterbook_manager/books.yml')
    out={};current=None
    for ln in path.read_text(encoding='utf-8-sig').splitlines():
        if (m:=re.match(r'^\s{2}-\s+id:\s*([\w-]+)\s*$',ln)):
            current=m.group(1);out[current]={}
        elif current and (m:=re.match(r'^\s{4}(source|title|public_path):\s*(.*?)\s*$',ln)):
            out[current][m.group(1)]=m.group(2).strip('"\'')
    valid={}
    for cid,d in out.items():
        if 'source' in d:
            src=safe_rel(d['source'])
            valid[cid]={'root':src,'title':d.get('title',cid)}
    must(bool(valid),'No registered Jupyter Book courses found')
    return valid

def load_source(path,course=None,repo=None):
    must(path.exists(),f'Input not found: {path}')
    files={}
    if path.suffix.lower()=='.md' and path.is_file():
        must(bool(course),'For a plain .md specify --course <registered-course-id>')
        files[path.name]=path.read_bytes()
        for folder in ['images','downloads']:
            d=path.parent/folder
            if d.is_dir():
                for p in d.rglob('*'):
                    must(not p.is_symlink(),f'Symlink refused: {p}')
                    if p.is_file():files[(Path(folder)/p.relative_to(d)).as_posix()]=p.read_bytes()
        return files,{'course_id':course,'entry':path.name,'title':path.stem.replace('_',' '),'raw_markdown':True}
    must(path.suffix.lower()=='.zip' and zipfile.is_zipfile(path),'Input must be .md or a valid ZIP')
    total=0;lower=set()
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.is_dir():continue
            name=info.filename
            safe_rel(name)
            must(not ((info.external_attr>>16)&0o170000)==0o120000,f'Symlink inside ZIP: {name}')
            must(info.file_size<=100*1024*1024,f'Oversized file: {name}')
            total+=info.file_size;must(total<=360*1024*1024,'ZIP too large after decompression')
            must(name.lower() not in lower,f'Duplicate case-insensitive ZIP name: {name}')
            lower.add(name.lower());files[name]=z.read(info)
    if 'chapter_meta.json' not in files:
        parents={x.split('/')[0] for x in files}
        if len(parents)==1 and all('/' in x for x in files):
            files={k.split('/',1)[1]:v for k,v in files.items()}
    must('chapter_meta.json' in files,'ZIP root must contain chapter_meta.json')
    try:meta=json.loads(files['chapter_meta.json'].decode('utf-8-sig'))
    except Exception as e:raise PublishError('Invalid chapter_meta.json: '+str(e)) from e
    must(isinstance(meta,dict),'chapter_meta.json must be an object')
    return files,meta

FIG=re.compile(r'(?m)^(\s*```\{figure\}\s+)([^\s]+)')
MDIMAGE=re.compile(r'(!\[[^\]]*\]\()([^\s)]+)(\))')
HTMLIMAGE=re.compile(r'(<img\s[^>]*?src=["\'])([^"\']+)(["\'])',re.I)
HTMLLINK=re.compile(r'(href=["\'])([^"\']+)(["\'])',re.I)
MDLINK=re.compile(r'(?<!!)\[([^\]]+)\]\(([^\s)]+)\)')
PUBLIC_LINK=re.compile(r'/assets/downloads/courses/([\w-]+)/([^\s"\')#?]+)')

def replacement_images(text,images,dest_stem):
    """Accept MyST, markdown and HTML. Require every local image and normalize just known refs."""
    prefix=dest_stem+'-assets/'
    out=[]
    def repl(m):
        path=m.group(2)
        if path.startswith('images/'):
            must(path in images,f'Image reference not found in package: {path}')
            out.append(path)
            return m.group(1)+prefix+path+(m.group(3) if m.lastindex and m.lastindex>=3 else '')
        if path.startswith(prefix+'images/'):
            key=path[len(prefix):]
            must(key in images,f'Canonical image missing from package: {path}')
            out.append(key)
        elif not (path.startswith(('http://','https://','data:','/','#'))):
            raise PublishError('Unknown relative image path (use images/name): '+path)
        return m.group(0)
    for rx in (FIG,MDIMAGE,HTMLIMAGE):text=rx.sub(repl,text)
    return text,out

def prepare(repo,files,meta,forced_course=None):
    books=registry(repo)
    if forced_course and not meta.get('raw_markdown') and meta.get('course_id')!=forced_course:
        raise PublishError('The --course argument contradicts ZIP course_id; refusing cross-course import')
    course=forced_course or str(meta.get('course_id',''))
    must(course in books,f'Course is not registered in books.yml: {course}. Existing courses: {", ".join(books)}')
    root=books[course]['root']
    entry=str(meta.get('entry',''))
    if not entry:
        candidates=[k for k in files if k.endswith('.md') and '/' not in k]
        must(len(candidates)==1,'Exactly one root Markdown entry is required')
        entry=candidates[0]
    safe_rel(entry)
    must(entry in files and entry.endswith('.md'),'Markdown entry missing in package: '+entry)
    if meta.get('destination_path'):
        dest_rel=safe_rel(meta['destination_path'])
        must(dest_rel.is_relative_to(root),f'destination_path must be under registered book {root}')
    else:
        notes='course-notes' if (repo/root/'course-notes').is_dir() else ('chapters' if (repo/root/'chapters').is_dir() else '')
        dest_rel=root/notes/entry
    must(dest_rel.suffix.lower()=='.md','Destination must be Markdown')
    dest_in_book=dest_rel.relative_to(root)
    must(dest_in_book.name!='index.md','Index files are not auto-published; use a chapter/page name')
    title=str(meta.get('title') or Path(entry).stem).replace('\n',' ').strip()
    must(title and len(title)<=160,'Invalid title')
    try:text=files[entry].decode('utf-8-sig')
    except UnicodeDecodeError:raise PublishError('Markdown not UTF-8')
    must(text.lstrip().startswith('# '),'Markdown must start with # H1')
    images={k for k in files if k.startswith('images/')}
    for key in images:
        safe_rel(key)
        must(re.fullmatch(r'images/[A-Za-z0-9_.-]+\.(png|jpeg|jpg|webp|svg|gif)',key,re.I) is not None,f'Unsafe image: {key}')
        b=files[key]
        must(bool(b),'Empty image: '+key)
        if key.lower().endswith('.png'): must(b.startswith(b'\x89PNG\r\n\x1a\n'),'Invalid PNG: '+key)
    if isinstance(meta.get('images'),list):
        declared=set(meta['images'])
        must(declared.issubset(images),'Images metadata lists missing images: '+str(declared-images))
    text,used_imgs=replacement_images(text,images,dest_in_book.stem)
    # Public downloads follow course id, page's relative parent inside book and page stem.
    public=Path('assets/downloads/courses')/course/dest_in_book.parent/dest_in_book.stem
    public_posix='/' + public.as_posix() + '/'
    links={}
    def dl_url(old):
        if old.startswith('downloads/'):
            base=old.partition('/')[2]
            must(bool(base) and '/' not in base,f'Only flat downloads are supported: {old}')
            url=public_posix+base
        elif old.startswith('/assets/downloads/courses/'):
            url=old
            must(url.startswith(public_posix),f'Public download link points outside this chapter: {url}')
            base=url.rsplit('/',1)[-1]
        else:return None
        key='downloads/'+base
        must(key in files and bool(files[key]),f'Linked download missing in ZIP: {key}')
        must(not any(p in url for p in ('?','#','%')),'Nonliteral URL forbidden: '+url)
        links[key]=url
        return url
    def html_repl(m):
        new=dl_url(m.group(2))
        return m.group(1)+(new or m.group(2))+m.group(3)
    text=HTMLLINK.sub(html_repl,text)
    def md_repl(m):
        new=dl_url(m.group(2))
        return '['+m.group(1)+']('+new+')' if new else m.group(0)
    text=MDLINK.sub(md_repl,text)
    # All references to the publisher's public root must point to available, linked files.
    for cid,rest in PUBLIC_LINK.findall(text):
        if cid==course and rest.startswith((dest_in_book.parent/dest_in_book.stem).as_posix()+'/'):
            k='downloads/'+rest.split('/')[-1]
            must(k in links,f'Unrecognized downloaded file link: {k}')
    downloads={public/key.removeprefix('downloads/'):files[key] for key in links}
    for path,data in downloads.items():
        p=str(path).lower()
        if p.endswith('.pdf'):must(data.startswith(b'%PDF-'),f'Invalid PDF: {path}')
        if p.endswith('.zip'):must(zipfile.is_zipfile(__import__('io').BytesIO(data)),f'Invalid inner ZIP: {path}')
        if p.endswith(('.ipynb','.json')):
            try:json.loads(data.decode('utf-8-sig'))
            except Exception:raise PublishError(f'Invalid notebook/JSON: {path}')
        if p.endswith('.py'):
            try:compile(data.decode('utf8'),str(path),'exec')
            except Exception:raise PublishError(f'Python file not parsable: {path}')
    images_out={dest_rel.parent/(dest_rel.stem+'-assets')/key:files[key] for key in images}
    target=inside(repo,dest_rel)
    toc=inside(repo,root/'_toc.yml')
    must(toc.is_file(),f'Missing TOC for course {course}: {toc}')
    # Rerun is idempotent when bytes are identical; changing an existing page
    # requires BOTH metadata opt-in and --allow-update (checked in publish).
    if target.is_file() and target.read_bytes()!=text.encode('utf8'):
        must(bool(meta.get('update_existing')),'Refusing to overwrite existing Markdown without update_existing=true')
    parent=str(meta.get('toc_parent') or '')
    if not parent and dest_in_book.parent.as_posix() not in ('.',''):
        candidate=(dest_in_book.parent/'index').as_posix()
        if re.search(r'^\s*- file:\s*'+re.escape(candidate)+r'\s*$',toc.read_text('utf8'),re.M):parent=candidate
    return {'course':course,'root':root,'entry':entry,'dest':dest_rel,'title':title,'toc':root/'_toc.yml',
            'parent':parent,'files':{dest_rel:text.encode('utf8'),**images_out,**downloads},
            'download_paths':list(downloads),'images':len(images_out),'text':text,'meta':meta}


def toc_insert(raw,dest_ref,title,parent=''):
    must('\n' not in title,'Newline in title')
    if re.search(r'^\s*-\s+file:\s*'+re.escape(dest_ref)+r'\s*$',raw,re.M):return raw
    entry='- file: '+dest_ref+'\n'+'  title: '+json.dumps(title,ensure_ascii=False)+'\n'
    lines=raw.splitlines(keepends=True)
    if parent:
        matches=[(i,len(line)-len(line.lstrip()),line) for i,line in enumerate(lines) if re.match(r'^\s*-\s+file:\s*'+re.escape(parent)+r'\s*$',line.strip())]
        must(len(matches)==1,'TOC parent not uniquely found: '+parent)
        i,indent,_=matches[0];end=i+1
        while end<len(lines):
            l=lines[end]
            if l.strip() and len(l)-len(l.lstrip())<=indent:break
            end+=1
        body=''.join(lines[i+1:end]);section_exists=bool(re.search(r'(?m)^\s*sections:\s*$',body))
        if section_exists:
            inserted=' '*(indent+4)+entry.replace('\n','\n'+' '*(indent+4)).rstrip()+'\n'
        else:
            inserted=' '*(indent+2)+'sections:\n'+' '*(indent+4)+entry.replace('\n','\n'+' '*(indent+4)).rstrip()+'\n'
        return ''.join(lines[:end])+inserted+''.join(lines[end:])
    # Append under top-level `chapters:` only (do not change `parts:`)
    idx=next((i for i,l in enumerate(lines) if re.fullmatch(r'chapters:\s*',l.strip()) and len(l)-len(l.lstrip())==0),None)
    must(idx is not None,'No top-level chapters: in TOC')
    end=idx+1
    while end<len(lines) and (not lines[end].strip() or lines[end].startswith((' ','\t','#'))):end+=1
    inserted='  '+entry.replace('\n','\n  ').rstrip()+'\n'
    return ''.join(lines[:end])+inserted+''.join(lines[end:])

MANIFEST=Path('tools/course_package_manifest.json')

def make_manifest(repo,course,md,downloads):
    p=repo/MANIFEST
    data=json.loads(p.read_text('utf8')) if p.is_file() else {'schema_version':1,'packages':[]}
    must(isinstance(data.get('packages'),list),'Malformed universal course package manifest')
    rec={'course_id':course,'markdown':md.as_posix(),'downloads':[q.as_posix() for q in sorted(downloads)]}
    recs=[r for r in data['packages'] if r.get('markdown')!=rec['markdown']]
    recs.append(rec);recs.sort(key=lambda r:(r['course_id'],r['markdown']))
    data['packages']=recs
    return (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8')

def publish(repo,source,course=None,commit=False,allow_update=False,also_stage=(),validate_only=False,dry_run=False):
    repo=repo.resolve();must((repo/'tools/jupyterbook_manager/books.yml').is_file(),'Not an expected course repository')
    must(git(repo,'rev-parse','--is-inside-work-tree').stdout.strip()=='true','Not a Git checkout')
    f,m=load_source(source,course,repo)
    pack=prepare(repo,f,m,course)
    if (repo/pack['dest']).is_file() and (repo/pack['dest']).read_bytes()!=pack['files'][pack['dest']]:
        must(allow_update and bool(pack['meta'].get('update_existing')),'Existing chapter edit requires --allow-update AND update_existing=true')
    toc_rel=pack['toc'];toc_path=inside(repo,toc_rel)
    toc_original=toc_path.read_text('utf8')
    target_in_book=pack['dest'].relative_to(pack['root']).with_suffix('').as_posix()
    toc_new=toc_insert(toc_original,target_in_book,pack['title'],pack['parent'])
    proposed=dict(pack['files'])
    if toc_new!=toc_original:proposed[toc_rel]=toc_new.encode('utf8')
    proposed[MANIFEST]=make_manifest(repo,pack['course'],pack['dest'],pack['download_paths'])
    extra=[safe_rel(x) for x in also_stage]
    for p in extra:must(inside(repo,p).is_file(),f'Extra install file not found: {p}')
    changes={r:b for r,b in proposed.items() if not (repo/r).is_file() or (repo/r).read_bytes()!=b}
    must(not any((repo/r).is_symlink() for r in proposed),'Symlink destination refused')
    print(f'[PREFLIGHT OK] {pack["course"]}: {pack["dest"]}, {pack["images"]} images, {len(pack["download_paths"])} downloads, {len(changes)} edits')
    for rel in sorted(changes):print(' + '+rel.as_posix())
    if validate_only or dry_run:
        print('[VALIDATED] Nothing written to the Git checkout.')
        return
    # Prevent accidental worktree overwrites of existing pages unless explicitly enabled.
    backups={};stage_list=sorted(set(proposed)|set(extra))
    try:
        for rel,data in changes.items():
            dst=inside(repo,rel);backups[rel]=dst.read_bytes() if dst.is_file() else None
            dst.parent.mkdir(exist_ok=True,parents=True)
            with tempfile.NamedTemporaryFile(delete=False,dir=dst.parent,prefix='.universal-course-',suffix='.tmp') as temp:
                temp.write(data);tmp=Path(temp.name)
            os.replace(tmp,dst)
        git(repo,'add','--',*[r.as_posix() for r in stage_list])
        for rel in stage_list:
            obj=git(repo,'rev-parse',':'+rel.as_posix(),check=False)
            must(obj.returncode==0,f'File not staged in Git: {rel}')
            disk=git(repo,'hash-object',rel.as_posix()).stdout.strip()
            must(obj.stdout.strip()==disk,f'Git index differs from disk: {rel}')
        print(f'[GIT INDEX VERIFIED] {len(stage_list)} chapter/installer paths; unrelated changes untouched.')
        if commit:
            approve=input('Type COMMIT to create a LOCAL commit (no Push): ').strip()
            must(approve=='COMMIT','Commit not approved; chapter remains staged, not committed.')
            staged=git(repo,'diff','--cached','--name-only','--',*[x.as_posix() for x in stage_list]).stdout.strip()
            if staged:
                git(repo,'commit','--only','-m',f'{pack["course"]}: publish {pack["dest"].stem} with verified downloads','--',*[x.as_posix() for x in stage_list])
            else:print('[NO OP] All files were already committed.')
            for rel in stage_list:
                head=git(repo,'rev-parse','HEAD:'+rel.as_posix(),check=False)
                must(head.returncode==0,'File not in HEAD: '+str(rel))
                disk=git(repo,'hash-object',rel.as_posix()).stdout.strip()
                must(head.stdout.strip()==disk,'HEAD does not match file: '+str(rel))
            print(f'[COMMIT VERIFIED] {pack["course"]} {pack["dest"].name}: all images, downloads and manifest present in HEAD.')
            print('[NEXT] GitHub Desktop > Push origin. No Push was performed.')
        else:print('[STAGED VERIFIED] Commit these paths in GitHub Desktop, then Push.')
    except Exception:
        # Only revert bytes modified by this run. Leave unrelated Git changes alone.
        for rel,old in backups.items():
            dst=repo/rel
            if old is None:dst.unlink(missing_ok=True)
            else:dst.write_bytes(old)
        git(repo,'reset','--quiet','--',*[x.as_posix() for x in backups],check=False)
        raise

def main(argv=None):
    ap=argparse.ArgumentParser(description='Publisher for any registered Jupyter Book course, from ZIP or .md')
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--course',help='Registered course id, required for raw Markdown; ZIP derives from metadata')
    ap.add_argument('--commit',action='store_true',help='Commit only own files after explicit COMMIT approval')
    ap.add_argument('--allow-update',action='store_true',help='Must also set update_existing=true in package metadata')
    ap.add_argument('--also-stage',action='append',default=[],help='Installer-owned repository file to include in same commit')
    ap.add_argument('--validate-only',action='store_true')
    ap.add_argument('--dry-run',action='store_true')
    a=ap.parse_args(argv)
    try:
        publish(a.repo,a.source,a.course,a.commit,a.allow_update,a.also_stage,a.validate_only,a.dry_run)
        return 0
    except (PublishError,OSError,ValueError,zipfile.BadZipFile) as e:
        print('[STOP] '+str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
