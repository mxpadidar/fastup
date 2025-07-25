import pytest
from fastapi.testclient import TestClient

from fastup.adapters.builtin_logger import BuiltInLogger
from fastup.adapters.settings import LOG_CONFIG
from fastup.domain.logger import Logger, LoggerFactory
from fastup.main import app


@pytest.fixture(scope="session")
def client():
    """fixture to create a test client for the fastapi application."""

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def logger_factory() -> LoggerFactory:
    """fixture to create a logger factory for the fastapi application."""

    def factory(name: str, level: int | None = None) -> Logger:
        """Create a logger instance with the given name and level."""
        if level is not None:
            LOG_CONFIG["root"]["level"] = level
        return BuiltInLogger(name=name, **LOG_CONFIG)

    return factory
