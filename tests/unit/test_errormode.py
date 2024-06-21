from __future__ import annotations

import warnings

from muutils.errormode import ErrorMode, ERROR_MODE_ALIASES

import pytest

"""
import typing
import warnings
from enum import Enum

class ErrorMode(Enum):
    EXCEPT = "except"
    WARN = "warn"
    IGNORE = "ignore"
    
    def process(
            self,
            msg: str,
            except_cls: typing.Type[Exception] = ValueError,
            warn_cls: typing.Type[Warning] = UserWarning,
            except_from: typing.Optional[typing.Type[Exception]] = None,
        ):
        if self is ErrorMode.EXCEPT:
            if except_from is not None:
                raise except_from(msg) from except_from
            else:
                raise except_cls(msg)
        elif self is ErrorMode.WARN:
            warnings.warn(msg, warn_cls)
        elif self is ErrorMode.IGNORE:
            pass
        else:
            raise ValueError(f"Unknown error mode {self}")
"""


def test_except():
    with pytest.raises(ValueError):
        ErrorMode.EXCEPT.process("test-except", except_cls=ValueError)

    with pytest.raises(TypeError):
        ErrorMode.EXCEPT.process("test-except", except_cls=TypeError)

    with pytest.raises(RuntimeError):
        ErrorMode.EXCEPT.process("test-except", except_cls=RuntimeError)

    with pytest.raises(KeyError):
        ErrorMode.EXCEPT.process("test-except", except_cls=KeyError)

    with pytest.raises(KeyError):
        ErrorMode.EXCEPT.process(
            "test-except", except_cls=KeyError, except_from=ValueError("base exception")
        )


def test_warn():
    with pytest.warns(UserWarning):
        ErrorMode.WARN.process("test-warn", warn_cls=UserWarning)

    with pytest.warns(Warning):
        ErrorMode.WARN.process("test-warn", warn_cls=Warning)

    with pytest.warns(DeprecationWarning):
        ErrorMode.WARN.process("test-warn", warn_cls=DeprecationWarning)


def test_ignore():
    with warnings.catch_warnings(record=True) as w:
        ErrorMode.IGNORE.process("test-ignore")

        ErrorMode.IGNORE.process("test-ignore", except_cls=ValueError)
        ErrorMode.IGNORE.process("test-ignore", except_from=TypeError)

        ErrorMode.IGNORE.process("test-ignore", warn_cls=UserWarning)

        assert len(w) == 0, f"There should be no warnings: {w}"


def test_except_custom():
    class MyCustomError(ValueError):
        pass

    with pytest.raises(MyCustomError):
        ErrorMode.EXCEPT.process("test-except", except_cls=MyCustomError)


def test_warn_custom():
    class MyCustomWarning(Warning):
        pass

    with pytest.warns(MyCustomWarning):
        ErrorMode.WARN.process("test-warn", warn_cls=MyCustomWarning)


def test_invalid_mode():
    with pytest.raises(ValueError):
        ErrorMode("invalid")


def test_except_mode_chained_exception():
    try:
        # set up the base exception
        try:
            raise KeyError("base exception")
        except Exception as base_exception:
            # catch it, raise another exception with it as the cause
            ErrorMode.EXCEPT.process(
                "Test chained exception",
                except_cls=RuntimeError,
                except_from=base_exception,
            )
    # catch the outer exception
    except RuntimeError as e:
        assert str(e) == "Test chained exception"
        # check that the cause is the base exception
        assert isinstance(e.__cause__, KeyError)
        assert repr(e.__cause__) == "KeyError('base exception')"
    else:
        assert False, "Expected RuntimeError with cause KeyError"


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
    ],
)
def test_from_any_strict_error(mode, excepted_error):
    with pytest.raises(excepted_error):
        ErrorMode.from_any(mode, allow_aliases=False)


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
