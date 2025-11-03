import abc
import logging

from fastup.domain import exceptions

logger = logging.getLogger(__name__)


class AbstractRepo[T](abc.ABC):
    """Repository interface for domain entities.

    Provides common repository operations and a convenience helper.
    """

    async def get(self, **kwargs) -> T | None:
        """Get an entity from the repository.

        :param kwargs: The keyword arguments to filter the entity.
        :return: The entity or None if not found.
        """
        if not kwargs:
            logger.error("get operation called without filters")
            return None

        try:
            return await self._get(**kwargs)
        except Exception as e:
            logger.error(f"Error during get operation: {e}")
            return None

    async def delete(self, entity: T, soft: bool = False) -> None:
        """Delete an entity from the repository.

        :param entity: The entity to delete.
        :param soft: Whether to perform a soft delete (default: False).
        :return: None
        """
        print(f"Deleting entity {entity} with soft={soft}")
        try:
            return await self._delete(entity, soft=soft)
        except AttributeError as e:
            logger.error("Attempted soft delete on entity without deleted_at attribute")
            raise exceptions.LogicalExc(
                message="entity does not support soft delete"
            ) from e

    async def get_or_raise_not_found(self, **kwargs) -> T:
        """Get an entity from the repository or raise a NotFound exception.

        :param kwargs: The keyword arguments used to filter the entity (e.g. id=..., email=...).
        :return: The entity when found.
        :raises NotFoundExc: If the entity does not exist.
        """
        ntt = await self.get(**kwargs)

        if ntt is None:
            raise exceptions.NotFoundExc(message="Resource not found")

        return ntt

    @abc.abstractmethod
    async def add(self, entity: T) -> T:
        """Add a new entity to the repository.

        :param entity: The entity to add.
        :return: The added entity.
        """
        ...

    @abc.abstractmethod
    async def refresh(self, entity: T) -> T:
        """Refresh an entity in the repository (reload from DB).

        :param entity: The entity to refresh.
        :return: The refreshed entity.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, **kwargs) -> T | None:
        """Internal get method to be implemented by subclasses."""
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self, entity: T, soft: bool = False) -> None:
        """Internal delete method to be implemented by subclasses.

        :raises AttributeError: If soft delete is requested but not supported.
        """
        raise NotImplementedError
