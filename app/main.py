import logging

import uvicorn

from app.config import settings

log_level = logging.DEBUG if settings.DEBUG else logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(settings.APP_NAME)


def main() -> None:
    """Start the FastAPI application using uvicorn server."""
    logger.info(f"Starting {settings.APP_NAME} application...")
    uvicorn.run(
        "app.entrypoint.server:server",
        host="127.0.0.1",
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
