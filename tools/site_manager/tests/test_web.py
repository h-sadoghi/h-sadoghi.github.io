from __future__ import annotations

import io
from pathlib import Path

from tools.site_manager.web import create_app


def test_main_page_and_markdown_preview(repo: Path) -> None:
    app = create_app(repo)
    app.testing = True
    client = app.test_client()
    page = client.get("/")
    assert page.status_code == 200
    assert "مدیریت محتوای محلی" in page.get_data(as_text=True)
    preview = client.post("/markdown-preview", data={"markdown": "# عنوان\n\n**متن**"})
    assert preview.status_code == 200
    assert "<h1>عنوان</h1>" in preview.json["html"]


def test_search_api(repo: Path) -> None:
    app = create_app(repo)
    app.testing = True
    response = app.test_client().get("/api/search?q=Existing")
    assert response.status_code == 200
    assert response.json[0]["path"] == "_pages/existing.md"


def test_jekyll_preview_reports_missing_bundler(repo: Path, monkeypatch) -> None:
    app = create_app(repo)
    app.testing = True
    preview = app.extensions["jekyll_preview"]
    monkeypatch.setattr(preview, "_port_open", lambda _host, _port: False)
    monkeypatch.setattr(preview, "_bundle_executable", lambda: None)

    response = app.test_client().post("/jekyll-preview")

    assert response.status_code == 409
    assert response.json["ok"] is False
    assert "Ruby/Bundler" in response.json["error"]


def test_browser_form_previews_import_with_multiple_images(repo: Path) -> None:
    app = create_app(repo)
    app.testing = True
    response = app.test_client().post(
        "/preview",
        data={
            "action": "add",
            "route": "teaching_signals",
            "title": "DFT آزمایشی",
            "status": "draft",
            "markdown_file": (io.BytesIO(b"# DFT\n\n![one](first image.png)\n![two](second.png)"), "DFT.md"),
            "assets": [
                (io.BytesIO(b"\x89PNG\r\n\x1a\none"), "first image.png"),
                (io.BytesIO(b"\x89PNG\r\n\x1a\ntwo"), "second.png"),
            ],
        },
        content_type="multipart/form-data",
    )
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "teaching-signals-dft-آزمایشی.md" in text
    assert "تأیید و ذخیره در مخزن محلی" in text
