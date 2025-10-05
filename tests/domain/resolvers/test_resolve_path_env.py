import pathlib
import tempfile

import pytest

from fastup.domain.resolvers import resolve_path_env


def test_returns_path_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    temp_path = tempfile.gettempdir()
    monkeypatch.setenv("MY_PATH", temp_path)

    fallback = pathlib.Path("/should/not/be/used")
    result = resolve_path_env("MY_PATH", fallback)

    assert result == pathlib.Path(temp_path).resolve()


def test_returns_fallback_when_env_not_set(tmp_path: pathlib.Path) -> None:
    result = resolve_path_env("MY_PATH", tmp_path)

    assert result == tmp_path.resolve()


def test_returns_resolved_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """returns resolved absolute path when env var is relative path."""

    relative_path = "."
    monkeypatch.setenv("MY_PATH", relative_path)

    result = resolve_path_env("MY_PATH", pathlib.Path("/should/not/be/used"))

    assert result == pathlib.Path(relative_path).resolve()


def test_raises_if_env_path_does_not_exist(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_path = "/some/fake/path/that/does/not/exist"
    monkeypatch.setenv("MY_PATH", fake_path)

    with pytest.raises(FileNotFoundError):
        resolve_path_env("MY_PATH", pathlib.Path("/fallback"))


def test_raises_if_fallback_path_does_not_exist() -> None:
    fallback = pathlib.Path("/non/existent/fallback")

    with pytest.raises(FileNotFoundError):
        resolve_path_env("MY_PATH", fallback)
