import abc

from app.domain.base import Repository
from app.domain.entities import User


class UserRepo(Repository[User], abc.ABC):
    """Repository interface for User entities."""

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        :param email: The email address of the user.
        :return: The user with the specified email address, or None if not found.
        """
        raise NotImplementedError
