import os

import pytest

from app.config.resolvers import resolve_str_env


def test_resolve_str_env_from_env(monkeypatch):
    """Test resolving a string from an environment variable."""
    monkeypatch.setenv("TEST_ENV_VAR", "hello from env")
    result = resolve_str_env("TEST_ENV_VAR", fallback="fallback")
    assert result == "hello from env"


def test_resolve_str_env_from_fallback():
    """Test resolving a string from a fallback value."""
    result = resolve_str_env("NON_EXISTENT_VAR", fallback="hello from fallback")
    assert result == "hello from fallback"


def test_resolve_str_env_no_env_no_fallback():
    """Test that ValueError is raised when no env var or fallback is present."""
    # Ensure the env var is not set
    if os.getenv("NON_EXISTENT_VAR"):
        os.environ.pop("NON_EXISTENT_VAR")

    with pytest.raises(ValueError):
        resolve_str_env("NON_EXISTENT_VAR")


def test_resolve_str_env_empty_env_var(monkeypatch):
    """Test resolving an empty string from an environment variable."""
    monkeypatch.setenv("TEST_EMPTY_ENV_VAR", "")
    result = resolve_str_env("TEST_EMPTY_ENV_VAR", fallback="fallback")
    assert result == ""
