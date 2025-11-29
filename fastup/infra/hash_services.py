import hashlib
import hmac
import secrets

import pwdlib
import pwdlib.exceptions

from fastup.core.services import HashService

from .pydantic_config import get_config

config = get_config()


class HMACHasher(HashService):
    """
    A secure signing service that implements HashService using HMAC-SHA256.

    This class is ideal for creating and verifying Message Authentication Codes
    (MACs) for tokens or other authenticated messages.
    """

    def __init__(self, key: bytes = config.hmac_secret_key) -> None:
        self._key: bytes = key

    def _hash_text(self, text: str) -> str:
        """Computes the HMAC-SHA256 signature for the given text."""
        return hmac.new(self._key, text.encode("utf-8"), hashlib.sha256).hexdigest()

    def _verify_hash(self, text: str, hashed: str) -> bool:
        """Verifies an HMAC signature using a secure, constant-time comparison."""
        expected_mac = self._hash_text(text)
        return secrets.compare_digest(expected_mac, hashed)


class Argon2PasswordHasher(HashService):
    """
    A secure password hashing service that implements HashService using Argon2.

    This class uses the `pwdlib` library to securely hash and verify passwords,
    automatically handling salt generation and algorithm parameter management.
    """

    def __init__(self):
        """Initializes the password hasher with recommended Argon2 settings."""
        self.hasher = pwdlib.PasswordHash.recommended()

    def _hash_text(self, text: str) -> str:
        """Hashes a password using Argon2 with an automatically generated salt."""
        return self.hasher.hash(text)

    def _verify_hash(self, text: str, hashed: str) -> bool:
        """Verifies a password against a stored Argon2 hash.

        Gracefully handles unrecognized hash formats by returning False.
        """
        try:
            return self.hasher.verify(text, hashed)
        except pwdlib.exceptions.UnknownHashError:
            return False
