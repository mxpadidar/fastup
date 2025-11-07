import typing


class Hasher(typing.Protocol):
    """Protocol for hashing and verifying arbitrary text.

    Implementations must produce an opaque string hash and must be able to
    verify that a given plaintext corresponds to a stored hash.

    Methods:
    - hash(text) -> str: produce a hash string for the given text.
    - verify(text, hashed) -> bool: True if text matches hashed.
    """

    def hash(self, text: str) -> str:
        """Return an opaque hash string for `text`. Must raise TypeError if `text` is not str."""
        ...

    def verify(self, text: str, hashed: str) -> bool:
        """Return True if `text` matches `hashed`. Must raise TypeError if inputs are not str."""
        ...
