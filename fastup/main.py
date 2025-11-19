import logging

import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s [%(module)s]",
    datefmt="%H:%M:%S",
)


def main():
    """Main entry point for the application."""
    logger = logging.getLogger(__name__)
    logger.info("Starting Server...")

    uvicorn.run(app="fastup.api.app:app", log_config=None, reload=True)


if __name__ == "__main__":
    main()
