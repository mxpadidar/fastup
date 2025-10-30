import pathlib

from .parsers import parse_toml_file
from .types import AppConfig, DBConfig, ServerConfig

root_dir = pathlib.Path(__file__).parent.parent.parent

try:
    confile = parse_toml_file(root_dir / "confile.toml")
except ValueError as e:
    raise RuntimeError(f"Error parsing config file: {e}")

try:
    LOG_CONFIG = parse_toml_file(root_dir / "logging.toml")
except ValueError as e:
    raise RuntimeError(f"Error parsing logging configuration file: {e}")

APP_CONFIG: AppConfig = confile["app"]

SERVER_CONFIG: ServerConfig = confile["server"]

DB_CONFIG: DBConfig = {
    "url": confile["database"]["url"],
    "echo": confile["database"]["echo"],
    "pool_size": 5,
    "pool_timeout": 30,
    "max_overflow": 10,
}
