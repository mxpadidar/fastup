from pwdlib import PasswordHash


class PwdlibPasswordHash:
    """pwdlib-based password hashing service."""

    def __init__(self):
        """Initialize the password hasher."""
        self.hasher = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        """Hash a plaintext password using Argon2.

        :param password: Plaintext password to hash.
        :return: An Argon2 hash string.
        :raises TypeError: If `password` is not a string.
        """
        if not isinstance(password, str):
            raise TypeError("password must be a string")

        return self.hasher.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a plaintext password against a stored Argon2 hash.

        :param password: Plaintext password to check.
        :param password_hash: Stored Argon2 hash to verify against.
        :return: True if the password matches the hash, False otherwise.
        :raises TypeError: If inputs are not strings.
        """
        if not isinstance(password, str) or not isinstance(password_hash, str):
            raise TypeError("password and password_hash must be strings")

        return self.hasher.verify(password, password_hash)
