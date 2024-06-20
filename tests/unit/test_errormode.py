import typing
import warnings

from muutils.errormode import ErrorMode

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
        ErrorMode.EXCEPT.process("test-except", except_cls=KeyError, except_from=ValueError("base exception"))


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
            ErrorMode.EXCEPT.process("Test chained exception", except_cls=RuntimeError, except_from=base_exception)
    # catch the outer exception
    except RuntimeError as e:
        assert str(e) == "Test chained exception"
        # check that the cause is the base exception
        assert isinstance(e.__cause__, KeyError)
        assert repr(e.__cause__) == "KeyError('base exception')"
    else:
        assert False, "Expected RuntimeError with cause KeyError"

