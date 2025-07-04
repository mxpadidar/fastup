import os
import pathlib
import tempfile
from typing import Generator

import pytest

from fastup.core import envlib
from fastup.core.errors import NotFoundErr, ValidationErr


@pytest.fixture
def tempenv() -> Generator[pathlib.Path, None, None]:
    """Create a temporary environment file for testing."""
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write("TEST_STR=hello\n")
        tmp.write("TEST_INT=42\n")
        tmp.write("TEST_BOOL=True\n")
        tmp_path = pathlib.Path(tmp.name)

    yield tmp_path

    tmp_path.unlink(missing_ok=True)


def test_loadenv_sets_environment_variables_correctly(tempenv: pathlib.Path) -> None:
    envlib.loadenv(tempenv)
    assert os.getenv("TEST_STR") == "hello"
    assert os.getenv("TEST_INT") == "42"
    assert os.getenv("TEST_BOOL") == "True"


def test_loadenv_raises_not_found_error_when_file_missing() -> None:
    missing_path = pathlib.Path("/some/nonexistent/file.env")
    with pytest.raises(NotFoundErr):
        envlib.loadenv(missing_path)


def test_getenv_returns_existing_string_variable_as_str() -> None:
    result = envlib.getenv("TEST_STR", "fallback")
    assert isinstance(result, str)
    assert result == "hello"


def test_getenv_returns_fallback_string_when_key_missing() -> None:
    result = envlib.getenv("MISSING_STR", "fallback")
    assert isinstance(result, str)
    assert result == "fallback"


def test_getenv_casts_existing_int_variable_correctly() -> None:
    os.environ["TEST_INT"] = "42"
    result = envlib.getenv("TEST_INT", 0)
    assert isinstance(result, int)
    assert result == 42


def test_getenv_returns_fallback_int_when_key_missing() -> None:
    result = envlib.getenv("MISSING_INT", 0)
    assert isinstance(result, int)
    assert result == 0


def test_getenv_raises_validation_error_for_invalid_int_cast() -> None:
    os.environ["TEST_INT_INVALID"] = "not_an_int"
    with pytest.raises(ValidationErr):
        envlib.getenv("TEST_INT_INVALID", 123)


def test_getenv_casts_true_string_to_boolean() -> None:
    os.environ["TEST_BOOL"] = "True"
    result = envlib.getenv("TEST_BOOL", False)
    assert result is True


def test_getenv_casts_false_string_to_boolean() -> None:
    os.environ["TEST_BOOL_FALSE"] = "false"
    result = envlib.getenv("TEST_BOOL_FALSE", True)
    assert result is False


def test_getenv_raises_validation_error_on_invalid_bool_cast() -> None:
    os.environ["TEST_BOOL_INVALID"] = "maybe"
    with pytest.raises(ValidationErr):
        envlib.getenv("TEST_BOOL_INVALID", True)


def test_getenv_raises_validation_error_when_key_missing_and_no_fallback() -> None:
    with pytest.raises(ValidationErr):
        envlib.getenv("MISSING_KEY", None)


def test_getenv_raises_validation_error_on_none_fallback() -> None:
    with pytest.raises(ValidationErr):
        envlib.getenv("MISSING_OPTIONAL", None)
