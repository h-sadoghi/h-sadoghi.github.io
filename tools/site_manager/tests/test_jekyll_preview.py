from __future__ import annotations

from pathlib import Path

import pytest

from tools.site_manager.jekyll_preview import JekyllPreviewError, JekyllPreviewManager


class FakeProcess:
    pid = 12345

    def __init__(self) -> None:
        self.return_code: int | None = None

    def poll(self) -> int | None:
        return self.return_code

    def terminate(self) -> None:
        self.return_code = 0

    def kill(self) -> None:
        self.return_code = -9

    def wait(self, timeout: int | None = None) -> int:
        assert timeout is not None
        assert self.return_code is not None
        return self.return_code


def test_start_uses_unpublished_and_project_destination(repo: Path, monkeypatch) -> None:
    manager = JekyllPreviewManager(repo, open_browser=False)
    bundle = repo / "Ruby33-x64" / "bin" / "bundle.cmd"
    bundle.parent.mkdir(parents=True)
    bundle.write_text("", encoding="utf-8")
    observed: dict = {}

    def fake_popen(command, **kwargs):
        observed["command"] = command
        observed["kwargs"] = kwargs
        return FakeProcess()

    monkeypatch.setattr(manager, "_bundle_executable", lambda: bundle)
    monkeypatch.setattr(manager, "_port_open", lambda _host, _port: False)
    monkeypatch.setattr(manager, "_http_ready", lambda: False)
    monkeypatch.setattr("tools.site_manager.jekyll_preview.subprocess.Popen", fake_popen)
    monkeypatch.setattr(
        "tools.site_manager.jekyll_preview.subprocess.run",
        lambda *_args, **_kwargs: manager._process.terminate(),
    )

    result = manager.start()

    assert result["state"] == "starting"
    assert "--unpublished" in observed["command"]
    assert "--config" in observed["command"]
    preview_config = manager.preview_config.read_text(encoding="utf-8")
    assert "enabled: false" in preview_config
    assert "assets/jupyter/" in preview_config
    assert observed["command"][observed["command"].index("--destination") + 1] == str(manager.destination)
    assert observed["kwargs"]["cwd"] == repo.resolve()
    manager.stop()


def test_repeated_start_reuses_managed_process(repo: Path, monkeypatch) -> None:
    manager = JekyllPreviewManager(repo, open_browser=False)
    process = FakeProcess()
    manager._process = process
    monkeypatch.setattr(manager, "_http_ready", lambda: True)
    monkeypatch.setattr(
        "tools.site_manager.jekyll_preview.subprocess.run",
        lambda *_args, **_kwargs: process.terminate(),
    )

    result = manager.start()

    assert result["reused"] is True
    assert result["ready"] is True
    assert result["pid"] == process.pid
    manager.stop()


def test_start_refuses_an_unmanaged_port_conflict(repo: Path, monkeypatch) -> None:
    manager = JekyllPreviewManager(repo, open_browser=False)
    monkeypatch.setattr(manager, "_port_open", lambda _host, _port: True)

    with pytest.raises(JekyllPreviewError, match="پورت 4000"):
        manager.start()
