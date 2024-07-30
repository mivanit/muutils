from typing import Callable, Any
import time


import io

from muutils.spinner import spinner_decorator, SpinnerContext, Spinner


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
    result1: str = long_running_function_with_status(1)
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
    assert isinstance(spinner.spinner_chars, list)
    assert isinstance(spinner.update_interval, float)
    assert isinstance(spinner.spinner_complete, str)
    assert isinstance(spinner.current_value, str)
    assert isinstance(spinner.message, str)
    assert isinstance(spinner.format_string, str)
    assert hasattr(spinner.output_stream, "write")
    assert callable(spinner.output_stream.write)
    assert callable(spinner.update_value)

    assert spinner.spinner_chars == ["|", "/", "-", "\\"]
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
    spinner = Spinner(spinner_chars=["A", "B", "C"])
    assert spinner.spinner_chars == ["A", "B", "C"]


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
