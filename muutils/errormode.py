from __future__ import annotations

import sys
import typing
import types
import warnings
from enum import Enum


class WarningFunc(typing.Protocol):
    def __call__(
        self,
        msg: str,
        category: typing.Type[Warning],
        source: typing.Any = None,
    ) -> None: ...


LoggingFunc = typing.Callable[[str], None]

GLOBAL_WARN_FUNC: WarningFunc = warnings.warn  # type: ignore[assignment]
GLOBAL_LOG_FUNC: LoggingFunc = print


class ErrorMode(Enum):
    EXCEPT = "except"
    WARN = "warn"
    LOG = "log"
    IGNORE = "ignore"

    def process(
        self,
        msg: str,
        except_cls: typing.Type[Exception] = ValueError,
        warn_cls: typing.Type[Warning] = UserWarning,
        except_from: typing.Optional[Exception] = None,
        warn_func: WarningFunc | None = None,
        log_func: LoggingFunc | None = None,
    ):
        if self is ErrorMode.EXCEPT:
            # except, possibly with a chained exception
            frame: types.FrameType = sys._getframe(1)
            traceback: types.TracebackType = types.TracebackType(
                None, frame, frame.f_lasti, frame.f_lineno
            )

            # Attach the new traceback to the exception and raise it without the internal call stack
            if except_from is not None:
                raise except_cls(msg).with_traceback(traceback) from except_from
            else:
                raise except_cls(msg).with_traceback(traceback)
        elif self is ErrorMode.WARN:
            # get global warn function if not passed
            if warn_func is None:
                warn_func = GLOBAL_WARN_FUNC
            # augment warning message with source
            if except_from is not None:
                msg = f"{msg}\n\tSource of warning: {except_from}"
            if warn_func == warnings.warn:
                # Store the original showwarning function
                original_showwarning = warnings.showwarning

                def custom_showwarning(
                    message: str,
                    category: typing.Type[Warning],
                    filename: str,
                    lineno: int,
                    file: typing.Optional[typing.TextIO] = None,
                    line: typing.Optional[str] = None,
                ) -> None:
                    # Get the frame where process() was called
                    frame = sys._getframe(
                        3
                    )  # Adjusted to account for the extra function call
                    # Call the original showwarning function
                    original_showwarning(
                        message,
                        category,
                        frame.f_code.co_filename,
                        frame.f_lineno,
                        file,
                        line,
                    )

                try:
                    warnings.showwarning = custom_showwarning
                    warn_func(msg, category=warn_cls)
                finally:
                    # Restore the original showwarning function
                    warnings.showwarning = original_showwarning
            else:
                # Use the provided warn_func as-is
                warn_func(msg, category=warn_cls)
        elif self is ErrorMode.LOG:
            # get global log function if not passed
            if log_func is None:
                log_func = GLOBAL_LOG_FUNC
            # log
            log_func(msg)
        elif self is ErrorMode.IGNORE:
            # do nothing
            pass
        else:
            raise ValueError(f"Unknown error mode {self}")

    @classmethod
    def from_any(
        cls,
        mode: "str|ErrorMode",
        allow_aliases: bool = True,
        allow_prefix: bool = True,
    ) -> ErrorMode:
        if isinstance(mode, ErrorMode):
            return mode
        elif isinstance(mode, str):
            # strip
            mode = mode.strip()

            # remove prefix
            if allow_prefix and mode.startswith("ErrorMode."):
                mode = mode[len("ErrorMode.") :]

            # lowercase and strip again
            mode = mode.strip().lower()

            if not allow_aliases:
                # try without aliases
                try:
                    return ErrorMode(mode)
                except ValueError as e:
                    raise KeyError(f"Unknown error mode {mode = }") from e
            else:
                # look up in aliases map
                return ERROR_MODE_ALIASES[mode]
        else:
            raise TypeError(
                f"Expected {ErrorMode = } or str, got {type(mode) = } {mode = }"
            )

    def __str__(self) -> str:
        return f"ErrorMode.{self.value.capitalize()}"

    def __repr__(self) -> str:
        return str(self)

    def serialize(self) -> str:
        return str(self)

    @classmethod
    def load(cls, data: str) -> ErrorMode:
        return cls.from_any(
            data,
            allow_aliases=False,
            allow_prefix=True,
        )


ERROR_MODE_ALIASES: dict[str, ErrorMode] = {
    # base
    "except": ErrorMode.EXCEPT,
    "warn": ErrorMode.WARN,
    "log": ErrorMode.LOG,
    "ignore": ErrorMode.IGNORE,
    # except
    "e": ErrorMode.EXCEPT,
    "error": ErrorMode.EXCEPT,
    "err": ErrorMode.EXCEPT,
    "raise": ErrorMode.EXCEPT,
    # warn
    "w": ErrorMode.WARN,
    "warning": ErrorMode.WARN,
    # log
    "l": ErrorMode.LOG,
    "print": ErrorMode.LOG,
    "output": ErrorMode.LOG,
    "show": ErrorMode.LOG,
    "display": ErrorMode.LOG,
    # ignore
    "i": ErrorMode.IGNORE,
    "silent": ErrorMode.IGNORE,
    "quiet": ErrorMode.IGNORE,
    "nothing": ErrorMode.IGNORE,
}
