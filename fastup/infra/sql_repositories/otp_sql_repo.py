import typing

from fastup.core.entities import Otp
from fastup.core.repositories import OtpRepo

from .base_sql_repo import SQLRepository


class OtpSQLRepo(SQLRepository[Otp], OtpRepo):
    """SQLAlchemy-backed repository for Otp."""

    @property
    def entity_cls(self) -> typing.Type[Otp]:  # pragma: no cover
        return Otp
