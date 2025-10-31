import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main() -> None:
    """Application entry point."""

    logger.info("FastUP is starting...")


if __name__ == "__main__":
    main()
