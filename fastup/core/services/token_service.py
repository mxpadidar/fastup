import typing


class TokenService(typing.Protocol):
    """Protocol for token services."""

    def encode(self, payload: dict) -> str:
        """Encode a payload into a token string."""
        ...

    def decode(self, token: str) -> dict:
        """Decode a token string into a payload dictionary."""
        ...
