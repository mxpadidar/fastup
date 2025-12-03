import asyncio

from fastup.core import bus
from fastup.core.config import Config
from fastup.infra.hash_services import Argon2PasswordHasher, HMACHasher
from fastup.infra.local_sms_service import LocalSMSService
from fastup.infra.orm_mapper import start_orm_mapper
from fastup.infra.pydantic_config import get_config
from fastup.infra.snowflake_idgen import SnowflakeIDGenerator
from fastup.infra.sql_unit_of_work import SQLUnitOfwWork


def bootstrap(config: Config | None = None, start_orm: bool = True) -> bus.MessageBus:
    """Build the application's MessageBus.

    The handlers signatures are inspected and dependencies are injected,
    so they must have type hints for all their parameters.

    :param config: Application configuration object.
    :param start_orm: Whether ORM mappings should be initialized before wiring.
    :return: A fully configured :class:`MessageBus` with injected handlers.
    :raises RuntimeError: If dependency injection fails (missing deps for a handler).
    """

    # intentional side-effect import
    #
    # Ensures all handler modules load and register themselves in the registry.
    # `handlers/__init__.py` must import each handler;
    # Without this import, no handlers get registered at runtime.
    from fastup.core import handlers  # noqa: F401

    if start_orm:
        start_orm_mapper()

    queue = asyncio.Queue()

    deps = {
        "config": config or get_config(),
        "uow": SQLUnitOfwWork(),
        "idgen": SnowflakeIDGenerator(),
        "hmac_hasher": HMACHasher(),
        "pwd_hasher": Argon2PasswordHasher(),
        "sms_service": LocalSMSService(),
        "event_queue": queue,
    }

    try:
        message_bus = bus.MessageBus(
            event_handlers={
                ev: [bus.inject_dependencies(h, deps) for h in handlers]
                for ev, handlers in bus.EVENT_HANDLERS.items()
            },
            command_handlers={
                cmd: bus.inject_dependencies(h, deps)
                for cmd, h in bus.COMMAND_HANDLERS.items()
            },
            queue=queue,
        )
    except RuntimeError as e:
        raise e

    return message_bus
