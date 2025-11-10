import typing

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from fastup.adapters import concrete, database
from fastup.domain import ports
from fastup.entrypoints.app import app


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def async_engine() -> typing.AsyncGenerator[AsyncEngine, None]:
    db_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    yield db_engine


@pytest.fixture(scope="session", autouse=True)
async def setup_db(
    async_engine: AsyncEngine,
) -> typing.AsyncGenerator[None, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(database.mapper_registry.metadata.create_all)
    database.start_orm_mapper()
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(database.mapper_registry.metadata.drop_all)
    await async_engine.dispose()


@pytest.fixture(scope="session")
def session_factory(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine, expire_on_commit=False)


@pytest.fixture
async def async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> typing.AsyncGenerator[AsyncSession, None]:
    async with session_factory() as db:
        yield db


@pytest.fixture
async def uow(session_factory: async_sessionmaker[AsyncSession]) -> ports.UnitOfWork:
    return concrete.SQLUoW(session_factory)


@pytest.fixture(scope="session")
def pwdlib_hasher() -> ports.Hasher:
    return concrete.PwdlibHasher()
