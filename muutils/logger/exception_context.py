from __future__ import annotations

import json
from types import TracebackType
from typing import IO

from muutils.json_serialize import json_serialize


class ExceptionContext:
    """context manager which catches all exceptions happening while the context is open, `.write()` the exception trace to the given stream, and then raises the exception


    for example:

    ```python
    errorfile = open('error.log', 'w')

    with ExceptionContext(errorfile):
            # do something that might throw an exception
            # if it does, the exception trace will be written to errorfile
            # and then the exception will be raised
    ```

    """

    def __init__(self, stream: IO[str]) -> None:
        self.stream: IO[str] = stream

    def __enter__(self) -> ExceptionContext:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> bool:
        if exc_type is not None:
            self.stream.write(
                json.dumps(
                    json_serialize(
                        {
                            "exc_type": exc_type,
                            "exc_value": exc_value,
                            "exc_traceback": exc_traceback,
                        }
                    )
                )
            )
            return False
        return True
