import abc
import logging
import typing

import sqlalchemy
from sqlalchemy.ext.asyncio.session import AsyncSession

from fastup.core.repositories import Repository

logger = logging.getLogger(__name__)


class SQLRepository[T](Repository[T], abc.ABC):
    """Abstract SQLAlchemy repository providing a base for concrete implementations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    @abc.abstractmethod
    def entity(self) -> typing.Type:
        raise NotImplementedError

    async def add(self, entity: T) -> None:
        """Adds a new entity to the current session."""
        self._session.add(entity)

    async def delete(self, entity: T) -> None:
        """Deletes an entity from the current session."""
        await self._session.delete(entity)

    async def refresh(self, entity: T) -> None:
        """Refreshes an entity's state from the database."""
        await self._session.refresh(entity)

    async def _get(self, **kwargs) -> T | None:
        """Retrieves an entity using the given filter arguments."""
        stmt = sqlalchemy.select(self.entity).filter_by(**kwargs)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
