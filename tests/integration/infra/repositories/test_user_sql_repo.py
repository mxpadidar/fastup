import datetime
import typing

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core.entities import User
from fastup.core.enums import UserSex
from fastup.core.repositories import UserRepo
from fastup.infra.sql_repositories import UserSQLRepo


@pytest.fixture
async def user_repo(db_session: AsyncSession) -> UserRepo:
    """Provides a UserSQLRepo instance with an active session."""
    return UserSQLRepo(db_session)


@pytest.fixture
async def active_user(db_session: AsyncSession) -> typing.AsyncGenerator[User, None]:
    """Provides an active (not deleted) user in the database."""
    user = User(id=1, phone="+989121234567", pwdhash="hash", sex=UserSex.MALE)
    db_session.add(user)
    await db_session.commit()
    yield user
    await db_session.delete(user)
    await db_session.commit()


@pytest.fixture
async def deleted_user(db_session: AsyncSession) -> typing.AsyncGenerator[User, None]:
    """Provides a deleted user in the database."""
    user = User(
        id=2,
        phone="09129876543",
        pwdhash="hash",
        sex=UserSex.MALE,
        deleted_at=datetime.datetime.now(datetime.UTC),
    )
    db_session.add(user)
    await db_session.commit()
    yield user
    await db_session.delete(user)
    await db_session.commit()


async def test_get_by_phone_returns_active_user(user_repo: UserRepo, active_user: User):
    """Returns the active user when only_active is default (True)."""
    result = await user_repo.get_by_phone(active_user.phone)
    assert result is not None
    assert result.id == active_user.id
    assert result.deleted_at is None


async def test_get_by_phone_ignores_deleted_by_default(
    user_repo: UserRepo, deleted_user: User
):
    """Returns None for deleted users when only_active=True (the default)."""
    result = await user_repo.get_by_phone(deleted_user.phone)
    assert result is None


async def test_get_by_phone_includes_deleted_when_flag_false(
    user_repo: UserRepo, deleted_user: User
):
    """Returns deleted user when only_active is set to False."""
    result = await user_repo.get_by_phone(deleted_user.phone, only_active=False)
    assert result is not None
    assert result.id == deleted_user.id
    assert result.deleted_at is not None


async def test_get_by_phone_returns_none_for_nonexistent(user_repo: UserRepo):
    """Returns None when no user with the phone exists."""
    result = await user_repo.get_by_phone("+989000000000")
    assert result is None
