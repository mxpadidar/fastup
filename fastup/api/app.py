import fastapi

from .v1.routes import router

app = fastapi.FastAPI()

app.include_router(router, prefix="/api/v1/fastup")
