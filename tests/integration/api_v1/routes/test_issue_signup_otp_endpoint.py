from datetime import datetime

import httpx
import pytest


async def test_issue_signup_otp_success_response(async_client: httpx.AsyncClient):
    """
    Ensure the signup OTP endpoint responds with 202, application/json content type,
    and a payload containing an 'id' and a correctly formatted 'expires_at' when given a valid phone number.
    """
    response = await async_client.post(
        "/api/v1/fastup/accounts/signup",
        json={"phone": "+989121234567"},
    )

    assert response.status_code == 202
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    id = data.get("id")
    expires_at = data.get("expires_at")
    assert id is not None and expires_at is not None

    # Validate that expires_at is properly formatted ISO datetime string
    expires_at_dt = datetime.fromisoformat(expires_at)
    assert isinstance(expires_at_dt, datetime)


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"phone": "invalid"}, id="invalid_phone_format"),
        pytest.param({}, id="missing_phone_field"),
        pytest.param({"phone": ""}, id="empty_phone_string"),
        pytest.param({"phone": None}, id="null_phone_value"),
    ],
)
async def test_signup_otp_returns_400_for_invalid_input(
    async_client: httpx.AsyncClient, payload: dict
):
    """
    Should return HTTP 400 Bad Request if the signup OTP endpoint receives
    invalid input—wrong format, missing, empty, or null phone field.
    """
    url = "/api/v1/fastup/accounts/signup"

    response = await async_client.post(url, json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "errors" in data or "error" in data


async def test_signup_otp_returns_400_for_malformed_json(
    async_client: httpx.AsyncClient,
):
    """
    Should return HTTP 400 Bad Request if the signup OTP endpoint receives
    malformed (non-JSON) content.
    """
    url = "/api/v1/fastup/accounts/signup"
    malformed_content = "not valid json"  # Not a valid JSON string

    response = await async_client.post(url, content=malformed_content)

    assert response.status_code == 400
    data = response.json()
    assert "errors" in data or "error" in data
