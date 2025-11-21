import abc

from fastup.core.entities import User

from .base_repo import Repository


class UserRepo(Repository[User], abc.ABC):
    """Repository for managing User entities."""

    pass
