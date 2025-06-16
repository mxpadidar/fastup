import fastapi


from fastup.api.routes import router as v1_router

app = fastapi.FastAPI()

app.include_router(v1_router, prefix="/api")
