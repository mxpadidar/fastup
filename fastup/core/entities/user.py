import dataclasses
import datetime

from fastup.core import enums

from .base_entity import Entity


@dataclasses.dataclass(kw_only=True)
class User(Entity):
    """User entity representing a registered user in the system."""

    id: int
    phone: str
    pwdhash: str
    fname: str | None = None
    lname: str | None = None
    sex: enums.UserSex
    status: enums.UserStatus = enums.UserStatus.INACTIVE
    is_admin: bool = False
    created_at: datetime.datetime = dataclasses.field(init=False)
    updated_at: datetime.datetime = dataclasses.field(init=False)
    deleted_at: datetime.datetime | None = None
