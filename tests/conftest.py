from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from fastup.adapters import settings
from fastup.adapters.builtin_logger import BuiltInLogger
from fastup.domain.logger import Logger, LoggerFactory
from fastup.main import app

engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")


@pytest.fixture(scope="session")
def client():
    """fixture to create a test client for the fastapi application."""

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def logger_factory() -> LoggerFactory:
    """fixture to create a logger factory for the fastapi application."""

    def factory(name: str, level: int | None = None) -> Logger:
        """Create a logger instance with the given name and level."""
        if level is not None:
            settings.LOG_CONFIG["root"]["level"] = level
        return BuiltInLogger(name=name, **settings.LOG_CONFIG)

    return factory


@pytest.fixture(scope="session")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """fixture to create a database engine for the fastapi application."""
    engine = create_async_engine(settings.DB_URL, echo=settings.DEBUG)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator:
    """fixture to create a database session for the fastapi application."""
    async with db_engine.begin() as conn:
        yield conn
    await db_engine.dispose()
