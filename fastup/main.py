import uvicorn
from fastapi import FastAPI

from fastup.adapters import settings
from fastup.entrypoints.routes import router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(router)


def main() -> None:
    """main entry point for the fastapi application."""
    uvicorn.run(
        "fastup.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG,
        log_config=settings.LOG_CONFIG,
    ) # pragma: no cover


if __name__ == "__main__":
    main()  # pragma: no cover
