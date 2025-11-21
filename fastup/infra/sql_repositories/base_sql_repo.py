import abc
import typing

import sqlalchemy
from sqlalchemy.ext.asyncio.session import AsyncSession

from fastup.core.repositories import Repository


class SQLRepository[T](Repository[T], abc.ABC):
    """Abstract SQLAlchemy repository providing a base for concrete implementations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @property
    @abc.abstractmethod
    def entity_cls(self) -> typing.Type:
        raise NotImplementedError

    async def get(self, id: int, **kwargs) -> T | None:
        """Retrieve an entity by ID with optional additional filters."""
        kwargs.update({"id": id})
        stmt = sqlalchemy.select(self.entity_cls).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, entity: T) -> None:
        """Adds a new entity to the current session."""
        self.session.add(entity)

    async def delete(self, entity: T) -> None:
        """Deletes an entity from the current session."""
        await self.session.delete(entity)

    async def refresh(self, entity: T) -> None:
        """Refreshes an entity's state from the database."""
        await self.session.refresh(entity)
