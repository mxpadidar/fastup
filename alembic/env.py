import asyncio
import logging
import logging.config

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from fastup import config
from fastup.adapters import database

logging.config.dictConfig(config.LOG_CONFIG)

target_metadata = database.mapper_registry.metadata


def do_migrations(connection: Connection) -> None:
    """Run Alembic migrations using a given database connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and execute migrations within an async context."""

    connectable = create_async_engine(
        config.DATABASE["url"],
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_migrations)

    await connectable.dispose()


def run_migrations() -> None:
    """Run database migrations in online (connected) mode."""
    asyncio.run(run_async_migrations())


run_migrations()
