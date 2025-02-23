"""decorator `spinner_decorator` and context manager `SpinnerContext` to display a spinner

using the base `Spinner` class while some code is running.
"""

import os
import time
from dataclasses import dataclass, field
import threading
import sys
from functools import wraps
from typing import (
    List,
    Dict,
    Callable,
    Any,
    Literal,
    Optional,
    TextIO,
    TypeVar,
    Sequence,
    Union,
    ContextManager,
)
import warnings

DecoratedFunction = TypeVar("DecoratedFunction", bound=Callable[..., Any])
"Define a generic type for the decorated function"


@dataclass
class SpinnerConfig:
    working: List[str] = field(default_factory=lambda: ["|", "/", "-", "\\"])
    success: str = "✔️"
    fail: str = "❌"

    def is_ascii(self) -> bool:
        "whether all characters are ascii"
        return all(s.isascii() for s in self.working + [self.success, self.fail])

    def eq_lens(self) -> bool:
        "whether all working characters are the same length"
        expected_len: int = len(self.working[0])
        return all(
            [
                len(char) == expected_len
                for char in self.working + [self.success, self.fail]
            ]
        )

    def is_valid(self) -> bool:
        "whether the spinner config is valid"
        return all(
            [
                len(self.working) > 0,
                isinstance(self.working, list),
                isinstance(self.success, str),
                isinstance(self.fail, str),
                all(isinstance(char, str) for char in self.working),
            ]
        )

    def __post_init__(self):
        if not self.is_valid():
            raise ValueError(f"Invalid SpinnerConfig: {self}")

    @classmethod
    def from_any(cls, arg: "SpinnerConfigArg") -> "SpinnerConfig":
        if isinstance(arg, str):
            return SPINNERS[arg]
        elif isinstance(arg, list):
            return SpinnerConfig(working=arg)
        elif isinstance(arg, dict):
            return SpinnerConfig(**arg)
        elif isinstance(arg, SpinnerConfig):
            return arg
        else:
            raise TypeError(
                f"to create a SpinnerConfig, you must pass a string (key), list (working seq), dict (kwargs to SpinnerConfig), or SpinnerConfig, but got {type(arg) = }, {arg = }"
            )


SpinnerConfigArg = Union[str, List[str], SpinnerConfig, dict]

SPINNERS: Dict[str, SpinnerConfig] = dict(
    default=SpinnerConfig(working=["|", "/", "-", "\\"], success="#", fail="X"),
    dots=SpinnerConfig(working=[".  ", ".. ", "..."], success="***", fail="xxx"),
    bars=SpinnerConfig(working=["|  ", "|| ", "|||"], success="|||", fail="///"),
    arrows=SpinnerConfig(working=["<", "^", ">", "v"], success="►", fail="✖"),
    arrows_2=SpinnerConfig(
        working=["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"], success="→", fail="↯"
    ),
    bouncing_bar=SpinnerConfig(
        working=["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]"],
        success="[====]",
        fail="[XXXX]",
    ),
    bar=SpinnerConfig(
        working=["[  ]", "[- ]", "[--]", "[ -]"],
        success="[==]",
        fail="[xx]",
    ),
    bouncing_ball=SpinnerConfig(
        working=[
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
        success="(●●●●●●)",
        fail="(  ✖  )",
    ),
    ooo=SpinnerConfig(working=[".", "o", "O", "o"], success="O", fail="x"),
    braille=SpinnerConfig(
        working=["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        success="⣿",
        fail="X",
    ),
    clock=SpinnerConfig(
        working=[
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
        ],
        success="✔️",
        fail="❌",
    ),
    hourglass=SpinnerConfig(working=["⏳", "⌛"], success="✔️", fail="❌"),
    square_corners=SpinnerConfig(working=["◰", "◳", "◲", "◱"], success="◼", fail="✖"),
    triangle=SpinnerConfig(working=["◢", "◣", "◤", "◥"], success="◆", fail="✖"),
    square_dot=SpinnerConfig(
        working=["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"], success="⣿", fail="❌"
    ),
    box_bounce=SpinnerConfig(working=["▌", "▀", "▐", "▄"], success="■", fail="✖"),
    hamburger=SpinnerConfig(working=["☱", "☲", "☴"], success="☰", fail="✖"),
    earth=SpinnerConfig(working=["🌍", "🌎", "🌏"], success="✔️", fail="❌"),
    growing_dots=SpinnerConfig(
        working=["⣀", "⣄", "⣤", "⣦", "⣶", "⣷", "⣿"], success="⣿", fail="✖"
    ),
    dice=SpinnerConfig(working=["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"], success="🎲", fail="✖"),
    wifi=SpinnerConfig(
        working=["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"], success="✔️", fail="❌"
    ),
    bounce=SpinnerConfig(working=["⠁", "⠂", "⠄", "⠂"], success="⠿", fail="⢿"),
    arc=SpinnerConfig(working=["◜", "◠", "◝", "◞", "◡", "◟"], success="○", fail="✖"),
    toggle=SpinnerConfig(working=["⊶", "⊷"], success="⊷", fail="⊗"),
    toggle2=SpinnerConfig(working=["▫", "▪"], success="▪", fail="✖"),
    toggle3=SpinnerConfig(working=["□", "■"], success="■", fail="✖"),
    toggle4=SpinnerConfig(working=["■", "□", "▪", "▫"], success="■", fail="✖"),
    toggle5=SpinnerConfig(working=["▮", "▯"], success="▮", fail="✖"),
    toggle7=SpinnerConfig(working=["⦾", "⦿"], success="⦿", fail="✖"),
    toggle8=SpinnerConfig(working=["◍", "◌"], success="◍", fail="✖"),
    toggle9=SpinnerConfig(working=["◉", "◎"], success="◉", fail="✖"),
    arrow2=SpinnerConfig(
        working=["⬆️ ", "↗️ ", "➡️ ", "↘️ ", "⬇️ ", "↙️ ", "⬅️ ", "↖️ "], success="➡️", fail="❌"
    ),
    point=SpinnerConfig(
        working=["∙∙∙", "●∙∙", "∙●∙", "∙∙●", "∙∙∙"], success="●●●", fail="xxx"
    ),
    layer=SpinnerConfig(working=["-", "=", "≡"], success="≡", fail="✖"),
    speaker=SpinnerConfig(
        working=["🔈 ", "🔉 ", "🔊 ", "🔉 "], success="🔊", fail="🔇"
    ),
    orangePulse=SpinnerConfig(
        working=["🔸 ", "🔶 ", "🟠 ", "🟠 ", "🔷 "], success="🟠", fail="❌"
    ),
    bluePulse=SpinnerConfig(
        working=["🔹 ", "🔷 ", "🔵 ", "🔵 ", "🔷 "], success="🔵", fail="❌"
    ),
    satellite_signal=SpinnerConfig(
        working=["📡   ", "📡·  ", "📡·· ", "📡···", "📡 ··", "📡  ·"],
        success="📡 ✔️ ",
        fail="📡 ❌ ",
    ),
    rocket_orbit=SpinnerConfig(
        working=["🌍🚀  ", "🌏 🚀 ", "🌎  🚀"], success="🌍  ✨", fail="🌍  💥"
    ),
    ogham=SpinnerConfig(working=["ᚁ ", "ᚂ ", "ᚃ ", "ᚄ", "ᚅ"], success="᚛᚜", fail="✖"),
    eth=SpinnerConfig(
        working=["᛫", "፡", "፥", "፤", "፧", "።", "፨"], success="፠", fail="✖"
    ),
)
# spinner configurations


class Spinner:
    """displays a spinner, and optionally elapsed time and a mutable value while a function is running.

    # Parameters:

    - `update_interval : float`
        how often to update the spinner display in seconds
        (defaults to `0.1`)
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
    - `format_string_when_updated : Union[bool,str]`
        whether to use a different format string when the value is updated.
        if `True`, use the default format string with a newline appended. if a string, use that string.
        this is useful if you want update_value to print to console and be preserved.
        (defaults to `False`)

    # Deprecated Parameters:

    - `spinner_chars : Union[str, Sequence[str]]`
        sequence of strings, or key to look up in `SPINNER_CHARS`, to use as the spinner characters
        (defaults to `"default"`)
    - `spinner_complete : str`
        string to display when the spinner is complete
        (defaults to looking up `spinner_chars` in `SPINNER_COMPLETE` or `"#"`)

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
        # no positional args
        *args,
        config: SpinnerConfigArg = "default",
        update_interval: float = 0.1,
        initial_value: str = "",
        message: str = "",
        format_string: str = "\r{spinner} ({elapsed_time:.2f}s) {message}{value}",
        output_stream: TextIO = sys.stdout,
        format_string_when_updated: Union[str, bool] = False,
        # deprecated
        spinner_chars: Optional[Union[str, Sequence[str]]] = None,
        spinner_complete: Optional[str] = None,
        # no other kwargs accepted
        **kwargs: Any,
    ):
        if args:
            raise ValueError(f"Spinner does not accept positional arguments: {args}")
        if kwargs:
            raise ValueError(
                f"Spinner did not recognize these keyword arguments: {kwargs}"
            )

        # old spinner display
        if (spinner_chars is not None) or (spinner_complete is not None):
            warnings.warn(
                "spinner_chars and spinner_complete are deprecated and will have no effect. Use `config` instead.",
                DeprecationWarning,
            )

        # config
        self.config: SpinnerConfig = SpinnerConfig.from_any(config)

        # special format string for when the value is updated
        self.format_string_when_updated: Optional[str] = None
        "format string to use when the value is updated"
        if format_string_when_updated is not False:
            if format_string_when_updated is True:
                # modify the default format string
                self.format_string_when_updated = format_string + "\n"
            elif isinstance(format_string_when_updated, str):
                # use the provided format string
                self.format_string_when_updated = format_string_when_updated
            else:
                raise TypeError(
                    "format_string_when_updated must be a string or True, got"
                    + f" {type(format_string_when_updated) = }{format_string_when_updated}"
                )

        # copy other kwargs
        self.update_interval: float = update_interval
        self.message: str = message
        self.current_value: Any = initial_value
        self.format_string: str = format_string
        self.output_stream: TextIO = output_stream

        # test out format string
        try:
            self.format_string.format(
                spinner=self.config.working[0],
                elapsed_time=0.0,
                message=self.message,
                value=self.current_value,
            )
        except Exception as e:
            raise ValueError(
                f"Invalid format string: {format_string}. Must take keys "
                + "'spinner: str', 'elapsed_time: float', 'message: str', and 'value: Any'."
            ) from e

        # init
        self.start_time: float = 0
        "for measuring elapsed time"
        self.stop_spinner: threading.Event = threading.Event()
        "to stop the spinner"
        self.spinner_thread: Optional[threading.Thread] = None
        "the thread running the spinner"
        self.value_changed: bool = False
        "whether the value has been updated since the last display"
        self.term_width: int
        "width of the terminal, for padding with spaces"
        try:
            self.term_width = os.get_terminal_size().columns
        except OSError:
            self.term_width = 80

        # state of the spinner
        self.state: Literal["initialized", "running", "success", "fail"] = "initialized"

    def spin(self) -> None:
        "Function to run in a separate thread, displaying the spinner and optional information"
        i: int = 0
        while not self.stop_spinner.is_set():
            # get current spinner str
            spinner: str = self.config.working[i % len(self.config.working)]

            # args for display string
            display_parts: Dict[str, Any] = dict(
                spinner=spinner,  # str
                elapsed_time=time.time() - self.start_time,  # float
                message=self.message,  # str
                value=self.current_value,  # Any, but will be formatted as str
            )

            # use the special one if needed
            format_str: str = self.format_string
            if self.value_changed and (self.format_string_when_updated is not None):
                self.value_changed = False
                format_str = self.format_string_when_updated

            # write and flush the display string
            output: str = format_str.format(**display_parts).ljust(self.term_width)
            self.output_stream.write(output)
            self.output_stream.flush()

            # wait for the next update
            time.sleep(self.update_interval)
            i += 1

    def update_value(self, value: Any) -> None:
        "Update the current value displayed by the spinner"
        self.current_value = value
        self.value_changed = True

    def start(self) -> None:
        "Start the spinner"
        self.start_time = time.time()
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()
        self.state = "running"

    def stop(self, failed: bool = False) -> None:
        "Stop the spinner"
        self.output_stream.write(
            self.format_string.format(
                spinner=self.config.success if not failed else self.config.fail,
                elapsed_time=time.time() - self.start_time,  # float
                message=self.message,  # str
                value=self.current_value,  # Any, but will be formatted as str
            ).ljust(self.term_width)
        )
        self.stop_spinner.set()
        if self.spinner_thread:
            self.spinner_thread.join()
        self.output_stream.write("\n")
        self.output_stream.flush()

        self.state = "fail" if failed else "success"


class NoOpContextManager(ContextManager):
    """A context manager that does nothing."""

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class SpinnerContext(Spinner, ContextManager):
    "see `Spinner` for parameters"

    def __enter__(self) -> "SpinnerContext":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop(failed=exc_type is not None)


SpinnerContext.__doc__ = Spinner.__doc__


# TODO: type hint that the `update_status` kwarg is not needed when calling the function we just decorated
def spinner_decorator(
    *args,
    # passed to `Spinner.__init__`
    config: SpinnerConfigArg = "default",
    update_interval: float = 0.1,
    initial_value: str = "",
    message: str = "",
    format_string: str = "{spinner} ({elapsed_time:.2f}s) {message}{value}",
    output_stream: TextIO = sys.stdout,
    # new kwarg
    mutable_kwarg_key: Optional[str] = None,
    # deprecated
    spinner_chars: Union[str, Sequence[str], None] = None,
    spinner_complete: Optional[str] = None,
    **kwargs,
) -> Callable[[DecoratedFunction], DecoratedFunction]:
    """see `Spinner` for parameters. Also takes `mutable_kwarg_key`

    `mutable_kwarg_key` is the key with which `Spinner().update_value`
    will be passed to the decorated function. if `None`, won't pass it.

    """

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
                config=config,
                update_interval=update_interval,
                initial_value=initial_value,
                message=message,
                format_string=format_string,
                output_stream=output_stream,
                spinner_chars=spinner_chars,
                spinner_complete=spinner_complete,
            )

            if mutable_kwarg_key:
                kwargs[mutable_kwarg_key] = spinner.update_value

            spinner.start()
            try:
                result: Any = func(*args, **kwargs)
                spinner.stop(failed=False)
            except Exception as e:
                spinner.stop(failed=True)
                raise e

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
