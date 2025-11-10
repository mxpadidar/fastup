import pathlib
import tempfile
from typing import Generator

import pytest

from fastup.config.parsers import parse_yaml_file


@pytest.fixture
def yaml_file() -> Generator[pathlib.Path, None, None]:
    """Create a temporary YAML file with test configuration data."""

    yaml_content = """
    app:
        name: test-app
        version: "1.0.0"
    database:
        host: localhost
        port: 5432
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        temp_path = pathlib.Path(f.name)

    yield temp_path

    temp_path.unlink()


def test_parse_yaml_valid_file(yaml_file: pathlib.Path):
    result = parse_yaml_file(yaml_file)

    assert result["app"]["name"] == "test-app"
    assert result["app"]["version"] == "1.0.0"
    assert result["database"]["host"] == "localhost"
    assert result["database"]["port"] == 5432


def test_parse_yaml_nonexistent_file():
    non_existent_path = pathlib.Path("does_not_exist.yaml")
    with pytest.raises(ValueError):
        parse_yaml_file(non_existent_path)


def test_parse_yaml_invalid_syntax():
    invalid_yaml_content = """
    app:
        name: "invalid
    """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(invalid_yaml_content)
        temp_path = pathlib.Path(f.name)

    try:
        with pytest.raises(ValueError):
            parse_yaml_file(temp_path)
    finally:
        temp_path.unlink()


def test_parse_yaml_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("")
        temp_path = pathlib.Path(f.name)

    try:
        result = parse_yaml_file(temp_path)
        assert result == {}
    finally:
        temp_path.unlink()
