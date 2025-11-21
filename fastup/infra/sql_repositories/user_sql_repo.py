import typing

from fastup.core.entities import User
from fastup.core.repositories import UserRepo

from .base_sql_repo import SQLRepository


class UserSQLRepo(SQLRepository[User], UserRepo):
    """SQLAlchemy-backed repository for User.

    This concrete repository binds the generic SQL repository implementation to
    the domain User entity.

    :param: Inherits constructor from AbstractSqlRepo(session: AsyncSession).
    """

    @property
    def entity(self) -> typing.Type:  # pragma: no cover
        return User
