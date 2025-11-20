from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from fastup.config import settings

DB_URL = URL.create(
    "postgresql+asyncpg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_async_engine(
    DB_URL,
    pool_size=settings.db_pool_size,
    pool_timeout=settings.db_pool_timeout,
    max_overflow=settings.db_pool_max_overflow,
    echo=settings.db_echo_sql,
)

sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

mapper_registry = registry()
