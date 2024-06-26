from __future__ import annotations

import typing
import warnings
from enum import Enum

# type hint a "warnings.warn" - like function with protocol
class WarningFunc(typing.Protocol):
    def __call__(
            self,
            msg: str,
            category: typing.Type[Warning],
            source: typing.Any = None,
        ) -> None:
        ...

class ErrorMode(Enum):
    EXCEPT = "except"
    WARN = "warn"
    IGNORE = "ignore"

    def process(
        self,
        msg: str,
        except_cls: typing.Type[Exception] = ValueError,
        warn_cls: typing.Type[Warning] = UserWarning,
        except_from: typing.Optional[Exception] = None,
        warn_func: WarningFunc = warnings.warn,
    ):
        if self is ErrorMode.EXCEPT:
            if except_from is not None:
                raise except_cls(msg) from except_from
            else:
                raise except_cls(msg)
        elif self is ErrorMode.WARN:
            if except_from is not None:
                msg = f"{msg}\n\tSource of warning: {except_from}"
            warn_func(msg, category=warn_cls, source=except_from)
        elif self is ErrorMode.IGNORE:
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
            raise TypeError(f"Expected {ErrorMode = } or str, got {type(mode) = } {mode = }")

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
    "ignore": ErrorMode.IGNORE,
    # except
    "e": ErrorMode.EXCEPT,
    "error": ErrorMode.EXCEPT,
    "err": ErrorMode.EXCEPT,
    "raise": ErrorMode.EXCEPT,
    # warn
    "w": ErrorMode.WARN,
    "warning": ErrorMode.WARN,
    # ignore
    "i": ErrorMode.IGNORE,
    "silent": ErrorMode.IGNORE,
    "quiet": ErrorMode.IGNORE,
    "nothing": ErrorMode.IGNORE,
}
