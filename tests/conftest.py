import datetime
import typing

import httpx
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastup.api.app import app
from fastup.core import repositories, services
from fastup.core.unit_of_work import UnitOfWork
from fastup.infra import sql_repositories
from fastup.infra.db import mapper_registry
from fastup.infra.hash_services import Argon2PasswordHasher, HMACHasher
from fastup.infra.orm_mapper import start_orm_mapper
from fastup.infra.snowflake_idgen import SnowflakeIDGenerator
from fastup.infra.sql_unit_of_work import SQLUnitOfwWork


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an async HTTP client for testing FastAPI endpoints."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def db_engine() -> typing.AsyncGenerator[AsyncEngine, None]:
    """Creates a new in-memory SQLite async engine for the test session."""
    yield create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)


@pytest.fixture(scope="session", autouse=True)
async def setup_db(db_engine: AsyncEngine) -> typing.AsyncGenerator[None, None]:
    """Sets up the database schema for the test session."""
    async with db_engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    start_orm_mapper()
    yield


@pytest.fixture(scope="session")
def sessionmaker(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Provides a session factory for creating new async sessions."""
    return async_sessionmaker(bind=db_engine, expire_on_commit=False)


@pytest.fixture
async def db_session(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> typing.AsyncGenerator[AsyncSession, None]:
    """Provides a new, transaction-scoped session for a test."""
    async with sessionmaker() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def uow(sessionmaker: async_sessionmaker[AsyncSession]) -> UnitOfWork:
    """Provide a SQL-based Unit of Work instance for testing database operations."""
    return SQLUnitOfwWork(sessionmaker)


@pytest.fixture(scope="session")
async def idgen() -> services.IDGenerator:
    """Provide a Snowflake ID generator instance for testing."""
    epoch = datetime.datetime.now().timestamp() * 1000
    return SnowflakeIDGenerator(epoch=int(epoch), node_id=1, worker_id=1)


@pytest.fixture(scope="session")
def argon2_hasher() -> Argon2PasswordHasher:
    """Provides an instance of the Argon2 password hasher."""
    return Argon2PasswordHasher()


@pytest.fixture(scope="session")
def hmac_hasher() -> HMACHasher:
    """Provides an instance of the HMAC hasher with the application secret key."""
    return HMACHasher(key=b"asdf")


@pytest.fixture
async def user_repo(db_session: AsyncSession) -> repositories.UserRepo:
    """Provides a UserSQLRepo instance with an active session."""
    return sql_repositories.UserSQLRepo(db_session)
