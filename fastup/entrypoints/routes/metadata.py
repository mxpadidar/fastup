from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """health check endpoint."""
    return {"status": "ok"}
