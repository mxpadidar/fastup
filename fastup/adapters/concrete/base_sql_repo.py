import abc
import datetime
import logging

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.ext.asyncio.session import AsyncSession

from fastup.domain.ports import AbstractRepo

logger = logging.getLogger(__name__)


class BaseSQLRepo[T](AbstractRepo[T], abc.ABC):
    """Abstract SQLAlchemy repository implementation.

    This class provides common SQL-based implementations for repository methods.
    Concrete repos should set the `ntt` property to the mapped entity class.

    :param session: AsyncSession instance used for DB operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    @abc.abstractmethod
    def ntt(self) -> type[T]:
        """The entity class mapped to the database.

        :return: The entity class/type.
        :raises NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError

    async def add(self, entity: T) -> T:
        """Add (attach) a new entity to the session.

        The entity will be persisted when the surrounding transaction/session is committed.

        :param entity: The entity to add.
        :return: The added entity (attached to the session).
        """
        self._session.add(entity)
        return entity

    async def refresh(self, entity: T) -> T:
        """Refresh an entity from the database.

        :param entity: The entity to refresh.
        :return: The refreshed entity.
        """
        await self._session.refresh(entity)
        return entity

    async def _get(self, **kwargs) -> T | None:
        """Get an entity by provided filters.

        :param kwargs: Filter kwargs forwarded to filter_by (e.g. id=1).
        :return: The entity or None if not found.
        :raises ValueError: If no filters provided.
        """
        stmt = sqlalchemy.select(self.ntt).filter_by(**kwargs)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _delete(self, entity: T, soft: bool = False) -> None:
        """Delete or soft-delete an entity.

        :param entity: The entity to delete.
        :param soft: When True, perform a soft-delete by setting `deleted_at` if supported.
        :return: None
        :raises AttributeError: If soft delete is requested but entity does not support it.
        """
        if not soft:
            return await self._session.delete(entity)
        # will be raised AttributeError if entity has no deleted_at attribute
        entity.deleted_at = datetime.datetime.now(tz=datetime.timezone.utc)  # type: ignore[attr-defined]
