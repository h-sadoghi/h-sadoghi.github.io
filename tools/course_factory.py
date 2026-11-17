#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stable author -> build -> validate -> stage/commit workflow for registered courses.

No network, Git push, or content generation by AI. Python 3.12 standard library.
Modes:
  new COURSE N TITLE: make an outside-repository authoring workspace and metadata.
  check SOURCE: strict check of a chapter package/authoring folder without publishing.
  publish SOURCE: build PDF if SOURCE is a folder, then call the installed universal publisher.

For ZIP input, a completed PDF must already be embedded; no rebuilding inside ZIP.
The delegated universal publisher is the SINGLE authority for repository paths,
TOC editing, Git staging, and verified local commit.
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

class FactoryError(RuntimeError): pass

def ensure(ok, message):
    if not ok: raise FactoryError(message)

def run(args, cwd=None, log=None):
    result=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,
                           text=True,encoding='utf-8',errors='replace')
    if log:
        Path(log).parent.mkdir(parents=True,exist_ok=True)
        Path(log).write_text('COMMAND: '+' '.join(map(str,args))+'\n'+result.stdout+'\n'+result.stderr,encoding='utf-8')
    if result.returncode:
        excerpt='\n'.join((result.stdout+'\n'+result.stderr).splitlines()[-18:])
        raise FactoryError('Command failed (exit '+str(result.returncode)+'):\n'+excerpt)
    return result.stdout

def registry(repo):
    path=repo/'tools/jupyterbook_manager/books.yml'
    ensure(path.is_file(),'Missing registered-course list: '+str(path))
    courses={};cid=None
    for line in path.read_text('utf-8-sig').splitlines():
        a=re.match(r'^\s{2}-\s+id:\s*([\w-]+)\s*$',line)
        b=re.match(r'^\s{4}source:\s*(\S+)\s*$',line)
        if a: cid=a.group(1); courses[cid]={}
        elif b and cid: courses[cid]['source']=b.group(1)
    return {k:v['source'] for k,v in courses.items() if 'source' in v}

def as_safe_path(value):
    ensure(isinstance(value,str) and bool(value),'Empty path')
    p=PurePosixPath(value)
    ensure('\\' not in value and not p.is_absolute() and not any(x in ('..','.') for x in p.parts)
           and not value.startswith('/'), 'Unsafe archive path: '+value)
    return p

def load_package(source):
    """Read from source folder OR zip; nonempty, flat, safe members only."""
    result={};total=0
    if source.is_dir():
        for file in source.rglob('*'):
            if file.is_symlink(): raise FactoryError('Symlink not allowed: '+str(file))
            if not file.is_file():continue
            rel=file.relative_to(source).as_posix()
            if rel.startswith(('_build/','_qa/','__pycache__/')) or '/__pycache__/' in rel or rel.startswith('.'):
                continue
            if rel.endswith(('.aux','.log','.out','.toc','.synctex.gz','.fls','.fdb_latexmk')):
                continue
            # Only the contract's 4 root members are packaged.
            if rel not in ('chapter_meta.json',) and not re.fullmatch(r'chapter\d{2}\.md',rel) and not rel.startswith(('images/','downloads/')):
                continue
            as_safe_path(rel)
            data=file.read_bytes();result[rel]=data
            total+=len(data)
    else:
        ensure(source.is_file() and zipfile.is_zipfile(source),'Input must be a chapter ZIP or a source folder')
        with zipfile.ZipFile(source) as z:
            seen=set()
            for info in z.infolist():
                if info.is_dir():continue
                rel=info.filename;as_safe_path(rel)
                ensure(not ((info.external_attr>>16)&0o170000)==0o120000,'Symlink inside ZIP: '+rel)
                ensure(rel.lower() not in seen,'Duplicate ZIP member: '+rel);seen.add(rel.lower())
                ensure(info.file_size <= 100*1024*1024,'Oversized member: '+rel)
                total+=info.file_size;ensure(total<=360*1024*1024,'Package too large')
                result[rel]=z.read(info)
    ensure(total<=360*1024*1024,'Package too large')
    return result

def validate_package(files,repo,strict=True):
    ensure('chapter_meta.json' in files,'Missing chapter_meta.json at package root')
    try: meta=json.loads(files['chapter_meta.json'].decode('utf-8-sig'))
    except Exception as e:raise FactoryError('chapter_meta.json invalid: '+str(e)) from e
    ensure(isinstance(meta,dict),'Metadata must be JSON object')
    courses=registry(repo);course=meta.get('course_id')
    ensure(course in courses,'Course not registered in books.yml: '+str(course))
    name=meta.get('entry')
    ensure(re.fullmatch(r'chapter\d{2}\.md',str(name)) is not None,'Entry must be chapterNN.md')
    ensure(name in files,'Chapter Markdown missing: '+str(name))
    root=PurePosixPath(courses[course]);dest=PurePosixPath(meta.get('destination_path',''))
    ensure(dest.is_relative_to(root) and dest.name.startswith('chapter-') and dest.suffix=='.md',
           'Destination is not inside registered course book')
    # No extra contract roots. Cannot tolerate 'some-folder/chapterNN.md'.
    for filename in files:
        as_safe_path(filename)
        ensure(filename=='chapter_meta.json' or filename==name or filename.startswith(('images/','downloads/')),
               'Unexpected file outside package contract: '+filename)
    try: md=files[name].decode('utf-8-sig')
    except UnicodeDecodeError:raise FactoryError('Markdown must be UTF-8')
    ensure(md.lstrip().startswith('# '),'Markdown must start with a level-one heading')
    ensure('@@FILL@@' not in md and 'TODO_AUTHOR' not in md,'Draft contains unfinished placeholders; write chapter first')
    ensure(len(md.strip())>=400,'Chapter is too short to be a completed teaching note')
    # The shared publisher recognizes MyST figures, Markdown images, HTML imgs.
    figures=re.findall(r'^\s*```\{figure\}\s+(images/[^\s]+)',md,re.M)
    figures+=re.findall(r'!\[[^\]]*\]\((images/[^)\s]+)\)',md)
    figures+=re.findall(r'<img[^>]*\bsrc=["\'](images/[^"\']+)',md,re.I)
    for img in figures:
        ensure(img in files and len(files[img])>500,'Referenced image missing or empty: '+img)
    for img in (k for k in files if k.startswith('images/')):
        data=files[img]
        if img.lower().endswith('.png'):ensure(data.startswith(b'\x89PNG\r\n\x1a\n'),'Bad PNG: '+img)
        ensure(len(data)>500,'Image file empty: '+img)
    downloads=re.findall(r'(?:href=["\']|\]\()(downloads/[^"\')\s]+)',md)
    public_prefix='/assets/downloads/courses/'+str(course)+'/'+dest.relative_to(root).parent.as_posix()+'/'+dest.stem+'/'
    # Handle root parent '.' by avoiding a stray /./.
    public_prefix=public_prefix.replace('/./','/')
    public_links=re.findall(r'(/assets/downloads/courses/[^"\')\s]+)',md)
    for url in public_links:
        ensure(url.startswith(public_prefix),'Public URL is outside target chapter: '+url)
        downloads.append('downloads/'+url.rsplit('/',1)[-1])
    for asset in downloads:
        ensure(asset in files and bool(files[asset]),'Linked download missing: '+asset)
    ensure(downloads,'At least one download link is required (usually PDF)')
    pdfs=[x for x in downloads if x.lower().endswith('.pdf')]
    ensure(pdfs,'A PDF link is required for complete chapter release')
    for p in pdfs:ensure(files[p].startswith(b'%PDF-'),'Invalid PDF: '+p)
    for key in files:
        if key.endswith('.ipynb') or key.endswith('.json'):
            try:json.loads(files[key].decode('utf-8-sig'))
            except Exception as e:raise FactoryError('Bad notebook/JSON: '+key+' '+str(e))
        if key.endswith('.py'):
            try:compile(files[key].decode('utf-8-sig'),key,'exec')
            except SyntaxError as e:raise FactoryError('Python syntax error in '+key+': '+str(e))
        if key.lower().endswith('.zip'):
            import io
            ensure(zipfile.is_zipfile(io.BytesIO(files[key])),'Damaged nested ZIP: '+key)
    if meta.get('images'):
        ensure(set(meta['images']).issubset(files.keys()),'Metadata lists missing image')
    if meta.get('linked_downloads'):
        ensure(set(meta['linked_downloads']).issubset(files.keys()),'Metadata lists missing download')
    print(f'[PACKAGE OK] {course} {name}: {len(figures)} image references, {len(set(downloads))} downloads, {len(files)} files',flush=True)
    return meta

def get_font():
    name=os.environ.get('COURSE_PERSIAN_FONT','Amiri').strip()
    ensure(name and all(ch not in name for ch in '\\{}\n\r'),'Invalid COURSE_PERSIAN_FONT')
    return name

def convert_figures(markdown):
    lines=markdown.splitlines();result=[];i=0
    while i<len(lines):
        m=re.match(r'^\s*```\{figure\}\s+([^\s]+)\s*$',lines[i])
        if not m:result.append(lines[i]);i+=1;continue
        image=m.group(1);j=i+1;caption=[]
        while j<len(lines) and not re.match(r'^\s*```\s*$',lines[j]):
            line=lines[j].strip()
            if line and not line.startswith(':'):caption.append(line)
            j+=1
        ensure(j<len(lines),'Unclosed MyST figure directive: '+image)
        result.append('!['+' '.join(caption).replace(']','')+']('+image+')')
        i=j+1
    return '\n'.join(result)+'\n'

def compile_pdf(work, files):
    meta=json.loads(files['chapter_meta.json'].decode('utf-8-sig'))
    mdname=meta['entry']; stem=Path(mdname).stem
    pdf_name='DataMining_Chapter'+stem[-2:]+'.pdf' if meta['course_id']=='data-mining' else stem+'.pdf'
    md=(work/mdname).read_text('utf-8-sig')
    ensure('@@FILL@@' not in md and len(md)>=400,'Fill in chapter before compilation')
    # Only rebuild PDF if the chapter links exactly to this expected generated PDF.
    expected='downloads/'+pdf_name
    if expected not in md:
        existing=re.findall(r'(?:href=["\']|\]\()(downloads/[^"\')\s]+\.pdf)',md)
        ensure(len(existing)==1,'Exactly one PDF download link is needed for automatic PDF compilation')
        expected=existing[0]; pdf_name=Path(expected).name
    # A dedicated handwritten TeX source always takes precedence when supplied as `source.tex`.
    pandoc=shutil.which('pandoc');xelatex=shutil.which('xelatex')
    ensure(pandoc is not None,'Pandoc not installed or not on PATH; cannot build PDF from Markdown')
    ensure(xelatex is not None,'XeLaTeX not installed or not on PATH; cannot build Persian PDF')
    downloads=work/'downloads';downloads.mkdir(exist_ok=True)
    out_tex=downloads/Path(pdf_name).with_suffix('.tex')
    out_pdf=downloads/pdf_name
    title=str(meta.get('title',stem))
    font=get_font()
    # Stable local header not committed as a package root file.
    with tempfile.TemporaryDirectory(prefix='course-factory-') as tmpd:
        tmp=Path(tmpd)
        src=tmp/'chapter_for_pandoc.md';src.write_text(convert_figures(md),encoding='utf-8')
        header=tmp/'fa_header.tex'
        header.write_text('\\usepackage{xepersian}\n\\settextfont{'+font+'}\n\\setlatintextfont{DejaVu Sans}\n',encoding='utf-8')
        run([pandoc,str(src),'-f','markdown+tex_math_dollars+fenced_code_attributes',
             '-s','-o',str(out_tex),'-H',str(header),
             '-V','documentclass=article','-V','fontsize=12pt','-V','geometry:margin=2.3cm',
             '-V','papersize=a4'],cwd=work,log=tmp/'pandoc.log')
    # Xelatex builds in downloads, reads images relative to current work directory.
    log=downloads/'COURSE_PDF_BUILD.log'
    for _ in range(2):
        run([xelatex,'-interaction=nonstopmode','-halt-on-error','-file-line-error',
             '-output-directory='+str(downloads),str(out_tex)],cwd=work,log=log)
    ensure(out_pdf.is_file() and out_pdf.stat().st_size>3000,'XeLaTeX did not create an adequate PDF')
    source_zip=downloads/(Path(pdf_name).stem+'_TEX_PDF_SOURCE.zip')
    with zipfile.ZipFile(source_zip,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as archive:
        archive.write(out_tex,out_tex.name)
        archive.write(out_pdf,out_pdf.name)
        for fig in sorted((work/'images').rglob('*')):
            if fig.is_file() and not fig.is_symlink():
                archive.write(fig,(Path('images')/fig.relative_to(work/'images')).as_posix())
    with zipfile.ZipFile(source_zip) as archive:
        ensure(archive.testzip() is None,'Source TeX/PDF ZIP CRC failed')
    print('[SOURCE ZIP OK] '+str(source_zip),flush=True)
    # Verify PDF page count when pdfinfo is available.
    pdfinfo=shutil.which('pdfinfo')
    if pdfinfo:
        info=run([pdfinfo,str(out_pdf)])
        pages=re.search(r'Pages:\s*(\d+)',info)
        if pages: print('[PDF OK] '+str(out_pdf)+'; '+pages.group(1)+' pages',flush=True)
    else:print('[PDF OK] '+str(out_pdf),flush=True)
    return out_pdf

def make_zip(source,files,meta):
    dest=source.parent/(source.name+'_ONECLICK.zip')
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for key,data in sorted(files.items()):
            z.writestr(key,data)
    with zipfile.ZipFile(dest) as z:
        ensure(z.testzip() is None,'ZIP failed CRC check')
    print('[ZIP OK] '+str(dest),flush=True)
    return dest

def new_project(repo,course,number,title,out=None):
    courses=registry(repo);ensure(course in courses,'Unknown course id: '+course)
    ensure(1<=number<=99,'Chapter number must be 1..99')
    ensure(title.strip() and len(title)<150,'Please give a real chapter title')
    if out is None:
        out=repo.parent/'_COURSE_WORKSPACES'/course/f'Chapter{number:02d}'
    ensure(not out.exists(),'Draft workspace already exists; refusing to replace '+str(out))
    out.mkdir(parents=True);(out/'images').mkdir();(out/'downloads').mkdir()
    md_name=f'chapter{number:02d}.md'
    book_root=repo/Path(courses[course])
    if (book_root/'course-notes/index.md').is_file():
        subfolder='course-notes'
    elif (book_root/'chapters/index.md').is_file():
        subfolder='chapters'
    else:
        # Match the first actual parent in this book's TOC, e.g. gonzalez/index.
        toc=(book_root/'_toc.yml').read_text('utf-8') if (book_root/'_toc.yml').is_file() else ''
        parent=re.search(r'(?m)^\s+- file:\s+([A-Za-z0-9_-]+)/index\s*$',toc)
        subfolder=parent.group(1) if parent and (book_root/parent.group(1)/'index.md').is_file() else ''
    rel=PurePosixPath(courses[course])/subfolder/f'chapter-{number:02d}.md'
    pdf=('DataMining_Chapter'+f'{number:02d}' if course=='data-mining' else f'chapter{number:02d}')+'.pdf'
    srczip=Path(pdf).stem+'_TEX_PDF_SOURCE.zip'
    tex=Path(pdf).stem+'.tex'
    meta={'schema_version':'standalone-chapter-package-1.0','course_id':course,'chapter_number':number,
          'title':title,'entry':md_name,'destination_path':rel.as_posix(),'update_existing':False,
          'images':[],'downloads':['downloads/'+pdf,'downloads/'+tex,'downloads/'+srczip],'linked_downloads':['downloads/'+pdf,'downloads/'+tex,'downloads/'+srczip],
          'learning_objectives':[],'sections':[]}
    (out/'chapter_meta.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n','utf-8')
    md=(f'# فصل {number} — {title}\n\n'
        '> **متن آموزشی آمادهٔ گسترش؛ پیش از انتشار باید همهٔ بخش‌ها تکمیل شوند.**\n\n'
        f'**فایل‌های فصل:** [دریافت PDF فصل](downloads/{pdf}) · [سورس XeLaTeX](downloads/{tex}) · [بستهٔ کامل سورس و شکل‌ها](downloads/{srczip}).\n\n'
        '## مسئلهٔ محوری\n\n@@FILL@@ — مسئله، داده و پرسش تحقیق را با مثال واقعی/ساختگی مشخص کنید.\n\n'
        '## ایده و شهود\n\n@@FILL@@ — تعریف مفاهیم و تبیین روش.\n\n'
        '## مدل ریاضی و محاسبهٔ دستی\n\n@@FILL@@ — فرمول‌ها را همراه مفروضات و مثال عددی بنویسید.\n\n'
        '## کد و تفسیر\n\n@@FILL@@ — کد با دادهٔ همین بسته و توضیح نتیجه.\n\n'
        '## تمرین‌ها و منابع\n\n@@FILL@@ — تمرین‌ها، پاسخ‌های نمونه، ارجاع دقیق به منابع.\n')
    (out/md_name).write_text(md,'utf-8')
    (out/'downloads'/'README_FA.md').write_text('# راهنمای بازتولید\n\nنام وابستگی‌ها، فرمان آزمون و محدودهٔ اعتبار نتایج را اینجا بنویسید.\n','utf-8')
    print('[CREATED] '+str(out)+'\n[WRITE] '+md_name+' then run the SAME command with this folder path.',flush=True)

def publish(repo,src,mode='publish',commit=True):
    ensure(src.exists(),'Input not found: '+str(src))
    ensure((repo/'tools/universal_course_publisher.py').is_file(),
           'Universal publisher is not installed. Install the Chapter 9/11 publisher first.')
    ensure((repo/'.git').exists(),'Not a Git repository: '+str(repo))
    if src.is_dir():
        files=load_package(src)
        ensure('chapter_meta.json' in files,'Source folder missing chapter_meta.json')
        if mode=='publish':
            compile_pdf(src,files)
            files=load_package(src)
        meta=validate_package(files,repo)
        if mode=='check':
            print('[CHECK ONLY] No Git changes.',flush=True);return
        dest=make_zip(src,files,meta)
    else:
        files=load_package(src);meta=validate_package(files,repo)
        if mode=='check':
            print('[CHECK ONLY] No Git changes.',flush=True);return
        dest=src
    cmd=[sys.executable,str(repo/'tools/universal_course_publisher.py'),
         '--repo',str(repo),'--source',str(dest)]
    run(cmd+['--validate-only'])
    print('[PUBLISHER PREFLIGHT OK] Import and Git index/HEAD verification delegated to existing universal publisher.',flush=True)
    if commit:cmd+=['--commit']
    # Do not capture stdout; direct prompt COMMIT must reach user's console.
    proc=subprocess.run(cmd,cwd=repo)
    ensure(proc.returncode==0,'Publisher failed. No Push. Return code: '+str(proc.returncode))
    print('[NEXT] Open GitHub Desktop and Push origin; verify new Deploy site and link workflows.',flush=True)

def main():
    ap=argparse.ArgumentParser(description='Reusable course content factory for registered Jupyter Books')
    ap.add_argument('mode',choices=('new','check','publish'))
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--course')
    ap.add_argument('--number',type=int)
    ap.add_argument('--title')
    ap.add_argument('--out',type=Path)
    ap.add_argument('--source',type=Path)
    ap.add_argument('--no-commit',action='store_true')
    args=ap.parse_args()
    try:
        repo=args.repo.resolve()
        if args.mode=='new':
            ensure(args.course and args.number and args.title,'NEW requires --course --number --title')
            new_project(repo,args.course,args.number,args.title,args.out)
        else:
            ensure(args.source is not None,'CHECK/PUBLISH requires --source')
            publish(repo,args.source.resolve(),args.mode,not args.no_commit)
        return 0
    except (FactoryError,OSError,ValueError,KeyError,zipfile.BadZipFile) as exc:
        print('[STOP] '+str(exc),file=sys.stderr,flush=True)
        return 2

if __name__=='__main__':raise SystemExit(main())
