from httpx import AsyncClient


async def test_health_check_endpoint_response(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_health_check_endpoint_headers(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.headers["content-type"] == "application/json"
