from fastapi import APIRouter

from .routes import meta_routes

router = APIRouter(prefix="/api/v1/fastup")

router.include_router(meta_routes.router)
