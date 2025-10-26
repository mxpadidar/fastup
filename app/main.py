import logging

import uvicorn
from fastapi import FastAPI

from app.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


app = FastAPI()


def main() -> None:
    logger.info(f"Starting {settings.APP_NAME} application...")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,
    )


if __name__ == "__main__":
    main()
