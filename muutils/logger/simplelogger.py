from __future__ import annotations

import json
import sys
import time
import typing
from typing import TextIO, Union

from muutils.json_serialize import JSONitem, json_serialize


class NullIO:
    """null IO class"""

    def __init__(self) -> None:
        pass

    def write(self, msg: str) -> int:
        """write to nothing! this throws away the message"""
        return len(msg)

    def flush(self) -> None:
        """flush nothing! this is a no-op"""
        pass

    def close(self) -> None:
        """close nothing! this is a no-op"""
        pass


AnyIO = Union[TextIO, NullIO]


class SimpleLogger:
    """logs training data to a jsonl file"""

    def __init__(
        self,
        log_path: str | None = None,
        log_file: AnyIO | None = None,
        timestamp: bool = True,
    ):
        self._timestamp: bool = timestamp
        self._log_path: str | None = log_path

        self._log_file_handle: AnyIO

        if (log_path is None) and (log_file is None):
            print(
                "[logger_internal] # no log file specified, will only write to console",
                sys.stderr,
            )
            self._log_file_handle = sys.stdout

        elif (log_path is not None) and (log_file is not None):
            raise ValueError(
                "cannot specify both log_path and log_file, use streams in `SimpleLogger`"
            )
        else:
            # now exactly one of the two is None
            if log_file is not None:
                self._log_file_handle = log_file
            else:
                assert log_path is not None
                self._log_file_handle = open(log_path, "w", encoding="utf-8")

    def log(self, msg: JSONitem, console_print: bool = False, **kwargs):
        """log a message to the log file, and optionally to the console"""
        if console_print:
            print(msg)

        if not isinstance(msg, typing.Mapping):
            msg = {"_msg": msg}

        if self._timestamp:
            msg["_timestamp"] = time.time()

        if len(kwargs) > 0:
            msg["_kwargs"] = kwargs

        self._log_file_handle.write(json.dumps(json_serialize(msg)) + "\n")
