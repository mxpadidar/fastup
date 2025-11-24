import typing

import httpx
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import clear_mappers

from fastup.api.app import app
from fastup.config import Config
from fastup.core import protocols, services, unit_of_work
from fastup.infra import (
    db,
    hash_services,
    orm_mapper,
    snowflake_idgen,
    sql_unit_of_work,
)


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an async HTTP client for testing FastAPI endpoints."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def db_engine() -> typing.AsyncGenerator[AsyncEngine, None]:
    """Session-scoped engine bound to an in-memory SQLite DB."""
    orm_mapper.start_orm_mapper()
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(db.mapper_registry.metadata.create_all)
    yield engine
    clear_mappers()
    await engine.dispose()


@pytest.fixture
async def db_conn(
    db_engine: AsyncEngine,
) -> typing.AsyncGenerator[AsyncConnection, None]:
    """Open a per-test DB connection inside a transaction.
    Roll back after the test to reset state."""
    async with db_engine.connect() as conn:
        trans = await conn.begin()
        try:
            yield conn
        finally:
            await trans.rollback()  # Rollback resets DB state for the next test


@pytest.fixture
def sessionmaker(db_conn: AsyncConnection) -> async_sessionmaker[AsyncSession]:
    """Return a sessionmaker bound to the per-test connection."""
    return async_sessionmaker(bind=db_conn, expire_on_commit=False, autoflush=False)


@pytest.fixture
async def db_session(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> typing.AsyncGenerator[AsyncSession, None]:
    """Provide an AsyncSession using the shared test transaction."""
    async with sessionmaker() as session:
        yield session


@pytest.fixture
def uow(sessionmaker: async_sessionmaker[AsyncSession]) -> unit_of_work.UnitOfWork:
    """Provide a SQL-based Unit of Work instance for testing database operations."""
    return sql_unit_of_work.SQLUnitOfwWork(sessionmaker)


@pytest.fixture(scope="session")
def idgen() -> services.IDGenerator:
    """Provide a Snowflake ID generator instance for testing."""
    return snowflake_idgen.SnowflakeIDGenerator()


@pytest.fixture(scope="session")
def argon2_hasher() -> services.HashService:
    """Provides an instance of the Argon2 password hasher."""
    return hash_services.Argon2PasswordHasher()


@pytest.fixture(scope="session")
def hmac_hasher() -> services.HashService:
    """Provides an instance of the HMAC hasher with the application secret key."""
    return hash_services.HMACHasher()


@pytest.fixture(scope="session")
def config() -> protocols.CoreConf:
    """Provides the application configuration for testing."""
    return Config()  # type: ignore
