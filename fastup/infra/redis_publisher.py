import json
import logging

from redis.asyncio.client import Redis

from fastup.core import enums

logger = logging.getLogger(__name__)


class RedisPublisher:
    def __init__(self, client: Redis) -> None:
        """Initialize the RedisPublisher with a Redis client."""
        self._redis = client

    async def publish(self, type: enums.EventType, payload: dict) -> None:
        msg = json.dumps(payload)
        subs = await self._redis.publish(type.value, msg)
        if subs == 0:
            logger.warning(f"No subscribers for event {type=}")

        logger.debug(f"Published event {type=} to {subs} subscribers.")
