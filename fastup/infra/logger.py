import logging

from fastup.infra import config


def setup_logger() -> None:
    """
    Set up the logger for the application.
    """
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
