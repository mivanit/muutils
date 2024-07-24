from typing import Callable, Any
import time

from muutils.spinner import spinner_decorator


def test_spinner_simple():
    @spinner_decorator(show_elapsed_time=True, update_interval=0.05)
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
        format_string="Current value: {}",
        mutable_kwarg_key="update_status",
        show_elapsed_time=True,
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
