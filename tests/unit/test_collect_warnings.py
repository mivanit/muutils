from __future__ import annotations

import sys
import warnings
from io import StringIO

import pytest

from muutils.collect_warnings import CollateWarnings


def test_basic_warning_capture():
    """Test that warnings issued inside the context populate the counts dict."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("test warning 1", UserWarning)
        warnings.warn("test warning 2", DeprecationWarning)

    assert len(cw.counts) == 2

    # Check that the warnings are in the counts dict
    warning_messages = [msg for (_, _, _, msg) in cw.counts.keys()]
    assert "test warning 1" in warning_messages
    assert "test warning 2" in warning_messages

    # Check that the category names are correct
    categories = [cat for (_, _, cat, _) in cw.counts.keys()]
    assert "UserWarning" in categories
    assert "DeprecationWarning" in categories

    # Check that counts are 1 for each
    assert all(count == 1 for count in cw.counts.values())


def test_collation():
    """Test that duplicate warnings from the same line increment count correctly."""
    with CollateWarnings(print_on_exit=False) as cw:
        # Issue the same warning multiple times from a loop (same line)
        for _ in range(3):
            warnings.warn("duplicate warning", UserWarning)
        warnings.warn("different warning", UserWarning)

    # The duplicate warnings from the same line should be collated
    # Find the duplicate warning entry
    duplicate_count = None
    different_count = None
    for (filename, lineno, category, message), count in cw.counts.items():
        if message == "duplicate warning":
            duplicate_count = count
        elif message == "different warning":
            different_count = count

    assert duplicate_count == 3
    assert different_count == 1


def test_print_on_exit_true():
    """Test that warnings are printed to stderr on exit when print_on_exit=True."""
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        with CollateWarnings(print_on_exit=True) as cw:
            warnings.warn("printed warning", UserWarning)

        assert cw

        # Get the output
        stderr_output = sys.stderr.getvalue()

        # Check that the warning was printed
        assert "printed warning" in stderr_output
        assert "UserWarning" in stderr_output
        assert "(1x)" in stderr_output  # Default format includes count

    finally:
        # Restore stderr
        sys.stderr = old_stderr


def test_print_on_exit_false():
    """Test that no output is produced but counts are tracked when print_on_exit=False."""
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        with CollateWarnings(print_on_exit=False) as cw:
            warnings.warn("silent warning", UserWarning)

        # Get the output
        stderr_output = sys.stderr.getvalue()

        # Check that nothing was printed
        assert stderr_output == ""

        # But counts should still be tracked
        assert len(cw.counts) == 1
        warning_messages = [msg for (_, _, _, msg) in cw.counts.keys()]
        assert "silent warning" in warning_messages

    finally:
        # Restore stderr
        sys.stderr = old_stderr


def test_custom_format_string():
    """Test that custom fmt parameter controls output format."""
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        custom_fmt = "WARNING: {message} ({category}) appeared {count} times"
        with CollateWarnings(print_on_exit=True, fmt=custom_fmt) as cw:
            warnings.warn("custom format warning", UserWarning)

        assert cw

        # Get the output
        stderr_output = sys.stderr.getvalue()

        # Check that the custom format was used
        assert "WARNING: custom format warning" in stderr_output
        assert "(UserWarning)" in stderr_output
        assert "appeared 1 times" in stderr_output

        # Check that default format was NOT used
        assert "(1x)" not in stderr_output

    finally:
        # Restore stderr
        sys.stderr = old_stderr


def test_multiple_different_warnings():
    """Test handling of multiple different warnings."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("warning 1", UserWarning)
        warnings.warn("warning 2", DeprecationWarning)
        warnings.warn("warning 3", FutureWarning)
        warnings.warn("warning 4", RuntimeWarning)

    assert len(cw.counts) == 4

    categories = [cat for (_, _, cat, _) in cw.counts.keys()]
    assert "UserWarning" in categories
    assert "DeprecationWarning" in categories
    assert "FutureWarning" in categories
    assert "RuntimeWarning" in categories


def test_no_warnings():
    """Test that CollateWarnings works correctly when no warnings are issued."""
    with CollateWarnings(print_on_exit=False) as cw:
        # No warnings issued
        pass

    assert len(cw.counts) == 0


def test_same_message_different_categories():
    """Test that same message with different categories are counted separately."""
    with CollateWarnings(print_on_exit=False) as cw:
        # Issue same message with different categories from the same line in a loop
        for _ in range(2):
            warnings.warn("same message", UserWarning)
        warnings.warn("same message", DeprecationWarning)

    # Find the counts for each category
    user_warning_count = 0
    deprecation_warning_count = 0
    for (_, _, category, message), count in cw.counts.items():
        if message == "same message" and category == "UserWarning":
            user_warning_count += count
        elif message == "same message" and category == "DeprecationWarning":
            deprecation_warning_count += count

    assert user_warning_count == 2
    assert deprecation_warning_count == 1


def test_filename_and_lineno_tracking():
    """Test that filename and line number are tracked correctly."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("tracked warning", UserWarning)

    assert len(cw.counts) == 1

    # Get the filename and lineno
    (filename, lineno, category, message) = list(cw.counts.keys())[0]

    # Check that filename and lineno are present and reasonable
    assert filename is not None
    assert isinstance(filename, str)
    assert lineno is not None
    assert isinstance(lineno, int)
    assert lineno > 0


def test_context_manager_re_entry_fails():
    """Test that CollateWarnings cannot be re-entered while active."""
    cw = CollateWarnings(print_on_exit=False)

    with cw:
        # Try to re-enter while still inside the context
        with pytest.raises(RuntimeError, match="cannot be re-entered"):
            with cw:
                pass


def test_format_string_all_fields():
    """Test that all format fields work correctly."""
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        fmt = "count={count} file={filename} line={lineno} cat={category} msg={message}"
        with CollateWarnings(print_on_exit=True, fmt=fmt) as cw:
            warnings.warn("test all fields", UserWarning)

        assert cw

        stderr_output = sys.stderr.getvalue()

        # Check that all fields are present
        assert "count=1" in stderr_output
        assert "file=" in stderr_output
        assert "line=" in stderr_output
        assert "cat=UserWarning" in stderr_output
        assert "msg=test all fields" in stderr_output

    finally:
        sys.stderr = old_stderr


def test_warning_with_stacklevel():
    """Test that warnings with different stacklevels are handled correctly."""

    def issue_warning():
        warnings.warn("nested warning", UserWarning, stacklevel=2)

    with CollateWarnings(print_on_exit=False) as cw:
        issue_warning()

    assert len(cw.counts) == 1
    warning_messages = [msg for (_, _, _, msg) in cw.counts.keys()]
    assert "nested warning" in warning_messages


def test_counts_dict_structure():
    """Test the structure of the counts dictionary."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("test warning", UserWarning)

    # Check that counts is a Counter
    from collections import Counter

    assert isinstance(cw.counts, Counter)

    # Check the key structure
    key = list(cw.counts.keys())[0]
    assert isinstance(key, tuple)
    assert len(key) == 4

    filename, lineno, category, message = key
    assert isinstance(filename, str)
    assert isinstance(lineno, int)
    assert isinstance(category, str)
    assert isinstance(message, str)


def test_large_number_of_warnings():
    """Test handling of a large number of duplicate warnings."""
    with CollateWarnings(print_on_exit=False) as cw:
        for i in range(1000):
            warnings.warn("repeated warning", UserWarning)

    assert len(cw.counts) == 1

    # Find the count
    count = list(cw.counts.values())[0]
    assert count == 1000


def test_mixed_warning_counts():
    """Test a mix of different warning counts."""
    with CollateWarnings(print_on_exit=False) as cw:
        # Warning A: 5 times
        for _ in range(5):
            warnings.warn("warning A", UserWarning)

        # Warning B: 3 times
        for _ in range(3):
            warnings.warn("warning B", DeprecationWarning)

        # Warning C: 1 time
        warnings.warn("warning C", FutureWarning)

    assert len(cw.counts) == 3

    # Extract counts by message
    counts_by_message = {}
    for (_, _, _, message), count in cw.counts.items():
        counts_by_message[message] = count

    assert counts_by_message["warning A"] == 5
    assert counts_by_message["warning B"] == 3
    assert counts_by_message["warning C"] == 1


def test_exception_propagation():
    """Test that exceptions from the with-block are propagated."""
    with pytest.raises(ValueError, match="test exception"):
        with CollateWarnings(print_on_exit=False) as cw:
            warnings.warn("warning before exception", UserWarning)
            raise ValueError("test exception")

    # Counts should still be populated even though an exception was raised
    assert len(cw.counts) == 1


def test_warning_with_special_characters():
    """Test warnings with special characters in messages."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("warning with 'quotes' and \"double quotes\"", UserWarning)
        warnings.warn("warning with\nnewline", UserWarning)
        warnings.warn("warning with\ttab", UserWarning)

    assert len(cw.counts) == 3

    messages = [msg for (_, _, _, msg) in cw.counts.keys()]
    assert "warning with 'quotes' and \"double quotes\"" in messages
    assert "warning with\nnewline" in messages
    assert "warning with\ttab" in messages


def test_empty_warning_message():
    """Test warning with empty message."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("", UserWarning)

    assert len(cw.counts) == 1
    messages = [msg for (_, _, _, msg) in cw.counts.keys()]
    assert "" in messages


def test_unicode_warning_message():
    """Test warnings with unicode characters."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("warning with unicode: 你好 мир 🌍", UserWarning)

    assert len(cw.counts) == 1
    messages = [msg for (_, _, _, msg) in cw.counts.keys()]
    assert "warning with unicode: 你好 мир 🌍" in messages


def test_custom_warning_class():
    """Test with custom warning classes."""

    class CustomWarning(UserWarning):
        pass

    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("custom warning", CustomWarning)

    assert len(cw.counts) == 1
    categories = [cat for (_, _, cat, _) in cw.counts.keys()]
    assert "CustomWarning" in categories


def test_default_format_string():
    """Test the default format string output."""
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        with CollateWarnings(print_on_exit=True) as cw:
            warnings.warn("test default format", UserWarning)

        assert cw

        stderr_output = sys.stderr.getvalue().strip()

        # Default format: "({count}x) {filename}:{lineno} {category}: {message}"
        assert stderr_output.startswith("(1x)")
        assert "UserWarning: test default format" in stderr_output
        assert ":" in stderr_output  # filename:lineno separator

    finally:
        sys.stderr = old_stderr


def test_collate_warnings_with_warnings_always():
    """Test that warnings.simplefilter('always') is set correctly."""
    # This test verifies that even if we would normally suppress duplicate warnings,
    # CollateWarnings captures them all
    with CollateWarnings(print_on_exit=False) as cw:
        # These would normally be suppressed if the same warning is issued twice
        # from the same location, but CollateWarnings should capture all of them
        for _ in range(3):
            warnings.warn("repeated warning", UserWarning)

    # All 3 warnings should be captured
    count = list(cw.counts.values())[0]
    assert count == 3


def test_multiple_warnings_same_line():
    """Test multiple different warnings from the same line."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("warning 1", UserWarning)
        warnings.warn("warning 2", UserWarning)  # noqa: E702

    # Should have 2 different warnings (different messages, same line)
    assert len(cw.counts) == 2


def test_counts_accessible_after_exit():
    """Test that counts are accessible after exiting the context."""
    with CollateWarnings(print_on_exit=False) as cw:
        warnings.warn("test warning", UserWarning)

    # After exiting, counts should still be accessible
    assert len(cw.counts) == 1
    assert cw.counts is not None

    # Should be able to iterate over counts
    for key, count in cw.counts.items():
        assert isinstance(key, tuple)
        assert isinstance(count, int)


def test_print_on_exit_default_true():
    """Test that print_on_exit defaults to True."""
    old_stderr = sys.stderr
    sys.stderr = StringIO()

    try:
        # Don't specify print_on_exit, should default to True
        with CollateWarnings() as cw:
            warnings.warn("default print test", UserWarning)

        assert cw
        stderr_output = sys.stderr.getvalue()
        assert "default print test" in stderr_output

    finally:
        sys.stderr = old_stderr


def test_exit_twice_fails():
    """Test that calling __exit__ twice raises RuntimeError."""
    cw = CollateWarnings(print_on_exit=False)

    # Enter the context
    cw.__enter__()

    # Exit once
    cw.__exit__(None, None, None)

    # Try to exit again - should raise RuntimeError
    with pytest.raises(RuntimeError, match="exited twice"):
        cw.__exit__(None, None, None)
