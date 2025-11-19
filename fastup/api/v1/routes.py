from fastapi.routing import APIRouter

from fastup.api.v1 import resp_models

router = APIRouter()


@router.get("/health", status_code=200, response_model=resp_models.HealthResp)
async def health():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}
