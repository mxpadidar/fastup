from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from fastup.bootstrap import bootstrap
from fastup.core.bus import MessageBus
from fastup.core.commands import Command
from fastup.core.unit_of_work import UnitOfWork


class Cmd(Command): ...


async def handler(cmd: Cmd, uow: UnitOfWork):
    return SimpleNamespace(id=1)


async def bad_handler(cmd: Cmd, missing_dep: str):
    raise NotImplementedError


@patch("fastup.core.bus.COMMAND_HANDLERS", {Cmd: handler})
async def test_bootstrap_wires_command_handlers_with_injected_dependencies():
    """Ensure command handlers are wrapped with dependency injection
    and receive the provided dependencies."""

    bus = bootstrap(start_orm=False)

    assert isinstance(bus, MessageBus)
    assert Cmd in bus.command_handlers

    wrapped = bus.command_handlers[Cmd]
    result = await wrapped(Cmd())

    assert result.id == 1  # to ensure handler executed successfully


@patch("fastup.core.bus.COMMAND_HANDLERS", {Cmd: bad_handler})
async def test_bootstrap_raises_when_dependency_injection_fails():
    """Ensure bootstrap surfaces dependency injection errors when
    a handler requires missing dependencies."""

    with pytest.raises(RuntimeError):
        bootstrap(start_orm=False)


@patch("fastup.bootstrap.start_orm_mapper")
def test_bootstrap_starts_orm_when_requested(mock_start_orm: Mock):
    """Ensure ORM is initialized when start_orm is True."""
    bootstrap(start_orm=True)
    mock_start_orm.assert_called_once()
