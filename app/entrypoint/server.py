from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapters import database
from app.config import settings

from .routes import router


@asynccontextmanager
async def lifespan(*args):  # pragma: no cover
    await database.init_db(database.mapper_registry.metadata)
    database.start_mappers()
    yield
    await database.async_engine.dispose()


server = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


server.include_router(router)
