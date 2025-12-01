from datetime import datetime

import httpx
import pytest

from fastup.core.enums import OtpIntent, OtpStatus


async def test_issue_otp_success_response(async_client: httpx.AsyncClient):
    """
    Ensure the issue OTP endpoint responds with 202, application/json content type,
    and a payload containing 'id', 'expires_at', and 'status' when given a valid phone number and intent.
    """
    response = await async_client.post(
        "/api/v1/fastup/otps",
        json={"phone": "+989121234567", "intent": OtpIntent.SIGN_UP},
    )

    assert response.status_code == 202
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    id = data.get("id")
    expires_at = data.get("expires_at")
    status = data.get("status")
    assert id is not None and expires_at is not None and status is not None

    # Validate that expires_at is properly formatted ISO datetime string
    expires_at_dt = datetime.fromisoformat(expires_at)
    assert isinstance(expires_at_dt, datetime)

    # Validate that status is ISSUED
    assert status == OtpStatus.ISSUED


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"phone": "invalid", "intent": OtpIntent.SIGN_UP}, id="invalid_phone_format"
        ),
        pytest.param({"intent": OtpIntent.SIGN_UP}, id="missing_phone_field"),
        pytest.param(
            {"phone": "", "intent": OtpIntent.SIGN_UP}, id="empty_phone_string"
        ),
        pytest.param(
            {"phone": None, "intent": OtpIntent.SIGN_UP}, id="null_phone_value"
        ),
        pytest.param({"phone": "+989121234567"}, id="missing_intent_field"),
        pytest.param(
            {"phone": "+989121234567", "intent": None}, id="null_intent_value"
        ),
        pytest.param(
            {"phone": "+989121234567", "intent": "invalid"}, id="invalid_intent_format"
        ),
        pytest.param("malformed_payload", id="non_json_payload"),
    ],
)
async def test_issue_otp_returns_400_for_invalid_input(
    async_client: httpx.AsyncClient, payload: dict
):
    """Should return HTTP 400 Bad Request if the OTP endpoint receives
    invalid input—wrong format, missing, empty, or null phone/intent field.
    """
    url = "/api/v1/fastup/otps"

    response = await async_client.post(url, json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "errors" in data
