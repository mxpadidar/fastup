import typing
from contextlib import asynccontextmanager

import fastapi
from fastapi.exceptions import RequestValidationError

from fastup.core.exceptions import BaseExc
from fastup.infra.orm_mapper import start_orm_mapper
from fastup.infra.pydantic_config import get_config

from .v1.exc_handlers import core_exception_handler, http_validation_exception_handler
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

app.add_exception_handler(BaseExc, core_exception_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, http_validation_exception_handler)  # type: ignore
