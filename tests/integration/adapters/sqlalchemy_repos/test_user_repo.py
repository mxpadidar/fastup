import datetime
import typing

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_repos import UserSQLAlchemyRepo
from app.domain import errors
from app.domain.entities import User


async def test_user_repo_add(
    user_repo: UserSQLAlchemyRepo,
    db_session: AsyncSession,
    user_factory: typing.Callable[[int, str], User],
):
    user = user_factory(100000, "test@example.com")
    await user_repo.add(user)

    fetched_user = await db_session.get(User, user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id


async def test_user_repo_get(user_repo: UserSQLAlchemyRepo, user: User):
    fetched_user = await user_repo.get(user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id


async def test_user_repo_get_nonexistent_user(user_repo: UserSQLAlchemyRepo):
    user = await user_repo.get(0)
    assert user is None


async def test_user_repo_get_soft_deleted_user(
    user_repo: UserSQLAlchemyRepo, db_session: AsyncSession, user: User
):
    # ensure user is soft deleted
    user.deleted_at = datetime.datetime.now(datetime.UTC)
    db_session.add(user)
    await db_session.commit()

    fetched_user = await user_repo.get(user.id)
    assert fetched_user is None


async def test_user_repo_get_by_email(user_repo: UserSQLAlchemyRepo, user: User):
    fetched_user = await user_repo.get_by_email(user.email)
    assert fetched_user is not None
    assert fetched_user.id == user.id


async def test_user_repo_get_by_email_nonexistent_email(user_repo: UserSQLAlchemyRepo):
    fetched_user = await user_repo.get_by_email("notfound@example.com")
    assert fetched_user is None


async def test_user_repo_get_by_email_soft_deleted_user(
    user_repo: UserSQLAlchemyRepo, db_session: AsyncSession, user: User
):
    # ensure user is soft deleted
    user.deleted_at = datetime.datetime.now(datetime.UTC)
    db_session.add(user)
    await db_session.commit()

    fetched_user = await user_repo.get_by_email(user.email)
    assert fetched_user is None


async def test_user_repo_delete(
    user_repo: UserSQLAlchemyRepo, db_session: AsyncSession, user: User
):
    await user_repo.delete(user)
    await db_session.commit()

    # Verify the user is soft deleted in the database
    deleted_user = await db_session.get(User, user.id)
    assert deleted_user is not None
    assert deleted_user.deleted_at is not None

    # Verify get method returns None for soft deleted user
    fetched_user = await user_repo.get(user.id)
    assert fetched_user is None


async def test_user_repo_refresh(
    user_repo: UserSQLAlchemyRepo, db_session: AsyncSession, user: User
):
    # Modify the user in the database using raw SQL (session unchanged)
    original_email = user.email
    new_email = "modified@example.com"
    await db_session.execute(
        text("UPDATE users SET email = :email WHERE id = :id"),
        {"email": new_email, "id": user.id},
    )
    await db_session.flush()

    # Refresh the entity from the database
    refreshed = await user_repo.refresh(user)

    # Assert the entity is reloaded with updated database state
    assert refreshed.email != original_email
    assert refreshed.email == new_email
    assert refreshed.id == user.id


async def test_user_reop_get_or_raise(user_repo: UserSQLAlchemyRepo, user: User):
    result = await user_repo.get_or_raise(lambda: user_repo.get(user.id))
    assert result == user


async def test_user_repo_get_or_raise_nonexistent_user(user_repo: UserSQLAlchemyRepo):
    with pytest.raises(errors.NotFoundErr):
        await user_repo.get_or_raise(lambda: user_repo.get(0))
