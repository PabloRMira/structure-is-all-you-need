from myapi.config import read_app_config
from myapi._version import __version__


def get_app(config: AppConfig) -> FastAPI:
    app = FastAPI(
        title="My API",
        docs_url="/api/docs"
        description="Standard API",
        version=__version__
    )
    app.include_router(
        router=get_endpoints(),
        prefix="/api/v1"
    )
    return app

def run_app(config_path: str) -> None:
    config = read_app_config(config_path)

    app = get_app(config)

    uvicorn.run(app, port=config.port, reload=False)
