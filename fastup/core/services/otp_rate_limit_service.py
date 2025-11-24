# import datetime

# from fastup.core.protocols import DomainConfig
# from fastup.core.unit_of_work import UnitOfWork


# class OtpRateLimiter:
#     """A service to enforce rate limits on OTP issuance."""

#     def __init__(self, uow: UnitOfWork, config: DomainConfig):
#         self._uow = uow
#         self._config = config
#         self._now = datetime.datetime.now(datetime.UTC)

#     async def check(self, phone: str, ipaddr: str) -> None:
#         """
#         Checks if a new OTP request is allowed for the given phone or IP address.

#         This method checks two independent limits:
#         1. The number of recent requests from the same phone number.
#         2. The number of recent requests from the same IP address.

#         :param phone: The phone number requesting the OTP.
#         :param ipaddr: The IP address of the requester.
#         :raises TooManyRequestsExc: If either the phone or IP limit is exceeded.
#         """
#         await self._check_phone_limit(phone)
#         await self._check_ip_limit(ipaddr)

#     async def _check_phone_limit(self, phone: str) -> None:
#         """Checks the rate limit for a single phone number."""
#         limit_start_time = self._now - self._config.otp_phone_rate_limit_window
#         recent_requests = await self._uow.otps.count(
#             phone=phone,
#             created_after=limit_start_time,
#         )
#         if recent_requests >= self._config.otp_phone_rate_limit_max_requests:
#             raise TooManyRequestsExc("Too many OTP requests for this phone number.")

#     async def _check_ip_limit(self, ipaddr: str) -> None:
#         """Checks the rate limit for a single IP address."""
#         limit_start_time = self._now - self._config.otp_ip_rate_limit_window
#         recent_requests = await self._uow.otps.count(
#             ipaddr=ipaddr,
#             created_after=limit_start_time,
#         )
#         if recent_requests >= self._config.otp_ip_rate_limit_max_requests:
#             raise TooManyRequestsExc("Too many OTP requests from this IP address.")


# # You might also want to update the __all__ list in services.py if you have one.
