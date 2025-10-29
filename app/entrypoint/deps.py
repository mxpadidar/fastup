from app import adapters
from app.config import settings
from app.domain import protocols
from app.domain.base import UnitOfWork

_hasher = adapters.PwdlibPasswordService()

_token_service = adapters.JwtTokenService(
    secret_key=settings.TOKEN_SECRET,
    issuer=settings.TOKEN_ISSUER,
    audience=settings.TOKEN_AUDIENCE,
    access_exp_delta=settings.TOKEN_ACCESS_EXP,
    refresh_exp_delta=settings.TOKEN_REFRESH_EXP,
)


def get_uow() -> UnitOfWork:
    """Returns SqlAlchemyUnitOfWork implementation of UnitOfWork"""
    return adapters.SqlAlchemyUoW(adapters.db_sessionmaker)


def get_pw_service() -> protocols.PasswordService:
    """Returns pwdlib hasher implementation of PasswordHasher"""
    return _hasher


def get_token_service() -> protocols.TokenService:
    """Returns JwtTokenService implementation of TokenService"""
    return _token_service
