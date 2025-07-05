from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastup.adapters import orm
from fastup.app import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """fixture to create a testclient for the fastapi app."""
    return TestClient(app)


def pytest_configure(config):
    """Configure pytest to use asyncio mode."""

    # This is necessary to ensure that pytest-asyncio works correctly
    config.option.asyncio_mode = "auto"


@pytest.fixture(scope="session")
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    """Create a test database engine and initialize schema."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(orm.mapper_registry.metadata.create_all)
        orm.start_mappers()
        yield conn

    await engine.dispose()


@pytest.fixture
async def async_session(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_maker = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session_maker() as session:
        yield session
