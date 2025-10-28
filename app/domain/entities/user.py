import dataclasses
import datetime
import typing

from app.domain import protocols


@dataclasses.dataclass
class User:
    """Represents a user entity"""

    id: int = dataclasses.field(init=False)
    email: str
    password_hash: str = dataclasses.field(init=False)
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime.datetime = dataclasses.field(init=False)
    updated_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None

    def set_password(
        self, password: str, pw_service: protocols.PasswordService
    ) -> None:
        """Set the user's password by hashing the provided password.

        :param password: The plain text password to hash.
        :param pw_service: The password service to use.
        """
        self.password_hash = pw_service.hash_password(password)

    def verify_password(
        self, password: str, pw_service: protocols.PasswordService
    ) -> bool:
        """Verify the provided password against the user's stored hash.

        :param password: The plain text password to verify.
        :param pw_service: The password service to use.
        :returns: True if the password matches, False otherwise.
        """
        return pw_service.verify_password(password, self.password_hash)

    def to_dict(self) -> dict[str, typing.Any]:
        """Convert the user entity to a dictionary representation.

        :returns: A dictionary containing user attributes.
        """
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
