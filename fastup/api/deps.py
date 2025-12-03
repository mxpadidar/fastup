import functools
from typing import Annotated

from fastapi import Depends, Request

from fastup.core.bus import MessageBus
from fastup.infra.pydantic_config import PydanticConfig, get_config
from fastup.infra.pyjwt_service import PyJWTService


def get_ipaddr(request: Request) -> str:
    """Extract client IP address from the request."""
    assert request.client
    return request.client.host


def get_bus(request: Request) -> MessageBus:
    """Dependency to get the message bus from the application state."""
    return request.app.state.bus


@functools.cache
def get_token_service(
    config: Annotated[PydanticConfig, Depends(get_config)],
) -> PyJWTService:
    """Dependency to get the token service from the application config."""
    return PyJWTService(secret_key=config.jwt_secret_key)
