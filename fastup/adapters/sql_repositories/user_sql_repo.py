from fastup.adapters.concrete import BaseSQLRepo
from fastup.domain.entities import User
from fastup.domain.repositories import UserRepo


class UserSQLRepo(BaseSQLRepo[User], UserRepo):
    """SQLAlchemy-backed repository for User.

    This concrete repository binds the generic SQL repository implementation to
    the domain User entity.

    :param: Inherits constructor from AbstractSqlRepo(session: AsyncSession).
    """

    @property
    def ntt(self) -> type[User]:  # pragma: no cover
        """Return the domain entity class mapped to the DB.

        :return: The User class used for ORM queries and mapping.
        """
        return User
