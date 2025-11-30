import functools
import inspect

from fastup.core.commands import Command
from fastup.core.events import Event

from .registry import Handler


def inject_dependencies(handler: Handler, deps: dict) -> Handler:
    """Inject dependencies into a handler using type hints.

    :param handler: The handler function to inject dependencies into.
    :param deps: A mapping of dependency names to their instances.
    :return: A new handler with dependencies injected.
    :raises RuntimeError: If a required dependency is missing or a parameter lacks a type annotation.
    """
    params = inspect.signature(handler).parameters
    handler_deps = {}
    for name, param in params.items():
        annotation = param.annotation

        # Require annotation on every parameter
        if annotation is inspect._empty or not isinstance(annotation, type):
            raise RuntimeError(
                f"Handler {handler.__name__!r} has parameter {name!r} without a type annotation. "
                "All handler parameters must be explicitly typed."
            )

        # Skip parameters typed as Command / Event
        if issubclass(annotation, (Command, Event)):
            continue

        # If it has a default, it's optional — skip requirement
        if param.default is not inspect._empty:
            continue

        if name not in deps:
            raise RuntimeError(
                f"Missing dependency {name!r} for handler {handler.__name__!r}."
            )

        handler_deps[name] = deps[name]

    return functools.partial(handler, **handler_deps)
