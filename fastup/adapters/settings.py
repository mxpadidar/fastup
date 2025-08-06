import pathlib

from fastup.adapters import utils
from fastup.domain.errors import FileParseErr

BASE_DIR = utils.get_env_path(
    "FASTUP_BASE_DIR", pathlib.Path(__file__).parent.parent.parent
)

try:
    CONFDICT = utils.parse_toml_file(
        utils.get_env_path(
            "FASTUP_CONFIG_PATH", BASE_DIR / "configs" / "dev.toml"
        )
    )
except (FileParseErr, FileNotFoundError) as e:  # pragma: no cover
    raise RuntimeError("failed to parse configuration file") from e

try:
    LOG_CONFIG = utils.parse_toml_file(
        utils.get_env_path(
            "FASTUP_LOG_CONF_PATH", BASE_DIR / "configs" / "logging.toml"
        )
    )
except (FileParseErr, FileNotFoundError) as e:  # pragma: no cover
    raise RuntimeError("failed to parse logging configuration file") from e

DEBUG = CONFDICT["app"]["debug"]
APP_NAME = CONFDICT["app"]["name"]
APP_VERSION = CONFDICT["app"]["version"]

DB_URL = "{driver}://{user}:{password}@{host}:{port}/{database}".format(
    driver="postgresql+asyncpg",
    user=utils.get_env_str("POSTGRES_USER", CONFDICT["database"]["user"]),
    password=utils.get_env_str(
        "POSTGRES_PASSWORD", CONFDICT["database"]["password"]
    ),
    host=utils.get_env_str("POSTGRES_HOST", CONFDICT["database"]["host"]),
    port=utils.get_env_int("POSTGRES_PORT", CONFDICT["database"]["port"]),
    database=utils.get_env_str(
        "POSTGRES_DATABASE_NAME", CONFDICT["database"]["dbname"]
    ),
)

DB_POOL_SIZE = CONFDICT["database"]["pool_size"]
DB_MAX_OVERFLOW = CONFDICT["database"]["max_overflow"]

try:
    DB_POOL_TIMEOUT = utils.parse_timeout(CONFDICT["database"]["pool_timeout"])
except ValueError as e:  # pragma: no cover
    raise RuntimeError("failed to parse database pool timeout") from e
