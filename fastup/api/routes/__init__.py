from fastapi import APIRouter

from .meta import router as meta

router = APIRouter()

router.include_router(meta)
