import typing

from fastapi import APIRouter, Depends

from app.domain import enums, handlers, protocols
from app.domain.base import UnitOfWork
from app.entrypoint import deps, request_models, response_models

router = APIRouter(prefix="/api/v1")


@router.get("/health", tags=["meta"], status_code=200)
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}


@router.post(
    "/signup",
    tags=["auth"],
    response_model=response_models.SignupResponseModel,
    status_code=201,
)
async def signup(
    uow: typing.Annotated[UnitOfWork, Depends(deps.get_uow)],
    pw_service: typing.Annotated[
        protocols.PasswordService, Depends(deps.get_pw_service)
    ],
    token_service: typing.Annotated[
        protocols.TokenService, Depends(deps.get_token_service)
    ],
    data: request_models.SignupRequestModel,
):
    """Create a new user account."""
    user = await handlers.handle_create_user(uow, pw_service, **data.model_dump())

    access_token, access_token_exp = token_service.encode(
        sub=str(user.id),
        token_type=enums.TokenType.ACCESS,
    )
    refresh_token, refresh_token_exp = token_service.encode(
        sub=str(user.id),
        token_type=enums.TokenType.REFRESH,
    )

    return {
        "user": user,
        "access_token": {
            "token": access_token,
            "exp": access_token_exp,
        },
        "refresh_token": {
            "token": refresh_token,
            "exp": refresh_token_exp,
        },
    }
