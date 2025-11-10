import pathlib
import typing

import yaml


def parse_yaml_file(path: pathlib.Path) -> dict[str, typing.Any]:
    """Parse a YAML file and return its contents as a dictionary.

    :param path: Path to the YAML file.
    :return: Dictionary containing the parsed YAML file contents.
    :raises ValueError: If the file cannot be found or is not valid YAML.
    """
    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if data is None:
                return {}
            return data
    except (FileNotFoundError, OSError, yaml.YAMLError) as e:
        raise ValueError(f"Error parsing YAML file '{path}': {e}") from e
