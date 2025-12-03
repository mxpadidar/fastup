import pydantic
from pydantic_extra_types.phone_numbers import PhoneNumber

from fastup.core import enums


class E164Phone(PhoneNumber):
    default_region_code = "IR"
    supported_regions = ["IR"]
    phone_format = "E164"


class IssueOtpReq(pydantic.BaseModel):
    phone: E164Phone
    intent: enums.OtpIntent


class VerifyOtpReq(pydantic.BaseModel):
    code: int
