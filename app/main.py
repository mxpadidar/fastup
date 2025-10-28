import logging
import logging.config

import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.entrypoint.routes import router

app = FastAPI(
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
