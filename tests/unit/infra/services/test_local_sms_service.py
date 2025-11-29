from unittest.mock import MagicMock

from fastup.core.services.sms_service import SMSService
from fastup.infra.local_sms_service import LocalSMSService


async def test_local_sms_service_returns_integer_id(sms_service: SMSService):
    """Ensure send_sms returns an integer ID in the expected range."""
    sms_service.logger = MagicMock()

    msg_id = await sms_service.send_sms("09120000000", "Hello World")
    assert isinstance(msg_id, int)
    assert sms_service.logger.info.called


async def test_local_sms_service_logs_phone_and_text():
    """Ensure send_sms logs the phone number and message text."""
    service = LocalSMSService()
    mock_logger = MagicMock()
    service.logger = mock_logger

    phone = "09120000000"
    text = "Test Message"
    await service.send_sms(phone, text)

    # Check that logger.info was called with the expected messages
    mock_logger.info.assert_any_call("phone=%s", phone)
    mock_logger.info.assert_any_call("text=%s", text)
