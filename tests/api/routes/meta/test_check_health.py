from fastapi.testclient import TestClient


def test_check_health(client: TestClient) -> None:
    response = client.get("/api/meta/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("health") is True
