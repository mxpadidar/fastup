import fastapi


from fastup.api.v1 import router as v1_router

app = fastapi.FastAPI()

app.include_router(v1_router, prefix="/api/v1")
