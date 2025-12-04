import asyncio
import logging
from typing import AsyncGenerator

from fastapi import HTTPException
from redis.asyncio import RedisError
from redis.asyncio.client import Redis

from fastup.core.enums import EventType

logger = logging.getLogger(__name__)


async def stream_notifications(redis: Redis) -> AsyncGenerator[bytes, None]:
    """
    Stream Redis notification events in SSE format.

    Opens a pubsub subscription on the notifications channel and yields each
    message as a `data:` SSE event. Continues until `should_stop()` returns
    True or the task is cancelled.
    """
    logger.info("Opening Redis pubsub connection for notifications")

    pubsub = redis.pubsub()
    await pubsub.subscribe(EventType.NOTIFICATION)

    try:
        while True:
            message = await pubsub.get_message(
                timeout=1.0, ignore_subscribe_messages=True
            )

            if message is None:
                await asyncio.sleep(0.1)
                continue

            raw = message["data"]
            data = raw.decode() if isinstance(raw, bytes) else str(raw)
            event = "data: {data}\n\n".format(data=data)
            yield event.encode()

    except asyncio.CancelledError:
        logger.info("Notification stream cancelled (client disconnect?)")
        return

    except RedisError as exc:
        logger.error("Redis error in notification stream: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Notification service unavailable",
        )

    except Exception:
        logger.exception("Unexpected error in notification stream")
        raise HTTPException(
            status_code=500,
            detail="Unexpected error in notification stream",
        )

    finally:
        await pubsub.unsubscribe(EventType.NOTIFICATION)
        await pubsub.aclose()
        logger.info("Closed Redis pubsub connection for notifications")
