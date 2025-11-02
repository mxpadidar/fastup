from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastup.adapters import database


@asynccontextmanager
async def app_lifespan(*args) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Manage application lifespan events.

    Handles startup and shutdown tasks:
    - Creates database tables
    - Initializes ORM mappings
    - Disposes database connections on shutdown
    """
    try:
        async with database.async_engine.begin() as conn:
            await conn.run_sync(database.mapper_registry.metadata.create_all)
        database.start_orm_mapper()
        yield
    finally:
        await database.async_engine.dispose()
