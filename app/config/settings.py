import pathlib

from .parsers import parse_toml_file

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent

try:
    confile = parse_toml_file(ROOT_DIR / "configs" / "dev.toml")
except ValueError as e:
    raise RuntimeError(f"Error parsing config file: {e}")

APP_NAME = confile["app"]["name"]
APP_VERSION = confile["app"]["version"]
DEBUG = confile["app"]["debug"]
PORT = confile["app"]["port"]
