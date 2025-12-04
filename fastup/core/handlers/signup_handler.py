from fastup.core.bus import register_command
from fastup.core.commands import SignupCommand
from fastup.core.entities.user import User
from fastup.core.enums import OtpStatus
from fastup.core.exceptions import ConflictExc
from fastup.core.services import HashService
from fastup.core.services.id_generator import IDGenerator
from fastup.core.unit_of_work import UnitOfWork


@register_command(SignupCommand)
async def handle_signup(
    cmd: SignupCommand, uow: UnitOfWork, argon2_hasher: HashService, idgen: IDGenerator
) -> User:
    async with uow:
        otp = await uow.otps.get_for_update(
            id=cmd.otp_id, status=OtpStatus.CONSUMED, ipaddr=cmd.ipaddr
        )
        otp.status = OtpStatus.USED
        otp_md = otp.metadata.copy()
        otp_md["used_for_signup_ip"] = cmd.ipaddr
        otp.metadata = otp_md

        user_id = await idgen.next_id()

        user = User(
            id=user_id,
            phone=otp.phone,
            pwdhash=argon2_hasher.hash(cmd.password),
            sex=cmd.sex,
            fname=cmd.first_name,
            lname=cmd.last_name,
        )

        try:
            await uow.users.add(user)
            await uow.commit()
        except ConflictExc:
            raise ConflictExc("User with this phone number already exists")

        return user
