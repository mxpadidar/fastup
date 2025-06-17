import pathlib

import dotenv

from fastup.utils import envars, parsers

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
config = parsers.parse_toml(base_dir / "config.toml")
dotenv_path = base_dir / ".env"

# Load environment variables from .env file if it exists
dotenv.load_dotenv(dotenv_path)


name = config["app"]["name"]
version = config["app"]["version"]
debug = config["app"]["debug"]

db_host = envars.get_str_env("DB_HOST", "localhost")
db_port = envars.get_int_env("DB_PORT", 5432)
db_user = envars.get_str_env("DB_USER", "postgres")
db_password = envars.get_str_env("DB_PASSWORD", "postgres")
db_name = envars.get_str_env("DB_NAME", "postgres")
