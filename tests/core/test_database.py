import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from fastup.core.database import get_engine, get_sessionmaker


@pytest.mark.asyncio
async def test_engine_can_connect() -> None:
    """Test if the engine can connect to the database."""
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except SQLAlchemyError as e:
        pytest.fail(f"Database connection failed: {e}")


@pytest.mark.asyncio
async def test_async_session_can_connect() -> None:
    """Test if AsyncSessionMaker can create a working session."""
    try:
        sessionmaker = get_sessionmaker(get_engine())
        async with sessionmaker() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except SQLAlchemyError as e:
        pytest.fail(f"Async session connection failed: {e}")
