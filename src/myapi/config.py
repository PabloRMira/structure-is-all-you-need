import json
from pathlib import Path

from loguru import logger
from pydantic import BaseModel


class AppConfig(BaseModel):
    allow_origins: list[str]
    port: int


def read_app_config(config_path: str | Path) -> AppConfig:
    logger.info("Reading app config")
    config_raw = json.loads(Path(config_path).read_text("utf8"))
    return AppConfig(**config_raw)
