from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)


def get_engine(
    url: str,
    pool_size: int = 5,
    pool_timeout: float = 30.0,
    max_overflow: int = 10,
) -> AsyncEngine:
    """create an asynchronous sqlalchemy engine."""
    print(f"{url=}, {pool_size=}, {max_overflow=}, {pool_timeout=}")
    return create_async_engine(
        url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        echo=False,  # Set to True for debugging
        future=True,  # Use the future API
    )


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
