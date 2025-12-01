import datetime

import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core.commands import VerifyOtpCommand
from fastup.core.config import Config
from fastup.core.entities import Otp
from fastup.core.enums import OtpIntent, OtpStatus
from fastup.core.exceptions import AccessDeniedExc, AttemptLimitReached, NotFoundExc
from fastup.core.handlers import handle_verify_otp
from fastup.core.services import HashService
from fastup.core.unit_of_work import UnitOfWork
from fastup.infra.sql_repositories import OtpSQLRepo
from fastup.infra.tables.otps_table import otps


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
async def cmd(db_session: AsyncSession, hmac_hasher: HashService) -> VerifyOtpCommand:
    """Persist an OTP and return the matching verification command."""
    now = datetime.datetime.now(datetime.UTC)
    otp = Otp(
        id=100,
        phone="0912",
        intent=OtpIntent.SIGN_UP,
        status=OtpStatus.SENT,
        otp_hash=hmac_hasher.hash("1010"),
        ipaddr="localhost",
        expires_at=now + datetime.timedelta(minutes=1),
    )
    db_session.add(otp)
    await db_session.commit()

    return VerifyOtpCommand(otp_id=otp.id, code="1010", ipaddr="localhost")


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_consumes_valid_code(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
):
    """Accepts a valid OTP and marks it as consumed."""
    otp = await handle_verify_otp(cmd, config, uow, hmac_hasher)

    assert otp.id == cmd.otp_id
    assert otp.status == OtpStatus.CONSUMED
    assert otp.consumed_at is not None


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_expired_token(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
    db_session: AsyncSession,
):
    """Rejects OTPs whose expiration timestamp has passed."""
    expired_at = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)
    await db_session.execute(
        sqlalchemy.update(otps)
        .where(otps.c.id == cmd.otp_id)
        .values(expires_at=expired_at)
    )
    await db_session.commit()

    with pytest.raises(AccessDeniedExc):
        await handle_verify_otp(cmd, config, uow, hmac_hasher)


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_incorrect_code(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
):
    """Rejects OTPs when the provided code does not match the stored hash."""
    wrong_cmd = VerifyOtpCommand(
        otp_id=cmd.otp_id,
        code="wrong-code",
        ipaddr=cmd.ipaddr,
    )

    with pytest.raises(AccessDeniedExc):
        await handle_verify_otp(wrong_cmd, config, uow, hmac_hasher)

    async with uow:
        otp = await uow.otps.get_for_update(
            id=cmd.otp_id, status=OtpStatus.SENT, ipaddr=cmd.ipaddr
        )
        assert otp.attempts == 1  # Ensure attempt counter incremented
        attmpt_md = otp.metadata.get("attempt[1]")
        assert attmpt_md is not None
        assert attmpt_md["tried_code"] == "wrong-code"


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_mismatched_ip(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
    db_session: AsyncSession,
):
    """Rejects OTPs when the IP address differs from the request origin."""
    await db_session.execute(
        sqlalchemy.update(otps).where(otps.c.id == cmd.otp_id).values(ipaddr="other-ip")
    )
    await db_session.commit()

    wrong_cmd = VerifyOtpCommand(
        otp_id=cmd.otp_id,
        code=cmd.code,
        ipaddr="different",
    )

    with pytest.raises(AccessDeniedExc):
        await handle_verify_otp(wrong_cmd, config, uow, hmac_hasher)


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_after_attempt_limit_reached(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
    db_session: AsyncSession,
):
    """Rejects OTPs once their attempt counter reaches the configured limit."""
    await db_session.execute(
        sqlalchemy.update(otps)
        .where(otps.c.id == cmd.otp_id)
        .values(attempts=config.otp_max_attempts)
    )
    await db_session.commit()

    with pytest.raises(AttemptLimitReached):
        await handle_verify_otp(cmd, config, uow, hmac_hasher)


async def test_verify_otp_raises_when_not_found(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
    monkeypatch: pytest.MonkeyPatch,
):
    """Raises AccessDenied when the repository cannot locate the OTP."""

    async def fake_get_for_update(*args, **kwargs):
        raise NotFoundExc("not found")

    monkeypatch.setattr(OtpSQLRepo, "get_for_update", fake_get_for_update)

    with pytest.raises(AccessDeniedExc):
        await handle_verify_otp(cmd, config, uow, hmac_hasher)


@pytest.mark.usefixtures("patch_otp_repo_get_for_update_timezone")
async def test_verify_otp_rejects_if_status_not_sent(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
    db_session: AsyncSession,
):
    """Rejects OTPs that are not in the SENT state (e.g., ISSUED, CONSUMED)."""
    await db_session.execute(
        sqlalchemy.update(otps)
        .where(otps.c.id == cmd.otp_id)
        .values(status=OtpStatus.ISSUED)
    )
    await db_session.commit()

    with pytest.raises(AccessDeniedExc):
        await handle_verify_otp(cmd, config, uow, hmac_hasher)
