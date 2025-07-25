import pathlib
import tomllib

from fastup.domain.errors import FileParseErr


def parse_toml_file(path: pathlib.Path) -> dict:
    """
    parse a toml file and return its contents as a dictionary.

    :param path: the path to the toml file.
    :return: a dictionary containing the parsed toml file contents.
    :raises FileParseErr: if the file cannot be found, is not a valid toml file,
                          or if there is an error reading the file.
    """
    try:
        with path.open("rb") as file:
            return tomllib.load(file)
    except (FileNotFoundError, tomllib.TOMLDecodeError, OSError) as e:
        raise FileParseErr(path) from e
