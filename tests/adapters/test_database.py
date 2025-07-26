import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from fastup.adapters import settings
from fastup.adapters.database import get_engine, get_sessionmaker


@pytest.mark.asyncio
async def test_engine_can_connect() -> None:
    """test if the engine can connect to the database."""
    try:
        engine = get_engine(
            settings.DB_URL,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
        )
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except SQLAlchemyError as e:
        pytest.fail(f"database connection failed: {e}")


@pytest.mark.asyncio
async def test_async_session_can_connect() -> None:
    """test if asyncsessionmaker can create a working session."""
    try:
        engine = get_engine(settings.DB_URL)
        sessionmaker = get_sessionmaker(engine)
        async with sessionmaker() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except SQLAlchemyError as e:
        pytest.fail(f"async session connection failed: {e}")
