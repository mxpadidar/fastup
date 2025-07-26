import re
from typing import Any


def parse_timeout(timeout: Any) -> float:
    """
    parse a timeout value and return it in seconds as a float.
    accepts:
      - int or float (returned as-is)
      - str like "500ms", "2.5s"
    raises:
      - ValueError for invalid formats
      - TypeError for unsupported types
    """
    if isinstance(timeout, (int, float)):
        return float(timeout)

    if not isinstance(timeout, str):
        raise TypeError

    pattern = r"^(\d+(?:\.\d+)?)(ms|s)$"
    match = re.match(pattern, timeout.strip())
    if not match:
        raise ValueError
    num_str, unit = match.groups()
    num = float(num_str)
    return num / 1000 if unit == "ms" else num
