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
        initial value to display after spinner+time. if `format_string` is None, will just always display this value
        (defaults to `"_"`)
        - `format_string : Optional[str]`
        string to format the mutable value value with
        (defaults to `None`)
        - `show_elapsed_time : bool`
        whether to display the elapsed time
        (defaults to `True`)
        - `time_fstring : _type_`
        format string for the elapsed time
        (defaults to `"({elapsed_time:.2f}s)"`)
        - `output_stream : TextIO`
        stream to write the spinner to
        (defaults to `sys.stdout`)
    """

    def __init__(
        self,
        *args,
        spinner_chars: Union[str, Sequence[str]] = "default",
        update_interval: float = 0.1,
        spinner_complete: Optional[str] = None,
        initial_value: str = "_",
        format_string: Optional[str] = None,
        show_elapsed_time: bool = True,
        time_fstring: str = "({elapsed_time:.2f}s)",
        output_stream: TextIO = sys.stdout,
    ):
        if args:
            raise ValueError("Spinner does not accept positional arguments")
        # copy kwargs
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
        self.update_interval: float = update_interval
        self.current_value: str = initial_value
        self.format_string: Optional[str] = format_string
        self.show_elapsed_time: bool = show_elapsed_time
        self.time_fstring: str = time_fstring
        self.output_stream: TextIO = output_stream

        # init
        self.start_time: float = 0
        self.stop_spinner: threading.Event = threading.Event()
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
    spinner_chars: Sequence[str] = ("|", "/", "-", "\\"),
    update_interval: float = 0.1,
    spinner_complete: Optional[str] = None,
    format_string: Optional[str] = None,
    mutable_kwarg_key: Optional[str] = None,
    show_elapsed_time: bool = True,
    time_fstring: str = "({elapsed_time:.2f}s)",
    output_stream: TextIO = sys.stdout,
) -> Callable[[DecoratedFunction], DecoratedFunction]:
    "see `Spinner` for parameters"

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

        # TODO: fix this
        return wrapper  # type: ignore[return-value]

    return decorator


spinner_decorator.__doc__ = Spinner.__doc__


class NoOpContextManager:
    """A context manager that does nothing."""

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
