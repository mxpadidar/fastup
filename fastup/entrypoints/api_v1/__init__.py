from fastapi import APIRouter

from .routes import auth_routes, meta_routes

router = APIRouter(prefix="/api/v1/fastup")

router.include_router(meta_routes.router)
router.include_router(auth_routes.auth_router)
