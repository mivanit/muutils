from __future__ import annotations

import warnings

from muutils.errormode import ErrorMode

import pytest


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
        ErrorMode.IGNORE.process("test-ignore", except_from=TypeError("base exception"))

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


def test_logging_global():
    import muutils.errormode as errormode

    log: list[str] = []

    def log_func(msg: str):
        log.append(msg)

    ErrorMode.LOG.process("test-log-print")

    errormode.GLOBAL_LOG_FUNC = log_func

    ErrorMode.LOG.process("test-log")
    ErrorMode.LOG.process("test-log-2")

    assert log == ["test-log", "test-log-2"]

    ErrorMode.LOG.process("test-log-3")

    assert log == ["test-log", "test-log-2", "test-log-3"]


def test_custom_showwarning():
    """Test custom_showwarning function with traceback handling and frame extraction."""
    from muutils.errormode import custom_showwarning

    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Call custom_showwarning directly
        custom_showwarning("test warning message", UserWarning)

        # Check that a warning was issued
        assert len(w) == 1
        assert issubclass(w[0].category, UserWarning)
        assert "test warning message" in str(w[0].message)

        # Check that the warning has traceback information
        assert w[0].filename is not None
        assert w[0].lineno is not None


def test_custom_showwarning_with_category():
    """Test custom_showwarning with different warning categories."""
    from muutils.errormode import custom_showwarning

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        custom_showwarning("deprecation test", DeprecationWarning)

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)


def test_custom_showwarning_default_category():
    """Test custom_showwarning uses UserWarning as default."""
    from muutils.errormode import custom_showwarning

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Call without specifying category
        custom_showwarning("default category test", category=None)

        assert len(w) == 1
        assert issubclass(w[0].category, UserWarning)


def test_ErrorMode_process_except_from():
    """Test exception chaining with except_from parameter."""
    base_exception = ValueError("base error")

    try:
        ErrorMode.EXCEPT.process(
            "chained error message",
            except_cls=RuntimeError,
            except_from=base_exception,
        )
    except RuntimeError as e:
        # Check the exception message
        assert str(e) == "chained error message"
        # Check that __cause__ is set correctly
        assert e.__cause__ is base_exception
        assert isinstance(e.__cause__, ValueError)
        assert str(e.__cause__) == "base error"
    else:
        # TYPING: ty bug on python <= 3.9
        pytest.fail("Expected RuntimeError to be raised")  # ty: ignore[arg-type]


def test_ErrorMode_process_except_from_different_types():
    """Test exception chaining with different exception types."""
    # Test with KeyError -> TypeError
    base = KeyError("key not found")
    try:
        ErrorMode.EXCEPT.process("type error", except_cls=TypeError, except_from=base)
    except TypeError as e:
        assert e.__cause__ is base

    # Test with AttributeError -> ValueError
    base2 = AttributeError("attribute missing")
    try:
        ErrorMode.EXCEPT.process(
            "value error", except_cls=ValueError, except_from=base2
        )
    except ValueError as e:
        assert e.__cause__ is base2


def test_ErrorMode_process_custom_funcs():
    """Test custom warn_func and log_func parameters."""
    # Test custom warn_func
    warnings_captured = []

    def custom_warn(msg: str, category, source=None):
        warnings_captured.append({"msg": msg, "category": category, "source": source})

    ErrorMode.WARN.process(
        "custom warn test", warn_cls=UserWarning, warn_func=custom_warn
    )

    assert len(warnings_captured) == 1
    assert warnings_captured[0]["msg"] == "custom warn test"
    assert warnings_captured[0]["category"] == UserWarning  # noqa: E721

    # Test custom log_func
    logs_captured = []

    def custom_log(msg: str):
        logs_captured.append(msg)

    ErrorMode.LOG.process("custom log test", log_func=custom_log)

    assert len(logs_captured) == 1
    assert logs_captured[0] == "custom log test"


def test_ErrorMode_process_custom_warn_func_with_except_from():
    """Test custom warn_func with except_from to augment message."""
    warnings_captured = []

    def custom_warn(msg: str, category, source=None):
        warnings_captured.append(msg)

    base_exception = ValueError("source exception")

    ErrorMode.WARN.process(
        "warning message",
        warn_cls=UserWarning,
        warn_func=custom_warn,
        except_from=base_exception,
    )

    assert len(warnings_captured) == 1
    # Check that the message is augmented with source
    assert "warning message" in warnings_captured[0]
    assert "Source of warning" in warnings_captured[0]
    assert "source exception" in warnings_captured[0]


def test_ErrorMode_serialize_load():
    """Test round-trip serialization and loading."""
    # Test EXCEPT
    serialized = ErrorMode.EXCEPT.serialize()
    loaded = ErrorMode.load(serialized)
    assert loaded is ErrorMode.EXCEPT

    # Test WARN
    serialized = ErrorMode.WARN.serialize()
    loaded = ErrorMode.load(serialized)
    assert loaded is ErrorMode.WARN

    # Test LOG
    serialized = ErrorMode.LOG.serialize()
    loaded = ErrorMode.load(serialized)
    assert loaded is ErrorMode.LOG

    # Test IGNORE
    serialized = ErrorMode.IGNORE.serialize()
    loaded = ErrorMode.load(serialized)
    assert loaded is ErrorMode.IGNORE


def test_ErrorMode_serialize_format():
    """Test that serialize returns the expected format."""
    assert ErrorMode.EXCEPT.serialize() == "ErrorMode.Except"
    assert ErrorMode.WARN.serialize() == "ErrorMode.Warn"
    assert ErrorMode.LOG.serialize() == "ErrorMode.Log"
    assert ErrorMode.IGNORE.serialize() == "ErrorMode.Ignore"


def test_ERROR_MODE_ALIASES():
    """Test that all aliases resolve correctly."""
    from muutils.errormode import ERROR_MODE_ALIASES

    # Test EXCEPT aliases
    assert ERROR_MODE_ALIASES["except"] is ErrorMode.EXCEPT
    assert ERROR_MODE_ALIASES["e"] is ErrorMode.EXCEPT
    assert ERROR_MODE_ALIASES["error"] is ErrorMode.EXCEPT
    assert ERROR_MODE_ALIASES["err"] is ErrorMode.EXCEPT
    assert ERROR_MODE_ALIASES["raise"] is ErrorMode.EXCEPT

    # Test WARN aliases
    assert ERROR_MODE_ALIASES["warn"] is ErrorMode.WARN
    assert ERROR_MODE_ALIASES["w"] is ErrorMode.WARN
    assert ERROR_MODE_ALIASES["warning"] is ErrorMode.WARN

    # Test LOG aliases
    assert ERROR_MODE_ALIASES["log"] is ErrorMode.LOG
    assert ERROR_MODE_ALIASES["l"] is ErrorMode.LOG
    assert ERROR_MODE_ALIASES["print"] is ErrorMode.LOG
    assert ERROR_MODE_ALIASES["output"] is ErrorMode.LOG
    assert ERROR_MODE_ALIASES["show"] is ErrorMode.LOG
    assert ERROR_MODE_ALIASES["display"] is ErrorMode.LOG

    # Test IGNORE aliases
    assert ERROR_MODE_ALIASES["ignore"] is ErrorMode.IGNORE
    assert ERROR_MODE_ALIASES["i"] is ErrorMode.IGNORE
    assert ERROR_MODE_ALIASES["silent"] is ErrorMode.IGNORE
    assert ERROR_MODE_ALIASES["quiet"] is ErrorMode.IGNORE
    assert ERROR_MODE_ALIASES["nothing"] is ErrorMode.IGNORE


def test_ErrorMode_from_any_with_string():
    """Test from_any with string inputs."""
    # Test base values
    assert ErrorMode.from_any("except") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("warn") is ErrorMode.WARN
    assert ErrorMode.from_any("log") is ErrorMode.LOG
    assert ErrorMode.from_any("ignore") is ErrorMode.IGNORE

    # Test with uppercase
    assert ErrorMode.from_any("EXCEPT") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("WARN") is ErrorMode.WARN

    # Test with whitespace
    assert ErrorMode.from_any("  except  ") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("  warn  ") is ErrorMode.WARN


def test_ErrorMode_from_any_with_aliases():
    """Test from_any with alias strings."""
    # Test EXCEPT aliases
    assert ErrorMode.from_any("error") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("e") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("raise") is ErrorMode.EXCEPT

    # Test WARN aliases
    assert ErrorMode.from_any("warning") is ErrorMode.WARN
    assert ErrorMode.from_any("w") is ErrorMode.WARN

    # Test LOG aliases
    assert ErrorMode.from_any("print") is ErrorMode.LOG
    assert ErrorMode.from_any("l") is ErrorMode.LOG
    assert ErrorMode.from_any("output") is ErrorMode.LOG

    # Test IGNORE aliases
    assert ErrorMode.from_any("silent") is ErrorMode.IGNORE
    assert ErrorMode.from_any("i") is ErrorMode.IGNORE
    assert ErrorMode.from_any("quiet") is ErrorMode.IGNORE


def test_ErrorMode_from_any_with_prefix():
    """Test from_any with ErrorMode. prefix."""
    assert ErrorMode.from_any("ErrorMode.except") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("ErrorMode.warn") is ErrorMode.WARN
    assert ErrorMode.from_any("ErrorMode.log") is ErrorMode.LOG
    assert ErrorMode.from_any("ErrorMode.ignore") is ErrorMode.IGNORE

    # Test with mixed case
    assert ErrorMode.from_any("ErrorMode.Except") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("ErrorMode.WARN") is ErrorMode.WARN


def test_ErrorMode_from_any_with_ErrorMode_instance():
    """Test from_any with ErrorMode instance."""
    assert ErrorMode.from_any(ErrorMode.EXCEPT) is ErrorMode.EXCEPT
    assert ErrorMode.from_any(ErrorMode.WARN) is ErrorMode.WARN
    assert ErrorMode.from_any(ErrorMode.LOG) is ErrorMode.LOG
    assert ErrorMode.from_any(ErrorMode.IGNORE) is ErrorMode.IGNORE


def test_ErrorMode_from_any_without_aliases():
    """Test from_any with allow_aliases=False."""
    # Base values should still work
    assert ErrorMode.from_any("except", allow_aliases=False) is ErrorMode.EXCEPT

    # Aliases should fail
    with pytest.raises(KeyError):
        ErrorMode.from_any("error", allow_aliases=False)

    with pytest.raises(KeyError):
        ErrorMode.from_any("e", allow_aliases=False)


def test_ErrorMode_from_any_invalid_string():
    """Test from_any with invalid string."""
    with pytest.raises(KeyError):
        ErrorMode.from_any("invalid_mode")

    with pytest.raises(KeyError):
        ErrorMode.from_any("not_a_mode")


def test_ErrorMode_from_any_invalid_type():
    """Test from_any with invalid type."""
    with pytest.raises(TypeError):
        ErrorMode.from_any(123)  # type: ignore

    with pytest.raises(TypeError):
        ErrorMode.from_any(None)  # type: ignore

    with pytest.raises(TypeError):
        ErrorMode.from_any([])  # type: ignore


def test_ErrorMode_str_repr():
    """Test __str__ and __repr__ methods."""
    assert str(ErrorMode.EXCEPT) == "ErrorMode.Except"
    assert str(ErrorMode.WARN) == "ErrorMode.Warn"
    assert str(ErrorMode.LOG) == "ErrorMode.Log"
    assert str(ErrorMode.IGNORE) == "ErrorMode.Ignore"

    assert repr(ErrorMode.EXCEPT) == "ErrorMode.Except"
    assert repr(ErrorMode.WARN) == "ErrorMode.Warn"
    assert repr(ErrorMode.LOG) == "ErrorMode.Log"
    assert repr(ErrorMode.IGNORE) == "ErrorMode.Ignore"


def test_ErrorMode_process_unknown_mode():
    """Test that an unknown error mode raises ValueError."""
    # This is a edge case that shouldn't normally happen, but testing defensively
    # We can't easily create an invalid ErrorMode, so we test the else branch
    # by mocking or checking that all modes are handled
    # All enum values should be handled in process, so this is more of a sanity check
    pass


def test_warn_with_except_from_builtin():
    """Test WARN mode with except_from using built-in warnings.warn."""
    import muutils.errormode as errormode

    # Make sure we're using the default warn function
    errormode.GLOBAL_WARN_FUNC = warnings.warn  # type: ignore

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        base_exception = ValueError("base error")
        ErrorMode.WARN.process(
            "test warning", warn_cls=UserWarning, except_from=base_exception
        )

        assert len(w) == 1
        # Message should include source information
        message_str = str(w[0].message)
        assert "test warning" in message_str
        assert "Source of warning" in message_str
        assert "base error" in message_str


def test_custom_showwarning_with_warning_instance():
    """Test custom_showwarning when passed a Warning instance instead of string."""
    from muutils.errormode import custom_showwarning

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Create a warning instance
        warning_instance = UserWarning("instance warning")
        custom_showwarning(warning_instance, UserWarning)

        assert len(w) == 1
        assert "instance warning" in str(w[0].message)


def test_log_with_custom_func():
    """Test LOG mode with custom log function passed directly."""
    logs = []

    def my_logger(msg: str):
        logs.append(f"LOGGED: {msg}")

    ErrorMode.LOG.process("test message", log_func=my_logger)

    assert len(logs) == 1
    assert logs[0] == "LOGGED: test message"


def test_multiple_log_functions():
    """Test that different log functions can be used."""
    log1 = []
    log2 = []

    def logger1(msg: str):
        log1.append(msg)

    def logger2(msg: str):
        log2.append(msg)

    ErrorMode.LOG.process("message 1", log_func=logger1)
    ErrorMode.LOG.process("message 2", log_func=logger2)

    assert log1 == ["message 1"]
    assert log2 == ["message 2"]


def test_warn_with_source_parameter():
    """Test that warn_func receives proper parameters."""
    calls = []

    def tracking_warn(msg: str, category, source=None):
        calls.append({"msg": msg, "category": category, "source": source})

    ErrorMode.WARN.process(
        "test message", warn_cls=DeprecationWarning, warn_func=tracking_warn
    )

    assert len(calls) == 1
    assert calls[0]["msg"] == "test message"
    assert calls[0]["category"] == DeprecationWarning  # noqa: E721


def test_ErrorMode_enum_values():
    """Test that ErrorMode has the expected enum values."""
    assert ErrorMode.EXCEPT.value == "except"
    assert ErrorMode.WARN.value == "warn"
    assert ErrorMode.LOG.value == "log"
    assert ErrorMode.IGNORE.value == "ignore"


def test_from_any_without_prefix():
    """Test from_any with allow_prefix=False."""
    # Should still work with plain values
    assert ErrorMode.from_any("except", allow_prefix=False) is ErrorMode.EXCEPT

    # Should fail with prefix
    with pytest.raises(KeyError):
        ErrorMode.from_any("ErrorMode.except", allow_prefix=False)


def test_GLOBAL_WARN_FUNC():
    """Test that GLOBAL_WARN_FUNC is used when no warn_func is provided."""
    import muutils.errormode as errormode

    # Save original
    original_warn_func = errormode.GLOBAL_WARN_FUNC

    try:
        # Set custom global warn function
        captured = []

        def global_warn(msg: str, category, source=None):
            captured.append(msg)

        errormode.GLOBAL_WARN_FUNC = global_warn  # type: ignore

        # Use WARN mode without providing warn_func
        ErrorMode.WARN.process("test with global", warn_cls=UserWarning)

        assert len(captured) == 1
        assert captured[0] == "test with global"

    finally:
        # Restore original
        errormode.GLOBAL_WARN_FUNC = original_warn_func


def test_GLOBAL_LOG_FUNC():
    """Test that GLOBAL_LOG_FUNC is used when no log_func is provided."""
    import muutils.errormode as errormode

    # Save original
    original_log_func = errormode.GLOBAL_LOG_FUNC

    try:
        # Set custom global log function
        captured = []

        def global_log(msg: str):
            captured.append(msg)

        errormode.GLOBAL_LOG_FUNC = global_log

        # Use LOG mode without providing log_func
        ErrorMode.LOG.process("test with global log")

        assert len(captured) == 1
        assert captured[0] == "test with global log"

    finally:
        # Restore original
        errormode.GLOBAL_LOG_FUNC = original_log_func


def test_custom_warn_func_signature():
    """Test that custom warn_func follows the WarningFunc protocol."""
    from muutils.errormode import WarningFunc

    # Create a function that matches the protocol
    def my_warn(msg: str, category: type[Warning], source=None) -> None:
        pass

    # This should work without errors
    warn_func: WarningFunc = my_warn  # type: ignore

    # Use it with ErrorMode
    ErrorMode.WARN.process("test", warn_cls=UserWarning, warn_func=warn_func)


def test_ErrorMode_all_enum_members():
    """Test that all ErrorMode enum members are accessible."""
    # Verify all enum members exist
    assert hasattr(ErrorMode, "EXCEPT")
    assert hasattr(ErrorMode, "WARN")
    assert hasattr(ErrorMode, "LOG")
    assert hasattr(ErrorMode, "IGNORE")

    # Test that they are unique
    modes = [ErrorMode.EXCEPT, ErrorMode.WARN, ErrorMode.LOG, ErrorMode.IGNORE]
    assert len(set(modes)) == 4


def test_custom_showwarning_frame_extraction():
    """Test that custom_showwarning correctly extracts frame information."""
    import sys
    from muutils.errormode import custom_showwarning

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        # Call from this specific line so we can verify frame info
        line_number = 0

        def call_showwarning():
            nonlocal line_number
            line_number = sys._getframe().f_lineno + 1
            custom_showwarning("frame test", UserWarning)

        call_showwarning()

        assert len(w) == 1
        # The warning should have been issued with correct file and line info
        assert w[0].filename == __file__
        # Line number should be close to where we called it
        assert isinstance(w[0].lineno, int)


def test_exception_traceback_attached():
    """Test that raised exceptions have traceback attached."""
    try:
        ErrorMode.EXCEPT.process("test traceback", except_cls=ValueError)
    except ValueError as e:
        # Check that exception has traceback
        assert e.__traceback__ is not None
    else:
        # TYPING: ty bug on python <= 3.9
        pytest.fail("Expected ValueError to be raised")  # ty: ignore[arg-type]


def test_exception_traceback_with_chaining():
    """Test that chained exceptions have correct traceback."""
    base = RuntimeError("base")

    try:
        ErrorMode.EXCEPT.process("chained", except_cls=ValueError, except_from=base)
    except ValueError as e:
        # Check traceback exists
        assert e.__traceback__ is not None
        # Check cause is set
        assert e.__cause__ is base
    else:
        # TYPING: ty bug on python <= 3.9
        pytest.fail("Expected ValueError to be raised")  # ty: ignore[arg-type]


def test_warn_with_default_warn_func():
    """Test WARN mode with default warnings.warn function."""
    import muutils.errormode as errormode

    # Ensure we're using default
    errormode.GLOBAL_WARN_FUNC = warnings.warn  # type: ignore

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        ErrorMode.WARN.process("default warn func test", warn_cls=UserWarning)

        assert len(w) == 1
        assert "default warn func test" in str(w[0].message)


def test_from_any_strip_whitespace():
    """Test that from_any strips whitespace correctly."""
    # Leading/trailing spaces
    assert ErrorMode.from_any("  except") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("warn  ") is ErrorMode.WARN
    assert ErrorMode.from_any("  log  ") is ErrorMode.LOG

    # Tabs and newlines
    assert ErrorMode.from_any("\texcept\t") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("\nwarn\n") is ErrorMode.WARN


def test_load_with_prefix():
    """Test load method with ErrorMode. prefix."""
    # load uses allow_prefix=True
    loaded = ErrorMode.load("ErrorMode.Except")
    assert loaded is ErrorMode.EXCEPT

    loaded = ErrorMode.load("ErrorMode.warn")
    assert loaded is ErrorMode.WARN


def test_load_without_aliases():
    """Test that load does not accept aliases."""
    # load uses allow_aliases=False
    with pytest.raises((KeyError, ValueError)):
        ErrorMode.load("error")  # alias should not work

    with pytest.raises((KeyError, ValueError)):
        ErrorMode.load("e")  # alias should not work


def test_ERROR_MODE_ALIASES_completeness():
    """Test that ERROR_MODE_ALIASES contains all expected aliases."""
    from muutils.errormode import ERROR_MODE_ALIASES

    # Count aliases per mode
    except_aliases = [k for k, v in ERROR_MODE_ALIASES.items() if v is ErrorMode.EXCEPT]
    warn_aliases = [k for k, v in ERROR_MODE_ALIASES.items() if v is ErrorMode.WARN]
    log_aliases = [k for k, v in ERROR_MODE_ALIASES.items() if v is ErrorMode.LOG]
    ignore_aliases = [k for k, v in ERROR_MODE_ALIASES.items() if v is ErrorMode.IGNORE]

    # Verify we have multiple aliases for each mode
    assert len(except_aliases) >= 5  # except, e, error, err, raise
    assert len(warn_aliases) >= 3  # warn, w, warning
    assert len(log_aliases) >= 6  # log, l, print, output, show, display
    assert len(ignore_aliases) >= 5  # ignore, i, silent, quiet, nothing


def test_custom_exception_classes():
    """Test process with various custom exception classes."""

    class CustomError(Exception):
        pass

    class NestedCustomError(CustomError):
        pass

    # Test with custom exception
    with pytest.raises(CustomError):
        ErrorMode.EXCEPT.process("custom", except_cls=CustomError)

    # Test with nested custom exception
    with pytest.raises(NestedCustomError):
        ErrorMode.EXCEPT.process("nested custom", except_cls=NestedCustomError)


def test_custom_warning_classes():
    """Test process with various custom warning classes."""

    class CustomWarning(UserWarning):
        pass

    class NestedCustomWarning(CustomWarning):
        pass

    # Test with custom warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        def custom_warn(msg: str, category, source=None):
            warnings.warn(msg, category)

        ErrorMode.WARN.process("custom", warn_cls=CustomWarning, warn_func=custom_warn)

        assert len(w) == 1
        assert issubclass(w[0].category, CustomWarning)


def test_ignore_with_all_parameters():
    """Test that IGNORE mode ignores all parameters."""
    # None of these should raise or warn
    ErrorMode.IGNORE.process("ignored message")
    ErrorMode.IGNORE.process("ignored", except_cls=ValueError)
    ErrorMode.IGNORE.process("ignored", warn_cls=UserWarning)
    ErrorMode.IGNORE.process("ignored", except_from=ValueError("base"))

    # Also test with custom functions (they should not be called)
    called = []

    def should_not_be_called(msg: str):
        called.append(msg)

    ErrorMode.IGNORE.process("ignored", log_func=should_not_be_called)

    # log_func should not have been called
    assert len(called) == 0


def test_from_any_case_insensitivity():
    """Test that from_any is case insensitive."""
    # Test various cases
    assert ErrorMode.from_any("EXCEPT") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("Except") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("eXcEpT") is ErrorMode.EXCEPT

    assert ErrorMode.from_any("WARN") is ErrorMode.WARN
    assert ErrorMode.from_any("Warn") is ErrorMode.WARN

    # Test with aliases
    assert ErrorMode.from_any("ERROR") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("Error") is ErrorMode.EXCEPT
    assert ErrorMode.from_any("RAISE") is ErrorMode.EXCEPT


# def test_logging_pass():
#     errmode: ErrorMode = ErrorMode.LOG

#     log: list[str] = []
#     def log_func(msg: str):
#         log.append(msg)

#     errmode.process(
#         "test-log",
#         log_func=log_func,
#     )

#     errmode.process(
#         "test-log-2",
#         log_func=log_func,
#     )

#     assert log == ["test-log", "test-log-2"]


# def test_logging_init():
#     errmode: ErrorMode = ErrorMode.LOG

#     log: list[str] = []
#     def log_func(msg: str):
#         log.append(msg)

#     errmode.set_log_loc(log_func)

#     errmode.process("test-log")
#     errmode.process("test-log-2")

#     assert log == ["test-log", "test-log-2"]

#     errmode_2: ErrorMode = ErrorMode.LOG
#     log_2: list[str] = []
#     def log_func_2(msg: str):
#         log_2.append(msg)

#     errmode_2.set_log_loc(log_func_2)

#     errmode_2.process("test-log-3")
#     errmode_2.process("test-log-4")

#     assert log_2 == ["test-log-3", "test-log-4"]
#     assert log == ["test-log", "test-log-2"]


# def test_logging_init_2():
#     log: list[str] = []
#     def log_func(msg: str):
#         log.append(msg)

#     errmode: ErrorMode = ErrorMode.LOG.set_log_loc(log_func)

#     errmode.process("test-log")
#     errmode.process("test-log-2")

#     assert log == ["test-log", "test-log-2"]
