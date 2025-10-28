import datetime
import typing


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
