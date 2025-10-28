import logging
import typing

from app.domain import errors
from app.domain.base import UnitOfWork
from app.domain.entities import User
from app.domain.protocols import PasswordService

logger = logging.getLogger(__name__)


class SignupData(typing.TypedDict):
    email: str
    password: str


async def handle_create_user(
    uow: UnitOfWork, pw_service: PasswordService, **data: typing.Unpack[SignupData]
) -> User:
    """Handle user creation (signup) process.

    :param uow: Unit of work for database operations.
    :param pw_service: Password service.
    :param data: Signup data containing email and password.
    :return: The created User entity.
    :raises ConflictError: If a user with the email already exists.
    """
    async with uow:
        user_exists = await uow.users.get_by_email(data["email"])
        if user_exists:
            logger.debug("User already exists", extra={"email": data["email"]})
            raise errors.ConflictErr(
                "User already exists", extra={"email": data["email"]}
            )

        user = User(email=data["email"], is_active=False)
        user.set_password(data["password"], pw_service)
        await uow.users.add(user)
        await uow.commit()

        await uow.users.refresh(user)
        return user
