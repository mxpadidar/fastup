import re


def parse_duration(duration: str) -> float:
    if isinstance(duration, (int, float)):
        return float(duration)

    if not isinstance(duration, str):
        raise TypeError

    pattern = r"^(\d+(?:\.\d+)?)(ms|s|m)$"
    match = re.match(pattern, duration.strip())
    if not match:
        raise ValueError
    num_str, unit = match.groups()
    num = float(num_str)
    if unit == "ms":
        return num / 1000
    elif unit == "s":
        return num
    else:  # unit == "m"
        return num * 60
