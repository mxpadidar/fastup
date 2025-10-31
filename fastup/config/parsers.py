import pathlib
import tomllib
import typing


def parse_toml_file(path: pathlib.Path) -> dict[str, typing.Any]:
    """Parse a TOML file and return its contents as a dictionary.

    :param path: Path to the TOML file.
    :return: Dictionary containing the parsed TOML file contents.
    :raises ValueError: If the file cannot be found, is not a valid TOML file,
    """
    try:
        with path.open("rb") as file:
            return tomllib.load(file)
    except (FileNotFoundError, tomllib.TOMLDecodeError, OSError) as e:
        raise ValueError(f"Error parsing TOML file '{path}': {e}") from e
