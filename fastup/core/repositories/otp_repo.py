import abc

from fastup.core.entities import Otp
from fastup.core.enums import OtpStatus

from .base_repo import Repository


class OtpRepo(Repository[Otp], abc.ABC):
    """Repository for managing Otp entities."""

    @abc.abstractmethod
    async def get_for_update(self, *, id: int, status: OtpStatus, ipaddr: str) -> Otp:
        """Get an OTP for update, locking the record.

        :param id: The ID of the OTP.
        :param status: The status of the OTP to filter by.
        :param ipaddr: The IP address associated with the OTP request.
        :return: The Otp entity.
        :raises NotFoundExc: If no matching OTP is found.
        """
        raise NotImplementedError
