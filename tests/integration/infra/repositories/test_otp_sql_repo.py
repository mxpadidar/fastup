import datetime
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core.entities import Otp
from fastup.core.enums import OtpIntent, OtpStatus
from fastup.core.exceptions import NotFoundExc
from fastup.infra.sql_repositories import OtpSQLRepo


@pytest.fixture
async def otp_repo(db_session: AsyncSession) -> AsyncGenerator[OtpSQLRepo, None]:
    """Provide a repository instance bound to the shared test session."""
    yield OtpSQLRepo(db_session)


@pytest.fixture
async def persisted_otp(db_session: AsyncSession, hmac_hasher) -> Otp:
    """Persist a baseline OTP record used across repository tests."""
    code = "1234"
    now = datetime.datetime.now(datetime.UTC)
    otp = Otp(
        id=1,
        phone="+989121234567",
        intent=OtpIntent.SIGN_UP,
        status=OtpStatus.SENT,
        otp_hash=hmac_hasher.hash(code),
        ipaddr="127.0.0.1",
        expires_at=now + datetime.timedelta(minutes=5),
    )
    db_session.add(otp)
    await db_session.commit()
    return otp


async def test_get_for_update_locks_and_returns_matching_record(
    otp_repo: OtpSQLRepo, persisted_otp: Otp
):
    """`get_for_update` should return the matching entity when filters align."""
    found = await otp_repo.get_for_update(
        id=persisted_otp.id,
        status=OtpStatus.SENT,
        ipaddr=persisted_otp.ipaddr,
    )

    assert found is not None
    assert found.id == persisted_otp.id
    assert found.status == persisted_otp.status
    assert found.ipaddr == persisted_otp.ipaddr


async def test_get_for_update_raises_not_found_for_missing_row(otp_repo: OtpSQLRepo):
    """Raise `NotFoundExc` when no record matches the provided identifier."""
    with pytest.raises(NotFoundExc):
        await otp_repo.get_for_update(id=999, status=OtpStatus.SENT, ipaddr="unknown")


async def test_get_for_update_respects_status_filter(
    otp_repo: OtpSQLRepo, persisted_otp: Otp
):
    """Ensure the status filter is enforced even when the ID matches."""
    with pytest.raises(NotFoundExc):
        await otp_repo.get_for_update(
            id=persisted_otp.id, status=OtpStatus.CONSUMED, ipaddr=persisted_otp.ipaddr
        )


async def test_get_for_update_respects_ipaddr_filter(
    otp_repo: OtpSQLRepo, persisted_otp: Otp
):
    """Ensure the IP address filter is enforced even when other fields match."""
    with pytest.raises(NotFoundExc):
        await otp_repo.get_for_update(
            id=persisted_otp.id, status=OtpStatus.SENT, ipaddr="other-ip"
        )
