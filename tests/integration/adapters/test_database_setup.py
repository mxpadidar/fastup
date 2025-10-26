import sqlalchemy

from app import adapters


async def test_database_engine():
    async with adapters.db_engine.begin() as conn:
        query = sqlalchemy.text("SELECT 1")
        result = await conn.execute(query)
        assert result.scalar() == 1


async def test_session_factory():
    async with adapters.db_sessionmaker() as session:
        query = sqlalchemy.text("SELECT 1")
        result = await session.execute(query)
        assert result.scalar() == 1
