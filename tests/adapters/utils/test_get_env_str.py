import pytest

from fastup.adapters.utils import get_env_str


def test_returns_env_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_VAR", "hello")
    assert get_env_str("MY_VAR") == "hello"
    monkeypatch.delenv("MY_VAR", raising=False)


def test_returns_fallback_when_env_not_set() -> None:
    assert get_env_str("UNSET_VAR", fallback="default") == "default"


def test_raises_error_when_env_not_set_and_no_fallback() -> None:
    with pytest.raises(ValueError):
        get_env_str("UNSET_VAR")
