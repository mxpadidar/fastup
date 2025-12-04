import asyncio
import logging
import warnings
from typing import AsyncGenerator, Callable

import httpx
import pytest
from redis.asyncio.client import Redis
from sqlalchemy import exc as sa_exc
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import clear_mappers

from fastup.api import app, deps
from fastup.core import bus, repositories, services, unit_of_work
from fastup.core.config import Config
from fastup.infra import (
    db,
    hash_services,
    local_sms_service,
    orm_mapper,
    pydantic_config,
    pyjwt_service,
    redis_client,
    redis_publisher,
    snowflake_idgen,
    sql_repositories,
    sql_unit_of_work,
)

warnings.filterwarnings("ignore", category=sa_exc.SAWarning)


@pytest.fixture
async def async_client(
    bus_provider: Callable, redis_provider: Callable
) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provides an async HTTP client for testing FastAPI endpoints."""
    app.app.dependency_overrides[deps.get_bus] = bus_provider
    app.app.dependency_overrides[redis_client.redis_client_provider] = redis_provider
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app.app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Session-scoped engine bound to an in-memory SQLite DB."""
    orm_mapper.start_orm_mapper()
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(db.mapper_registry.metadata.create_all)
    yield engine
    clear_mappers()
    await engine.dispose()


@pytest.fixture
async def db_conn(db_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    """Open a per-test DB connection inside a transaction.
    Roll back after the test to reset state."""
    async with db_engine.connect() as conn:
        trans = await conn.begin()
        try:
            yield conn
        finally:
            if trans.is_active:
                await trans.rollback()  # Rollback if not already rolled back


@pytest.fixture
def sessionmaker(db_conn: AsyncConnection) -> async_sessionmaker[AsyncSession]:
    """Return a sessionmaker bound to the per-test connection."""
    return async_sessionmaker(bind=db_conn, expire_on_commit=False, autoflush=False)


@pytest.fixture
async def db_session(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Provide an AsyncSession using the shared test transaction."""
    async with sessionmaker() as session:
        yield session


@pytest.fixture
def uow(sessionmaker: async_sessionmaker[AsyncSession]) -> unit_of_work.UnitOfWork:
    """Provides a SQL-based Unit of Work instance for testing database operations."""
    return sql_unit_of_work.SQLUnitOfwWork(session_factory=sessionmaker)


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
    return hash_services.HMACHasher(key=b"asdf")


@pytest.fixture
def user_repo(db_session: AsyncSession) -> repositories.UserRepo:
    """Provides a UserSQLRepo instance with an active session."""
    return sql_repositories.UserSQLRepo(db_session)


@pytest.fixture(scope="session")
def config() -> Config:
    return pydantic_config.get_config()  # type: ignore


@pytest.fixture(scope="session")
def sms_service() -> services.SMSService:
    """Provides a local SMS service instance for testing."""
    return local_sms_service.LocalSMSService()


@pytest.fixture
def bus_provider(
    config: Config,
    uow: unit_of_work.UnitOfWork,
    idgen: services.IDGenerator,
    hmac_hasher: services.HashService,
    argon2_hasher: services.HashService,
    sms_service: services.SMSService,
    publisher: services.Publisher,
) -> Callable[[], bus.MessageBus]:
    """Provides a bus factory for overriding the default bus in tests."""
    queue = asyncio.Queue()
    deps = {
        "config": config,
        "uow": uow,
        "idgen": idgen,
        "hmac_hasher": hmac_hasher,
        "argon2_hasher": argon2_hasher,
        "sms_service": sms_service,
        "event_queue": queue,
        "publisher": publisher,
    }
    msgbus = bus.MessageBus(
        event_handlers={
            ev: [bus.inject_dependencies(h, deps) for h in handlers]
            for ev, handlers in bus.EVENT_HANDLERS.items()
        },
        command_handlers={
            cmd: bus.inject_dependencies(h, deps)
            for cmd, h in bus.COMMAND_HANDLERS.items()
        },
        queue=queue,
    )

    def get_bus_override() -> bus.MessageBus:
        return msgbus

    return get_bus_override


@pytest.fixture(scope="session")
def jwt_service() -> pyjwt_service.PyJWTService:
    return pyjwt_service.PyJWTService(secret_key="test-secret-key")


@pytest.fixture(scope="session")
async def redis(
    config: pydantic_config.PydanticConfig,
) -> AsyncGenerator[Redis, None]:
    """Provide a Redis client for testing."""
    redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db + 1,
        decode_responses=True,
    )
    yield redis
    await redis.flushdb()
    await redis.aclose()


@pytest.fixture
def publisher(redis: Redis) -> services.Publisher:
    """Provide a RedisPublisher instance."""
    return redis_publisher.RedisPublisher(redis)


@pytest.fixture
def redis_provider(redis: Redis) -> Callable[[], Redis]:
    """Provides a Redis client provider for dependency injection in tests."""

    def get_redis_override() -> Redis:
        logging.getLogger("redis").info("Providing test Redis client")
        return redis

    return get_redis_override
