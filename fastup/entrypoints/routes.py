import logging

from fastapi.routing import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/fastup/v1")

@router.get("/health", tags=["meta"])
async def health_check(
):
    """health check endpoint to verify the service is running."""
    logger.info("health check endpoint called")
    return {"status": "ok"}
