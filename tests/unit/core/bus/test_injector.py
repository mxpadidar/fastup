from asyncio import iscoroutinefunction

import pytest

from fastup.core.bus import inject_dependencies
from fastup.core.commands import Command
from fastup.core.events import Event

command = Command()
event = Event()


async def test_inject_dependencies_successfully_injects_required_params():
    """Injection succeeds when all required dependencies are provided."""

    async def handler(cmd: Command, dep1: int, dep2: int) -> None: ...

    deps = {"dep1": 123, "dep2": 456}
    wrapped = inject_dependencies(handler, deps)
    assert iscoroutinefunction(wrapped)

    result = await wrapped(command)
    assert result is None  # to check that the handler was called successfully


async def test_inject_dependencies_raises_when_param_has_no_annotation():
    """A required parameter missing a type annotation should cause a runtime error."""

    async def handler(cmd: Command, dep) -> None: ...

    with pytest.raises(RuntimeError):
        inject_dependencies(handler, {"dep1": 1})


async def test_inject_dependencies_raises_when_required_dep_missing():
    """Injection fails if a required dependency is not provided."""

    async def handler(cmd: Command, dep1: int, dep2: int) -> None: ...

    deps = {"dep1": 123}  # missing dep2
    with pytest.raises(RuntimeError):
        inject_dependencies(handler, deps)


async def test_inject_dependencies_allows_default_arguments():
    """Parameters with default values must not be treated as required."""

    async def handler(cmd: Command, dep: str = "x") -> None: ...

    deps = {}
    wrapped = inject_dependencies(handler, deps)
    assert iscoroutinefunction(wrapped)


def test_inject_dependencies_ignores_event_param():
    """Parameters annotated as Event types should be ignored and not treated as dependencies."""

    async def handler(event: Event) -> None: ...

    wrapped = inject_dependencies(handler, deps={})
    assert iscoroutinefunction(wrapped)
