import datetime

import pydantic

from fastup.core import enums


class HealthResp(pydantic.BaseModel):
    status: str


class OtpResp(pydantic.BaseModel):
    id: int
    status: enums.OtpStatus
    expires_at: datetime.datetime


class TokenResp(pydantic.BaseModel):
    raw: str
    exp: datetime.datetime
    typ: str


class UserResp(pydantic.BaseModel):
    id: int
    phone: str
    fname: str | None = None
    lname: str | None = None
    sex: enums.UserSex
    status: enums.UserStatus
    created_at: datetime.datetime
