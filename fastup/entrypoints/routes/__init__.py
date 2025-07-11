from fastapi.routing import APIRouter

from .metadata import router as metadata_router

router = APIRouter(prefix="/api/v1")

router.include_router(metadata_router, prefix="/metadata", tags=["metadata"])
