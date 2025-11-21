import typing

import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core.entities import User
from fastup.core.enums import UserSex
from fastup.core.repositories import Repository
from fastup.infra.sql_repositories import SQLRepository
from fastup.infra.tables.users_table import users


@pytest.fixture
async def repo(db_session: AsyncSession) -> Repository:
    """Provides a UserSQLRepository instance with an active session."""

    class UserSQLRepository(SQLRepository[User]):
        @property
        def entity_cls(self) -> typing.Type:
            return User

    return UserSQLRepository(db_session)


@pytest.fixture
async def user(db_session: AsyncSession) -> typing.AsyncGenerator[User, None]:
    """Provides a persisted user entity for tests."""
    new_user = User(
        id=1_000_001,
        phone="0912",
        pwdhash="pwd",
        sex=UserSex.MALE,
    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    yield new_user


async def test_repo_add_persists_entity(repo: SQLRepository, db_session: AsyncSession):
    """Verifies add() correctly adds a new entity to the session."""
    new_user = User(
        id=1_000_001,
        phone="0912",
        pwdhash="pwd",
        sex=UserSex.MALE,
    )
    await repo.add(new_user)
    await db_session.flush()  # Manually flush to check persistence

    persisted_user = await db_session.get(User, new_user.id)
    assert persisted_user is not None
    assert persisted_user.id == new_user.id
    assert persisted_user.phone == new_user.phone


async def test_repo_get_by_id_returns_correct_entity(user: User, repo: SQLRepository):
    """Verifies get() can retrieve an existing entity by its ID."""
    retrieved_user = await repo.get(id=user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id


async def test_repo_get_with_additional_filters(user: User, repo: SQLRepository):
    """Verifies get() can retrieve an entity by ID with additional filters."""
    retrieved_user = await repo.get(id=user.id, phone=user.phone)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.phone == user.phone


async def test_repo_get_returns_none_for_nonexistent_entity(repo: SQLRepository):
    """Verifies get() returns None when no entity matches the filter."""
    retrieved_user = await repo.get(id=0)
    assert retrieved_user is None


async def test_repo_delete_removes_entity(
    user: User, repo: SQLRepository, db_session: AsyncSession
):
    """Verifies delete() removes an entity from the database."""
    # Ensure the user exists before deletion
    user_to_delete = await db_session.get(User, user.id)
    assert user_to_delete is not None

    await repo.delete(user_to_delete)
    await db_session.flush()

    # Verify the user is gone
    deleted_user = await db_session.get(User, user.id)
    assert deleted_user is None


async def test_repo_refresh_updates_entity_state(
    user: User, repo: SQLRepository, db_session: AsyncSession
):
    """Verifies refresh() updates an entity's attributes from the database."""
    # Simulate an external change to the user's data
    new_phone = "0913"
    await db_session.execute(
        sqlalchemy.update(users).where(users.c.id == user.id).values(phone=new_phone)
    )
    await db_session.commit()

    # The in-memory 'user' object still has the old phone
    assert user.phone != new_phone

    await repo.refresh(user)

    # After refresh, the object should have the new phone
    assert user.phone == new_phone
