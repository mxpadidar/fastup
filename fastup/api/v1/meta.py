from fastapi import APIRouter
from sqlalchemy import text

from fastup.core.database import engine
from fastup.core.settings import version

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/app/version")
async def get_app_version():
    return {"version": version}


@router.get("/db/version")
async def get_db_version():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        db_version = result.scalar()
    return {"db_version": db_version}
