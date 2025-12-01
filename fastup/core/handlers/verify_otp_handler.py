import datetime
import logging

from fastup.core.bus import register_command
from fastup.core.commands import VerifyOtpCommand
from fastup.core.config import Config
from fastup.core.entities import Otp
from fastup.core.enums import OtpStatus
from fastup.core.exceptions import AccessDeniedExc, AttemptLimitReached, NotFoundExc
from fastup.core.services import HashService
from fastup.core.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


@register_command(VerifyOtpCommand)
async def handle_verify_otp(
    cmd: VerifyOtpCommand,
    config: Config,
    uow: UnitOfWork,
    hmac_hasher: HashService,
) -> Otp:
    """Handle OTP verification requests.

    :param cmd: Command containing the OTP identifier, code, and requesting IP address.
    :param config: Application configuration for OTP validation rules.
    :param uow: Unit of work for database access and locking.
    :param hmac_hasher: Hasher for comparing OTP codes.
    :returns: The consumed OTP entity.
    :raises AccessDeniedExc: For missing, expired, invalid, or exhausted OTPs
                        to avoid leaking any authentication state from the API.
    """
    async with uow:
        try:
            otp = await uow.otps.get_for_update(
                id=cmd.otp_id, status=OtpStatus.SENT, ipaddr=cmd.ipaddr
            )
        except NotFoundExc as exc:
            logger.debug(f"OTP {cmd.otp_id} not found or not in SENT status")
            raise AccessDeniedExc("Otp is invalid or expired") from exc

        if otp.attempts >= config.otp_max_attempts:
            logger.debug(f"OTP {otp.id} exceeded maximum verification attempts")
            raise AttemptLimitReached

        if otp.is_expired:
            logger.debug(f"OTP {otp.id} has expired at {otp.expires_at}")
            raise AccessDeniedExc("Otp is invalid or expired")

        if not hmac_hasher.verify(cmd.code, otp.otp_hash):
            logger.debug(f"OTP {otp.id} verification failed for code {cmd.code}")
            otp.attempts = otp.attempts + 1
            md = otp.metadata.copy()
            md[f"attempt[{otp.attempts}]"] = {
                "tried_code": cmd.code,
                "tried_at": datetime.datetime.now(datetime.UTC).isoformat(),
            }
            otp.metadata = md
            await uow.commit()
            raise AccessDeniedExc("Otp is invalid or expired")

        otp.consumed_at = datetime.datetime.now(datetime.UTC)
        otp.status = OtpStatus.CONSUMED
        await uow.commit()

        return otp
