from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from .pydantic_config import get_config

config = get_config()

DB_URL = URL.create(
    "postgresql+asyncpg",
    username=config.db_user,
    password=config.db_password,
    host=config.db_host,
    port=config.db_port,
    database=config.db_name,
)

engine = create_async_engine(
    DB_URL,
    pool_size=config.db_pool_size,
    pool_timeout=config.db_pool_timeout,
    max_overflow=config.db_pool_max_overflow,
    echo=config.db_echo_sql,
)

sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

mapper_registry = registry()
