import pytest

from fastup.domain.ports import Hasher


def test_pwdlib_hasher_hash(pwdlib_hasher: Hasher):
    password = "secure_password"
    password_hash = pwdlib_hasher.hash(password)
    assert isinstance(password_hash, str)
    assert password_hash != password


def test_pwdlib_hasher_verify_correct_password(pwdlib_hasher: Hasher):
    password = "secure_password"
    password_hash = pwdlib_hasher.hash(password)
    assert pwdlib_hasher.verify(password, password_hash) is True


def test_pwdlib_hasher_verify_incorrect_password(pwdlib_hasher: Hasher):
    password = "secure_password"
    password_hash = pwdlib_hasher.hash(password)
    assert pwdlib_hasher.verify("wrong_password", password_hash) is False


def test_pwdlib_hasher_verify__invalid_inputs(pwdlib_hasher: Hasher):
    password = "secure_password"
    password_hash = pwdlib_hasher.hash(password)
    with pytest.raises(TypeError):
        pwdlib_hasher.verify(None, password_hash)  # type: ignore

    with pytest.raises(TypeError):
        pwdlib_hasher.verify(password, None)  # type: ignore


def test_pwdlib_hasher_hash_non_string_input(pwdlib_hasher: Hasher):
    with pytest.raises(TypeError):
        pwdlib_hasher.hash(None)  # type: ignore


def test_pwdlib_hasher_verify_unknown_hash(pwdlib_hasher: Hasher):
    with pytest.raises(ValueError):
        pwdlib_hasher.verify("password", "invalid_hash")
