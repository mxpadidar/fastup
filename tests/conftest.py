import pytest
from fastapi.testclient import TestClient

from fastup.app import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """fixture to create a testclient for the fastapi app."""
    return TestClient(app)
