from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from fastup import config
from fastup.adapters import database

from .api_v1 import router


@asynccontextmanager
async def lifespan(*args) -> AsyncGenerator[None, None]:  # pragma: no cover
    """Handle app startup and shutdown."""
    try:
        database.start_orm_mapper()
        yield
    finally:
        await database.async_engine.dispose()


app = FastAPI(
    title=config.APP["name"], version=config.APP["version"], lifespan=lifespan
)

app.include_router(router)
