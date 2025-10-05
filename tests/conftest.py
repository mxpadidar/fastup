import pytest
from fastapi.testclient import TestClient

from fastup.main import app


@pytest.fixture(scope="session")
def client():
    """fixture to create a test client for the fastapi application."""

    with TestClient(app) as test_client:
        yield test_client
