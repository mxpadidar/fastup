import pathlib
import tempfile

import pytest

from app.config.parsers import parse_toml_file


def test_parse_toml_file_valid():
    """Test parsing a valid TOML file."""
    toml_content = """
    [app]
    name = "test-app"
    version = "1.0.0"
    debug = true

    [database]
    host = "localhost"
    port = 5432
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(toml_content)
        temp_path = pathlib.Path(f.name)

    try:
        result = parse_toml_file(temp_path)

        assert result["app"]["name"] == "test-app"
        assert result["app"]["version"] == "1.0.0"
        assert result["app"]["debug"] is True
        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432
    finally:
        temp_path.unlink()


def test_parse_toml_file_not_found():
    """Test parsing a non-existent TOML file."""
    non_existent_path = pathlib.Path("does_not_exist.toml")

    with pytest.raises(ValueError):
        parse_toml_file(non_existent_path)


def test_parse_toml_file_invalid_toml():
    """Test parsing an invalid TOML file."""
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


def test_parse_toml_file_empty():
    """Test parsing an empty TOML file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write("")
        temp_path = pathlib.Path(f.name)

    try:
        result = parse_toml_file(temp_path)
        assert result == {}
    finally:
        temp_path.unlink()
