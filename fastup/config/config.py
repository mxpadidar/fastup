import pathlib

from .parsers import parse_toml_file
from .types import AppConf, ServerConf

root_dir = pathlib.Path(__file__).parent.parent.parent

try:
    confile = parse_toml_file(root_dir / "confile.toml")
except ValueError as e:  # pragma: no cover
    raise RuntimeError(f"Error parsing config file: {e}")


try:
    LOG_CONFIG = parse_toml_file(root_dir / "logging.toml")
except ValueError as e:  # pragma: no cover
    raise RuntimeError(f"Error parsing logging configuration file: {e}")


APP: AppConf = confile["app"]

SERVER: ServerConf = confile["server"]
