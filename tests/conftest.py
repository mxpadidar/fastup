import typing

import httpx
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import adapters
from app.domain import protocols
from app.main import app

db_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
db_sessionmaker = async_sessionmaker(db_engine, expire_on_commit=False)



@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
def password_service() -> protocols.PasswordService:
    return adapters.PwdlibPasswordService()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database() -> typing.AsyncGenerator[None, None]:
    async with db_engine.begin() as conn:
        await conn.run_sync(adapters.db_registry.metadata.create_all)
    adapters.start_orm_mappings()
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(adapters.db_registry.metadata.drop_all)
    await db_engine.dispose()


@pytest.fixture
async def db_session() -> typing.AsyncGenerator[AsyncSession, None]:
    """Provide a per-test AsyncSession."""
    async with db_sessionmaker() as session:
        yield session
