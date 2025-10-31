from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastup.config import DATABASE

async_engine = create_async_engine(
    DATABASE["url"],
    pool_size=DATABASE["pool_size"],
    pool_timeout=DATABASE["pool_timeout"],
    max_overflow=DATABASE["max_overflow"],
    echo=False,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
