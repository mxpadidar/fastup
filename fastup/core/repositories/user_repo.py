import abc

from fastup.core.entities import User

from .base_repo import Repository


class UserRepo(Repository[User], abc.ABC):
    """Repository for managing User entities."""

    @abc.abstractmethod
    async def get_by_phone(self, phone: str, only_active: bool = True) -> User | None:
        """Retrieve a user by phone number, with an option to include deleted users.

        By default, this method searches only for active users (where deleted_at is NULL).
        Setting `only_active` to False will bypass the soft-delete check and retrieve
        a user regardless of their status.

        :param phone: The phone number to search for.
        :param only_active: If True (default), only return active users.
                            If False, return any user matching the phone number.
        :returns: The user if found according to the filter, otherwise None.
        """
        raise NotImplementedError
