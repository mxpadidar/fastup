import pathlib

from fastup.utils import parsers

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent


config = parsers.parse_toml(base_dir / "config.toml")

name = config["app"]["name"]
version = config["app"]["version"]
debug = config["app"]["debug"]
