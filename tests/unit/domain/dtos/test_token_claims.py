import datetime
import uuid

import pytest

from app.domain import errors
from app.domain.dtos import TokenClaims
from app.domain.enums import TokenType


def test_from_dict_with_valid_claims():
    data = {
        "iss": "test_issuer",
        "sub": "user123",
        "aud": "test_audience",
        "iat": int(
            datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
        ),
        "exp": int(
            datetime.datetime(2023, 1, 2, tzinfo=datetime.timezone.utc).timestamp()
        ),
        "typ": "access",
        "jti": uuid.uuid4().hex,
    }
    claims = TokenClaims.from_dict(data)
    assert claims.iss == "test_issuer"
    assert claims.sub == "user123"
    assert claims.aud == "test_audience"
    assert claims.typ == TokenType.ACCESS
    assert isinstance(claims.jti, uuid.UUID)


def test_from_dict_with_missing_sub():
    with pytest.raises(errors.ValidationErr):
        TokenClaims.from_dict(
            {
                "iss": "test_issuer",
                "aud": "test_audience",
                "iat": 1640995200,
                "exp": 1641081600,
                "typ": "access",
                "jti": str(uuid.uuid4()),
            }
        )


def test_from_dict_with_empty_sub():
    with pytest.raises(errors.ValidationErr):
        TokenClaims.from_dict(
            {
                "iss": "test_issuer",
                "sub": "",
                "aud": "test_audience",
                "iat": 1640995200,
                "exp": 1641081600,
                "typ": "access",
                "jti": str(uuid.uuid4()),
            }
        )


def test_from_dict_with_invalid_iat():
    with pytest.raises(errors.ValidationErr):
        TokenClaims.from_dict(
            {
                "iss": "test_issuer",
                "sub": "user123",
                "aud": "test_audience",
                "iat": "invalid",
                "exp": 1641081600,
                "typ": "access",
                "jti": str(uuid.uuid4()),
            }
        )


def test_from_dict_with_invalid_jti():
    with pytest.raises(errors.ValidationErr):
        TokenClaims.from_dict(
            {
                "iss": "test_issuer",
                "sub": "user123",
                "aud": "test_audience",
                "iat": 1640995200,
                "exp": 1641081600,
                "typ": "access",
                "jti": "invalid-uuid",
            }
        )
