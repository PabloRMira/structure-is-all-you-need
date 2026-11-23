from fastapi import APIRouter
from myapi.schemas import HealthStatus, HealthStatusCode


def get_endpoints() -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def check_health() -> HealthStatus:
        "Check health status of the API"
    
        return HealthStatus(status=HealthStatusCode.UP)

    return router
