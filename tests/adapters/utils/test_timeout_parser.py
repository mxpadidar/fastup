from typing import Any

import pytest

from fastup.adapters.utils import parse_timeout


@pytest.mark.parametrize(
    "value, expected",
    [
        ("500ms", 0.5),
        ("1000ms", 1.0),
        ("2s", 2.0),
        ("2.5s", 2.5),
        (5, 5.0),
        (3.3, 3.3),
    ],
)
def test_parse_timeout_valid(value: Any, expected: float) -> None:
    assert parse_timeout(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "100",  # missing unit
        "5seconds",  # invalid unit
        "s2",  # invalid format
        "abc",  # non-numeric
        " ",  # blank string
        "",  # empty string
    ],
)
def test_parse_timeout_invalid_string(value: str) -> None:
    with pytest.raises(ValueError):
        parse_timeout(value)


@pytest.mark.parametrize(
    "value",
    [
        None,
        [],
        {},
        object(),
    ],
)
def test_parse_timeout_invalid_type(value: Any) -> None:
    with pytest.raises(TypeError):
        parse_timeout(value)
