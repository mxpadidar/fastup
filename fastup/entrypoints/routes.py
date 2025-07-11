from fastapi.routing import APIRouter

router = APIRouter(prefix="/api/fastup/v1")


@router.get("/health", tags=["meta"])
async def health_check():
    """health check endpoint to verify the service is running."""
    return {"status": "ok"}
