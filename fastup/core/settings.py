import pathlib
import tomllib

from fastup.core import envlib
from fastup.core.logger import get_logger

logger = get_logger("settings")

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent

confile = base_dir / "config.toml"

try:
    with open(confile, "rb") as f:
        config = tomllib.load(f)
except FileNotFoundError:
    logger.error("%s not found.", confile.as_posix())
    raise RuntimeError(
        "confile not found. ensure config.toml exists in the base directory."
    )

if debug := config["app"].get("debug", False):
    env_file = base_dir / ".env"
    envlib.loadenv(env_file)

app_name = config["app"]["name"]
app_version = config["app"]["version"]

log_level = config["app"].get("log_level", "info")

server_host = config["server"]["host"]
server_port = config["server"]["port"]

db_pool_size = config["database"]["pool_size"]
db_max_overflow = config["database"]["max_overflow"]
db_pool_timeout = config["database"]["pool_timeout"]

db_host = envlib.getenv("DB_HOST", "127.0.0.1")
db_port = envlib.getenv("DB_PORT", 5432)
db_user = envlib.getenv("DB_USER", "postgres")
db_password = envlib.getenv("DB_PASSWORD", "password")
db_name = envlib.getenv("DB_NAME", "fastup")
