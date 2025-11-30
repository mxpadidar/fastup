from fastapi import Request

from fastup.core.bus import MessageBus


def get_ipaddr(request: Request) -> str:
    """Extract client IP address from the request."""
    assert request.client
    return request.client.host


def get_bus(request: Request) -> MessageBus:
    """Dependency to get the message bus from the application state."""
    return request.app.state.bus
