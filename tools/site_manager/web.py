from __future__ import annotations

import os
import shutil
import socket
import subprocess
import threading
import webbrowser
from pathlib import Path

import markdown as markdown_lib
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

from .assets import AssetInput
from .frontmatter import split_front_matter
from .manager import SiteManager
from .utils import SiteManagerError, contained_path


def create_app(repo_root: str | Path) -> Flask:
    app = Flask(__name__)
    app.config.update(MAX_CONTENT_LENGTH=64 * 1024 * 1024, JSON_AS_ASCII=False)
    manager = SiteManager(repo_root)
    app.extensions["site_manager"] = manager

    def uploaded_assets() -> list[AssetInput]:
        return [
            AssetInput(file.filename or "file", file.read(), "browser-upload")
            for file in request.files.getlist("assets")
            if file and file.filename
        ]

    def form_fields() -> dict:
        return {
            key: request.form.get(key, "").strip()
            for key in ("title", "slug", "author", "date", "description", "tags", "status", "lang", "bibtex")
        }

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            routes=manager.route_choices(),
            items=manager.browse()[:500],
            plan=None,
            result=None,
            error="",
        )

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
            else:
                plan = manager.preview_add(request.form.get("route", ""), form_fields(), markdown_text, uploaded_assets())
            return render_template("index.html", routes=manager.route_choices(), items=manager.browse()[:500], plan=plan.public(), result=None, error="")
        except (SiteManagerError, UnicodeDecodeError) as exc:
            return render_template("index.html", routes=manager.route_choices(), items=manager.browse()[:500], plan=None, result=None, error=str(exc)), 400

    @app.post("/apply/<token>")
    def apply(token: str):
        try:
            result = manager.add(token, confirm=request.form.get("confirm") == "yes")
            return render_template("index.html", routes=manager.route_choices(), items=manager.browse()[:500], plan=None, result=result, error="")
        except SiteManagerError as exc:
            return render_template("index.html", routes=manager.route_choices(), items=manager.browse()[:500], plan=None, result=None, error=str(exc)), 400

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
            with socket.create_connection(("127.0.0.1", 4000), timeout=0.3):
                threading.Timer(0.1, lambda: webbrowser.open("http://127.0.0.1:4000")).start()
                return jsonify({"ok": True, "url": "http://127.0.0.1:4000", "reused": True})
        except OSError:
            pass
        if shutil.which("bundle") is None:
            return jsonify({"ok": False, "error": "Ruby/Bundler روی این رایانه در PATH موجود نیست؛ پیش‌نمایش Markdown همچنان قابل استفاده است."}), 409
        command = ["bundle", "exec", "jekyll", "serve", "--host", "127.0.0.1", "--port", "4000", "--livereload"]
        flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        subprocess.Popen(command, cwd=manager.repo_root, creationflags=flags)
        threading.Timer(3, lambda: webbrowser.open("http://127.0.0.1:4000")).start()
        return jsonify({"ok": True, "url": "http://127.0.0.1:4000", "reused": False})

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
