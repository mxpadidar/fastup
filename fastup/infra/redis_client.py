import functools

from redis.asyncio.client import Redis

from .pydantic_config import get_config

_config = get_config()


@functools.cache
def redis_client_provider() -> Redis:
    """Provides a Redis client instance based on the application configuration."""
    return Redis(
        host=_config.redis_host,
        port=_config.redis_port,
        db=_config.redis_db,
        decode_responses=True,
    )
