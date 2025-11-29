import datetime
import logging

from fastup.core.enums import OtpStatus
from fastup.core.events import OtpIssuedEvent
from fastup.core.exceptions import SmsSendFailed
from fastup.core.services import SMSService
from fastup.core.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


async def handle_otp_issued_event(
    event: OtpIssuedEvent, uow: UnitOfWork, sms_service: SMSService
) -> None:
    """Send signup OTP via SMS and record delivery metadata.

    Processes an OtpIssuedEvent by retrieving the corresponding OTP record,
    sending the OTP code via SMS using the provided SMS service, and updating
    the OTP status and metadata in the database.

    :param event: OtpIssuedEvent instance containing `otp_id` and `code`.
    :param uow: UnitOfWork used to load the OTP record and persist status/metadata.
    :param sms_service: SMSService implementation used to deliver the SMS.
    :raises SmsSendFailed: If the SMS sending fails.
    :raises Exception: Re-raises exceptions from the SMS provider or UoW"""

    logger.debug(f"Processing SignupOtpIssued event: otp_id={event.otp_id}")

    async with uow:
        otp = await uow.otps.get(event.otp_id)
        if otp is None:
            logger.warning(
                f"OTP record not found for otp_id={event.otp_id}; skipping SMS send"
            )
            return

        try:
            message_id = await sms_service.send_otp(
                phone=otp.phone, otp_code=event.code, intent=otp.intent
            )
        except SmsSendFailed as e:
            logger.error(
                f"Failed to send OTP SMS for otp_id={event.otp_id} phone={otp.phone}; exc={e}"
            )
            raise

        otp.status = OtpStatus.SENT
        md = otp.metadata.copy()
        md["otp_sent_at"] = datetime.datetime.now(datetime.UTC).isoformat()
        md["message_id"] = message_id
        otp.metadata = md
        await uow.commit()

        logger.info(
            f"OTP sent and status updated for otp_id={event.otp_id} phone={otp.phone}"
        )
