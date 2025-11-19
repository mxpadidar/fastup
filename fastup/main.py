import logging

import uvicorn


def main():
    """Main entry point for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s [%(name)s]",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting...")

    uvicorn.run(app="fastup.api.app:app", log_config=None, reload=True)


if __name__ == "__main__":
    main()
