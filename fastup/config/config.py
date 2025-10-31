import pathlib

from .parsers import parse_toml_file
from .types import AppConf

root_dir = pathlib.Path(__file__).parent.parent.parent

try:
    confile = parse_toml_file(root_dir / "confile.toml")
except ValueError as e:  # pragma: no cover
    raise RuntimeError(f"Error parsing config file: {e}")

APP: AppConf = confile["app"]
