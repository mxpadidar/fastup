import typing


class PasswordHash(typing.Protocol):
    """Protocol for password hashing and verification."""

    def hash(self, password: str) -> str:
        """Hash a plaintext password and return the hashed password.

        :param password: Plaintext password to hash.
        :return: The hashed password.
        :raises TypeError: If `password` is not a string.
        """
        ...

    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a plaintext password against hashed password.

        :param password: Plaintext password to check.
        :param password_hash: Hashed password to verify against.
        :return: True if the password matches the hash, False otherwise.
        :raises TypeError: If inputs are not strings.
        """
        ...
