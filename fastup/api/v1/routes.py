from typing import Annotated

from fastapi.params import Depends
from fastapi.routing import APIRouter

from fastup.api import deps
from fastup.api.v1 import req_models, resp_models
from fastup.core import commands, entities, enums
from fastup.core.bus import MessageBus
from fastup.infra.pydantic_config import PydanticConfig, get_config
from fastup.infra.pyjwt_service import PyJWTService

router = APIRouter()


@router.get("/health", status_code=200, response_model=resp_models.HealthResp)
async def health():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}


@router.post("/otps", status_code=202, response_model=resp_models.OtpResp)
async def issue_otp(
    data: req_models.IssueOtpReq,
    ipaddr: Annotated[str, Depends(deps.get_ipaddr)],
    bus: Annotated[MessageBus, Depends(deps.get_bus)],
):
    """Issue an OTP for phone number verification.

    Creates and sends a one-time password. The OTP is valid
    for a limited time and must be verified to complete registration.
    """
    match data.intent:
        case enums.OtpIntent.SIGN_UP:
            cmd = commands.IssueSignupOtpCommand(phone=data.phone, ipaddr=ipaddr)
        # case _: rejected by pydantic with 400 status code
    otp = await bus.handle(cmd)
    return otp


@router.patch("/otps/{otp_id}", status_code=200, response_model=resp_models.TokenResp)
async def verify_otp(
    otp_id: int,
    data: req_models.VerifyOtpReq,
    ipaddr: Annotated[str, Depends(deps.get_ipaddr)],
    bus: Annotated[MessageBus, Depends(deps.get_bus)],
    token_service: Annotated[PyJWTService, Depends(deps.get_token_service)],
    config: Annotated[PydanticConfig, Depends(get_config)],
):
    """Verify a previously issued OTP.

    Confirms that the provided OTP code matches the one issued for the given ID.
    Successful verification allows the user to proceed with registration with provided token.
    """
    cmd = commands.VerifyOtpCommand(otp_id=otp_id, code=str(data.code), ipaddr=ipaddr)
    otp = await bus.handle(cmd)
    assert isinstance(otp, entities.Otp)
    token = token_service.encode(
        sub=str(otp.id), typ="signup", ttl=config.signup_token_ttl
    )
    return token
