from typing import Any

import pytest

from fastup.domain.parsers import parse_duration


@pytest.mark.parametrize(
    "value, expected",
    [
        ("500ms", 0.5),
        ("1000ms", 1.0),
        ("2s", 2.0),
        ("2.5s", 2.5),
        ("1m", 60.0),
        ("2m", 120.0),
        ("1.5m", 90.0),
        (5, 5.0),
        (3.3, 3.3),
    ],
)
def test_parse_duration_valid(value: Any, expected: float) -> None:
    assert parse_duration(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "100",  # missing unit
        "5seconds",  # invalid unit
        "5minutes",  # invalid unit
        "s2",  # invalid format
        "m2",  # invalid format
        "abc",  # non-numeric
        " ",  # blank string
        "",  # empty string
    ],
)
def test_parse_duration_invalid_string(value: str) -> None:
    with pytest.raises(ValueError):
        parse_duration(value)


@pytest.mark.parametrize(
    "value",
    [
        None,
        [],
        {},
        object(),
    ],
)
def test_parse_duration_invalid_type(value: Any) -> None:
    with pytest.raises(TypeError):
        parse_duration(value)
