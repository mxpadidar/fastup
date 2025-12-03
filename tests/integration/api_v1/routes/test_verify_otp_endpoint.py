import datetime

import httpx
import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import NamedTuple

from fastup.core.config import Config
from fastup.core.entities import Otp
from fastup.core.enums import OtpIntent, OtpStatus
from fastup.core.services import HashService
from fastup.infra.sql_repositories import OtpSQLRepo
from fastup.infra.tables.otps_table import otps


class OtpCode(NamedTuple):
    id: int
    code: str


@pytest.fixture
def patch_otp_repo_get_for_update_timezone(monkeypatch: pytest.MonkeyPatch):
    """Ensure SQLite’s naive datetimes do not break the timezone-sensitive handler."""
    original = OtpSQLRepo.get_for_update

    async def wrapper(*args, **kwargs):
        otp = await original(*args, **kwargs)
        otp.expires_at = otp.expires_at.replace(tzinfo=datetime.UTC)
        return otp

    monkeypatch.setattr(OtpSQLRepo, "get_for_update", wrapper)


@pytest.fixture
async def otp_code(db_session: AsyncSession, hmac_hasher: HashService) -> OtpCode:
    """Persist an OTP and return the matching verification command."""
    now = datetime.datetime.now(datetime.UTC)
    otp = Otp(
        id=100,
        phone="0912",
        intent=OtpIntent.SIGN_UP,
        status=OtpStatus.SENT,
        otp_hash=hmac_hasher.hash("1010"),
        ipaddr="127.0.0.1",
        expires_at=now + datetime.timedelta(minutes=1),
    )
    db_session.add(otp)
    await db_session.commit()
    return OtpCode(id=otp.id, code="1010")


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_returns_token_on_success(
    async_client: httpx.AsyncClient, otp_code: OtpCode
):
    """Successfully verifies an OTP and returns a freshly generated token."""
    response = await async_client.patch(
        f"/api/v1/fastup/otps/{otp_code.id}", json={"code": otp_code.code}
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()
    raw = data.get("raw")
    exp = data.get("exp")
    typ = data.get("typ")

    assert raw is not None
    assert exp is not None
    assert typ == "signup"

    exp_dt = datetime.datetime.fromisoformat(exp)
    assert isinstance(exp_dt, datetime.datetime)


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_wrong_code(
    async_client: httpx.AsyncClient, otp_code: OtpCode
):
    """Rejects verification when the provided OTP code is incorrect."""
    response = await async_client.patch(
        f"/api/v1/fastup/otps/{otp_code.id}", json={"code": 9999}
    )
    assert response.status_code == 403


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_expired_code(
    async_client: httpx.AsyncClient, db_session: AsyncSession, otp_code: OtpCode
):
    """Rejects verification after the OTP has expired."""
    expired_at = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)
    await db_session.execute(
        sqlalchemy.update(otps)
        .where(otps.c.id == otp_code.id)
        .values(expires_at=expired_at)
    )
    await db_session.commit()

    response = await async_client.patch(
        f"/api/v1/fastup/otps/{otp_code.id}", json={"code": otp_code.code}
    )
    assert response.status_code == 403


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_after_attempt_limit(
    async_client: httpx.AsyncClient,
    db_session: AsyncSession,
    otp_code: OtpCode,
    config: Config,
):
    """Rejects verification once OTP attempt count reaches the configured limit."""
    await db_session.execute(
        sqlalchemy.update(otps)
        .where(otps.c.id == otp_code.id)
        .values(attempts=config.otp_max_attempts)
    )
    await db_session.commit()

    response = await async_client.patch(
        f"/api/v1/fastup/otps/{otp_code.id}", json={"code": otp_code.code}
    )

    assert response.status_code == 429


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_returns_403_when_not_found(async_client: httpx.AsyncClient):
    """Returns 403 when verifying an OTP that does not exist."""
    response = await async_client.patch(
        "/api/v1/fastup/otps/99999", json={"code": "1234"}
    )
    assert response.status_code == 403


async def test_verify_otp_rejects_invalid_payload(async_client: httpx.AsyncClient):
    """Rejects malformed request payloads lacking the required 'code' field."""
    response = await async_client.patch(
        "/api/v1/fastup/otps/100", json={"invalid": "payload"}
    )

    assert response.status_code == 400
