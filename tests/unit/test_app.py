from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from myapi.app import get_app, start_server
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


class RecordingRunner:
    """Hand-written fake ServerRunner that records what it was called with."""

    def __init__(self) -> None:
        self.app: FastAPI | None = None
        self.port: int | None = None

    def __call__(self, app: FastAPI, port: int) -> None:
        self.app = app
        self.port = port


def test_start_server_builds_app_and_runs_on_configured_port() -> None:
    config = AppConfig(allow_origins=[], port=1234)
    runner = RecordingRunner()

    start_server(config, runner)

    assert isinstance(runner.app, FastAPI)
    assert runner.port == 1234
