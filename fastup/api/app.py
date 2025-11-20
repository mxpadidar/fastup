import fastapi

from fastup.config import settings

from .v1.routes import router

app = fastapi.FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
)

app.include_router(router, prefix="/api/v1/fastup")
