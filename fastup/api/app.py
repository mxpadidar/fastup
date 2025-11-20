import typing
from contextlib import asynccontextmanager

import fastapi

from fastup.config import get_config
from fastup.infra.orm_mapper import start_orm_mapper

from .v1.routes import router

config = get_config()


@asynccontextmanager
async def lifespan(*args) -> typing.AsyncGenerator[None, None]:  # pragma: no cover
    """Manage application lifespan events."""
    try:
        start_orm_mapper()
        yield
    finally:
        pass


app = fastapi.FastAPI(
    lifespan=lifespan,
    title=config.app_name,
    version=config.version,
    debug=config.debug,
)


app.include_router(router, prefix="/api/v1/fastup")
