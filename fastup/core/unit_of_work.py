import abc
import logging
import typing

from fastup.core import exceptions, repositories

logger = logging.getLogger(__name__)


class UnitOfWork(abc.ABC):
    """Base Unit of Work for managing database transactions.

    repositories should be initialized in implementation.
    """

    users: repositories.UserRepo

    async def __aenter__(self) -> typing.Self:
        """Enter the async context and return the UoW instance."""
        return self

    async def __aexit__(self, *args) -> None:
        """Exit the async context and rollback if not committed."""
        await self.rollback()

    async def commit(self) -> None:
        """Commit the current transaction.

        :raises UoWIsNotAvailable: If the UoW is not ready.
        """
        if not self.is_ready:
            logger.error("UnitOfWork is using out of context")
            raise exceptions.UnitOfWorkContextExc
        await self._commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self._rollback()

    @property
    @abc.abstractmethod
    def is_ready(self) -> bool:
        """Check if the UoW is ready for use.

        :return: True if the UoW is ready, False otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError
