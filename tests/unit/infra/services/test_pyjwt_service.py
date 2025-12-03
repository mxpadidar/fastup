import datetime

import jwt
import pytest

from fastup.infra.pyjwt_service import InvalidTokenExc, PyJWTService, Token


@pytest.fixture
def ttl() -> datetime.timedelta:
    return datetime.timedelta(minutes=5)


def test_encode_creates_token_with_correct_attributes(
    jwt_service: PyJWTService, ttl: datetime.timedelta
):
    """Test that encoding produces a Token object with correct subject, type, and expiration."""
    token = jwt_service.encode("user-123", "access", ttl)

    assert isinstance(token, Token)
    assert token.sub == "user-123"
    assert token.typ == "access"
    assert token.exp - datetime.datetime.now(datetime.UTC) <= ttl


def test_decode_restores_original_token_object(
    jwt_service: PyJWTService, ttl: datetime.timedelta
):
    """Test that decoding a token recreates the original Token object with all attributes."""
    issued = jwt_service.encode("foo", "signup", ttl)
    decoded = jwt_service.decode(issued.raw)

    assert decoded.sub == issued.sub
    assert decoded.typ == issued.typ
    assert decoded.id == issued.id
    assert decoded.exp == issued.exp
    assert decoded.raw == issued.raw


def test_decode_rejects_malformed_token_strings(jwt_service: PyJWTService):
    """Test that decoding raises InvalidTokenExc for malformed token strings."""
    with pytest.raises(InvalidTokenExc):
        jwt_service.decode("invalid.jwt.token")


def test_decode_rejects_expired_tokens(jwt_service: PyJWTService):
    """Test that decoding raises InvalidTokenExc for expired tokens."""
    expired_ttl = datetime.timedelta(seconds=-100)
    expired_token = jwt_service.encode("user", "access", expired_ttl)
    with pytest.raises(InvalidTokenExc):
        jwt_service.decode(expired_token.raw)


def test_decode_rejects_tokens_with_invalid_signatures(
    jwt_service: PyJWTService, ttl: datetime.timedelta
):
    """Test that decoding raises InvalidTokenExc for tokens with invalid signatures."""
    valid_token = jwt_service.encode("user", "access", ttl)
    # Tamper with the token (change one character)
    tampered_raw = valid_token.raw[:-1] + ("x" if valid_token.raw[-1] != "x" else "y")
    with pytest.raises(InvalidTokenExc):
        jwt_service.decode(tampered_raw)


EXP = datetime.datetime.now(datetime.UTC).timestamp() + 300


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"exp": EXP, "typ": "access", "jti": "test-jti"},
            id="missing_sub",
        ),
        pytest.param(
            {"sub": "user", "exp": EXP, "jti": "test-jti"},
            id="missing_typ",
        ),
        pytest.param(
            {"sub": "user", "exp": EXP, "typ": "access"},
            id="missing_jti",
        ),
        pytest.param(
            {"sub": "user", "exp": EXP, "typ": 123, "jti": "test-jti"},
            id="invalid_typ",
        ),
        pytest.param(
            {
                "sub": "user",
                "exp": "not-a-timestamp",
                "typ": "access",
                "jti": "test-jti",
            },
            id="invalid_exp",
        ),
    ],
)
def test_decode_rejects_tokens_with_invalid_claims(jwt_service: PyJWTService, payload):
    """Test that decoding raises InvalidTokenExc for tokens with missing or malformed claims."""
    invalid_token = jwt.encode(payload, "test-secret-key", algorithm="HS256")
    with pytest.raises(InvalidTokenExc):
        jwt_service.decode(invalid_token)
