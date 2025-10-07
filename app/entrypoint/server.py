from fastapi import FastAPI

from app.config import settings

from .routes import router

server = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

server.include_router(router)
