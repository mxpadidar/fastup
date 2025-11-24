import typing

import sqlalchemy

from fastup.core.entities import User
from fastup.core.repositories import UserRepo

from .base_sql_repo import SQLRepository


class UserSQLRepo(SQLRepository[User], UserRepo):
    """SQLAlchemy-backed repository for User."""

    @property
    def entity_cls(self) -> typing.Type:  # pragma: no cover
        return User

    async def get_by_phone(self, phone: str, only_active: bool = True) -> User | None:
        """Retrieve a user by phone number, with an option to include deleted users."""
        stmt = sqlalchemy.select(self.entity_cls).where(self.entity_cls.phone == phone)
        if only_active:
            stmt = stmt.where(self.entity_cls.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
