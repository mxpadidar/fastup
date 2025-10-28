import typing

import httpx
import pytest

from app import adapters
from app.domain import protocols
from app.main import app


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
def password_service() -> protocols.PasswordService:
    return adapters.PwdlibPasswordService()
