import logging
import pathlib
import tomllib

from fastup.core.errors import ServerErr
from fastup.infra import envlib

logging.basicConfig(format="%(levelname)s:   %(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
confile = base_dir / "config.toml"
envfile = base_dir / ".env"

try:
    with open(confile, "rb") as f:
        config = tomllib.load(f)
        logger.debug("loaded configuration from %s", confile.as_posix())
except FileNotFoundError as e:
    logger.error("%s not found.", confile.as_posix())
    raise ServerErr("configuration file not found.") from e

try:
    envlib.loadenv(envfile)
    logger.debug("loaded environment variables from %s", envfile.as_posix())
except FileNotFoundError as e:
    logger.error("%s does not exist, skipping dotenv loading.", envfile.as_posix())
    raise ServerErr("environment file not found.") from e

secret_key: str = envlib.getenv("SECRET_KEY", "default_secret_key")

log_level: str = config["app"].get("log_level", "info")
debug: bool = config["app"].get("debug", False)

app_title: str = config["app"]["name"]
app_version: str = config["app"]["version"]

server_host: str = config["server"]["host"]
server_port: int = config["server"]["port"]
