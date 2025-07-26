import pathlib

from fastup.adapters import utils
from fastup.domain.errors import FileParseErr

BASE_DIR = utils.resolve_path_from_env(
    "FASTUP_BASE_DIR", pathlib.Path(__file__).parent.parent.parent
)

try:
    CONFDICT = utils.parse_toml_file(
        utils.resolve_path_from_env(
            "FASTUP_CONFIG_PATH", BASE_DIR / "configs" / "dev.toml"
        )
    )
except FileParseErr as e:
    raise RuntimeError("failed to parse configuration file") from e

DEBUG = CONFDICT["app"]["debug"]

APP_NAME = CONFDICT["app"]["name"]

APP_VERSION = CONFDICT["app"]["version"]

try:
    LOG_CONFIG = utils.parse_toml_file(
        utils.resolve_path_from_env(
            "FASTUP_LOG_CONF_PATH", BASE_DIR / "configs" / "logging.toml"
        )
    )
except FileParseErr as e:
    raise RuntimeError("failed to parse logging configuration file") from e
DB_URL = "{driver}://{user}:{password}@{host}:{port}/{database}".format(
    driver="postgresql+asyncpg",
    user=utils.get_env_str("POSTGRES_USER"),
    password=utils.get_env_str("POSTGRES_PASSWORD"),
    host=utils.get_env_str("POSTGRES_HOST"),
    port=utils.get_env_int("POSTGRES_PORT"),
    database=utils.get_env_str("POSTGRES_DATABASE_NAME"),
)

DB_POOL_SIZE = CONFDICT["database"]["pool_size"]
DB_MAX_OVERFLOW = CONFDICT["database"]["max_overflow"]
DB_POOL_TIMEOUT = CONFDICT["database"]["pool_timeout"]
