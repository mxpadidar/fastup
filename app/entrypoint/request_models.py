import pydantic


class SignupRequestModel(pydantic.BaseModel):
    """Signup request model"""

    email: pydantic.EmailStr
    password: str
