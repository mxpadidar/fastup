import datetime
import typing

from app.domain import dtos, enums


class PasswordService(typing.Protocol):
    """Protocol for password hashing and verification."""

    def hash_password(self, password: str) -> str:
        """Hash a plaintext password and return the hashed password.

        :param password: Plaintext password to hash.
        :return: The hashed password.
        :raises TypeError: If `password` is not a string.
        """
        ...

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a plaintext password against hashed password.

        :param password: Plaintext password to check.
        :param password_hash: Hashed password to verify against.
        :return: True if the password matches the hash, False otherwise.
        :raises TypeError: If inputs are not strings.
        """
        ...


class Entity(typing.Protocol):
    """Protocol defining the interface for domain entities."""

    id: int

    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    deleted_at: datetime.datetime | None

    def to_dict(self) -> dict:
        """Convert the entity to a dictionary representation."""
        ...


class TokenService(typing.Protocol):
    """Protocol defining the interface for token services."""

    def encode(
        self, sub: str, token_type: enums.TokenType
    ) -> tuple[str, datetime.datetime]:
        """Encode a new token for the given subject and type.

        :param sub: The subject identifier (e.g., user ID).
        :param token_type: The type of token to encode (access or refresh).
        :return: A tuple containing the string representation of the encoded token and its expiration time.
        """
        ...

    def decode(self, token: str, token_type: enums.TokenType) -> dtos.TokenClaims:
        """Decode and validate the given token.

        :param token: The token string to decode and validate.
        :param token_type: The expected type of the token.
        :return: A TokenClaims object containing the decoded claims.
        :raises InvalidTokenErr: If the token is invalid, expired, or does not match the expected type.
        """
        ...
