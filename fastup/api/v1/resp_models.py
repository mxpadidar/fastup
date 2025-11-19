import pydantic


class HealthResp(pydantic.BaseModel):
    status: str
