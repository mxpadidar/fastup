from fastapi.testclient import TestClient

from fastup.core import settings


def test_get_app_details(client: TestClient) -> None:
    response = client.get("/api/meta/app")
    assert response.status_code == 200
    data = response.json()
    assert data.get("version") == settings.version
    assert data.get("name") == settings.name
