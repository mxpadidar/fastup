import logging

from app.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


def main() -> None:
    """Application entry point."""

    logger.info("Application started")


if __name__ == "__main__":
    main()
