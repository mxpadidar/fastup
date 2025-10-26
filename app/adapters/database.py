from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

db_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=False,
)

db_sessionmaker = async_sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
)
