import random

from fastup.core.services import SMSService


class LocalSMSService(SMSService):
    """Local (development) implementation of SMSService.

    This implementation does not call any external provider. Instead it logs
    the message and returns a synthetic integer message id."""

    async def send_sms(self, phone: str, text: str) -> int:
        """Send an SMS by logging it and returning a synthetic message id.

        :param phone: Destination phone number.
        :param text: Message body to deliver.
        :return: Synthetic integer message id."""

        msg_id = random.randint(1000, 9999)
        self.logger.info(">" * 30)
        self.logger.info("phone=%s", phone)
        self.logger.info("text=%s", text)
        self.logger.info("<" * 30)
        return msg_id
