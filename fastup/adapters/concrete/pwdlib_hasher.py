import pwdlib
import pwdlib.exceptions


class PwdlibHasher:
    """pwdlib-based hasher using Argon2 algorithm."""

    def __init__(self):
        """Initialize the password hasher."""
        self.hasher = pwdlib.PasswordHash.recommended()

    def hash(self, text: str) -> str:
        """Hash a plaintext using Argon2.

        :param text: plaintext to hash
        :return: An Argon2 hash string.
        :raises TypeError: If `text` is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        return self.hasher.hash(text)

    def verify(self, text: str, hashed: str) -> bool:
        """Verify a plaintext string against a stored Argon2 hash.

        :param text: The plaintext to verify.
        :param hashed: The stored Argon2 hash string.
        :return: True if `text` matches `hashed`, False otherwise.
        :raises TypeError: If `text` or `hashed` are not strings.
        :raises ValueError: If the provided hash format is not recognized.
        """
        if not isinstance(text, str) or not isinstance(hashed, str):
            raise TypeError("text and hashed values must be strings")

        try:
            return self.hasher.verify(text, hashed)
        except pwdlib.exceptions.UnknownHashError as e:
            raise ValueError("The provided hash format is not recognized") from e
