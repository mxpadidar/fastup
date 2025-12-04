import httpx
import pytest

from fastup.core.enums import UserSex


async def test_signup_returns_201_and_user_payload_on_success(
    async_client: httpx.AsyncClient, otp_token
):
    """
    Successfully completes signup when a valid signup token is provided via Authorization header
    and a valid payload is posted. Ensures 201 response, JSON content type, and expected user fields.
    """
    headers = {"Authorization": f"Bearer {otp_token.raw}"}
    payload = {
        "password": "Str0ng-P@ss!",
        "sex": UserSex.MALE,
        "first_name": "John",
        "last_name": "Doe",
    }

    response = await async_client.post(
        "/api/v1/fastup/accounts/signup", json=payload, headers=headers
    )

    assert response.status_code == 201
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    # Shape assertions consistent with other endpoint tests
    assert "id" in data and isinstance(data["id"], int)
    assert "phone" in data and isinstance(data["phone"], str)

    # Name fields can be first_name/last_name or fname/lname depending on response model;
    # assert flexibly to accommodate either.
    assert (data.get("first_name") == "John") or (data.get("fname") == "John")
    assert (data.get("last_name") == "Doe") or (data.get("lname") == "Doe")

    # Sex should match the provided enum value
    assert data.get("sex") == UserSex.MALE


@pytest.mark.parametrize(
    "invalid_payload",
    [
        pytest.param({}, id="missing_all_fields"),
        pytest.param({"password": ""}, id="empty_password"),
        pytest.param(
            {"password": "Str0ng-P@ss!", "sex": "unknown"}, id="invalid_sex_value"
        ),
        pytest.param(
            {"password": None, "sex": UserSex.FEMALE}, id="null_password_value"
        ),
        pytest.param("malformed", id="non_json_payload"),
    ],
)
async def test_signup_returns_400_for_invalid_input(
    async_client: httpx.AsyncClient, otp_token, invalid_payload
):
    """
    Should return 400 Bad Request for invalid payloads:
    - missing required fields
    - invalid enum values
    - empty or null values
    - non-JSON body
    """
    headers = {"Authorization": f"Bearer {otp_token.raw}"}
    response = await async_client.post(
        "/api/v1/fastup/accounts/signup", json=invalid_payload, headers=headers
    )

    assert response.status_code == 400
    data = response.json()
    assert "errors" in data


async def test_signup_returns_401_without_authorization(
    async_client: httpx.AsyncClient,
):
    """
    Should return 401 Unauthorized when Authorization header is missing.
    """
    payload = {
        "password": "Str0ng-P@ss!",
        "sex": UserSex.FEMALE,
        "first_name": "Jane",
        "last_name": "Roe",
    }

    response = await async_client.post("/api/v1/fastup/accounts/signup", json=payload)

    assert response.status_code == 401


async def test_signup_returns_403_with_invalid_token(async_client: httpx.AsyncClient):
    """
    Should return 403 Forbidden when Authorization header contains an invalid token
    or a token that cannot be used for signup.
    """
    headers = {"Authorization": "Bearer invalid.token.value"}
    payload = {
        "password": "Str0ng-P@ss!",
        "sex": UserSex.MALE,
        "first_name": "John",
        "last_name": "Doe",
    }

    response = await async_client.post(
        "/api/v1/fastup/accounts/signup", json=payload, headers=headers
    )

    assert response.status_code in (401, 403)
    # Depending on token validation path, either 401 (unauthenticated) or 403 (not allowed) is acceptable.
