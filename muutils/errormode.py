from __future__ import annotations

import typing
import warnings
from enum import Enum


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
    ):
        if self is ErrorMode.EXCEPT:
            if except_from is not None:
                raise except_cls(msg) from except_from
            else:
                raise except_cls(msg)
        elif self is ErrorMode.WARN:
            warnings.warn(msg, warn_cls)
        elif self is ErrorMode.IGNORE:
            pass
        else:
            raise ValueError(f"Unknown error mode {self}")

    @classmethod
    def from_any(cls, mode: "str|ErrorMode", allow_aliases: bool = True) -> ErrorMode:
        if isinstance(mode, ErrorMode):
            return mode
        elif isinstance(mode, str):
            mode = mode.strip().lower()
            if not allow_aliases:
                try:
                    return ErrorMode(mode)
                except ValueError as e:
                    raise KeyError(f"Unknown error mode {mode}") from e
            else:
                return ERROR_MODE_ALIASES[mode]
        else:
            raise TypeError(f"Expected {ErrorMode} or str, got {type(mode) = }")


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
