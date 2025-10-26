import logging
import logging.config
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app import adapters
from app.config import settings
from app.entrypoint.routes import router


@asynccontextmanager
async def lifespan(*args):  # pragma: no cover
    """Manage application lifespan events.

    Handles startup and shutdown tasks:
    - Creates database tables on startup
    - Initializes ORM mappings
    - Disposes database connections on shutdown

    :param args: FastAPI application instance (unused).
    """
    async with adapters.db_engine.begin() as conn:
        await conn.run_sync(adapters.db_registry.metadata.create_all)
    adapters.start_orm_mappings()
    yield
    await adapters.db_engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(router)


def main() -> None:
    """Run the FastAPI application with uvicorn server.

    Configures logging and starts the uvicorn ASGI server
    with settings from application configuration.
    """
    logging.config.dictConfig(settings.LOG_CONFIG)
    logging.getLogger(__name__).info("Starting application")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=settings.LOG_CONFIG,
    )


if __name__ == "__main__":
    main()
