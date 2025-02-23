import io
import time
from typing import Callable, Any

import pytest

from muutils.spinner import (
    SPINNERS,
    spinner_decorator,
    SpinnerContext,
    Spinner,
    SpinnerConfig,
)


def test_spinner_simple():
    @spinner_decorator(update_interval=0.05)
    def long_running_function_simple() -> str:
        """
        An example function decorated with spinner_decorator, using only the spinner and elapsed time.

        Returns:
        str: A completion message.
        """
        for _ in range(1):
            time.sleep(0.1)  # Simulate some work
        return "Simple function completed"

    print("\nRunning simple function with only spinner and elapsed time:")
    result2: str = long_running_function_simple()
    print(result2)


def test_spinner_complex():
    # Example usage
    @spinner_decorator(
        message="Current value: ",
        mutable_kwarg_key="update_status",
        update_interval=0.05,
    )
    def long_running_function_with_status(
        normal_arg: int, update_status: Callable[[Any], None]
    ) -> str:
        """
        An example function decorated with spinner_decorator, using all features.

        Args:
        normal_arg (int): A normal argument to demonstrate that other arguments still work.
        update_status (Callable[[Any], None]): Function to update the status displayed by the spinner.

        Returns:
        str: A completion message.
        """
        for i in range(normal_arg):
            time.sleep(0.1)  # Simulate some work
            update_status(f"Step {i+1} of {normal_arg}")
        return "Function with status completed"

    # Run the example functions
    print("Running function with status updates:")
    result1: str = long_running_function_with_status(1)  # type: ignore[call-arg]
    print(result1)


def test_spinner_decorator_bare():
    @spinner_decorator()
    def example_function():
        return "Done"

    result = example_function()
    assert result == "Done"


def test_spinner_ctx_mgr():
    with SpinnerContext(message="Current value: ", update_interval=0.05) as spinner:
        for i in range(1):
            time.sleep(0.1)
            spinner.update_value(f"Step {i+1}")
    print("Done!")


def test_spinner_initialization():
    spinner = Spinner()
    assert isinstance(spinner, Spinner)
    assert isinstance(spinner.config.working, list)
    assert isinstance(spinner.config.success, str)
    assert isinstance(spinner.config.fail, str)
    assert isinstance(spinner.update_interval, float)
    assert isinstance(spinner.current_value, str)
    assert isinstance(spinner.message, str)
    assert isinstance(spinner.format_string, str)
    assert hasattr(spinner.output_stream, "write")
    assert callable(spinner.output_stream.write)
    assert callable(spinner.update_value)

    assert spinner.config.working == ["|", "/", "-", "\\"]
    assert spinner.format_string == "\r{spinner} ({elapsed_time:.2f}s) {message}{value}"
    assert spinner.update_interval == 0.1


def test_spinner_update_value():
    spinner = Spinner()
    spinner.update_value("Test")
    assert spinner.current_value == "Test"


def test_spinner_context_manager():
    string_io = io.StringIO()
    with SpinnerContext(output_stream=string_io):
        pass
    assert string_io.getvalue().endswith("\n")


@spinner_decorator()
def example_function():
    return "Done"


def test_spinner_decorator():
    result = example_function()
    assert result == "Done"


def test_spinner_custom_chars():
    spinner = Spinner(config=["A", "B", "C"])
    assert spinner.config.working == ["A", "B", "C"]


def test_spinner_custom_time_format():
    spinner = Spinner(format_string="[{elapsed_time:.1f}s]")
    assert spinner.format_string == "[{elapsed_time:.1f}s]"


def test_spinner_context_manager_with_updates():
    string_io = io.StringIO()
    with SpinnerContext(
        message="Status: ", output_stream=string_io, update_interval=0.05
    ) as spinner:
        spinner.update_value("Working")
        time.sleep(0.1)
        spinner.update_value("Finishing")
        time.sleep(0.1)

    output = string_io.getvalue()
    print(output)
    assert "Status: Working" in output
    assert "Status: Finishing" in output


def test_spinner_context_exception_handling():
    string_io = io.StringIO()
    try:
        with SpinnerContext(output_stream=string_io, update_interval=0.05) as spinner:
            spinner.update_value("Before exception")
            time.sleep(0.1)
            raise ValueError("Test exception")
    except ValueError:
        pass

    output = string_io.getvalue()
    print(output)
    assert "Before exception" in output
    assert output.endswith("\n")


def test_spinner_long_running_task():
    string_io = io.StringIO()

    @spinner_decorator(
        message="Iteration: ",
        output_stream=string_io,
        update_interval=0.05,
        mutable_kwarg_key="update",
    )
    def long_task(iterations, update):
        for i in range(iterations):
            update(i + 1)
            time.sleep(0.1)

    long_task(3, update=lambda x: x)

    output = string_io.getvalue()
    print(output)
    for i in range(1, 4):
        assert f"Iteration: {i}" in output


def test_spinner_init_from_config():
    """Test various ways of initializing spinner with config parameter"""
    # From string key
    sp1 = Spinner(config="clock")
    assert sp1.config.working == [
        "🕛",
        "🕐",
        "🕑",
        "🕒",
        "🕓",
        "🕔",
        "🕕",
        "🕖",
        "🕗",
        "🕘",
        "🕙",
        "🕚",
    ]
    assert sp1.config.success == "✔️"
    assert sp1.config.fail == "❌"

    # From list
    sp2 = Spinner(config=["A", "B", "C"])
    assert sp2.config.working == ["A", "B", "C"]
    assert sp2.config.success == "✔️"  # Default
    assert sp2.config.fail == "❌"  # Default

    # From dict
    sp3 = Spinner(config=dict(working=["1", "2"], success="OK", fail="NO"))
    assert sp3.config.working == ["1", "2"]
    assert sp3.config.success == "OK"
    assert sp3.config.fail == "NO"

    # From SpinnerConfig
    cfg = SpinnerConfig(working=["X", "Y"], success="DONE", fail="FAIL")
    sp4 = Spinner(config=cfg)
    assert sp4.config.working == ["X", "Y"]
    assert sp4.config.success == "DONE"
    assert sp4.config.fail == "FAIL"


def test_spinner_exception_messages():
    """Test that exception messages are preserved during spinner execution"""
    string_io = io.StringIO()
    custom_message = "Custom error occurred!"

    # Test with context manager
    try:
        with SpinnerContext(output_stream=string_io, message="Processing: ") as spinner:
            spinner.update_value("Step 1")
            time.sleep(0.1)
            raise ValueError(custom_message)
    except ValueError as e:
        assert str(e) == custom_message
        output = string_io.getvalue()
        assert "Processing: Step 1" in output
        assert output.count("\n") == 1  # Should have exactly one newline at the end

    # Test with decorator
    string_io = io.StringIO()

    @spinner_decorator(output_stream=string_io, message="Working: ")
    def failing_function():
        time.sleep(0.1)
        raise RuntimeError(custom_message)

    with pytest.raises(RuntimeError) as exc_info:
        failing_function()

    assert str(exc_info.value) == custom_message
    output = string_io.getvalue()
    assert "Working: " in output
    assert output.count("\n") == 1


def test_spinner_state_transitions():
    """Test that spinner state transitions work correctly"""
    spinner = Spinner()
    assert spinner.state == "initialized"

    spinner.start()
    assert spinner.state == "running"

    spinner.stop()
    assert spinner.state == "success"

    # New spinner for failure test
    spinner = Spinner()
    spinner.start()
    spinner.stop(failed=True)
    assert spinner.state == "fail"


def test_spinner_nested():
    """Test nested spinners behavior"""
    string_io = io.StringIO()

    with SpinnerContext(output_stream=string_io, message="Outer: ") as outer:
        outer.update_value("Step 1")
        time.sleep(0.1)

        with SpinnerContext(output_stream=string_io, message="Inner: ") as inner:
            inner.update_value("Processing")
            time.sleep(0.1)

        outer.update_value("Step 2")
        time.sleep(0.1)

    output = string_io.getvalue()
    assert "Outer: Step 1" in output
    assert "Inner: Processing" in output
    assert "Outer: Step 2" in output


def test_spinner_value_updates():
    """Test that the spinner correctly stores and formats values"""
    spinner = Spinner(format_string="{spinner} {value}")

    # Test various types of values
    test_values = [
        42,
        3.14,
        ["a", "b", "c"],
        {"key": "value"},
        (1, 2, 3),
        None,
        True,
        b"bytes",
    ]

    for value in test_values:
        spinner.update_value(value)
        assert spinner.current_value == value

        # Test format string rendering without output stream
        rendered = spinner.format_string.format(
            spinner=spinner.config.working[0], elapsed_time=0.0, message="", value=value
        )
        assert str(value) in rendered


@pytest.mark.skip(
    reason="""shows a warning:
tests/unit/test_spinner.py::test_spinner_output_stream_errors
  .venv/Lib/site-packages/_pytest/threadexception.py:82: PytestUnhandledThreadExceptionWarning: Exception in thread Thread-16 (spin)      

  Traceback (most recent call last):
    File "Lib/threading.py", line 1052, in _bootstrap_inner
      self.run()
    File "Lib/threading.py", line 989, in run
      self._target(*self._args, **self._kwargs)
    File "muutils/spinner.py", line 369, in spin
      self.output_stream.write(output)
    File "tests/unit/test_spinner.py", line 328, in write
      raise IOError("Write failed")
  OSError: Write failed

    warnings.warn(pytest.PytestUnhandledThreadExceptionWarning(msg))

"""
)
def test_spinner_output_stream_errors():
    """Test spinner behavior with problematic output streams"""

    class BrokenStream:
        def write(self, _):
            raise IOError("Write failed")

        def flush(self):
            raise IOError("Flush failed")

    # Test with broken stream
    with pytest.raises(IOError):
        with SpinnerContext(output_stream=BrokenStream()):  # type: ignore
            time.sleep(0.01)


def test_spinner_width_calculations():
    """Test that individual updates are width-compliant"""
    narrow_width = 40
    spinner = Spinner()
    spinner.term_width = narrow_width

    test_value = "ABC"
    spinner.update_value(test_value)

    # Format a single update line
    output_line = spinner.format_string.format(
        spinner=spinner.config.working[0],
        elapsed_time=0.0,
        message="Test: ",
        value=test_value,
    ).rstrip()  # Remove any trailing spaces but keep \r

    # Check the actual content length (excluding \r)
    content_length = len(output_line.replace("\r", ""))
    assert (
        content_length <= narrow_width
    ), f"Line too long: {content_length} > {narrow_width}"


def test_format_string_updates():
    """Test that format_string_when_updated modifies the formatting as expected"""
    spinner = Spinner(
        format_string="Normal: {value}", format_string_when_updated="Update: {value}"
    )

    # Test normal format
    normal = spinner.format_string.format(
        spinner=spinner.config.working[0], elapsed_time=0.0, message="", value="test"
    )
    assert normal.startswith("Normal: ")

    # Test update format
    spinner.value_changed = True
    if spinner.format_string_when_updated:
        update = spinner.format_string_when_updated.format(
            spinner=spinner.config.working[0],
            elapsed_time=0.0,
            message="",
            value="test",
        )
        assert update.startswith("Update: ")


def test_spinner_state_handling():
    """Test spinner state transitions and error handling"""
    spinner = Spinner()
    assert spinner.state == "initialized"

    # Test normal flow
    spinner.start()
    assert spinner.state == "running"
    spinner.stop(failed=False)
    assert spinner.state == "success"

    # Test error flow
    spinner = Spinner()
    spinner.start()
    spinner.stop(failed=True)
    assert spinner.state == "fail"

    # Test context manager error handling
    error_caught = False
    try:
        with SpinnerContext() as sp:
            raise ValueError("Test error")
    except ValueError:
        error_caught = True
        assert sp.state == "fail"

    assert error_caught, "Context manager should propagate errors"


@pytest.mark.parametrize(
    "kwargs, expected_substrings, find_all",
    [
        (
            # Input
            dict(
                format_string="Test: {message}{value}",  # Include message placeholder
                message="MSG:",
                initial_value="VAL",
            ),
            # Expected substrings
            ["Test:", "MSG:", "VAL"],
            True,
        ),
        (
            # Input with empty values
            dict(format_string="{spinner}{value}", message="", initial_value=""),
            # Should at least contain a spinner char
            [char for char in Spinner().config.working],
            False,
        ),
    ],
)
def test_spinner_output_formatting(kwargs, expected_substrings, find_all):
    """Test that spinner formatting is applied correctly without checking exact output"""

    spinner = Spinner(**kwargs)
    # Test format string compilation
    output = spinner.format_string.format(
        spinner=spinner.config.working[0],
        elapsed_time=0.0,
        message=spinner.message,
        value=spinner.current_value,
    )

    # Verify required parts are present
    if find_all:
        for part in expected_substrings:
            assert part in output, f"Missing {part} in output: {output}"
    else:
        found = False
        for part in expected_substrings:
            if part in output:
                found = True
                break
        assert found, f"None of {expected_substrings} found in output: {output}"


@pytest.mark.parametrize(
    "config",
    [
        "default",
        "clock",
        ["A", "B"],
        ["A", "B", "C"],
        dict(),
        dict(working=["X", "Y"]),
        dict(success="OK"),
        dict(fail="NO"),
        dict(working=["1", "2"], success="OK"),
        dict(working=["1", "2"], fail="NO"),
        dict(success="OK", fail="NO"),
        dict(working=["1", "2"], success="OK", fail="NO"),
        SpinnerConfig(working=["1", "2"]),
        SpinnerConfig(working=["1", "2"], success="OK", fail="NO"),
    ],
)
def test_spinner_config_validation(config):
    """Test that spinner configuration is validated correctly"""
    sp = Spinner(config=config)
    if isinstance(config, str):
        pass
    elif isinstance(config, list):
        assert sp.config.working == config
    elif isinstance(config, dict):
        if "working" in config:
            assert sp.config.working == config["working"]
        if "success" in config:
            assert sp.config.success == config["success"]
        if "fail" in config:
            assert sp.config.fail == config["fail"]
    elif isinstance(config, SpinnerConfig):
        assert sp.config == config
        assert sp.config.working == config.working
        assert sp.config.success == config.success
        assert sp.config.fail == config.fail


@pytest.mark.parametrize(
    "kwargs, exception_type",
    [
        (dict(config=123), TypeError),
        (dict(config=123.45), TypeError),
        (dict(config=True), TypeError),
        (dict(config=None), TypeError),
        (dict(config=""), KeyError),
        (dict(config="nonexistent_style"), KeyError),
        (dict(config=[]), ValueError),
        (dict(config=dict(nonexistent_key="stuff")), TypeError),
        (dict(format_string="{invalid_key}"), ValueError),
        (dict(unknown_param=123), ValueError),
    ],
)
def test_spinner_init_invalid(kwargs, exception_type):
    """Test invalid initialization scenarios"""
    with pytest.raises(exception_type):
        Spinner(**kwargs)


@pytest.mark.parametrize(
    "config,expected",
    [
        # ASCII-only configurations
        (SpinnerConfig(working=["|", "/", "-", "\\"], success="#", fail="X"), True),
        (SpinnerConfig(working=[".", "o", "O"], success="*", fail="x"), True),
        (SpinnerConfig(working=["[   ]", "[-  ]"], success="[--]", fail="[XX]"), True),
        # Non-ASCII configurations
        (SpinnerConfig(working=["←", "↑", "→", "↓"], success="►", fail="✖"), False),
        (SpinnerConfig(working=["🌍", "🌎", "🌏"], success="✔️", fail="❌"), False),
        (SpinnerConfig(working=["⠋", "⠙", "⠹"], success="⣿", fail="⢿"), False),
        # Mixed ASCII and Unicode
        (SpinnerConfig(working=["->", "=>", "→"], success="✓", fail="X"), False),
        # Whitespace
        (SpinnerConfig(working=["  ", " |", "| "], success=" ", fail=" "), True),
    ],
)
def test_is_ascii(config: SpinnerConfig, expected: bool):
    """Test is_ascii() method with various configurations"""
    assert config.is_ascii() is expected


@pytest.mark.parametrize(
    "config,expected",
    [
        # Equal length configurations
        (SpinnerConfig(working=["abc", "def", "ghi"], success="xyz", fail="err"), True),
        (SpinnerConfig(working=["🌍 ", "🌎 ", "🌏 "], success="✔️ ", fail="❌ "), False),
        (SpinnerConfig(working=["[=]", "[-]", "[|]"], success="[#]", fail="[X]"), True),
        # Varying length configurations
        (SpinnerConfig(working=[".", "..", "..."], success="***", fail="x"), False),
        (
            SpinnerConfig(
                working=["[    ]", "[=   ]", "[===]"], success="[==]", fail="[X]"
            ),
            False,
        ),
        (
            SpinnerConfig(working=["📡   ", "📡·  ", "📡···"], success="📡", fail="❌"),
            False,
        ),
        # Whitespace variations
        (SpinnerConfig(working=["  ", "   ", "    "], success=" ", fail="  "), False),
        # Single characters
        (SpinnerConfig(working=["a", "b", "c"], success="x", fail="y"), True),
    ],
)
def test_eq_lens(config: SpinnerConfig, expected: bool):
    """Test eq_lens() method with various configurations"""
    assert config.eq_lens() is expected


@pytest.mark.parametrize(
    "config",
    [
        # Valid configurations
        SpinnerConfig(working=["|", "/", "-", "\\"], success="#", fail="X"),
        SpinnerConfig(working=["🌍", "🌎", "🌏"], success="✔️", fail="❌"),
        SpinnerConfig(working=["⠋"], success="⣿", fail="⢿"),  # Single working char
        SpinnerConfig(working=[""], success="", fail=""),  # Empty strings
    ],
)
def test_valid_configs(config: SpinnerConfig):
    """Test valid spinner configurations"""
    assert config.is_valid() is True


@pytest.mark.parametrize(
    "invalid_config",
    [
        # Invalid working list type
        pytest.param(
            lambda: SpinnerConfig(working="|/-\\", success="#", fail="X"),  # type: ignore[arg-type]
            id="string-instead-of-list",
        ),
        # Invalid working list contents
        pytest.param(
            lambda: SpinnerConfig(working=[1, 2, 3], success="#", fail="X"),  # type: ignore[list-item]
            id="non-string-items",
        ),
        # Invalid success type
        pytest.param(
            lambda: SpinnerConfig(working=["|", "/"], success=123, fail="X"),  # type: ignore[arg-type]
            id="non-string-success",
        ),
        # Invalid fail type
        pytest.param(
            lambda: SpinnerConfig(working=["|", "/"], success="#", fail=None),  # type: ignore[arg-type]
            id="none-fail",
        ),
        # Empty working list
        pytest.param(
            lambda: SpinnerConfig(working=[], success="#", fail="X"),
            id="empty-working-list",
        ),
    ],
)
def test_invalid_configs(invalid_config):
    """Test that invalid configurations raise ValueError"""
    with pytest.raises(ValueError):
        invalid_config()


@pytest.mark.parametrize(
    "config,ascii_result,eq_lens_result",
    [
        # Mixed ASCII/Unicode test cases
        (
            SpinnerConfig(working=["->", "=>", "→"], success="✓", fail="X"),
            False,  # is_ascii
            False,  # eq_lens
        ),
        # Multi-byte Unicode test cases
        (
            SpinnerConfig(working=["🌍", "🌎"], success="🎉", fail="💥"),
            False,  # is_ascii
            True,  # eq_lens
        ),
        # Whitespace test cases
        (
            SpinnerConfig(working=["  ", " |", "| "], success="VV", fail="XX"),
            True,  # is_ascii
            True,  # eq_lens
        ),
        # Empty string test cases
        (
            SpinnerConfig(working=[""], success="", fail=""),
            True,  # is_ascii
            True,  # eq_lens
        ),
    ],
)
def test_combined_validations(
    config: SpinnerConfig, ascii_result: bool, eq_lens_result: bool
):
    """Test multiple validation methods together"""
    assert config.is_valid() is True
    assert config.is_ascii() is ascii_result
    assert config.eq_lens() is eq_lens_result


# Additional edge cases and stress tests
@pytest.mark.parametrize(
    "test_input,expected_valid",
    [
        # Very long strings
        (
            SpinnerConfig(
                working=["a" * 1000, "b" * 1000], success="c" * 1000, fail="d" * 1000
            ),
            True,
        ),
        # Special characters
        (SpinnerConfig(working=["\n", "\t", "\r"], success="\n", fail="\r"), True),
        # Mixed newlines and spaces
        (SpinnerConfig(working=[" \n ", " \t ", " \r "], success=" ", fail=" "), True),
    ],
)
def test_edge_cases(test_input: SpinnerConfig, expected_valid: bool):
    """Test edge cases and special scenarios"""
    assert test_input.is_valid() is expected_valid


@pytest.mark.parametrize(
    "name, config",
    list(SPINNERS.items()),
)
def test_all(name: str, config: SpinnerConfig):
    """Test all spinner configurations"""
    assert config.is_valid()
    # just test the methods run, they won't all be ASCII or equal length
    config.is_ascii()
    config.eq_lens()

    # creating config from this config
    assert SpinnerConfig.from_any(name) == config
    assert SpinnerConfig.from_any(config) == config
    assert (
        SpinnerConfig.from_any(
            dict(working=config.working, success=config.success, fail=config.fail)
        )
        == config
    )
