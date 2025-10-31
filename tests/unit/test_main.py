from fastup.main import main


def test_main_returns_none():
    """Ensure main() returns None (sanity check for test setup)."""
    assert main() is None
