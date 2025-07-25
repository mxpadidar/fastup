import pathlib
import tempfile

import pytest

from fastup.adapters.utils.toml_parser import parse_toml_file
from fastup.domain.errors import FileParseErr


def test_parse_valid_toml():
    content = b"""
    [tool]
    name = "my-app"
    version = "1.0.0"
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_path = pathlib.Path(tmp.name)

    data = parse_toml_file(tmp_path)
    assert data["tool"]["name"] == "my-app"
    assert data["tool"]["version"] == "1.0.0"


def test_parse_invalid_toml_raises_file_parse_err():
    content = b"""
    [tool
    name = "bad"
    """  # Invalid TOML syntax
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_path = pathlib.Path(tmp.name)

    with pytest.raises(FileParseErr):
        parse_toml_file(tmp_path)


def test_missing_file_raises_file_parse_err():
    path = pathlib.Path("/non/existent/path/config.toml")
    with pytest.raises(FileParseErr):
        parse_toml_file(path)


def test_unreadable_file_raises_file_parse_err(monkeypatch):
    """simulate oserror when trying to open the file."""

    path = pathlib.Path(__file__)  # any valid file path

    def mock_open(*args, **kwargs):
        raise OSError

    monkeypatch.setattr(pathlib.Path, "open", mock_open)

    with pytest.raises(FileParseErr):
        parse_toml_file(path)
