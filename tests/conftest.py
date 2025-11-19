import typing

import httpx
import pytest

from fastup.api.app import app


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an async HTTP client for testing FastAPI endpoints."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
