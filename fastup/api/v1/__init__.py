from fastapi import APIRouter


from .meta import router as meta_router

router = APIRouter()

router.include_router(meta_router)
