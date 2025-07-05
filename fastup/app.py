from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastup.adapters import orm
from fastup.core import settings
from fastup.core.logger import get_logger

logger = get_logger("app")


@asynccontextmanager
async def lifespan(*args, **kwargs):
    orm.start_mappers()
    yield
    logger.info("application shutdown")


app = FastAPI(
    lifespan=lifespan,
    description="fastapi starter kit",
    title=settings.app_name,
    version=settings.app_version,
)


if __name__ == "__main__":
    uvicorn.run(
        "fastup.app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
