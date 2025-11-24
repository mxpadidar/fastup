import datetime

import pydantic


class HealthResp(pydantic.BaseModel):
    status: str


class OtpResp(pydantic.BaseModel):
    id: int
    expires_at: datetime.datetime
