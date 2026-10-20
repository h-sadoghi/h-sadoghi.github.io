from __future__ import annotations

import atexit
import os
import subprocess
import threading
import webbrowser
from pathlib import Path

import markdown as markdown_lib
from flask import Flask, jsonify, render_template, request, url_for

from .assets import AssetInput
from .frontmatter import split_front_matter
from .jekyll_preview import JekyllPreviewError, JekyllPreviewManager
from .manager import SiteManager
from .utils import SiteManagerError, contained_path


def create_app(repo_root: str | Path) -> Flask:
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=64 * 1024 * 1024, JSON_AS_ASCII=False)
    manager = SiteManager(repo_root)
    jekyll = JekyllPreviewManager(repo_root)
    app.extensions["site_manager"] = manager
    app.extensions["jekyll_preview"] = jekyll
    atexit.register(jekyll.stop)

    def uploaded_assets() -> list[AssetInput]:
        return [
            AssetInput(file.filename or "file", file.read(), "browser-upload")
            for file in request.files.getlist("assets")
            if file and file.filename
        ]

    def form_fields() -> dict:
        fields = {
            key: request.form.get(key, "").strip()
            for key in ("title", "slug", "author", "date", "description", "tags", "status", "lang", "bibtex", "chapter", "chapters")
        }
        if fields.get("status") == "preserve":
            fields["status"] = ""
        return fields

    def page(**values):
        context = {
            "routes": manager.route_choices(),
            "courses": manager.courses(),
            "items": manager.browse()[:500],
            "plan": None,
            "result": None,
            "error": "",
            "active": "add",
        }
        context.update(values)
        return render_template("index.html", **context)

    @app.get("/")
    def index():
        return page(active=request.args.get("view", "add"))

    @app.post("/preview")
    def preview():
        try:
            action = request.form.get("action", "add")
            markdown_text = request.form.get("markdown", "")
            uploaded = request.files.get("markdown_file")
            if uploaded and uploaded.filename:
                if not uploaded.filename.lower().endswith((".md", ".markdown")):
                    raise SiteManagerError("فایل متن ورودی باید Markdown باشد.")
                markdown_text = uploaded.read().decode("utf-8-sig")
            if action == "edit":
                relative = request.form.get("existing_path", "").strip()
                plan = manager.preview_edit(relative, form_fields(), markdown_text if markdown_text else None, uploaded_assets())
            elif action == "course":
                plan = manager.preview_course(form_fields())
            else:
                plan = manager.preview_add(request.form.get("route", ""), form_fields(), markdown_text, uploaded_assets())
            active = "course" if action == "course" else "browse" if action == "edit" else "add"
            return page(plan=plan.public(), active=active)
        except (SiteManagerError, UnicodeDecodeError) as exc:
            action = request.form.get("action", "add")
            active = "course" if action == "course" else "browse" if action == "edit" else "add"
            return page(error=str(exc), active=active), 400

    @app.post("/apply/<token>")
    def apply(token: str):
        try:
            result = manager.add(token, confirm=request.form.get("confirm") == "yes")
            return page(result=result, active=request.form.get("active", "add"))
        except SiteManagerError as exc:
            return page(error=str(exc), active=request.form.get("active", "add")), 400

    @app.post("/markdown-preview")
    def markdown_preview():
        text = request.form.get("markdown", "")
        try:
            _, body, _ = split_front_matter(text)
        except SiteManagerError:
            body = text
        html = markdown_lib.markdown(body, extensions=["extra", "fenced_code", "tables", "codehilite"])
        return jsonify({"html": html})

    @app.get("/api/search")
    def search():
        return jsonify(manager.browse(request.args.get("q", ""), request.args.get("type", ""))[:200])

    @app.get("/api/content")
    def content():
        try:
            return jsonify(manager.read_content(request.args.get("path", "").strip()))
        except SiteManagerError as exc:
            return jsonify({"ok": False, "error": str(exc), "solution": "فایل را دوباره از فهرست مطالب موجود انتخاب کنید."}), 400

    @app.post("/open-source")
    def open_source():
        try:
            path = contained_path(manager.repo_root, request.form.get("path", ""))
            if not path.exists():
                raise SiteManagerError("فایل وجود ندارد.")
            if os.name == "nt":
                subprocess.Popen(["explorer.exe", "/select,", str(path)])
            return jsonify({"ok": True, "path": str(path)})
        except SiteManagerError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400

    @app.post("/jekyll-preview")
    def jekyll_preview():
        try:
            return jsonify(jekyll.start())
        except JekyllPreviewError as exc:
            return jsonify({**jekyll.status(), "ok": False, "error": str(exc)}), 409

    @app.get("/jekyll-preview/status")
    def jekyll_preview_status():
        return jsonify(jekyll.status())

    @app.post("/jekyll-preview/stop")
    def jekyll_preview_stop():
        return jsonify(jekyll.stop())

    @app.get("/github-desktop")
    def github_desktop():
        return render_template("github_desktop.html")

    @app.errorhandler(413)
    def too_large(_error):
        return "حجم مجموع فایل‌ها از ۶۴ مگابایت بیشتر است.", 413

    return app


def run(repo_root: str | Path, open_browser: bool = True) -> None:
    app = create_app(repo_root)
    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8765")).start()
    # Never expose this authoring service to the network.
    app.run(host="127.0.0.1", port=8765, debug=False, use_reloader=False)
