import logging

import uvicorn
from fastapi import FastAPI

from fastup.infra import config
from fastup.infra.settings import get_settings

logger = logging.getLogger(__name__)


def setup_logger() -> None:
    """
    Set up the logger for the application.
    """
    logging.basicConfig(
        level=config.log_level.upper(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure uvicorn loggers manually
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = True


app = FastAPI(title=config.app_title, version=config.app_version)


def main() -> None:
    """main entry point for the fastapi application."""

    setup_logger()

    logger.info(get_settings().model_dump_json(indent=2))

    uvicorn.run(
        "fastup.app:app",
        host=config.server_host,
        port=config.server_port,
        reload=config.debug,
        log_config=None,
    )


if __name__ == "__main__":
    main()
