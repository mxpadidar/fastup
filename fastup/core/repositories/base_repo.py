import abc

from fastup.core import exceptions


class Repository[T](abc.ABC):
    """Generic repository interface for domain entities."""

    async def get(self, **kwargs) -> T | None:
        """Gets an entity by the given filter arguments.

        :return: The entity or None if not found.
        :raises InternalExc: If called without any filter arguments.
        """
        if not kwargs:
            raise exceptions.InternalExc("get must be called with at least one filter.")
        return await self._get(**kwargs)

    async def get_or_raise(self, **kwargs) -> T:
        """
        Gets an entity or raises NotFoundExc if it does not exist.

        :return: The entity.
        :raises InternalExc: If called without any filter arguments.
        :raises NotFoundExc: If the entity is not found.
        """
        entity = await self.get(**kwargs)
        if entity is None:
            raise exceptions.NotFoundExc("The requested entity was not found.")
        return entity

    @abc.abstractmethod
    async def add(self, entity: T) -> None:
        """Adds a new entity to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, entity: T) -> None:
        """Deletes an entity from the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    async def refresh(self, entity: T) -> None:
        """Refreshes an entity's state from the database."""
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, **kwargs) -> T | None:
        """Internal implementation for retrieving an entity."""
        raise NotImplementedError
