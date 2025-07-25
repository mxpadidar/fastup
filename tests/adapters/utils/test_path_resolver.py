import pathlib
import tempfile

import pytest

from fastup.adapters.utils import resolve_path_from_env


def test_returns_path_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    temp_path = tempfile.gettempdir()
    monkeypatch.setenv("MY_PATH", temp_path)

    default = pathlib.Path("/default/path")
    result = resolve_path_from_env("MY_PATH", default)

    assert result == pathlib.Path(temp_path).resolve()

    # clean up the environment variable
    monkeypatch.delenv("MY_PATH", raising=False)


def test_returns_default_path_when_env_not_set() -> None:
    default = pathlib.Path("/default/path")
    result = resolve_path_from_env("MY_PATH", default)

    assert result == default.resolve()


def test_returns_resolved_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """test that the returned path is resolved to an absolute path."""

    relative_path = "./"
    monkeypatch.setenv("MY_PATH", relative_path)

    result = resolve_path_from_env("MY_PATH", pathlib.Path("/fallback"))

    assert result == pathlib.Path(relative_path).resolve()

    # clean up the environment variable
    monkeypatch.delenv("MY_PATH", raising=False)


def test_env_var_set_to_nonexistent_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """test that the function returns the path as is when
    the env var points to a non-existent path."""
    fake_path = "/some/fake/path/that/does/not/exist"

    monkeypatch.setenv("MY_PATH", fake_path)

    result = resolve_path_from_env("MY_PATH", pathlib.Path("/fallback"))

    assert result == pathlib.Path(fake_path).resolve()
