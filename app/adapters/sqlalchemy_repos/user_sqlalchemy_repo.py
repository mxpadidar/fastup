import datetime
import typing

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import User
from app.domain.repositories import UserRepo


class UserSQLAlchemyRepo(UserRepo):
    """SQLAlchemy implementation of UserRepo."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the SQLAlchemy repository.

        :param session: The SQLAlchemy session to use.
        """
        self.session = session

    async def add(self, ntt: User) -> User:
        """Add a new entity to the session.

        :param ntt: The entity to add.
        """
        self.session.add(ntt)
        return ntt

    async def delete(self, ntt: User) -> None:
        """Soft delete the user entity.

        :param ntt: The entity to delete.
        """
        ntt.deleted_at = datetime.datetime.now(tz=datetime.timezone.utc)
        await self.add(ntt)

    async def refresh(self, ntt: User) -> User:
        """Refresh the entity in the session.

        :param ntt: The entity to refresh.
        """
        await self.session.refresh(ntt)
        return ntt

    @typing.no_type_check
    async def get(self, id: int) -> User | None:
        """Get a non-deleted user by ID.

        :param id: The ID of the user to retrieve.
        :return: The user if found, None otherwise.
        """
        stmt = select(User).where(
            User.id == id,
            User.deleted_at.is_(None),
        )
        return await self.session.scalar(stmt)

    @typing.no_type_check
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a non-deleted user by email address.

        :param email: The email address of the user.
        :return: The user if found, None otherwise.
        """
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
        return await self.session.scalar(stmt)
