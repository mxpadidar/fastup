import abc
import logging
import typing

from fastup.core import exceptions, repositories

logger = logging.getLogger(__name__)


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
        :raises ConflictExc: If a conflict occurs during commit.
        :raises InternalExc: If any unexpected error occurs during commit.
        """
        if not self.is_ready:
            raise exceptions.UnitOfWorkContextExc
        try:
            await self._commit()
        except exceptions.ConflictExc:
            raise
        except Exception as exc:
            await self.rollback()
            logger.exception("Internal error during UoW commit: %s", exc)
            raise exceptions.InternalExc(
                "An internal error occurred during commit.",
                extra={"original_exception": str(exc)},
            )

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
        """Commit the current transaction.

        :raises ConflictExc: If a conflict occurs during commit.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError
