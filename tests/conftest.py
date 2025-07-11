import pytest
from fastapi.testclient import TestClient

from fastup.main import app


@pytest.fixture(scope="session")
def client():
    """Fixture to create a test client for the FastAPI application."""

    with TestClient(app) as test_client:
        yield test_client
