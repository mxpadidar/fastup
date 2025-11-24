from fastup.core.commands import IssueSignupOtpCommand
from fastup.core.entities import Otp
from fastup.core.enums import OtpIntent
from fastup.core.exceptions import ConflictExc
from fastup.core.protocols import CoreConf
from fastup.core.services import HashService, IDGenerator
from fastup.core.unit_of_work import UnitOfWork
from fastup.core.utils import generate_otp, get_utc_now


async def handle_issue_signup_otp(
    cmd: IssueSignupOtpCommand,
    config: CoreConf,
    uow: UnitOfWork,
    idgen: IDGenerator,
    hmach_hasher: HashService,
) -> Otp:
    """Handle signup OTP issuance.

    :param cmd: Command containing phone number and IP address.
    :param config: Domain configuration for OTP settings.
    :param uow: Unit of Work for database transactions.
    :param idgen: ID generator service.
    :param hmach_hasher: Hash service for OTP code.
    :returns: The created OTP entity.
    :raises ConflictExc: If phone number is already registered.
    """
    async with uow:
        user = await uow.users.get_by_phone(phone=cmd.phone)
        if user is not None:
            # This logic can be expanded to handle different user statuses.
            raise ConflictExc(
                "A user with this phone number already exists.",
                extra={
                    "status": user.status,
                    "created_at": user.created_at.isoformat(),
                },
            )

        otp_id = await idgen.next_id()
        otp_code = generate_otp(config.otp_length)
        otp = Otp(
            id=otp_id,
            phone=cmd.phone,
            intent=OtpIntent.SIGN_UP,
            otp_hash=hmach_hasher.hash(otp_code),
            attempts=0,
            ipaddr=cmd.ipaddr,
            expires_at=get_utc_now() + config.otp_lifetime,
        )

        await uow.otps.add(otp)
        await uow.commit()

        return otp
