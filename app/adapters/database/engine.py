from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import DB_CONFIG

async_engine = create_async_engine(
    DB_CONFIG["url"],
    pool_size=DB_CONFIG["pool_size"],
    pool_timeout=DB_CONFIG["pool_timeout"],
    max_overflow=DB_CONFIG["max_overflow"],
    echo=False,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
