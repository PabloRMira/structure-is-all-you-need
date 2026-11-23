from fastapi.testclient import TestClient


def test_health_endpoint_returns_up(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_health_endpoint_reflects_allowed_origin(client: TestClient) -> None:
    response = client.get("/api/v1/health", headers={"Origin": "https://example.com"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://example.com"


def test_openapi_schema_is_served(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "My API"
