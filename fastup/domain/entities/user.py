import dataclasses
import datetime

from fastup.domain import enums


@dataclasses.dataclass(kw_only=True)
class User:
    """Represents an application user/account and profile data
    used by authentication and authorization logic.

    Invariants:
    - At least one of email or phone must be present.
    """

    id: int = dataclasses.field(init=False)
    display_name: str
    email: str | None = None
    phone: str | None = None
    pwdhash: str
    fname: str | None = None
    lname: str | None = None
    sex: enums.UserSex
    status: enums.UserStatus = enums.UserStatus.INACTIVE
    is_admin: bool = False
    created_at: datetime.datetime = dataclasses.field(init=False)
    updated_at: datetime.datetime = dataclasses.field(init=False)
    deleted_at: datetime.datetime | None = None
