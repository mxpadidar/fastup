import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from fastup.core.database import engine


def test_database_connection():
    """Test if the database connection can be established."""

    qs = text("SELECT 1")

    try:
        with engine.connect() as conn:
            result = conn.execute(qs)
            assert result.scalar() == 1
    except OperationalError:
        pytest.fail("Could not connect to the database")
