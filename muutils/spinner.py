import time
import threading
import sys
from functools import wraps
from typing import Callable, Any, Optional, TypeVar, Sequence

# Define a generic type for the decorated function
DecoratedFunction = TypeVar("DecoratedFunction", bound=Callable[..., Any])


def spinner_decorator(
    format_string: Optional[str] = None,
    mutable_kwarg_key: Optional[str] = None,
    show_elapsed_time: bool = True,
    spinner_chars: Sequence[str] = ("|", "/", "-", "\\"),
    time_fstring: str = "({elapsed_time:.2f}s)",
    update_interval: float = 0.1,
) -> Callable[[DecoratedFunction], DecoratedFunction]:
    """
    A decorator that displays a spinner, and optionally elapsed time and a mutable value while a function is running.

    Args:
    format_string (Optional[str]): A format string for displaying the mutable value.
    mutable_kwarg_key (Optional[str]): The keyword argument name for the update function in the decorated function. If None, mutable value feature is disabled.
    show_elapsed_time (bool): Whether to display the elapsed time.

    Returns:
    Callable[[F], F]: A decorator function.
    """

    def decorator(func: DecoratedFunction) -> DecoratedFunction:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time: float = time.time()
            stop_spinner: threading.Event = threading.Event()
            current_value: list[str] = [""] if mutable_kwarg_key else []

            def spin() -> None:
                """
                Function to run in a separate thread, displaying the spinner and optional information.
                """
                i: int = 0
                while not stop_spinner.is_set():
                    spinner: str = spinner_chars[i % len(spinner_chars)]

                    # Construct the display string
                    display_parts: list[str] = [f"\r{spinner}"]

                    if show_elapsed_time:
                        elapsed_time: float = time.time() - start_time
                        display_parts.append(
                            time_fstring.format(elapsed_time=elapsed_time)
                        )

                    if mutable_kwarg_key and current_value:
                        if format_string:
                            display_parts.append(format_string.format(current_value[0]))
                        else:
                            display_parts.append(str(current_value[0]))

                    display: str = " ".join(display_parts)
                    sys.stdout.write(display)
                    sys.stdout.flush()
                    time.sleep(update_interval)
                    i += 1

            # Start the spinner thread
            spinner_thread: threading.Thread = threading.Thread(target=spin)
            spinner_thread.start()

            if mutable_kwarg_key:

                def update_value(new_value: Any) -> None:
                    "update the current value displayed by the spinner"
                    current_value[0] = new_value

                # Add the update_value function to kwargs only if mutable_kwarg_key is not None
                kwargs[mutable_kwarg_key] = update_value

            try:
                # Call the decorated function
                result: Any = func(*args, **kwargs)
            finally:
                # Stop the spinner thread
                stop_spinner.set()
                spinner_thread.join()
                sys.stdout.write("\n")
                sys.stdout.flush()

            return result

        return wrapper  # type: ignore

    return decorator
