import pytest
from fastapi.testclient import TestClient

from app.entrypoint.server import server


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(server)
