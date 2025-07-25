from fastapi import Depends
from fastapi.routing import APIRouter

from fastup.domain.logger import LoggerFactory
from fastup.entrypoints.dependencies import provide_logger_factory

router = APIRouter()


@router.get("/health")
async def health_check(
    logger_factory: LoggerFactory = Depends(provide_logger_factory),
):
    """health check endpoint."""
    logger = logger_factory(__name__)
    await logger.info("health check endpoint called")
    return {"status": "ok"}
