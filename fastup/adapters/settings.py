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

