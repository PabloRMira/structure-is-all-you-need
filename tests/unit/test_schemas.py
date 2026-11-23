import pytest
from pydantic import ValidationError

from myapi.schemas import HealthStatus, HealthStatusCode


def test_health_status_code_values() -> None:
    assert HealthStatusCode.UP == "UP"
    assert HealthStatusCode.DOWN == "DOWN"
    assert HealthStatusCode.UNKNOWN == "UNKNOWN"
    assert {code.value for code in HealthStatusCode} == {"UP", "DOWN", "UNKNOWN"}


def test_health_status_serialization() -> None:
    status = HealthStatus(status=HealthStatusCode.UP)

    assert status.model_dump(mode="json") == {"status": "UP"}


def test_health_status_accepts_raw_string() -> None:
    status = HealthStatus(status="DOWN")

    assert status.status is HealthStatusCode.DOWN


def test_health_status_rejects_unknown_value() -> None:
    with pytest.raises(ValidationError):
        HealthStatus(status="SIDEWAYS")
