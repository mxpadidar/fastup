from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.domain.entities import User


async def test_signup_endpoint_valid_data(
    async_client: AsyncClient, db_session: AsyncSession
):
    response = await async_client.post(
        "/api/v1/signup",
        json={"email": "newuser@example.com", "password": "securepassword123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["is_active"] is False

    assert "access_token" in data
    assert "token" in data["access_token"]
    assert "exp" in data["access_token"]
    assert "refresh_token" in data
    assert "token" in data["refresh_token"]
    assert "exp" in data["refresh_token"]

    # cleanup
    user = await db_session.get(User, data["user"]["id"])
    await db_session.delete(user)
    await db_session.commit()


async def test_signup_endpoint_existing_email_returns_409(
    async_client: AsyncClient, user: User
):
    response = await async_client.post(
        "/api/v1/signup",
        json={"email": user.email, "password": "newpassword"},
    )
    assert response.status_code == 409


async def test_signup_endpoint_invalid_email_returns_422(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/signup",
        json={"email": "invalidemail", "password": "password"},
    )
    assert response.status_code == 422


async def test_signup_endpoint_missing_field_returns_422(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/signup",
        json={"email": "test@example.com"},  # missing password
    )
    assert response.status_code == 422
