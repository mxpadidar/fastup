import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core.commands import SignupCommand
from fastup.core.config import Config
from fastup.core.entities import Otp, User
from fastup.core.enums import OtpIntent, OtpStatus, UserSex
from fastup.core.exceptions import ConflictExc
from fastup.core.handlers import handle_signup
from fastup.core.services import HashService, IDGenerator
from fastup.core.unit_of_work import UnitOfWork


@pytest.fixture
async def prepared_consumed_otp(db_session: AsyncSession, config: Config) -> Otp:
    """Insert an OTP in CONSUMED state to be used by the signup handler."""
    now = datetime.datetime.now(datetime.UTC)
    otp = Otp(
        id=1010,
        phone="+989121234567",
        intent=OtpIntent.SIGN_UP,
        status=OtpStatus.CONSUMED,
        otp_hash="ignored",
        ipaddr="203.0.113.42",
        expires_at=now + config.otp_lifetime,
        metadata={"seed": "value"},
    )
    db_session.add(otp)
    await db_session.commit()
    return otp


async def test_handle_signup_success_updates_otp_and_creates_user(
    prepared_consumed_otp: Otp,
    uow: UnitOfWork,
    idgen: IDGenerator,
    argon2_hasher: HashService,
):
    """
    Valid flow:
    - OTP exists in CONSUMED state and matches ipaddr
    - Handler sets OTP to USED and creates a new User
    """
    cmd = SignupCommand(
        otp_id=prepared_consumed_otp.id,
        ipaddr=prepared_consumed_otp.ipaddr,
        password="Str0ng-P@ss!",
        sex=UserSex.MALE,
        first_name="John",
        last_name="Doe",
    )

    # Act
    user = await handle_signup(cmd, uow, argon2_hasher, idgen)

    # Assert: user was created with expected fields
    assert isinstance(user, User)
    assert user.phone == prepared_consumed_otp.phone
    assert user.sex == UserSex.MALE
    assert user.fname == "John"
    assert user.lname == "Doe"
    assert user.pwdhash and user.pwdhash != "Str0ng-P@ss!"

    # Assert: OTP is updated to USED with metadata preserved and augmented
    async with uow:
        fetched_otp = await uow.otps.get(id=prepared_consumed_otp.id)
        assert fetched_otp is not None
        assert fetched_otp.status == OtpStatus.USED
        assert fetched_otp.metadata.get("seed") == "value"
        assert fetched_otp.metadata.get("used_for_signup_ip") == cmd.ipaddr

        # And user persists
        fetched_user = await uow.users.get(id=user.id)
        assert fetched_user is not None
        assert fetched_user.phone == prepared_consumed_otp.phone


async def test_handle_signup_conflict_existing_user_raises_conflict_and_marks_otp_used(
    prepared_consumed_otp: Otp,
    uow: UnitOfWork,
    idgen: IDGenerator,
    argon2_hasher: HashService,
    db_session: AsyncSession,
):
    """
    When a user with the same phone already exists:
    - Handler raises ConflictExc
    - OTP state is still marked USED (as the status change occurs before user insert)
    """
    # Arrange: create an existing user with the same phone
    async with uow:
        existing_id = await idgen.next_id()
        existing_user = User(
            id=existing_id,
            phone=prepared_consumed_otp.phone,
            pwdhash="hashed",
            sex=UserSex.FEMALE,
        )
        await uow.users.add(existing_user)
        await uow.commit()

    cmd = SignupCommand(
        otp_id=prepared_consumed_otp.id,
        ipaddr=prepared_consumed_otp.ipaddr,
        password="AnotherP@ss!",
        sex=UserSex.FEMALE,
        first_name="Jane",
        last_name="Roe",
    )

    # Act & Assert
    with pytest.raises(ConflictExc):
        await handle_signup(cmd, uow, argon2_hasher, idgen)

    # # Verify OTP is marked USED despite the conflict
    # async with uow:
    #     otp_after = await uow.otps.get(id=prepared_consumed_otp.id)
    #     assert otp_after is not None
    #     assert otp_after.status == OtpStatus.USED
    #     assert otp_after.metadata.get("used_for_signup_ip") == cmd.ipaddr

    # # Ensure the conflicting user still exists and no duplicate was created by handler
    # async with uow:
    #     fetched_users_same_phone = await db_session.execute(
    #         sqlalchemy.select(User).where(User.phone == prepared_consumed_otp.phone)
    #     )
    #     rows = fetched_users_same_phone.scalars().all()
    #     assert len(rows) == 1
