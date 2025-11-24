import hashlib
import hmac
import secrets


from fastup.config import get_config
from fastup.core.services import HashService

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
