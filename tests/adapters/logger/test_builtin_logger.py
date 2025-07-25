import logging

import pytest

from fastup.domain.logger import LoggerFactory


@pytest.mark.asyncio
async def test_builtin_logger_levels(
    caplog: pytest.LogCaptureFixture,
    logger_factory: LoggerFactory,
) -> None:
    """Test logging at info, error, and debug levels."""
    logger = logger_factory("test_logger", level=logging.DEBUG)

    with caplog.at_level(logging.DEBUG):
        await logger.info("user {user_id} logged in", user_id=42)
        await logger.error("error occurred: {code}", code=500)
        await logger.debug("debugging {feature}", feature="feature-x")

    messages = [(r.levelname, r.message) for r in caplog.records]

    assert ("INFO", "user 42 logged in") in messages
    assert ("ERROR", "error occurred: 500") in messages
    assert ("DEBUG", "debugging feature-x") in messages


@pytest.mark.asyncio
async def test_logger_handles_missing_keys(
    caplog: pytest.LogCaptureFixture,
    logger_factory: LoggerFactory,
) -> None:
    """test that the logger handles missing keys gracefully."""
    logger = logger_factory("test_logger")
    with caplog.at_level(logging.INFO):
        await logger.info("hello {name}", wrong_key="value")

    messages = [(r.levelname, r.message) for r in caplog.records]
    assert (
        "INFO",
        "[logger formatting error: missing key 'name'] hello {name}",
    ) in messages
