def test_health_check(client):
    """Test the health check endpoint returns correct response."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_headers(client):
    """Test the health check endpoint has proper content type."""
    response = client.get("/api/v1/health")

    assert response.headers["content-type"] == "application/json"


def test_health_check_method_not_allowed(client):
    """Test the health check endpoint only accepts GET requests."""
    response = client.post("/api/v1/health")

    assert response.status_code == 405
