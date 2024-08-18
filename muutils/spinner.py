import time
import threading
import sys
from functools import wraps
from typing import Callable, Any, Optional, TextIO, TypeVar, Sequence, Dict, Union

# Define a generic type for the decorated function
DecoratedFunction = TypeVar("DecoratedFunction", bound=Callable[..., Any])

SPINNER_CHARS: Dict[str, Sequence[str]] = dict(
    default=["|", "/", "-", "\\"],
    dots=[".  ", ".. ", "..."],
    arrows=["<", "^", ">", "v"],
    arrows_2=["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
    bouncing_bar=["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]"],
    bouncing_ball=[
        "( ●    )",
        "(  ●   )",
        "(   ●  )",
        "(    ● )",
        "(     ●)",
        "(    ● )",
        "(   ●  )",
        "(  ●   )",
        "( ●    )",
        "(●     )",
    ],
    ooo=[".", "o", "O", "o"],
    braille=["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    clock=["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"],
    hourglass=["⏳", "⌛"],
    square_corners=["◰", "◳", "◲", "◱"],
    triangle=["◢", "◣", "◤", "◥"],
    square_dot=[
        "⣷",
        "⣯",
        "⣟",
        "⡿",
        "⢿",
        "⣻",
        "⣽",
        "⣾",
    ],
    box_bounce=["▌", "▀", "▐", "▄"],
    hamburger=["☱", "☲", "☴"],
    earth=["🌍", "🌎", "🌏"],
    growing_dots=["⣀", "⣄", "⣤", "⣦", "⣶", "⣷", "⣿"],
)

SPINNER_COMPLETE: Dict[str, str] = dict(
    default="#",
    dots="***",
    arrows="#",
    arrows_2="#",
    bouncing_bar="[====]",
    bouncing_ball="(●●●●●●)",
    ooo="#",
    braille="⣿",
    clock="✔️",
    hourglass="✔️",
    square_corners="◼",
    triangle="◆",
    square_dot="⣿",
    box_bounce="■",
    hamburger="☰",
    earth="✔️",
    growing_dots="⣿",
)


class Spinner:
    """displays a spinner, and optionally elapsed time and a mutable value while a function is running.

    # Parameters:
        - `spinner_chars : Union[str, Sequence[str]]`
        sequence of strings, or key to look up in `SPINNER_CHARS`, to use as the spinner characters
        (defaults to `"default"`)
        - `update_interval : float`
        how often to update the spinner display in seconds
        (defaults to `0.1`)
        - `spinner_complete : str`
        string to display when the spinner is complete
        (defaults to looking up `spinner_chars` in `SPINNER_COMPLETE` or `"#"`)
        - `initial_value : str`
        initial value to display with the spinner
        (defaults to `""`)
        - `message : str`
        message to display with the spinner
        (defaults to `""`)
        - `format_string : str`
        string to format the spinner with. must have `"\\r"` prepended to clear the line.
        allowed keys are `spinner`, `elapsed_time`, `message`, and `value`
        (defaults to `"\\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
        - `output_stream : TextIO`
        stream to write the spinner to
        (defaults to `sys.stdout`)

    # Methods:
    - `update_value(value: Any) -> None`
        update the current value displayed by the spinner

    # Usage:

    ## As a context manager:
    ```python
    with SpinnerContext() as sp:
        for i in range(1):
            time.sleep(0.1)
            spinner.update_value(f"Step {i+1}")
    ```

    ## As a decorator:
    ```python
    @spinner_decorator
    def long_running_function():
        for i in range(1):
            time.sleep(0.1)
            spinner.update_value(f"Step {i+1}")
        return "Function completed"
    ```
    """

    def __init__(
        self,
        *args,
        spinner_chars: Union[str, Sequence[str]] = "default",
        update_interval: float = 0.1,
        spinner_complete: Optional[str] = None,
        initial_value: str = "",
        message: str = "",
        format_string: str = "\r{spinner} ({elapsed_time:.2f}s) {message}{value}",
        output_stream: TextIO = sys.stdout,
        **kwargs: Any,
    ):
        if args:
            raise ValueError(f"Spinner does not accept positional arguments: {args}")
        if kwargs:
            raise ValueError(
                f"Spinner did not recognize these keyword arguments: {kwargs}"
            )

        # spinner display
        self.spinner_complete: str = (
            (
                # if None, use `spinner_chars` key as default
                SPINNER_COMPLETE.get(spinner_chars, "#")
                if isinstance(spinner_chars, str)
                else "#"
            )
            if spinner_complete is None
            # if not None, use the value provided
            else spinner_complete
        )
        self.spinner_chars: Sequence[str] = (
            SPINNER_CHARS[spinner_chars]
            if isinstance(spinner_chars, str)
            else spinner_chars
        )

        # copy kwargs
        self.update_interval: float = update_interval
        self.message: str = message
        self.current_value: Any = initial_value
        self.format_string: str = format_string
        self.output_stream: TextIO = output_stream

        # test out format string
        try:
            self.format_string.format(
                spinner=self.spinner_chars[0],
                elapsed_time=0.0,
                message=self.message,
                value=self.current_value,
            )
        except Exception as e:
            raise ValueError(
                f"Invalid format string: {format_string}. Must take keys 'spinner: str', 'elapsed_time: float', 'message: str', and 'value: Any'."
            ) from e

        # init
        self.start_time: float = 0
        self.stop_spinner: threading.Event = threading.Event()
        self.spinner_thread: Optional[threading.Thread] = None

    def spin(self) -> None:
        "Function to run in a separate thread, displaying the spinner and optional information"
        i: int = 0
        while not self.stop_spinner.is_set():
            # get current spinner str
            spinner: str = self.spinner_chars[i % len(self.spinner_chars)]

            # Construct the display string
            display_parts: dict[str, Any] = dict(
                spinner=spinner,  # str
                elapsed_time=time.time() - self.start_time,  # float
                message=self.message,  # str
                value=self.current_value,  # Any, but will be formatted as str
            )

            # write and flush the display string
            output: str = self.format_string.format(**display_parts)
            self.output_stream.write(output)
            self.output_stream.flush()

            # wait for the next update
            time.sleep(self.update_interval)
            i += 1

    def update_value(self, value: Any) -> None:
        "Update the current value displayed by the spinner"
        self.current_value = value

    def start(self) -> None:
        "Start the spinner"
        self.start_time = time.time()
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self) -> None:
        "Stop the spinner"
        self.output_stream.write(f"\r{self.spinner_complete}")
        self.stop_spinner.set()
        if self.spinner_thread:
            self.spinner_thread.join()
        self.output_stream.write("\n")
        self.output_stream.flush()


class SpinnerContext(Spinner):
    "see `Spinner` for parameters"

    def __enter__(self) -> "SpinnerContext":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()


SpinnerContext.__doc__ = Spinner.__doc__


def spinner_decorator(
    *args,
    # passed to `Spinner.__init__`
    spinner_chars: Union[str, Sequence[str]] = "default",
    update_interval: float = 0.1,
    spinner_complete: Optional[str] = None,
    initial_value: str = "",
    message: str = "",
    format_string: str = "{spinner} ({elapsed_time:.2f}s) {message}{value}",
    output_stream: TextIO = sys.stdout,
    # new kwarg
    mutable_kwarg_key: Optional[str] = None,
    **kwargs,
) -> Callable[[DecoratedFunction], DecoratedFunction]:
    "see `Spinner` for parameters. Also takes `mutable_kwarg_key`, the keyword argument with which to pass `Spinner().update_value` to the decorated function."

    if len(args) > 1:
        raise ValueError(
            f"spinner_decorator does not accept positional arguments: {args}"
        )
    if kwargs:
        raise ValueError(
            f"spinner_decorator did not recognize these keyword arguments: {kwargs}"
        )

    def decorator(func: DecoratedFunction) -> DecoratedFunction:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            spinner: Spinner = Spinner(
                spinner_chars=spinner_chars,
                update_interval=update_interval,
                spinner_complete=spinner_complete,
                initial_value=initial_value,
                message=message,
                format_string=format_string,
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

        # TODO: fix this type ignore
        return wrapper  # type: ignore[return-value]

    if not args:
        # called as `@spinner_decorator(stuff)`
        return decorator
    else:
        # called as `@spinner_decorator` without parens
        return decorator(args[0])


spinner_decorator.__doc__ = Spinner.__doc__


class NoOpContextManager:
    """A context manager that does nothing."""

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
