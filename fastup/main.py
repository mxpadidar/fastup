import logging

from fastup import config

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main() -> None:
    """Application entry point."""

    logger.info(f"{config.APP['name']} is starting...")


if __name__ == "__main__":
    main()
