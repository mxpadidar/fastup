import logging

from app.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(f"Starting {settings.APP_NAME} application...")


if __name__ == "__main__":
    main()
