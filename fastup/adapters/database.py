from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastup.adapters.settings import (
    DB_MAX_OVERFLOW,
    DB_POOL_SIZE,
    DB_POOL_TIMEOUT,
    DB_URL,
)


def get_engine() -> AsyncEngine:
    return create_async_engine(
        DB_URL,
        pool_size=DB_POOL_SIZE,
        max_overflow=DB_MAX_OVERFLOW,
        pool_timeout=DB_POOL_TIMEOUT,
    )


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
