from fastapi import Depends
from fastapi.routing import APIRouter

from fastup.domain.logger import LoggerFactory
from fastup.entrypoints.dependencies import provide_logger_factory

router = APIRouter(prefix="/api/fastup/v1")


@router.get("/health", tags=["meta"])
async def health_check(
    logger_factory: LoggerFactory = Depends(provide_logger_factory),
):
    """health check endpoint to verify the service is running."""
    logger = logger_factory("routes.health")
    await logger.info("health check endpoint called")
    return {"status": "ok"}
