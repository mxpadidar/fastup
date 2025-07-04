import uvicorn
from fastapi import FastAPI

from fastup.core import settings

app = FastAPI(
    description="fastapi starter kit",
    title=settings.app_name,
    version=settings.app_version,
)


if __name__ == "__main__":
    uvicorn.run(
        "fastup.app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
