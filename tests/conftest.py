import pytest
from fastapi.testclient import TestClient

from fastup.app import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Fixture to create a TestClient for the FastAPI app."""
    return TestClient(app)
