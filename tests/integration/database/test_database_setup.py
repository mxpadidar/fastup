import sqlalchemy

from fastup.adapters import database


async def test_db_engine():
    async with database.async_engine.begin() as conn:
        query = sqlalchemy.text("SELECT 1")
        result = await conn.execute(query)
        assert result.scalar() == 1


async def test_db_session_factory():
    async with database.async_session_factory() as session:
        query = sqlalchemy.text("SELECT 1")
        result = await session.execute(query)
        assert result.scalar() == 1
