from httpx import AsyncClient


async def test_health_endpoint_returns_200_ok_with_correct_body(
    async_client: AsyncClient,
):
    """
    Ensures the /health endpoint returns a 200 OK status code and the
    expected JSON body `{"status": "ok"}`.
    """
    response = await async_client.get("/api/v1/fastup/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_health_endpoint_returns_application_json_content_type_header(
    async_client: AsyncClient,
):
    """
    Verifies that the /health endpoint's response includes the correct
    'content-type: application/json' header.
    """
    response = await async_client.get("/api/v1/fastup/health")
    assert response.headers["content-type"] == "application/json"
