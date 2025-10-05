import pathlib

from fastup.domain import parsers, resolvers

BASE_DIR = resolvers.resolve_path_env(
    "FASTUP_DIR", pathlib.Path(__file__).parent.parent.parent
)

try:
    CONFDICT = parsers.parse_toml_file(
        resolvers.resolve_path_env(
            "FASTUP_CONFIG_PATH", BASE_DIR / "configs" / "dev.toml"
        )
    )
except (ValueError, FileNotFoundError) as e:  # pragma: no cover
    raise RuntimeError("failed to parse configuration file") from e

try:
    LOG_CONFIG = parsers.parse_toml_file(
        resolvers.resolve_path_env(
            "FASTUP_LOG_CONF_PATH", BASE_DIR / "configs" / "logging.toml"
        )
    )
except (ValueError, FileNotFoundError) as e:  # pragma: no cover
    raise RuntimeError("failed to parse logging configuration file") from e

DEBUG = CONFDICT["app"]["debug"]
APP_NAME = CONFDICT["app"]["name"]
APP_VERSION = CONFDICT["app"]["version"]

try:
    DB_URL = "{driver}://{user}:{password}@{host}:{port}/{database}".format(
        driver="postgresql+asyncpg",
        user=resolvers.resolve_str_env("POSTGRES_USER"),
        password=resolvers.resolve_str_env("POSTGRES_PASSWORD"),
        host=resolvers.resolve_str_env("POSTGRES_HOST"),
        port=resolvers.resolve_int_env("POSTGRES_PORT"),
        database=resolvers.resolve_str_env("POSTGRES_DATABASE_NAME"),
    )
except ValueError as e:  # pragma: no cover
    raise RuntimeError("failed to construct database URL") from e

DB_POOL_SIZE = CONFDICT["database"]["pool_size"]
DB_MAX_OVERFLOW = CONFDICT["database"]["max_overflow"]

try:
    DB_POOL_TIMEOUT = parsers.parse_duration(
        CONFDICT["database"]["pool_timeout"],
    )
except ValueError as e:  # pragma: no cover
    raise RuntimeError("failed to parse database pool timeout") from e
