import datetime

import pytest

from app.config.parsers import parse_duration


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("45s", datetime.timedelta(seconds=45)),
        ("15m", datetime.timedelta(minutes=15)),
        ("1h", datetime.timedelta(hours=1)),
        ("1d", datetime.timedelta(days=1)),
        ("0s", datetime.timedelta(seconds=0)),
    ],
)
def test_parse_duration_valid_input(input_str, expected):
    assert parse_duration(input_str) == expected


@pytest.mark.parametrize(
    "input_str",
    ["45x", "abc", "45", "", "45sm", "-45s", "45.5s"],
)
def test_parse_duration_invalid_input(input_str):
    with pytest.raises(ValueError):
        parse_duration(input_str)


def test_parse_duration_non_string_input():
    """Test that non-string inputs raise TypeError."""
    with pytest.raises(TypeError, match="duration value must be a string"):
        parse_duration(45)  # type: ignore
    with pytest.raises(TypeError):
        parse_duration(None)  # type: ignore
