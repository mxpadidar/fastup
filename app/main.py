import logging
import logging.config

import uvicorn
from fastapi import FastAPI

from app.config import APP_CONFIG, LOG_CONFIG, SERVER_CONFIG
from app.entrypoint import routes

app = FastAPI(title=APP_CONFIG["title"], version=APP_CONFIG["version"])

app.include_router(routes.router)


def main() -> None:
    """Application entry point."""

    logging.config.dictConfig(LOG_CONFIG)

    uvicorn.run(
        "app.main:app",
        host=SERVER_CONFIG["host"],
        port=SERVER_CONFIG["port"],
        reload=SERVER_CONFIG["debug"],
        log_config=LOG_CONFIG,
    )


if __name__ == "__main__":
    main()
