import abc
import typing

from fastup.core import exceptions, repositories


class UnitOfWork(abc.ABC):
    """Base Unit of Work for managing database transactions."""

    users: repositories.UserRepo
    otps: repositories.OtpRepo

    async def __aenter__(self) -> typing.Self:
        """Enter the async context and return the UoW instance."""
        return self

    async def __aexit__(self, *args) -> None:
        """Exit the async context and rollback if not committed."""
        await self.rollback()

    async def commit(self) -> None:
        """Commit the current transaction.

        :raises UnitOfWorkContextExc: If the UoW is not ready.
        """
        if not self.is_ready:
            raise exceptions.UnitOfWorkContextExc
        await self._commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self._rollback()

    @property
    @abc.abstractmethod
    def is_ready(self) -> bool:
        """Check if the UoW is ready for use."""
        raise NotImplementedError

    @abc.abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError
