from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """test the health check endpoint."""
    response = client.get("/api/v1/metadata/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
