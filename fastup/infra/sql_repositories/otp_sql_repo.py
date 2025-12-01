import typing

import sqlalchemy

from fastup.core.entities import Otp
from fastup.core.enums import OtpStatus
from fastup.core.exceptions import NotFoundExc
from fastup.core.repositories import OtpRepo

from .base_sql_repo import SQLRepository


class OtpSQLRepo(SQLRepository[Otp], OtpRepo):
    """SQLAlchemy-backed repository for Otp."""

    @property
    def entity_cls(self) -> typing.Type[Otp]:  # pragma: no cover
        return Otp

    async def get_for_update(self, *, id: int, status: OtpStatus, ipaddr: str) -> Otp:
        """Get an OTP for update, locking the record."""
        stmt = (
            sqlalchemy.select(self.entity_cls)
            .where(
                self.entity_cls.id == id,  # type: ignore
                self.entity_cls.status == status,  # type: ignore
                self.entity_cls.ipaddr == ipaddr,  # type: ignore
            )
            .with_for_update()
        )

        result = await self.session.execute(stmt)
        otp = result.scalar_one_or_none()
        if otp is None:
            raise NotFoundExc("Otp does not exist.")
        return otp
