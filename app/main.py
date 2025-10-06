import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s - %(name)s] %(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("fastup-main")


def main() -> None:
    """Application entry point."""
    logger.info("Hello, world!")


if __name__ == "__main__":
    main()
