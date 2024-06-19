"""logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both console and a file
- `Logger` class handles levels in a slightly different way than default python `logging`,
        and also has "streams" which allow for different sorts of output in the same logger
        this was mostly made with training models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the duration of a block of code
"""

from __future__ import annotations

import json
import time
import typing
from functools import partial
from typing import Callable, Sequence

from muutils.json_serialize import JSONitem, json_serialize
from muutils.logger.exception_context import ExceptionContext
from muutils.logger.headerfuncs import HEADER_FUNCTIONS, HeaderFunction
from muutils.logger.loggingstream import LoggingStream
from muutils.logger.simplelogger import AnyIO, SimpleLogger

# pylint: disable=arguments-differ, bad-indentation, trailing-whitespace, trailing-newlines, unnecessary-pass, consider-using-with, use-dict-literal


def decode_level(level: int) -> str:
    if not isinstance(level, int):
        raise TypeError(f"level must be int, got {type(level) = } {level = }")

    if level < -255:
        return f"FATAL_ERROR({level})"
    elif level < 0:
        return f"WARNING({level})"
    else:
        return f"INFO({level})"


# todo: add a context which catches and logs all exceptions
class Logger(SimpleLogger):
    """logger with more features, including log levels and streams

    # Parameters:
            - `log_path : str | None`
            default log file path
            (defaults to `None`)
            - `log_file : AnyIO | None`
            default log io, should have a `.write()` method (pass only this or `log_path`, not both)
            (defaults to `None`)
            - `timestamp : bool`
            whether to add timestamps to every log message (under the `_timestamp` key)
            (defaults to `True`)
            - `default_level : int`
            default log level for streams/messages that don't specify a level
            (defaults to `0`)
            - `console_print_threshold : int`
            log level at which to print to the console, anything greater will not be printed unless overridden by `console_print`
            (defaults to `50`)
            - `level_header : HeaderFunction`
            function for formatting log messages when printing to console
            (defaults to `HEADER_FUNCTIONS["md"]`)
    - `keep_last_msg_time : bool`
            whether to keep the last message time
            (defaults to `True`)


    # Raises:
            - `ValueError` : _description_
    """

    def __init__(
        self,
        log_path: str | None = None,
        log_file: AnyIO | None = None,
        default_level: int = 0,
        console_print_threshold: int = 50,
        level_header: HeaderFunction = HEADER_FUNCTIONS["md"],
        streams: dict[str | None, LoggingStream] | Sequence[LoggingStream] = (),
        keep_last_msg_time: bool = True,
        # junk args
        timestamp: bool = True,
        **kwargs,
    ):
        # junk arg checking
        # ==================================================
        if len(kwargs) > 0:
            raise ValueError(f"unrecognized kwargs: {kwargs}")

        if not timestamp:
            raise ValueError(
                "timestamp must be True -- why would you not want timestamps?"
            )

        # timing
        # ==================================================
        # timing compares
        self._keep_last_msg_time: bool = keep_last_msg_time
        # TODO: handle per stream?
        self._last_msg_time: float | None = time.time()

        # basic setup
        # ==================================================
        # init BaseLogger
        super().__init__(log_file=log_file, log_path=log_path, timestamp=timestamp)

        # level-related
        self._console_print_threshold: int = console_print_threshold
        self._default_level: int = default_level

        # set up streams
        self._streams: dict[str | None, LoggingStream] = (
            streams
            if isinstance(streams, typing.Mapping)
            else {s.name: s for s in streams}
        )
        # default error stream
        if "error" not in self._streams:
            self._streams["error"] = LoggingStream(
                "error",
                aliases={
                    "err",
                    "except",
                    "Exception",
                    "exception",
                    "exceptions",
                    "errors",
                },
            )

        # check alias duplicates
        alias_set: set[str | None] = set()
        for stream in self._streams.values():
            for alias in stream.aliases:
                if alias in alias_set:
                    raise ValueError(f"alias {alias} is already in use")
                alias_set.add(alias)

        # add aliases
        for stream in tuple(self._streams.values()):
            for alias in stream.aliases:
                if alias not in self._streams:
                    self._streams[alias] = stream

        # print formatting
        self._level_header: HeaderFunction = level_header

        print({k: str(v) for k, v in self._streams.items()})

    def _exception_context(
        self,
        stream: str = "error",
        # level: int = -256,
        # **kwargs,
    ) -> ExceptionContext:
        s: LoggingStream = self._streams[stream]
        return ExceptionContext(stream=s)

    def log(  # type: ignore # yes, the signatures are different here.
        self,
        msg: JSONitem = None,
        lvl: int | None = None,
        stream: str | None = None,
        console_print: bool = False,
        extra_indent: str = "",
        **kwargs,
    ):
        """logging function

        ### Parameters:
         - `msg : JSONitem`
           message (usually string or dict) to be logged
         - `lvl : int | None`
           level of message (lower levels are more important)
           (defaults to `None`)
         - `console_print : bool`
           override `console_print_threshold` setting
           (defaults to `False`)
         - `stream : str | None`
           whether to log to a stream (defaults to `None`), which logs to the default `None` stream
           (defaults to `None`)
        """

        # add to known stream names if not present
        if stream not in self._streams:
            self._streams[stream] = LoggingStream(stream)

        # set default level to either global or stream-specific default level
        # ========================================
        if lvl is None:
            if stream is None:
                lvl = self._default_level
            else:
                if self._streams[stream].default_level is not None:
                    lvl = self._streams[stream].default_level
                else:
                    lvl = self._default_level

        assert lvl is not None, "lvl should not be None at this point"

        # print to console with formatting
        # ========================================
        _printed: bool = False
        if console_print or (lvl <= self._console_print_threshold):
            # add some formatting
            print(
                self._level_header(
                    msg=msg,
                    lvl=lvl,
                    stream=stream,
                    extra_indent=extra_indent,
                )
            )

            # store the last message time
            if self._last_msg_time is not None:
                self._last_msg_time = time.time()

            _printed = True

        # convert and add data
        # ========================================
        # converting to dict
        msg_dict: typing.Mapping
        if not isinstance(msg, typing.Mapping):
            msg_dict = {"_msg": msg}
        else:
            msg_dict = msg

        # level+stream metadata
        if lvl is not None:
            msg_dict["_lvl"] = lvl

        # msg_dict["_stream"] = stream # moved to LoggingStream

        # extra data in kwargs
        if len(kwargs) > 0:
            msg_dict["_kwargs"] = kwargs

        # add default contents (timing, etc)
        msg_dict = {
            **{k: v() for k, v in self._streams[stream].default_contents.items()},
            **msg_dict,
        }

        # write
        # ========================================
        logfile_msg: str = json.dumps(json_serialize(msg_dict)) + "\n"
        if (
            (stream is None)
            or (stream not in self._streams)
            or (self._streams[stream].handler is None)
        ):
            # write to the main log file if no stream is specified
            self._log_file_handle.write(logfile_msg)
        else:
            # otherwise, write to the stream-specific file
            s_handler: AnyIO | None = self._streams[stream].handler
            if s_handler is not None:
                s_handler.write(logfile_msg)
            else:
                raise ValueError(
                    f"stream handler is None! something in the logging stream setup is wrong:\n{self}"
                )

        # if it was important enough to print, flush all streams
        if _printed:
            self.flush_all()

    def log_elapsed_last(
        self,
        lvl: int | None = None,
        stream: str | None = None,
        console_print: bool = True,
        **kwargs,
    ) -> float:
        """logs the time elapsed since the last message was printed to the console (in any stream)"""
        if self._last_msg_time is None:
            raise ValueError("no last message time!")
        else:
            return self.log(
                {"elapsed_time": round(time.time() - self._last_msg_time, 6)},
                lvl=(lvl if lvl is not None else self._console_print_threshold),
                stream=stream,
                console_print=console_print,
                **kwargs,
            )

    def flush_all(self):
        """flush all streams"""

        self._log_file_handle.flush()

        for stream in self._streams.values():
            if stream.handler is not None:
                stream.handler.flush()

    def __getattr__(self, stream: str) -> Callable:
        if stream.startswith("_"):
            raise AttributeError(f"invalid stream name {stream} (no underscores)")
        return partial(self.log, stream=stream)

    def __getitem__(self, stream: str):
        return partial(self.log, stream=stream)

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)
