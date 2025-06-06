from fastapi.testclient import TestClient

from fastup.core.settings import version


def test_version_route(client: TestClient) -> None:
    response = client.get("/api/v1/meta/app/version")
    assert response.status_code == 200

    data = response.json()
    assert data.get("version") == version


def test_db_version_route(client: TestClient) -> None:
    response = client.get("/api/v1/meta/db/version")
    assert response.status_code == 200

    data = response.json()
    assert "db_version" in data
    print(data)
