import fastapi

from fastup.config import get_config

from .v1.routes import router

config = get_config()


app = fastapi.FastAPI(
    title=config.app_name,
    version=config.version,
    debug=config.debug,
)

app.include_router(router, prefix="/api/v1/fastup")
