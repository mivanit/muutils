import time
import threading
import sys
from functools import wraps
from typing import Callable, Any, Optional, TextIO, TypeVar, Sequence

# Define a generic type for the decorated function
DecoratedFunction = TypeVar("DecoratedFunction", bound=Callable[..., Any])


class Spinner:
    """
    Base class for spinner functionality.
    """

    def __init__(
        self,
        format_string: Optional[str] = None,
        show_elapsed_time: bool = True,
        spinner_chars: Sequence[str] = ("|", "/", "-", "\\"),
        time_fstring: str = "({elapsed_time:.2f}s)",
        update_interval: float = 0.1,
        output_stream: TextIO = sys.stdout,
        initial_value: str = "_",
    ):
        # copy args
        self.format_string: Optional[str] = format_string
        self.show_elapsed_time: bool = show_elapsed_time
        self.spinner_chars: Sequence[str] = spinner_chars
        self.time_fstring: str = time_fstring
        self.update_interval: float = update_interval
        self.output_stream: TextIO = output_stream

        # init
        self.start_time: float = 0
        self.stop_spinner: threading.Event = threading.Event()
        self.current_value: str = initial_value
        self.spinner_thread: Optional[threading.Thread] = None

    def spin(self) -> None:
        """
        Function to run in a separate thread, displaying the spinner and optional information.
        """
        i: int = 0
        while not self.stop_spinner.is_set():
            spinner: str = self.spinner_chars[i % len(self.spinner_chars)]

            # Construct the display string
            display_parts: list[str] = [f"\r{spinner}"]

            if self.show_elapsed_time:
                elapsed_time: float = time.time() - self.start_time
                display_parts.append(
                    self.time_fstring.format(elapsed_time=elapsed_time)
                )

            if self.current_value:
                if self.format_string:
                    display_parts.append(self.format_string.format(self.current_value))
                else:
                    display_parts.append(str(self.current_value))

            display: str = " ".join(display_parts)
            self.output_stream.write(display)
            self.output_stream.flush()
            time.sleep(self.update_interval)
            i += 1

    def update_value(self, new_value: Any) -> None:
        """
        Update the current value displayed by the spinner.
        """
        self.current_value = str(new_value)

    def start(self) -> None:
        """
        Start the spinner.
        """
        self.start_time = time.time()
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self) -> None:
        """
        Stop the spinner.
        """
        self.stop_spinner.set()
        if self.spinner_thread:
            self.spinner_thread.join()
        self.output_stream.write("\n")
        self.output_stream.flush()


class SpinnerContext(Spinner):
    """
    A context manager that displays a spinner, and optionally elapsed time and a mutable value.
    """

    def __enter__(self) -> "SpinnerContext":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()


def spinner_decorator(
    *args,
    format_string: Optional[str] = None,
    mutable_kwarg_key: Optional[str] = None,
    show_elapsed_time: bool = True,
    spinner_chars: Sequence[str] = ("|", "/", "-", "\\"),
    time_fstring: str = "({elapsed_time:.2f}s)",
    update_interval: float = 0.1,
    output_stream: TextIO = sys.stdout,
) -> Callable[[DecoratedFunction], DecoratedFunction]:
    """
    A decorator that displays a spinner, and optionally elapsed time and a mutable value while a function is running.

    KwArgs:
    format_string (Optional[str]): A format string for displaying the mutable value.
    mutable_kwarg_key (Optional[str]): The keyword argument name for the update function in the decorated function. If None, mutable value feature is disabled.
    show_elapsed_time (bool): Whether to display the elapsed time.

    Returns:
    Callable[[F], F]: A decorator function.
    """
    if args:
        raise ValueError("spinner_decorator does not accept positional arguments")

    def decorator(func: DecoratedFunction) -> DecoratedFunction:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            spinner: Spinner = Spinner(
                format_string=format_string,
                show_elapsed_time=show_elapsed_time,
                spinner_chars=spinner_chars,
                time_fstring=time_fstring,
                update_interval=update_interval,
                output_stream=output_stream,
            )

            if mutable_kwarg_key:
                kwargs[mutable_kwarg_key] = spinner.update_value

            spinner.start()
            try:
                result: Any = func(*args, **kwargs)
            finally:
                spinner.stop()

            return result

        return wrapper

    return decorator
