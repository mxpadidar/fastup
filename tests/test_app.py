def test_fastapi_app(client) -> None:
    """Test the FastAPI app to ensure it is running,
    and returns a 404 for an invalid endpoint."""
    response = client.get("/some/invalid/endpoint")
    assert response.status_code == 404
