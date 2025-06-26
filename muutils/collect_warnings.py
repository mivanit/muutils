from __future__ import annotations

import sys
import warnings
from collections import Counter
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, Literal


class CollateWarnings(AbstractContextManager["CollateWarnings"]):
    """Capture every warning issued inside a `with` block and print a collated
    summary when the block exits.

    Internally this wraps `warnings.catch_warnings(record=True)` so that all
    warnings raised in the block are recorded.  When the context exits, identical
    warnings are grouped and (optionally) printed with a user-defined format.

    # Parameters:
     - `print_on_exit : bool`
       Whether to print the summary when the context exits
       (defaults to `True`)
     - `fmt : str`
       Format string used for printing each line of the summary.
       Available fields are:

       * `{count}`     : number of occurrences
       * `{filename}`  : file where the warning originated
       * `{lineno}`    : line number
       * `{category}`  : warning class name
       * `{message}`   : warning message text

       (defaults to `"({count}x) {filename}:{lineno} {category}: {message}"`)

    # Returns:
     - `CollateWarnings`
       The context-manager instance.  After exit, the attribute
       `counts` holds a mapping

       ```python
       {(filename, lineno, category, message): count}
       ```

    # Usage:
    ```python
    >>> import warnings
    >>> with CollateWarnings() as cw:
    ...     warnings.warn("deprecated", DeprecationWarning)
    ...     warnings.warn("deprecated", DeprecationWarning)
    ...     warnings.warn("other", UserWarning)
    (2x) /tmp/example.py:42 DeprecationWarning: deprecated
    (1x) /tmp/example.py:43 UserWarning: other
    >>> cw.counts
    {('/tmp/example.py', 42, 'DeprecationWarning', 'deprecated'): 2,
     ('/tmp/example.py', 43, 'UserWarning', 'other'): 1}
    ```
    """

    _active: bool
    _catcher: Any
    _records: list[warnings.WarningMessage]
    counts: Counter[
        tuple[
            str,  # filename
            int,  # lineno
            str,  # category name
            str,  # message
        ]
    ]
    print_on_exit: bool
    fmt: str

    def __init__(
        self,
        print_on_exit: bool = True,
        fmt: str = "({count}x) {filename}:{lineno} {category}: {message}",
    ) -> None:
        self.print_on_exit = print_on_exit
        self.fmt = fmt
        self._active = False
        self._records = []
        self.counts = Counter()

    def __enter__(self) -> CollateWarnings:
        if self._active:
            raise RuntimeError("CollateWarnings cannot be re-entered")

        self._active = True
        self._catcher = warnings.catch_warnings(record=True)
        self._records = self._catcher.__enter__()
        warnings.simplefilter("always")  # capture every warning
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        if not self._active:
            raise RuntimeError("CollateWarnings exited twice")

        self._active = False
        # stop capturing
        self._catcher.__exit__(exc_type, exc_val, exc_tb)

        # collate
        self.counts = Counter(
            (
                rec.filename,
                rec.lineno,
                rec.category.__name__,
                str(rec.message),
            )
            for rec in self._records
        )

        if self.print_on_exit:
            for (filename, lineno, category, message), count in self.counts.items():
                print(
                    self.fmt.format(
                        count=count,
                        filename=filename,
                        lineno=lineno,
                        category=category,
                        message=message,
                    ),
                    file=sys.stderr,
                )

        # propagate any exception from the with-block
        return False
