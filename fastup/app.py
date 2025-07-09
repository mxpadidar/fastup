import uvicorn
from fastapi import FastAPI

from fastup.infra import config

app = FastAPI(title=config.app_title, version=config.app_version)


def main() -> None:
    """main entry point for the fastapi application."""

    uvicorn.run(
        "fastup.app:app",
        host=config.server_host,
        port=config.server_port,
        reload=config.debug,
        log_level=config.log_level.lower(),
    )


if __name__ == "__main__":
    main()
