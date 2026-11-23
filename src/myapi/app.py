import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myapi._version import __version__
from myapi.api.api_v1.endpoints import get_endpoints
from myapi.config import AppConfig, read_app_config


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


def run_app(config_path: str) -> None:
    config = read_app_config(config_path)

    app = get_app(config)

    uvicorn.run(app, port=config.port, reload=False)
