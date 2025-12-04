import asyncio
import json
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from redis.asyncio.client import Redis
from redis.exceptions import RedisError

from fastup.api.v1.views import stream_notifications
from fastup.core.enums import EventType
from fastup.core.services import Publisher


def parse_sse_message(sse_msg: str) -> dict:
    """Parse an SSE-formatted message string into a dictionary."""
    if not sse_msg.startswith("data: ") or not sse_msg.endswith("\n\n"):
        raise ValueError("Invalid SSE message format")
    data_str = sse_msg[6:-2]  # Strip "data: " prefix and "\n\n" suffix
    return json.loads(data_str)


async def test_stream_notifications_yields_messages(redis: Redis, publisher: Publisher):
    """Test generator receives and yields published messages."""

    async def reader(gen):
        return await gen.__anext__()

    streamer = stream_notifications(redis)
    reader_task = asyncio.create_task(reader(streamer))
    await asyncio.sleep(0.05)  # wait for subscription

    payload = {"msg": "hello-world"}
    await publisher.publish(EventType.NOTIFICATION, payload)
    sse_msg = await asyncio.wait_for(reader_task, timeout=2.0)

    data = parse_sse_message(sse_msg.decode("utf-8"))
    assert data == payload
    await streamer.aclose()


async def test_stream_notifications_no_messages(redis: Redis):
    """Test generator times out when no messages are published."""
    streamer = stream_notifications(redis)
    with pytest.raises(StopAsyncIteration):
        await asyncio.wait_for(streamer.__anext__(), timeout=0.2)

    await streamer.aclose()


async def test_stream_notifications_redis_error(
    monkeypatch: pytest.MonkeyPatch, redis: Redis
):
    """Test that Redis errors raise HTTPException with 503."""

    pubsub = redis.pubsub()
    await pubsub.subscribe(EventType.NOTIFICATION)

    fake_get_message = AsyncMock(side_effect=RedisError("connection lost"))
    monkeypatch.setattr(pubsub, "get_message", fake_get_message)
    monkeypatch.setattr(redis, "pubsub", lambda: pubsub)

    streamer = stream_notifications(redis)

    with pytest.raises(HTTPException) as exc:
        await streamer.__anext__()
    assert exc.value.status_code == 503

    await streamer.aclose()


async def test_stream_notifications_unexpected_exception(
    monkeypatch: pytest.MonkeyPatch, redis: Redis
):
    """Test that generic exceptions propagate as-is."""

    pubsub = redis.pubsub()
    await pubsub.subscribe(EventType.NOTIFICATION)

    fake_get_message = AsyncMock(side_effect=ValueError("oops"))
    monkeypatch.setattr(pubsub, "get_message", fake_get_message)
    monkeypatch.setattr(redis, "pubsub", lambda: pubsub)

    streamer = stream_notifications(redis)

    with pytest.raises(HTTPException) as exc:
        await streamer.__anext__()

    assert exc.value.status_code == 500

    await streamer.aclose()
