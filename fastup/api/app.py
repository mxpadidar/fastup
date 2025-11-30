import logging
import typing
from contextlib import asynccontextmanager

import fastapi
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import clear_mappers

from fastup.bootstrap import bootstrap
from fastup.core.exceptions import BaseExc
from fastup.infra.pydantic_config import get_config

from .v1.exc_handlers import core_exception_handler, http_validation_exception_handler
from .v1.routes import router

logger = logging.getLogger(__name__)

config = get_config()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncGenerator[None, None]:
    """Manage application lifespan events."""
    try:
        app.state.bus = bootstrap()
        yield

    except RuntimeError as e:
        logger.error(f"Application failed to start: {e}")
        raise e

    finally:
        clear_mappers()


app = fastapi.FastAPI(
    lifespan=lifespan, title=config.app_name, version=config.version, debug=config.debug
)


app.include_router(router, prefix="/api/v1/fastup")

app.add_exception_handler(BaseExc, core_exception_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, http_validation_exception_handler)  # type: ignore
