import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=False,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def init_db(metadata: sqlalchemy.MetaData) -> None:  # pragma: no cover
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
