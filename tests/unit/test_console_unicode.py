import pytest
from unittest.mock import patch

from muutils.console_unicode import get_console_safe_str


@pytest.mark.parametrize(
    "default, fallback, encoding, expected",
    [
        ("hello", "world", "ASCII", "hello"),
        ("café", "cafe", "ASCII", "cafe"),
        ("", "", "ASCII", ""),
        ("こんにちは", "hello", "ASCII", "hello"),
        ("💖", "heart", "ASCII", "heart"),
        ("1234", "numbers", "ASCII", "1234"),
        ("ABCé123", "ABC123", "ASCII", "ABC123"),
        ("café", "cafe", "UTF-8", "café"),
        ("こんにちは", "hello", "UTF-8", "こんにちは"),
        ("💖", "heart", "UTF-8", "💖"),
    ],
)
def test_get_console_safe_str(default, fallback, encoding, expected):
    with patch("locale.getpreferredencoding", return_value=encoding):
        result = get_console_safe_str(default, fallback)
        assert (
            result == expected
        ), f"Test failed for default='{default}', fallback='{fallback}', encoding='{encoding}'. Expected '{expected}', got '{result}'."
