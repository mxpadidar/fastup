import abc
import typing

from app.domain import errors, protocols


class Repository[T: protocols.Entity](abc.ABC):
    """Base repository interface for domain entities."""

    @abc.abstractmethod
    async def add(self, ntt: T) -> T:
        """Add a new entity to the repository.

        :param ntt: The entity to add.
        :return: The added entity.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, ntt: T) -> None:
        """Delete an entity from the repository.

        :param ntt: The entity to delete.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def refresh(self, ntt: T) -> T:
        """Refresh an entity in the repository.

        :param ntt: The entity to refresh.
        :return: The refreshed entity.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id: int) -> T | None:
        """Get an entity by its ID.

        :param id: The entity ID.
        :return: The entity if found, None otherwise.
        """
        raise NotImplementedError

    async def get_or_raise(
        self, func: typing.Callable[..., typing.Awaitable[T | None]]
    ) -> T:
        """Get an entity by running the provided function or raise NotFoundError if None.

        :param func: A callable that returns an awaitable entity or None.
        :return: The entity.
        :raises NotFoundError: If the function returns None.
        """
        ntt = await func()
        if ntt is None:
            raise errors.NotFoundErr
        return ntt
