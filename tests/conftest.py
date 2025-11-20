import typing

import httpx
import pytest

from fastup.api.app import app
from fastup.core import protocols
from fastup.infra.snowflake_idgen import SnowflakeIDGen


@pytest.fixture
async def async_client() -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an async HTTP client for testing FastAPI endpoints."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def idgen() -> protocols.IDGen:
    """Provide a Snowflake ID generator instance for testing."""
    return SnowflakeIDGen(epoch=1609459200000, node_id=1, worker_id=1)
