import pytest

from fastup.domain.resolvers import resolve_str_env


def test_returns_env_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_VAR", "hello")
    assert resolve_str_env("MY_VAR") == "hello"
    monkeypatch.delenv("MY_VAR", raising=False)


def test_returns_fallback_when_env_not_set() -> None:
    assert resolve_str_env("UNSET_VAR", fallback="default") == "default"


def test_raises_error_when_env_not_set_and_no_fallback() -> None:
    with pytest.raises(ValueError):
        resolve_str_env("UNSET_VAR")
