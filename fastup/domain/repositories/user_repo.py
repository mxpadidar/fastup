import abc

from fastup.domain import exceptions
from fastup.domain.entities import User
from fastup.domain.ports import AbstractRepo


class UserRepo(AbstractRepo[User], abc.ABC):
    """User-specific repository interface.

    Provides convenience helpers that raise a NotFoundExc with a clear message.

    Inherits AbstractRepo methods (get/add/delete/refresh).

    :param: User is the domain User entity type.
    """

    async def get_by_id_or_raise(self, id: int) -> User:
        """Get user by id or raise NotFoundExc.

        :param id: User id.
        :return: The found User.
        :raises exceptions.NotFoundExc: If user is not found.
        """
        try:
            return await self.get_or_raise_not_found(id=id, deleted_at=None)
        except exceptions.NotFoundExc:
            raise exceptions.NotFoundExc(message="User not found")

    async def get_by_email_or_raise(self, email: str) -> User:
        """Get user by email or raise NotFoundExc.

        :param email: User email.
        :return: The found User.
        :raises exceptions.NotFoundExc: If user is not found.
        """
        try:
            return await self.get_or_raise_not_found(email=email, deleted_at=None)
        except exceptions.NotFoundExc:
            raise exceptions.NotFoundExc(message="User not found")

    async def get_by_phone_or_raise(self, phone: str) -> User:
        """Get user by phone or raise NotFoundExc.

        :param phone: User phone (e.g. E.164).
        :return: The found User.
        :raises exceptions.NotFoundExc: If user is not found.
        """
        try:
            return await self.get_or_raise_not_found(phone=phone, deleted_at=None)
        except exceptions.NotFoundExc:
            raise exceptions.NotFoundExc(message="User not found")
