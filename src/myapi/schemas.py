from enum import StrEnum

from pydantic import BaseModel, Field


class HealthStatusCode(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


class HealthStatus(BaseModel):
    "Health status of the API"

    status: HealthStatusCode = Field(description="Health status")
