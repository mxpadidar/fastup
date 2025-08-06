import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
)

from fastup.adapters.database import Database


@pytest.fixture
def db_url() -> str:
    return "sqlite+aiosqlite:///:memory:"


def test_second_initialization_raises(db_url: str) -> None:
    _ = Database(db_url)
    with pytest.raises(RuntimeError):
        Database(db_url)


def test_engine_is_initialized(db_url: str) -> None:
    db = Database(db_url)
    engine = db.engine
    assert isinstance(engine, AsyncEngine)


def test_sessionmaker_is_initialized(db_url: str) -> None:
    db = Database(db_url)
    sm = db.sessionmaker
    assert isinstance(sm, async_sessionmaker)


def test_url_property(db_url: str) -> None:
    db = Database(db_url)
    assert db.url == db_url


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the singleton between tests."""
    Database._instance = None
    Database._initialized = False
