import pytest

from fastup.core.services import HashService

# A list of the fixture names to avoid repetition in parametrize calls
HASHER_FIXTURE_NAMES = ["argon2_hasher", "hmac_hasher"]


@pytest.mark.parametrize("hasher_fixture_name", HASHER_FIXTURE_NAMES)
def test_hash_creates_valid_and_different_string(
    hasher_fixture_name: str, request: pytest.FixtureRequest
):
    """
    Tests that hash() produces a non-empty string that is different from
    the original plaintext.
    """
    # Arrange
    hasher: HashService = request.getfixturevalue(hasher_fixture_name)
    plain_text = "a-secret-password-for-mxpadidar"

    # Act
    hashed_text = hasher.hash(plain_text)

    # Assert
    assert isinstance(hashed_text, str)
    assert hashed_text != ""
    assert hashed_text != plain_text


@pytest.mark.parametrize("hasher_fixture_name", HASHER_FIXTURE_NAMES)
def test_verify_handles_correct_and_incorrect_text(
    hasher_fixture_name: str, request: pytest.FixtureRequest
):
    """
    Tests that verify() returns True for the correct text and False for an
    incorrect one.
    """
    # Arrange
    hasher: HashService = request.getfixturevalue(hasher_fixture_name)
    plain_text = "correct-password"
    wrong_text = "wrong-password"
    hashed_text = hasher.hash(plain_text)

    # Act & Assert
    assert hasher.verify(plain_text, hashed_text) is True, (
        "Verification of correct text failed."
    )
    assert hasher.verify(wrong_text, hashed_text) is False, (
        "Verification of wrong text succeeded unexpectedly."
    )


@pytest.mark.parametrize("hasher_fixture_name", HASHER_FIXTURE_NAMES)
def test_hash_raises_errors_for_invalid_input(
    hasher_fixture_name: str, request: pytest.FixtureRequest
):
    """
    Tests that the public hash() method raises errors for invalid inputs
    like None or empty strings.
    """
    # Arrange
    hasher: HashService = request.getfixturevalue(hasher_fixture_name)

    # Act & Assert
    with pytest.raises(TypeError, match="must be a string"):
        hasher.hash(None)  # type: ignore

    with pytest.raises(ValueError, match="cannot be empty"):
        hasher.hash("")


@pytest.mark.parametrize("hasher_fixture_name", HASHER_FIXTURE_NAMES)
def test_verify_raises_errors_for_invalid_input(
    hasher_fixture_name: str, request: pytest.FixtureRequest
):
    """
    Tests that the public verify() method raises errors for invalid inputs
    like None or empty strings.
    """
    # Arrange
    hasher: HashService = request.getfixturevalue(hasher_fixture_name)
    hashed_text = hasher.hash("a-valid-password")

    # Act & Assert for TypeError
    with pytest.raises(TypeError, match="must be strings"):
        hasher.verify(None, hashed_text)  # type: ignore

    with pytest.raises(TypeError, match="must be strings"):
        hasher.verify("a-valid-password", None)  # type: ignore

    # Act & Assert for ValueError
    with pytest.raises(ValueError, match="cannot be empty"):
        hasher.verify("", hashed_text)

    with pytest.raises(ValueError, match="cannot be empty"):
        hasher.verify("a-valid-password", "")


@pytest.mark.parametrize("hasher_fixture_name", HASHER_FIXTURE_NAMES)
def test_verify_handles_malformed_hash(
    hasher_fixture_name: str, request: pytest.FixtureRequest
):
    """
    Tests that verify() returns False for a hash that is structurally
    invalid, corrupted, or in an unknown format.
    """
    # Arrange
    hasher: HashService = request.getfixturevalue(hasher_fixture_name)
    plain_text = "any-password"
    malformed_hash = "this-is-not-a-valid-hash-format"

    # Act
    result = hasher.verify(plain_text, malformed_hash)

    # Assert
    assert result is False, "Verification should fail for a malformed hash."
