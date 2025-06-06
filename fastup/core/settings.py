import pathlib

from dotenv import load_dotenv

from fastup.core.utils import (
    get_bool_env,
    get_database_dsn,
    get_env_variable,
    load_toml,
)

base_dir = pathlib.Path(__file__).parent.parent.parent

confile = base_dir / "config.toml"

if not confile.exists():
    raise RuntimeError

env = get_env_variable("ENVIRONMENT", "dev")

if not env == "prod":
    load_dotenv(base_dir / ".env")

try:
    config = load_toml(confile)
except Exception as e:
    raise RuntimeError(f"Failed to load configuration file: {e}")

debug = get_bool_env("DEBUG", config["app"]["debug"])

version = config["app"]["version"]

database_dsn = get_database_dsn(**config["database"])
