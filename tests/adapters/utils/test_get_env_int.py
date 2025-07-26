import pytest

from fastup.adapters.utils import get_env_int


def test_returns_env_value_as_int(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MY_INT", "123")
    assert get_env_int("MY_INT") == 123
    monkeypatch.delenv("MY_INT", raising=False)


def test_returns_fallback_when_env_not_set() -> None:
    assert get_env_int("UNSET_INT", fallback=42) == 42


def test_raises_when_env_and_fallback_missing() -> None:
    with pytest.raises(ValueError):
        get_env_int("UNSET_INT")


def test_raises_when_env_value_not_int(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BAD_INT", "not-a-number")
    with pytest.raises(ValueError):
        get_env_int("BAD_INT")
    monkeypatch.delenv("BAD_INT", raising=False)
