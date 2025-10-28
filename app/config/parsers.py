import datetime
import pathlib
import re
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


def parse_duration(value: str) -> datetime.timedelta:
    """
    Parse a short duration string into a datetime.timedelta.

    Supported formats: "45s", "15m", "1h", "1d" (seconds, minutes, hours, days).
    Leading/trailing whitespace is allowed. Unit is case-insensitive.

    :param value: Duration string to parse.
    :return: datetime.timedelta representing the parsed duration.
    :raises TypeError: If value is not a string.
    :raises ValueError: If the string doesn't match supported formats.
    """

    _DURATION_RE = re.compile(r"^\s*(\d+)\s*([smhd])\s*$", re.IGNORECASE)

    if not isinstance(value, str):
        raise TypeError("duration value must be a string")

    match_obj = _DURATION_RE.match(value)
    if not match_obj:
        raise ValueError(f"Invalid duration format: {value!r}")
    amount = int(match_obj.group(1))
    unit = match_obj.group(2).lower()

    match unit:
        case "s":
            return datetime.timedelta(seconds=amount)
        case "m":
            return datetime.timedelta(minutes=amount)
        case "h":
            return datetime.timedelta(hours=amount)
        case "d":
            return datetime.timedelta(days=amount)
        case _:  # pragma: no cover
            raise ValueError(f"Unsupported duration unit: {unit!r}")
