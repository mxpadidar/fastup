from fastapi.routing import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/health", tags=["meta"], status_code=200)
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}
