from fastup.core.bus import register_command
from fastup.core.commands import LoginCommand
from fastup.core.entities import User
from fastup.core.exceptions import AuthFailedExc
from fastup.core.services import HashService
from fastup.core.unit_of_work import UnitOfWork


@register_command(LoginCommand)
async def handle_authentication(
    cmd: LoginCommand, uow: UnitOfWork, arog2_hasher: HashService
) -> User:
    async with uow:
        user = await uow.users.get_by_phone(cmd.phone)
        if user is None:
            raise AuthFailedExc
        if not arog2_hasher.verify(cmd.password, user.pwdhash):
            raise AuthFailedExc

        return user
