from fastapi.routing import APIRouter

from fastup.entrypoints.api_v1 import response_models

router = APIRouter(prefix="/meta")


@router.get(
    "/health",
    tags=["meta"],
    status_code=200,
    response_model=response_models.HealthResp,
)
async def health():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}
