import datetime
import random
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastup.core import enums
from fastup.core.entities import Otp
from fastup.core.events import OtpIssuedEvent
from fastup.core.exceptions import SmsSendFailed
from fastup.core.handlers import handle_otp_issued_event
from fastup.core.services import HashService, SMSService
from fastup.core.unit_of_work import UnitOfWork
from fastup.infra.redis_publisher import RedisPublisher


class MockSMS(SMSService):
    """A mock SMS service for testing purposes."""

    deliveries: list[tuple[int, str]] = []  # msgid, phone

    async def send_sms(self, phone: str, text: str) -> int:
        message_id = random.randint(100, 999)
        self.deliveries.append((message_id, phone))
        return message_id


@pytest.fixture
async def event(
    db_session: AsyncSession, hmac_hasher: HashService
) -> AsyncGenerator[OtpIssuedEvent]:
    """Creates and yields an OtpIssuedEvent for testing;
    it also creates an otp record in the database for the event."""

    code = "1010"
    now = datetime.datetime.now(datetime.UTC)
    otp = Otp(
        id=100,
        phone="0912",
        intent=enums.OtpIntent.SIGN_UP,
        otp_hash=hmac_hasher.hash(code),
        ipaddr="localhost",
        expires_at=now + datetime.timedelta(minutes=1),
    )
    db_session.add(otp)
    await db_session.commit()
    yield OtpIssuedEvent(otp_id=otp.id, code=code)

    await db_session.delete(otp)
    await db_session.commit()


async def test_handle_otp_issued_event_sends_sms_and_updates_status(
    event: OtpIssuedEvent, uow: UnitOfWork
):
    """Verifies that the handler sends an SMS and updates the OTP status."""

    mock_sms = MockSMS()
    mock_publisher = MagicMock(spec=RedisPublisher)

    await handle_otp_issued_event(
        event=event, uow=uow, sms_service=mock_sms, publisher=mock_publisher
    )

    msgid, _ = mock_sms.deliveries.pop()

    async with uow:
        updated_otp = await uow.otps.get(event.otp_id)
        assert updated_otp is not None
        assert updated_otp.status == enums.OtpStatus.SENT
        assert "otp_sent_at" in updated_otp.metadata
        assert updated_otp.metadata["message_id"] == msgid


async def test_handle_otp_issued_event_logs_warning_when_otp_not_found(uow: UnitOfWork):
    """Verifies that the handler logs a warning and does not send SMS
    when the OTP record is not found."""

    mock_sms = MockSMS()
    event = OtpIssuedEvent(otp_id=999, code="123456")  # Non-existent OTP ID
    mock_publisher = MagicMock(spec=RedisPublisher)

    await handle_otp_issued_event(
        event=event, uow=uow, sms_service=mock_sms, publisher=mock_publisher
    )

    assert len(mock_sms.deliveries) == 0


async def test_handle_otp_issued_event_raises_exception_when_sms_send_fails(
    event: OtpIssuedEvent, uow: UnitOfWork
):
    """Verifies that the handler raises SmsSendFailed when SMS sending fails."""

    failing_sms = MagicMock(spec=SMSService)
    failing_sms.send_otp = AsyncMock(
        side_effect=SmsSendFailed("Failed to send SMS message.")
    )
    mock_publisher = MagicMock(spec=RedisPublisher)

    with pytest.raises(SmsSendFailed):
        await handle_otp_issued_event(
            event=event, uow=uow, sms_service=failing_sms, publisher=mock_publisher
        )


async def test_handle_otp_issued_event_publishes_sse(
    event: OtpIssuedEvent, uow: UnitOfWork
):
    """Verify that OTP handler sends SMS and publishes SSE message."""

    mock_sms = MockSMS()
    mock_publisher = AsyncMock(spec=RedisPublisher)

    await handle_otp_issued_event(
        event=event, uow=uow, sms_service=mock_sms, publisher=mock_publisher
    )

    assert mock_publisher.publish.await_count == 1
    call_args = mock_publisher.publish.call_args[1]  # kwargs
    assert call_args["type"] == enums.EventType.NOTIFICATION
    assert call_args["payload"]["event"] == "otp_sent"
