from fastapi import APIRouter
from fastup.core.settings import version


router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/version")
async def get_version():
    return {"version": version}
