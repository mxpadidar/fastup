from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastup.core import settings
from fastup.core.logger import get_logger

logger = get_logger("database")

url = "{driver}://{user}:{password}@{host}:{port}/{database}".format(
    driver="postgresql+asyncpg",
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)


def get_engine() -> AsyncEngine:
    return create_async_engine(
        url,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_timeout=settings.db_pool_timeout,
    )


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
