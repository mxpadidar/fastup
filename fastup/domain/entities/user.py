import dataclasses
import datetime

from fastup.domain import enums


@dataclasses.dataclass
class User:
    """Represents an application user/account and profile data
    used by authentication and authorization logic.

    Invariants:
    - At least one of email or phone_e164 must be present.
    - pwdhash must be a hashed password (never store plain text).
    """

    id: int = dataclasses.field(init=False)
    display_name: str
    email: str | None = None
    phone_e164: str | None = None
    pwdhash: str  # hashed password
    fname: str | None = None
    lname: str | None = None
    sex: enums.UserSex
    status: enums.UserStatus = enums.UserStatus.INCOMPLETE
    is_admin: bool = False
    created_at: datetime.datetime = dataclasses.field(init=False)
    updated_at: datetime.datetime = dataclasses.field(init=False)
    deleted_at: datetime.datetime | None = None  # soft-delete timestamp
