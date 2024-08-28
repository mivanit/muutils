"""(deprecated) experimenting with logging utilities"""

import warnings

from muutils.logger.logger import Logger
from muutils.logger.loggingstream import LoggingStream
from muutils.logger.simplelogger import SimpleLogger
from muutils.logger.timing import TimerContext

warnings.warn(
    DeprecationWarning(
        "muutils.logger is no longer maintained. Consider using [trnbl](https://github.com/mivanit/trnbl) instead."
    )
)

__all__ = [
    # submodules
    "exception_context",
    "headerfuncs",
    "log_util",
    "logger",
    "loggingstream",
    "simplelogger",
    "timing",
    # imports
    "Logger",
    "LoggingStream",
    "SimpleLogger",
    "TimerContext",
]
