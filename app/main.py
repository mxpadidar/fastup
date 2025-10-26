import logging

import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.entrypoint import routes

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(routes.router)


def main() -> None:
    """Application entry point."""

    logging.basicConfig(level=settings.LOG_LEVEL)

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,
    )


if __name__ == "__main__":
    main()
