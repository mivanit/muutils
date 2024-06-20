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
            except_from: typing.Optional[typing.Type[Exception]] = None,
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