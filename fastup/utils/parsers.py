import pathlib
import tomllib

from fastup.core import errors


def parse_toml(path: pathlib.Path) -> dict:
    """
    parse a toml file to dict.

    raise FileDoesNotExistErr if file does not exists.
    """
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        raise errors.FileDoesNotExistErr(path)
