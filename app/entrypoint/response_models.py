import datetime

import pydantic


class UserResponse(pydantic.BaseModel):
    """User response model"""

    id: int
    email: pydantic.EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None


class TokenResponse(pydantic.BaseModel):
    """Token response model"""

    token: str
    exp: datetime.datetime


class SignupResponseModel(pydantic.BaseModel):
    """Signup response model"""

    user: UserResponse
    access_token: TokenResponse
    refresh_token: TokenResponse
