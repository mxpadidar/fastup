import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.adapters.concrete import SQLUoW
from fastup.domain import exceptions
from fastup.domain.entities import User
from fastup.domain.enums import UserSex
from fastup.domain.ports import UnitOfWork


@pytest.fixture
def sample_user() -> User:
    user = User(
        email="test@example.com",
        phone="+12025550122",
        display_name="Test User",
        pwdhash="hashed_password",
        sex=UserSex.MALE,
    )
    user.id = 1
    return user


async def test_uow_context_manager(uow: SQLUoW):
    async with uow:
        assert uow.session is not None
        assert isinstance(uow.session, AsyncSession)

    # After exiting the context, the session should be None
    with pytest.raises(exceptions.UoWIsNotReady):
        assert uow.session


async def test_uow_commit_persists_changes(
    uow: UnitOfWork, async_session: AsyncSession, sample_user: User
):
    async with uow:
        await uow.users.add(sample_user)
        await uow.commit()

    got = await async_session.get(User, sample_user.id)
    assert got is not None
    assert got.email == sample_user.email

    # cleanup
    await async_session.delete(got)
    await async_session.commit()


async def test_uow_rollback_discards_changes(
    uow: UnitOfWork, async_session: AsyncSession, sample_user: User
):
    async with uow:
        await uow.users.add(sample_user)
        await uow.rollback()

    got = await async_session.get(User, sample_user.id)
    assert got is None


async def test_uow_discards_changes_whitout_commit(
    uow: UnitOfWork, async_session: AsyncSession, sample_user: User
):
    async with uow:
        await uow.users.add(sample_user)

    got = await async_session.get(User, sample_user.id)
    assert got is None


async def test_uow_raises_outside_context(uow: UnitOfWork):
    with pytest.raises(exceptions.UoWIsNotReady):
        await uow.commit()
