from typing import Protocol

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myapi._version import __version__
from myapi.api.api_v1.endpoints import get_endpoints
from myapi.config import AppConfig, read_app_config


class ServerRunner(Protocol):
    """Starts a FastAPI app. The seam that lets tests inject a fake."""

    def __call__(self, app: FastAPI, port: int) -> None: ...


def get_app(config: AppConfig) -> FastAPI:
    app = FastAPI(
        title="My API",
        docs_url="/api/docs",
        description="Standard API",
        version=__version__,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        router=get_endpoints(),
        prefix="/api/v1",
    )
    return app


def run_uvicorn(app: FastAPI, port: int) -> None:
    # Bind all interfaces so the server is reachable from outside its container.
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)


def start_server(config: AppConfig, run_server: ServerRunner = run_uvicorn) -> None:
    app = get_app(config)
    run_server(app, config.port)


def run_app(config_path: str) -> None:
    config = read_app_config(config_path)
    start_server(config)
