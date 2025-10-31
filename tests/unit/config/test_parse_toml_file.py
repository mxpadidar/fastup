import pathlib
import tempfile
from typing import Generator

import pytest

from fastup.config.parsers import parse_toml_file


@pytest.fixture
def toml_file() -> Generator[pathlib.Path, None, None]:
    """Create a temporary TOML file with test configuration data."""

    toml_content = """
    [app]
    name = "test-app"
    version = "1.0.0"
    [database]
    host = "localhost"
    port = 5432
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(toml_content)
        temp_path = pathlib.Path(f.name)

    yield temp_path

    temp_path.unlink()


def test_parse_toml_valid_file(toml_file: pathlib.Path):
    result = parse_toml_file(toml_file)

    assert result["app"]["name"] == "test-app"
    assert result["app"]["version"] == "1.0.0"
    assert result["database"]["host"] == "localhost"
    assert result["database"]["port"] == 5432


def test_parse_toml_nonexistent_file():
    non_existent_path = pathlib.Path("does_not_exist.toml")
    with pytest.raises(ValueError):
        parse_toml_file(non_existent_path)


def test_parse_toml_invalid_syntax():
    invalid_toml_content = """
    [app
    name = "invalid toml
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(invalid_toml_content)
        temp_path = pathlib.Path(f.name)

    try:
        with pytest.raises(ValueError):
            parse_toml_file(temp_path)
    finally:
        temp_path.unlink()


def test_parse_toml_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write("")
        temp_path = pathlib.Path(f.name)

    try:
        result = parse_toml_file(temp_path)
        assert result == {}
    finally:
        temp_path.unlink()
