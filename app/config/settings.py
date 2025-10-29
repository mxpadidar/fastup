import pathlib

from .parsers import parse_duration, parse_toml_file

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent

try:
    confile = parse_toml_file(ROOT_DIR / "confile.toml")
except ValueError as e:
    raise RuntimeError(f"Error parsing config file: {e}")

try:
    LOG_CONFIG = parse_toml_file(ROOT_DIR / "logging.toml")
except ValueError as e:
    raise RuntimeError(f"Error parsing logging configuration file: {e}")


APP_NAME = confile["app"]["name"]
APP_VERSION = confile["app"]["version"]
DEBUG = confile["app"]["debug"]
PORT = confile["app"]["port"]

DATABASE_URL = confile["database"]["url"]
DATABASE_POOL_SIZE = confile["database"].get("pool_size", 5)
DATABASE_POOL_TIMEOUT = confile["database"].get("pool_timeout", 5)
DATABASE_MAX_OVERFLOW = confile["database"].get("max_overflow", 10)

TOKEN_SECRET = confile["token"]["secret"]
TOKEN_ISSUER = confile["token"]["issuer"]
TOKEN_AUDIENCE = confile["token"]["audience"]
TOKEN_ACCESS_EXP = parse_duration(confile["token"]["access_exp"])
TOKEN_REFRESH_EXP = parse_duration(confile["token"]["refresh_exp"])
