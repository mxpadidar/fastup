import logging

import uvicorn

from app.config import settings

logger = logging.getLogger(settings.APP_NAME)


def main() -> None:
    """Start the FastAPI application using uvicorn server."""
    logger.info(f"Starting {settings.APP_NAME} application...")
    uvicorn.run(
        "app.entrypoint.server:server",
        host="127.0.0.1",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=settings.LOG_CONFIG,
    )


if __name__ == "__main__":
    main()
