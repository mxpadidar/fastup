import tomllib
import pathlib
from functools import lru_cache


@lru_cache()
def load_config(path: pathlib.Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


base_dir = pathlib.Path(__file__).resolve().parent.parent.parent


config = load_config(base_dir / "config.toml")

version = config["fastup"]["version"]
