# Codex Specification — Sadoghi Local Jekyll Content Manager (MVP)

## Goal

Build a small, reliable **local-only Python authoring tool** for the existing al-folio/Jekyll repository. The user—not AI—chooses the category and destination. The tool handles files, images, YAML front matter, metadata, and local validation. **Do not rebuild the site as a different CMS or theme.** Do not automatically publish to GitHub.

Repositories:

- Main working directory: `J:\SadoghiSite2\h-sadoghi.github.io`
- Historical reference only: `J:\SadoghiSite2\hadisadoghiyazdi1971.github.io`
- Production repository: `h-sadoghi/h-sadoghi.github.io`
- Current configured `origin` may be `hadisadoghiyazdi1971/h-sadoghi.github.io` (fork); `upstream` may be the production repo. Confirm both with Git instead of assuming.

## Initial investigation / safety

1. Read actual repository files: `_config.yml`, `_pages/`, `_posts/`, `_projects/`, `_bibliography/`, `_data/`, collections, people/profile structures, asset conventions, relevant Liquid templates, nav definitions, and workflows. Identify all real content routes; do not assume a generic al-folio clone.
2. Verify current Git status, branch, remotes, and whether PR #4 changes exist locally or on upstream. Preserve the most recent reviewed content; do not check out an older branch and accidentally lose the migration.
3. Make a fresh feature branch and verified backup before any existing content edits. No reset --hard, force push, history rewrite, automatic deploy, or GitHub account changes.
4. Produce a concise `SITE_INFORMATION_ARCHITECTURE_PROPOSAL.md` mapping **current page, preferred category, canonical page, duplication/redirect risk**. This is a proposal only: **do not bulk move, delete, or reclassify existing site content until explicit user approval**.

## Proposed audience-facing categories (editable, not hard-coded)

- Home / About / CV / Contact
- Research: Publications, Research Projects, Lab & research themes
- People & Students: People, student work, Ph.D./M.Sc. thesis records, alumni
- Teaching: courses, course notes, assignments
- Library: notes, talks/presentations, reference archive
- News / Blog

These are navigation concepts, not instructions to create new Jekyll collections. Prefer compatible existing collections and URLs. Articles, projects, publications, student profiles, student thesis records, and resources are different **content types**. A content item should have one canonical home and optional cross-links; avoid duplicating it into several collections.

## Architecture

Small Python package, e.g. `tools/site_manager/` and a one-click `RUN_SITE_MANAGER.cmd`:

- `Flask` for a simple browser UI bound strictly to `127.0.0.1:8765`.
- `ruamel.yaml` (round-trip handling of existing YAML) and Markdown preview library.
- No SQLite, no remote backend, no login, no external SaaS, no AI-driven mandatory routing.
- Configurable routing map in **one** file, e.g. `tools/site_manager/content_routes.yml`, generated after reading the _actual_ repo. Avoid needlessly changing site `_config.yml`.
- Clear separation: repo-inspector, section/type router, content importer, asset importer/link rewriter, front-matter editor, validator, web UI. Expose a small Python API (`preview_add`, `add`, `preview_edit`, `edit`, `validate`) for batch workflows.

## Required screen (Persian labels preferred, UTF-8/RTL support)

A single main screen with:

1. Action: **Add / Edit existing / Browse & search**.
2. Content type and section/subsection: selected explicitly by the user, using route names discovered from the repository. Type may be post, teaching note, project, student profile, thesis, presentation, resource, publication (BibTeX).
3. Title, author(s), date, description/summary, tags, status (`draft`/`ready`) as appropriate to type. Fields are optional unless truly required.
4. Import existing `.md` (or paste Markdown); choose/upload multiple image and PDF files. Do not demand conversion to HTML.
5. **Preview / Show exact file changes / Confirm write to local repository**. Display resolved target path, proposed URL, YAML front matter, generated image paths, and duplicates/conflicts.
6. A button to open edited source and (when available) open local Jekyll preview; a separate link explaining GitHub Desktop workflow. No Push/Merge buttons in the tool.

## Editing/authoring semantics

- Preserve existing front matter, Markdown body, code fences, math, Persian RTL text, Liquid references and relative links. When editing, retain existing permalink unless the user approves a change.
- Use a valid template for each **real** content type found in the repository, and validate it. Do not use one generic template for bibliography, projects, and posts.
- Determine the correct destination from `content_routes.yml`, based on explicit user choice. Refuse unknown routes instead of guessing.
- Create safe, stable slugs and prevent filename/permalink collisions; don't overwrite without a diff and affirmative confirmation.
- Copy selected images to a stable per-content asset location such as `assets/content/<slug>/` (verify repo conventions). Correct Markdown/Liquid asset links. Check file types and missing files; never read/write outside configured project and explicitly chosen sources.
- Support both **adding** new content and **editing** existing entries; search by title, URL, filename and content type.
- Detect probable duplicate publications by normalized DOI, title/year, and BibTeX key. For BibTeX import, preserve the existing bibliography's working syntax and do not silently overwrite a record.
- Do not modify `_config.yml`, theme files, navigation or collection declarations during an ordinary add/edit; if a structural change is required, explain it and require a separate approval step.
- Drafts should not accidentally become public (respect Jekyll `published: false` or project-specific draft convention).
- Before applying, show diff. After applying, show changed files and validation status. Each operation must be locally reversible using backups and Git; don't automatically commit.

## Validation and preview

- Mandatory quick checks on changed files: YAML parsing, duplicate path/permalink, missing local image targets, Markdown/front matter, asset safety, and relevant BibTeX validations. Use existing CI rules where possible.
- Quick preview of Markdown in the web UI must work without Ruby/Jekyll. Exact site-style preview should launch/reuse the existing local Jekyll environment **only if already available**, on a separate localhost port (e.g. 4000), and clearly say when it cannot run.
- Avoid running the 10–20 minute production ImageMagick/PurgeCSS build for every minor edit; make full build a separate optional pre-publication check.
- Test on a temporary fixture/copy first: Persian Markdown with 2 images, image filename with spaces, draft post, project, duplicate title, editing an existing record, and publication duplicate DOI. Verify no modifications to original files in preview mode.
- Include automated unit tests; no destructive cleanup or full-site migration.

## Deliverables and completion

- A small working tool directly in the existing repository, not just a conceptual report.
- `RUN_SITE_MANAGER.cmd` that creates/uses a local venv if appropriate, checks dependencies gracefully and opens `http://127.0.0.1:8765`.
- `README_FA.md` limited to simple use instructions for a non-developer; include explicit GitHub Desktop steps: commit locally, push feature branch to fork, open PR to production, merge after green checks. Explain that **Push to the fork alone does not update the production site**. If future direct Push-to-production is desired, that requires a separately authorized remote/account permissions setup.
- `SITE_INFORMATION_ARCHITECTURE_PROPOSAL.md`: exact inventory and proposed **non-destructive** cleanup, duplicates, navigation and URLs to preserve; wait for owner to approve any bulk information architecture restructuring.
- `SITE_MANAGER_TEST_REPORT.md`: actual tests, screenshots if possible, list of changed files, failures/limitations, and exact run command.
- One concise handoff ZIP of tool + guides/reports (do not duplicate all site sources). Confirm it is possible to use GitHub Desktop to commit resulting Jekyll files.
- **No Push, PR, Merge, Deploy, automated site-wide reorganization or removal.**

## Acceptance scenario

The owner has `D:\Notes\DFT.md` with two nearby images. They launch `RUN_SITE_MANAGER.cmd`, select `Teaching > Signals and Systems`, import the Markdown and the images, enter or confirm title/author, preview expected URL and changes, click **Save to local site**. The tool writes valid Jekyll-compatible files into the real repository with correct image links and reports all changes. The owner inspects GitHub Desktop Changes, commits, pushes a feature branch, creates and merges a PR after checks. The tool never chooses the academic section instead of the owner.
