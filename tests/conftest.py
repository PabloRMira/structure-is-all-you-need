from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from myapi.app import get_app
from myapi.config import AppConfig


@pytest.fixture
def app_config() -> AppConfig:
    return AppConfig(allow_origins=["https://example.com"], port=8000)


@pytest.fixture
def client(app_config: AppConfig) -> Iterator[TestClient]:
    with TestClient(get_app(app_config)) as test_client:
        yield test_client
