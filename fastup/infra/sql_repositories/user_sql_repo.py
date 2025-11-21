import typing

from fastup.core.entities import User
from fastup.core.repositories import UserRepo

from .base_sql_repo import SQLRepository


class UserSQLRepo(SQLRepository[User], UserRepo):
    """SQLAlchemy-backed repository for User."""

    @property
    def entity_cls(self) -> typing.Type:  # pragma: no cover
        return User
