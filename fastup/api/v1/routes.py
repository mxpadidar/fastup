from typing import Annotated

from fastapi.params import Depends
from fastapi.routing import APIRouter

from fastup.api import deps
from fastup.api.v1 import req_models, resp_models
from fastup.config import get_config
from fastup.core import commands, enums, handlers, protocols, services
from fastup.core.unit_of_work import UnitOfWork

router = APIRouter()


@router.get("/health", status_code=200, response_model=resp_models.HealthResp)
async def health():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}


@router.post("/otps", status_code=202, response_model=resp_models.OtpResp)
async def issue_otp(
    data: req_models.IssueOtpReq,
    ipaddr: Annotated[str, Depends(deps.get_ipaddr)],
    uow: Annotated[UnitOfWork, Depends(deps.get_uow)],
    idgen: Annotated[services.IDGenerator, Depends(deps.get_idgen)],
    hmac_hasher: Annotated[services.HashService, Depends(deps.get_hmac_hasher)],
    config: Annotated[protocols.CoreConf, Depends(get_config)],
):
    """Issue an OTP for phone number verification.

    Creates and sends a one-time password. The OTP is valid
    for a limited time and must be verified to complete registration.
    """
    match data.intent:
        case enums.OtpIntent.SIGN_UP:
            cmd = commands.IssueSignupOtpCommand(phone=data.phone, ipaddr=ipaddr)
        # case _: rejected by pydantic with 400 status code
    otp = await handlers.handle_issue_signup_otp(
        cmd=cmd, config=config, uow=uow, idgen=idgen, hmac_hasher=hmac_hasher
    )
    return otp  # pragma: no cover
