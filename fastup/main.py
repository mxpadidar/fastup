import logging
import logging.config

import uvicorn
from fastapi import FastAPI

from fastup import config
from fastup.entrypoints import api_v1

app = FastAPI(
    title=config.APP["name"],
    version=config.APP["version"],
)

app.include_router(api_v1.router)


def main() -> None:
    """Application entry point."""

    logging.config.dictConfig(config.LOG_CONFIG)
    logging.getLogger("main").info("Application starting...")

    uvicorn.run(
        "fastup.main:app",
        host=config.SERVER["host"],
        port=config.SERVER["port"],
        reload=config.SERVER["debug"],
        log_config=None,
    )


if __name__ == "__main__":
    main()
