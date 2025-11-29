from unittest.mock import AsyncMock

import pytest

from fastup.core.enums import OtpIntent
from fastup.core.exceptions import SmsSendFailed
from fastup.core.services.sms_service import SMSService


class MockSMS(SMSService):
    """Mock implementation of SMSService for testing."""

    def __init__(self) -> None:
        super().__init__()
        self.send_sms_mock = AsyncMock()

    async def send_sms(self, phone: str, text: str) -> int:
        return await self.send_sms_mock(phone, text)


@pytest.fixture
def mock_sms() -> MockSMS:
    return MockSMS()


async def test_send_otp_calls_send_sms_with_correct_text(mock_sms: MockSMS):
    """Test that send_otp calls send_sms with the correct message text."""
    mock_sms.send_sms_mock.return_value = 12345
    result = await mock_sms.send_otp(
        phone="+1234567890", otp_code="5678", intent=OtpIntent.SIGN_UP
    )
    assert result == 12345


async def test_send_otp_handles_send_sms_exception(mock_sms: MockSMS):
    """Test that send_otp raises SmsSendFailed when send_sms fails."""

    mock_sms.send_sms_mock.side_effect = Exception("SMS provider error")
    with pytest.raises(SmsSendFailed, match="Failed to send SMS message."):
        await mock_sms.send_otp(
            phone="+1234567890", otp_code="5678", intent=OtpIntent.SIGN_UP
        )
