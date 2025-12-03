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
