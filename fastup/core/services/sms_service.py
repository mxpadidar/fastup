import abc
import logging

from fastup.core.enums import OtpIntent
from fastup.core.exceptions import SmsSendFailed


class SMSService(abc.ABC):
    """Abstract base for SMS delivery implementations."""

    def __init__(self) -> None:
        """Initialize the SMS service with a logger factory."""

        self.logger = logging.getLogger(__name__)

    async def send_otp(self, *, phone: str, otp_code: str, intent: OtpIntent) -> int:
        """Send a one-time password (OTP) to a phone number.

        :param phone: Destination phone number (e.g. in E.164 format).
        :param otp_code: The one-time password code to deliver.
        :param intent: The intent/purpose of the OTP (used for message text).
        :return: Provider-specific integer result (e.g. message id).
        :raises SmsSendFailed: If the underlying send_sms call fails."""

        text = f"Your OTP code for {intent} is {otp_code}"
        try:
            result = await self.send_sms(phone, text)
        except Exception as exc:
            self.logger.error("Failed to send SMS to %s for intent=%s", phone, intent)
            raise SmsSendFailed("Failed to send SMS message.") from exc

        return result

    @abc.abstractmethod
    async def send_sms(self, phone: str, text: str) -> int:
        """Perform the actual SMS delivery.

        :param phone: Destination phone number.
        :param text: Message body to send.
        :return: Provider-specific integer result (for example a message id).
        :raises: Implementations may raise provider-specific exceptions on failure."""

        raise NotImplementedError
