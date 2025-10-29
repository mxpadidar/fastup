from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app import adapters


@asynccontextmanager
async def app_lifespan(*args) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Manage application lifespan events.

    Handles startup and shutdown tasks:
    - Initializes ORM mappings
    - Disposes database connections on shutdown
    """
    try:
        adapters.start_orm_mappings()
        yield
    finally:
        await adapters.db_engine.dispose()
