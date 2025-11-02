from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastup.adapters import database


@asynccontextmanager
async def app_lifespan(*args) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Manage application lifespan events.

    Handles startup and shutdown tasks:
    - Initializes ORM mappings
    - Disposes database connections on shutdown
    """
    try:
        database.start_orm_mapper()
        yield
    finally:
        await database.async_engine.dispose()
