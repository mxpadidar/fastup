import asyncio
import datetime

import pytest

from fastup.core.commands import IssueSignupOtpCommand
from fastup.core.config import Config
from fastup.core.entities import Otp, User
from fastup.core.enums import OtpIntent, UserSex
from fastup.core.exceptions import ConflictExc
from fastup.core.handlers import handle_issue_signup_otp
from fastup.core.services import HashService, IDGenerator
from fastup.core.unit_of_work import UnitOfWork


@pytest.fixture
def event_queue() -> asyncio.Queue:
    return asyncio.Queue()


@pytest.fixture
def cmd() -> IssueSignupOtpCommand:
    return IssueSignupOtpCommand(phone="+989111234567", ipaddr="127.0.0.1")


async def test_handle_issue_signup_otp_creates_and_persists_otp(
    cmd: IssueSignupOtpCommand,
    config: Config,
    uow: UnitOfWork,
    idgen: IDGenerator,
    hmac_hasher: HashService,
    event_queue: asyncio.Queue,
):
    """Verifies that the handler creates and persists a new OTP entity
    for a new phone number."""
    # Act
    otp = await handle_issue_signup_otp(
        cmd=cmd,
        config=config,
        uow=uow,
        idgen=idgen,
        hmac_hasher=hmac_hasher,
        event_queue=event_queue,
    )

    # Assert
    assert isinstance(otp, Otp)
    assert otp.id is not None
    assert otp.phone == cmd.phone
    assert otp.intent == OtpIntent.SIGN_UP
    assert otp.attempts == 0
    assert otp.ipaddr == cmd.ipaddr
    assert otp.otp_hash is not None
    assert otp.expires_at is not None

    # Verify OTP is persisted in database
    async with uow:
        retrieved_otp = await uow.otps.get(id=otp.id)
        assert retrieved_otp is not None
        assert retrieved_otp.id == otp.id
        assert retrieved_otp.phone == cmd.phone


async def test_handle_issue_signup_otp_sets_correct_expiration(
    cmd: IssueSignupOtpCommand,
    config: Config,
    uow: UnitOfWork,
    idgen: IDGenerator,
    hmac_hasher: HashService,
    event_queue: asyncio.Queue,
):
    """
    Verifies that the handler sets the OTP expiration time correctly
    based on the config's otp_lifetime."""
    # Arrange
    before_time = datetime.datetime.now(datetime.UTC)

    # Act
    otp = await handle_issue_signup_otp(
        cmd=cmd,
        config=config,
        uow=uow,
        idgen=idgen,
        hmac_hasher=hmac_hasher,
        event_queue=event_queue,
    )

    # Assert
    after_time = datetime.datetime.now(datetime.UTC)
    expected_min_expiry = before_time + config.otp_lifetime
    expected_max_expiry = after_time + config.otp_lifetime

    assert expected_min_expiry <= otp.expires_at <= expected_max_expiry


async def test_handle_issue_signup_otp_hashes_code_securely(
    cmd: IssueSignupOtpCommand,
    config: Config,
    uow: UnitOfWork,
    idgen: IDGenerator,
    hmac_hasher: HashService,
    event_queue: asyncio.Queue,
):
    """Verifies that the handler hashes the OTP code and does not store
    it in plain text."""
    # Act
    otp = await handle_issue_signup_otp(
        cmd=cmd,
        config=config,
        uow=uow,
        idgen=idgen,
        hmac_hasher=hmac_hasher,
        event_queue=event_queue,
    )

    # Assert: The stored hash should not be a simple digit string
    assert otp.otp_hash is not None
    assert not otp.otp_hash.isdigit()
    assert len(otp.otp_hash) > config.otp_length


async def test_handle_issue_signup_otp_raises_conflict_when_user_exists(
    cmd: IssueSignupOtpCommand,
    config: Config,
    uow: UnitOfWork,
    idgen: IDGenerator,
    hmac_hasher: HashService,
    event_queue: asyncio.Queue,
):
    """Verifies that the handler raises ConflictExc when the phone number
    is already registered to an existing user."""
    # Arrange: Create an existing user with the same phone
    async with uow:
        user_id = await idgen.next_id()
        existing_user = User(
            id=user_id, phone=cmd.phone, pwdhash="hashed", sex=UserSex.MALE
        )
        await uow.users.add(existing_user)
        await uow.commit()

    # Act & Assert
    with pytest.raises(ConflictExc):
        await handle_issue_signup_otp(
            cmd=cmd,
            config=config,
            uow=uow,
            idgen=idgen,
            hmac_hasher=hmac_hasher,
            event_queue=event_queue,
        )


async def test_handle_issue_signup_otp_allows_multiple_otps_for_same_phone(
    cmd: IssueSignupOtpCommand,
    config: Config,
    uow: UnitOfWork,
    idgen: IDGenerator,
    hmac_hasher: HashService,
    event_queue: asyncio.Queue,
):
    """Verifies that the handler can create multiple OTPs for the same
    phone number (for retry scenarios)."""
    # Act: Create two OTPs for the same phone number
    otp1 = await handle_issue_signup_otp(
        cmd=cmd,
        config=config,
        uow=uow,
        idgen=idgen,
        hmac_hasher=hmac_hasher,
        event_queue=event_queue,
    )
    otp2 = await handle_issue_signup_otp(
        cmd=cmd,
        config=config,
        uow=uow,
        idgen=idgen,
        hmac_hasher=hmac_hasher,
        event_queue=event_queue,
    )

    # Assert: Both OTPs should be distinct
    assert otp1.id != otp2.id
    assert otp1.otp_hash != otp2.otp_hash
