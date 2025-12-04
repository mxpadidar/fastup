import functools
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request

from fastup.core.bus import MessageBus
from fastup.infra.pydantic_config import PydanticConfig, get_config
from fastup.infra.pyjwt_service import PyJWTService

logger = logging.getLogger(__name__)


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


async def get_otp_id(
    request: Request,
    token_service: Annotated[PyJWTService, Depends(get_token_service)],
) -> int:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header"
        )

    raw_token = auth_header[len("Bearer ") :]
    try:
        token = token_service.decode(raw_token)
        return int(token.sub)
    except Exception as e:
        logger.error("Failed to decode OTP token: %s", e)
        raise HTTPException(status_code=401, detail="Invalid token") from e
