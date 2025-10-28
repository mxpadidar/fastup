import typing

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import SqlAlchemyUoW
from app.domain import errors
from app.domain.base import UnitOfWork
from app.domain.entities import User


async def test_uow_context_manager(uow: SqlAlchemyUoW):
    async with uow:
        assert uow.session is not None
        assert isinstance(uow.session, AsyncSession)

    # After exiting the context, the session should be None
    with pytest.raises(errors.UoWIsNotReady):
        assert uow.session


async def test_uow_commit_persists_changes(
    uow: UnitOfWork,
    db_session: AsyncSession,
    user_factory: typing.Callable[[int, str], User],
):
    user = user_factory(1, "test@example.com")

    async with uow:
        await uow.users.add(user)
        await uow.commit()

    fetched_user = await db_session.get(User, user.id)
    assert fetched_user is not None
    assert fetched_user.email == user.email

    # cleanup
    await db_session.delete(fetched_user)
    await db_session.commit()


async def test_uow_rollback_discards_changes(
    uow: UnitOfWork,
    db_session: AsyncSession,
    user_factory: typing.Callable[[int, str], User],
):
    user = user_factory(1, "test@example.com")

    async with uow:
        await uow.users.add(user)
        await uow.rollback()

    fetched_user = await db_session.get(User, user.id)
    assert fetched_user is None


async def test_uow_raises_outside_context(uow: UnitOfWork):
    with pytest.raises(errors.UoWIsNotReady):
        await uow.commit()
