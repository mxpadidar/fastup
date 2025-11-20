import abc


class Repository[T](abc.ABC):
    """Generic repository interface for domain entities."""

    async def get(self, id: int, **kwargs) -> T | None:
        """Retrieve an entity by ID with optional additional filters.

        :param id: The unique identifier of the entity.
        :param kwargs: Additional filter criteria (e.g., deleted_at=None).
        :returns: The entity if found, None otherwise.
        """
        raise NotImplementedError

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
