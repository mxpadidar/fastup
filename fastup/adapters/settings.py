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
