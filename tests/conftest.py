from fastapi.testclient import TestClient
import pytest
from fastup.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Fixture to create a TestClient for the FastAPI app."""
    return TestClient(app)
