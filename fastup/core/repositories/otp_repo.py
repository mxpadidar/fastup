import abc

from fastup.core.entities import Otp

from .base_repo import Repository


class OtpRepo(Repository[Otp], abc.ABC):
    """Repository for managing Otp entities."""

    pass
