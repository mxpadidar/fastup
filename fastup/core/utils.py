import datetime
import secrets
import string


def generate_otp(length: int) -> str:
    """Generate a cryptographically secure random numeric OTP code."""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def get_utc_now() -> datetime.datetime:
    """Get current UTC datetime with timezone awareness."""
    return datetime.datetime.now(datetime.UTC)
