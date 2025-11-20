import pytest
import sqlalchemy
from sqlalchemy.exc import OperationalError

from fastup.infra import db


async def test_database_engine_can_establish_a_connection_and_execute_a_query():
    """
    Validates that the SQLAlchemy engine can successfully connect to the
    configured database and execute a basic query.

    Skips the test if the database is not available.
    """
    try:
        async with db.engine.begin() as conn:
            query = sqlalchemy.text("SELECT 1")
            result = await conn.execute(query)
            assert result.scalar() == 1

    except OperationalError:
        pytest.skip("Requires running PostgreSQL database (not available in tests).")


async def test_database_sessionmaker_can_create_a_session_and_execute_a_query():
    """
    Validates that the sessionmaker can create a new session that successfully
    connects to the configured database and executes a basic query.

    Skips the test if the database is not available.
    """
    try:
        async with db.sessionmaker() as session:
            query = sqlalchemy.text("SELECT 1")
            result = await session.execute(query)
            assert result.scalar() == 1
    except OperationalError:
        pytest.skip("Requires running PostgreSQL database (not available in tests).")
