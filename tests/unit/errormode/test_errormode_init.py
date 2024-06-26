from __future__ import annotations


from muutils.errormode import ErrorMode, ERROR_MODE_ALIASES

import pytest


def test_invalid_mode():
    with pytest.raises(ValueError):
        ErrorMode("invalid")


@pytest.mark.parametrize(
    "mode, expected_mode",
    [
        ("except", ErrorMode.EXCEPT),
        ("warn", ErrorMode.WARN),
        ("ignore", ErrorMode.IGNORE),
        ("Except", ErrorMode.EXCEPT),
        ("Warn", ErrorMode.WARN),
        ("Ignore", ErrorMode.IGNORE),
        ("  \teXcEpT  \n", ErrorMode.EXCEPT),
        ("WaRn  \t", ErrorMode.WARN),
        ("  \tIGNORE", ErrorMode.IGNORE),
    ],
)
def test_from_any_strict_ok(mode, expected_mode):
    assert ErrorMode.from_any(mode, allow_aliases=False) == expected_mode


@pytest.mark.parametrize(
    "mode, excepted_error",
    [
        (42, TypeError),
        (42.0, TypeError),
        (None, TypeError),
        (object(), TypeError),
        (True, TypeError),
        (False, TypeError),
        (["except"], TypeError),
        ("invalid", KeyError),
        ("  \tinvalid", KeyError),
        ("e", KeyError),
        (" E", KeyError),
        ("w", KeyError),
        ("W", KeyError),
        ("i", KeyError),
        ("I", KeyError),
        ("silent", KeyError),
        ("Silent", KeyError),
        ("quiet", KeyError),
        ("Quiet", KeyError),
        ("raise", KeyError),
        ("Raise", KeyError),
        ("error", KeyError),
        ("Error", KeyError),
        ("err", KeyError),
        ("ErR\t", KeyError),
        ("warning", KeyError),
        ("Warning", KeyError),
        ("ErrorMode.EXCEPT", KeyError),
        ("ErrorMode.WARN", KeyError),
        ("ErrorMode.IGNORE", KeyError),
        ("  \tErrorMode.EXCEPT  \t", KeyError),
        ("  \tErrorMode.WARN  \t", KeyError),
        ("  \tErrorMode.IGNORE  \t", KeyError),
    ],
)
def test_from_any_strict_error(mode, excepted_error):
    with pytest.raises(excepted_error):
        ErrorMode.from_any(mode, allow_aliases=False, allow_prefix=False)


@pytest.mark.parametrize(
    "mode, expected_mode",
    [
        *list(ERROR_MODE_ALIASES.items()),
        *list((a.upper(), b) for a, b in ERROR_MODE_ALIASES.items()),
        *list((a.title(), b) for a, b in ERROR_MODE_ALIASES.items()),
        *list((a.capitalize(), b) for a, b in ERROR_MODE_ALIASES.items()),
        *list((f"  \t{a}  \t", b) for a, b in ERROR_MODE_ALIASES.items()),
    ],
)
def test_from_any_aliases_ok(mode, expected_mode):
    assert ErrorMode.from_any(mode) == expected_mode
    assert ErrorMode.from_any(mode, allow_aliases=True) == expected_mode


@pytest.mark.parametrize(
    "mode, excepted_error",
    [
        (42, TypeError),
        (42.0, TypeError),
        (None, TypeError),
        (object(), TypeError),
        (True, TypeError),
        (False, TypeError),
        (["except"], TypeError),
        ("invalid", KeyError),
        ("  \tinvalid", KeyError),
    ],
)
def test_from_any_aliases_error(mode, excepted_error):
    with pytest.raises(excepted_error):
        ErrorMode.from_any(mode, allow_aliases=True)


@pytest.mark.parametrize(
    "mode, excepted_error",
    [
        (42, TypeError),
        (42.0, TypeError),
        (None, TypeError),
        (object(), TypeError),
        (True, TypeError),
        (False, TypeError),
        (["except"], TypeError),
        ("invalid", KeyError),
        ("  \tinvalid", KeyError),
        ("ErrorMode.EXCEPT", KeyError),
        ("ErrorMode.WARN", KeyError),
        ("ErrorMode.IGNORE", KeyError),
        ("  \tErrorMode.EXCEPT  \t", KeyError),
        ("  \tErrorMode.WARN  \t", KeyError),
        ("  \tErrorMode.IGNORE  \t", KeyError),
    ],
)
def test_from_any_no_prefix_error(mode, excepted_error):
    with pytest.raises(excepted_error):
        ErrorMode.from_any(mode, allow_aliases=True, allow_prefix=False)


@pytest.mark.parametrize(
    "mode, expected_mode",
    [
        ("ErrorMode.EXCEPT", ErrorMode.EXCEPT),
        ("ErrorMode.WARN", ErrorMode.WARN),
        ("ErrorMode.IGNORE", ErrorMode.IGNORE),
        ("  ErrorMode.EXCEPT  ", ErrorMode.EXCEPT),
        ("\tErrorMode.WARN\n", ErrorMode.WARN),
        (" \t ErrorMode.IGNORE \n ", ErrorMode.IGNORE),
    ],
)
def test_from_any_with_prefix(mode, expected_mode):
    assert ErrorMode.from_any(mode, allow_prefix=True) == expected_mode


@pytest.mark.parametrize(
    "mode, expected_error",
    [
        ("ErrorMode.EXCEPT", KeyError),
        ("ErrorMode.WARN", KeyError),
        ("ErrorMode.IGNORE", KeyError),
        ("  ErrorMode.EXCEPT  ", KeyError),
        ("\tErrorMode.WARN\n", KeyError),
        (" \t ErrorMode.IGNORE \n ", KeyError),
    ],
)
def test_from_any_without_prefix(mode, expected_error):
    with pytest.raises(expected_error):
        ErrorMode.from_any(mode, allow_prefix=False)


@pytest.mark.parametrize(
    "mode, expected_mode",
    [
        ("ErrorMode.except", ErrorMode.EXCEPT),
        ("ErrorMode.warn", ErrorMode.WARN),
        ("ErrorMode.ignore", ErrorMode.IGNORE),
        ("ErrorMode.EXCEPT", ErrorMode.EXCEPT),
        ("ErrorMode.WARN", ErrorMode.WARN),
        ("ErrorMode.IGNORE", ErrorMode.IGNORE),
        ("  ErrorMode.eXcEpT  ", ErrorMode.EXCEPT),
        ("\tErrorMode.WaRn\n", ErrorMode.WARN),
        (" \t ErrorMode.IgNoRe \n ", ErrorMode.IGNORE),
    ],
)
def test_from_any_with_prefix_case_insensitive(mode, expected_mode):
    assert ErrorMode.from_any(mode, allow_prefix=True) == expected_mode


@pytest.mark.parametrize(
    "mode, expected_error",
    [
        ("ErrorMode.invalid", KeyError),
        ("ErrorMode.", KeyError),
        ("ErrorMode", KeyError),
        ("errormode.EXCEPT", KeyError),
        ("ErrorMode.E", KeyError),
        ("ErrorMode.W", KeyError),
        ("ErrorMode.I", KeyError),
    ],
)
def test_from_any_with_prefix_invalid(mode, expected_error):
    with pytest.raises(expected_error):
        ErrorMode.from_any(mode, allow_prefix=False)


def test_from_any_with_prefix_and_aliases():
    assert (
        ErrorMode.from_any("ErrorMode.e", allow_prefix=True, allow_aliases=True)
        == ErrorMode.EXCEPT
    )
    assert (
        ErrorMode.from_any("ErrorMode.w", allow_prefix=True, allow_aliases=True)
        == ErrorMode.WARN
    )
    assert (
        ErrorMode.from_any("ErrorMode.i", allow_prefix=True, allow_aliases=True)
        == ErrorMode.IGNORE
    )


def test_from_any_with_prefix_no_aliases():
    with pytest.raises(KeyError):
        ErrorMode.from_any("ErrorMode.e", allow_prefix=True, allow_aliases=False)
    with pytest.raises(KeyError):
        ErrorMode.from_any("ErrorMode.w", allow_prefix=True, allow_aliases=False)
    with pytest.raises(KeyError):
        ErrorMode.from_any("ErrorMode.i", allow_prefix=True, allow_aliases=False)


# Tests for new string representation methods


def test_str_representation():
    assert str(ErrorMode.EXCEPT) == "ErrorMode.Except"
    assert str(ErrorMode.WARN) == "ErrorMode.Warn"
    assert str(ErrorMode.IGNORE) == "ErrorMode.Ignore"


def test_repr_representation():
    assert repr(ErrorMode.EXCEPT) == "ErrorMode.Except"
    assert repr(ErrorMode.WARN) == "ErrorMode.Warn"
    assert repr(ErrorMode.IGNORE) == "ErrorMode.Ignore"


def test_serialize():
    assert ErrorMode.EXCEPT.serialize() == "ErrorMode.Except"
    assert ErrorMode.WARN.serialize() == "ErrorMode.Warn"
    assert ErrorMode.IGNORE.serialize() == "ErrorMode.Ignore"


def test_load():
    assert ErrorMode.load("ErrorMode.Except") == ErrorMode.EXCEPT
    assert ErrorMode.load("ErrorMode.Warn") == ErrorMode.WARN
    assert ErrorMode.load("ErrorMode.Ignore") == ErrorMode.IGNORE

    with pytest.raises(KeyError):
        ErrorMode.load("ErrorMode.Invalid")
