from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from muutils.logger.simplelogger import AnyIO, NullIO
from muutils.misc import sanitize_fname


@dataclass
class LoggingStream:
    """properties of a logging stream

    - `name: str` name of the stream
    - `aliases: set[str]` aliases for the stream
            (calls to these names will be redirected to this stream. duplicate alises will result in errors)
            TODO: perhaps duplicate alises should result in duplicate writes?
    - `file: str|bool|AnyIO|None` file to write to
            - if `None`, will write to standard log
            - if `True`, will write to `name + ".log"`
            - if `False` will "write" to `NullIO` (throw it away)
            - if a string, will write to that file
            - if a fileIO type object, will write to that object
    - `default_level: int|None` default level for this stream
    - `default_contents: dict[str, Callable[[], Any]]` default contents for this stream
    - `last_msg: tuple[float, Any]|None` last message written to this stream (timestamp, message)
    """

    name: str | None
    aliases: set[str | None] = field(default_factory=set)
    file: str | bool | AnyIO | None = None
    default_level: int | None = None
    default_contents: dict[str, Callable[[], Any]] = field(default_factory=dict)
    handler: AnyIO | None = None

    # TODO: implement last-message caching
    # last_msg: tuple[float, Any]|None = None

    def make_handler(self) -> AnyIO | None:
        if self.file is None:
            return None
        elif isinstance(self.file, str):
            # if its a string, open a file
            return open(
                self.file,
                "w",
                encoding="utf-8",
            )
        elif isinstance(self.file, bool):
            # if its a bool and true, open a file with the same name as the stream (in the current dir)
            # TODO: make this happen in the same dir as the main logfile?
            if self.file:
                return open(  # type: ignore[return-value]
                    f"{sanitize_fname(self.name)}.log.jsonl",
                    "w",
                    encoding="utf-8",
                )
            else:
                return NullIO()
        else:
            # if its neither, check it has `.write()` and `.flush()` methods
            if (
                (
                    not hasattr(self.file, "write")
                    or (not callable(self.file.write))
                    or (not hasattr(self.file, "flush"))
                    or (not callable(self.file.flush))
                )
                or (not hasattr(self.file, "close"))
                or (not callable(self.file.close))
            ):
                raise ValueError(f"stream {self.name} has invalid handler {self.file}")
            # ignore type check because we know it has a .write() method,
            # assume the user knows what they're doing
            return self.file  # type: ignore

    def __post_init__(self):
        self.aliases = set(self.aliases)
        if any(x.startswith("_") for x in self.aliases if x is not None):
            raise ValueError(
                "stream names or aliases cannot start with an underscore, sorry"
            )
        self.aliases.add(self.name)
        self.default_contents["_timestamp"] = time.time
        self.default_contents["_stream"] = lambda: self.name
        self.handler = self.make_handler()

    def __del__(self):
        if self.handler is not None:
            self.handler.flush()
            self.handler.close()

    def __str__(self):
        return f"LoggingStream(name={self.name}, aliases={self.aliases}, file={self.file}, default_level={self.default_level}, default_contents={self.default_contents})"
