import logging

from app.config import settings

log_level = logging.DEBUG if settings.DEBUG else logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(settings.APP_NAME)


def main() -> None:
    """Application entry point."""
    logger.info(f"Starting {settings.APP_NAME} application...")


if __name__ == "__main__":
    main()
