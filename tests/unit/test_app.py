import json
from pathlib import Path

from fastapi import FastAPI
from pytest import MonkeyPatch
from starlette.middleware.cors import CORSMiddleware

from myapi import app as app_module
from myapi.app import get_app, run_app
from myapi.config import AppConfig


def test_get_app_returns_fastapi_instance(app_config: AppConfig) -> None:
    app = get_app(app_config)

    assert isinstance(app, FastAPI)


def test_get_app_metadata(app_config: AppConfig) -> None:
    app = get_app(app_config)

    assert app.title == "My API"
    assert app.docs_url == "/api/docs"
    assert app.description == "Standard API"
    assert app.version  # populated from setuptools_scm


def test_get_app_registers_health_route(app_config: AppConfig) -> None:
    app = get_app(app_config)

    assert "/api/v1/health" in app.openapi()["paths"]


def test_get_app_configures_cors_with_allowed_origins() -> None:
    config = AppConfig(allow_origins=["https://allowed.example"], port=8000)

    app = get_app(config)

    cors = next(m for m in app.user_middleware if m.cls is CORSMiddleware)
    assert cors.kwargs["allow_origins"] == ["https://allowed.example"]


def test_run_app_reads_config_and_starts_server(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"allow_origins": [], "port": 1234}), encoding="utf8")

    calls: dict[str, object] = {}

    def fake_run(app: object, *, port: int, reload: bool) -> None:
        calls["app"] = app
        calls["port"] = port
        calls["reload"] = reload

    monkeypatch.setattr(app_module.uvicorn, "run", fake_run)

    run_app(str(config_path))

    assert isinstance(calls["app"], FastAPI)
    assert calls["port"] == 1234
    assert calls["reload"] is False
