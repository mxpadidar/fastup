import pydantic
from pydantic_extra_types.phone_numbers import PhoneNumber


class E164Phone(PhoneNumber):
    default_region_code = "IR"
    supported_regions = ["IR"]
    phone_format = "E164"


class IssueSignupOtpReq(pydantic.BaseModel):
    phone: E164Phone
