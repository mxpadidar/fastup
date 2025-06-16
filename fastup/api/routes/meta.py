from fastapi import APIRouter

from fastup.core import settings

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/health")
async def check_health():
    return {"health": True}


@router.get("/app")
async def get_app_details():
    return {
        "name": settings.name,
        "version": settings.version,
    }
