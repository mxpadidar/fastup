import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core import exceptions
from fastup.core.entities import User
from fastup.core.enums import UserSex
from fastup.core.unit_of_work import UnitOfWork
from fastup.infra.sql_unit_of_work import SQLUnitOfwWork


@pytest.fixture
def sample_user() -> User:
    """Provides a sample user entity for testing."""
    return User(id=1_000_001, phone="0912", pwdhash="pwd", sex=UserSex.MALE)


async def test_uow_session_is_available_only_within_its_context(uow: SQLUnitOfwWork):
    """
    Verifies the UoW session is active inside the `async with` block
    and raises an exception if accessed outside of it.
    """
    async with uow:
        assert uow.session is not None
        assert isinstance(uow.session, AsyncSession)

    # After exiting, accessing the session should raise UnitOfWorkContextExc
    with pytest.raises(exceptions.UnitOfWorkContextExc):
        assert uow.session


async def test_uow_calling_commit_outside_context_raises_exception(uow: UnitOfWork):
    """
    Verifies that calling commit() outside the `async with` block
    raises a UnitOfWorkContextExc.
    """
    with pytest.raises(exceptions.UnitOfWorkContextExc):
        await uow.commit()


async def test_uow_commit_successfully_persists_changes_to_database(
    uow: UnitOfWork, db_session: AsyncSession, sample_user: User
):
    """
    Verifies that after a successful commit, changes made within the UoW
    are persisted in the database.
    """
    # Act: Add a user and commit within the UoW
    async with uow:
        await uow.users.add(sample_user)
        await uow.commit()

    # Assert: The user exists in a separate, subsequent session
    persisted_user = await db_session.get(User, sample_user.id)
    assert persisted_user is not None
    assert persisted_user.phone == sample_user.phone


async def test_uow_rollback_discards_all_changes_made_within_context(
    uow: UnitOfWork, db_session: AsyncSession, sample_user: User
):
    """
    Verifies that after a rollback, changes made within the UoW are
    discarded and not persisted.
    """
    # Act: Add a user but then roll back the UoW
    async with uow:
        await uow.users.add(sample_user)
        await uow.rollback()

    # Assert: The user does not exist in a separate session
    persisted_user = await db_session.get(User, sample_user.id)
    assert persisted_user is None


async def test_uow_exiting_context_implicitly_rolls_back_uncommitted_changes(
    uow: UnitOfWork, db_session: AsyncSession, sample_user: User
):
    """
    Verifies that if the UoW context is exited without an explicit commit,
    all changes are automatically rolled back.
    """
    # Act: Add a user within the UoW but do not commit
    async with uow:
        await uow.users.add(sample_user)

    # Assert: The user does not exist in a separate session
    persisted_user = await db_session.get(User, sample_user.id)
    assert persisted_user is None
