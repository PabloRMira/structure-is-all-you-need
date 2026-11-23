import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from myapi.config import AppConfig, read_app_config


def test_read_app_config_parses_json(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"allow_origins": ["https://example.com"], "port": 8080}),
        encoding="utf8",
    )

    config = read_app_config(config_path)

    assert config == AppConfig(allow_origins=["https://example.com"], port=8080)


def test_read_app_config_accepts_str_path(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"allow_origins": [], "port": 9000}), encoding="utf8")

    config = read_app_config(str(config_path))

    assert config.port == 9000
    assert config.allow_origins == []


def test_read_app_config_rejects_missing_field(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"port": 8080}), encoding="utf8")

    with pytest.raises(ValidationError):
        read_app_config(config_path)


def test_read_app_config_rejects_wrong_type(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps({"allow_origins": ["x"], "port": "not-an-int"}), encoding="utf8"
    )

    with pytest.raises(ValidationError):
        read_app_config(config_path)


def test_read_app_config_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_app_config(tmp_path / "does-not-exist.json")
