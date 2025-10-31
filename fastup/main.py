import logging
import logging.config

from fastup import config


def main() -> None:
    """Application entry point."""

    logging.config.dictConfig(config.LOG_CONFIG)
    logging.getLogger("main").info("Application starting...")


if __name__ == "__main__":
    main()
