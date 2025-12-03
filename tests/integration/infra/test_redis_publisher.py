import json

import pytest
from redis.asyncio.client import Redis

from fastup.core.enums import EventType
from fastup.infra.redis_publisher import RedisPublisher


async def test_publish_and_receive(publisher: RedisPublisher, redis: Redis):
    """Integration test: publish a message and verify subscriber receives it."""
    test_message = {"event": "test", "data": "hello"}

    # Subscribe to the channel
    pubsub = redis.pubsub()
    await pubsub.subscribe(EventType.NOTIFICATION)

    # Publish the message
    await publisher.publish(EventType.NOTIFICATION, test_message)

    # Wait for the message to arrive
    async for msg in pubsub.listen():
        if msg["type"] == "message":
            received = json.loads(msg["data"])
            assert received == test_message
            break

    # Cleanup
    await pubsub.unsubscribe(EventType.NOTIFICATION)
    await pubsub.aclose()


@pytest.mark.asyncio
async def test_publish_warns_no_subscribers(publisher: RedisPublisher, caplog):
    """Verify that publishing to a channel with no subscribers logs a warning."""
    test_channel = EventType.NOTIFICATION
    test_message = {"event": "no_subscriber"}

    caplog.set_level("WARNING")
    await publisher.publish(test_channel, test_message)

    assert any("No subscribers" in r.message for r in caplog.records)
