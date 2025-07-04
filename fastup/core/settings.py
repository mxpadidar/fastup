import pathlib
import tomllib

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent

try:
    confile = base_dir / "config.toml"
    with open(confile, "rb") as f:
        config = tomllib.load(f)
except FileNotFoundError:
    raise RuntimeError(
        "confile not found. ensure config.toml exists in the base directory."
    )

app_name = config["app"]["name"]
app_version = config["app"]["version"]
debug = config["app"].get("debug", False)

server_host = config["server"]["host"]
server_port = config["server"]["port"]
