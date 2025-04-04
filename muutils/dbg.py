"""

this code is based on an implementation of the Rust builtin `dbg!` for Python, originally from
https://github.com/tylerwince/pydbg/blob/master/pydbg.py
although it has been significantly modified

licensed under MIT:

Copyright (c) 2019 Tyler Wince

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from __future__ import annotations

import inspect
import sys
import typing
from pathlib import Path
import functools

# type defs
_ExpType = typing.TypeVar("_ExpType")


# Sentinel type for no expression passed
class _NoExpPassedSentinel:
    """Unique sentinel type used to indicate that no expression was passed."""

    pass


_NoExpPassed = _NoExpPassedSentinel()

# global variables
_CWD: Path = Path.cwd().absolute()
_COUNTER: int = 0

# configuration
PATH_MODE: typing.Literal["relative", "absolute"] = "relative"
DEFAULT_VAL_JOINER: str = " = "


# path processing
def _process_path(path: Path) -> str:
    path_abs: Path = path.absolute()
    fname: Path
    if PATH_MODE == "absolute":
        fname = path_abs
    elif PATH_MODE == "relative":
        try:
            # if it's inside the cwd, print the relative path
            fname = path.relative_to(_CWD)
        except ValueError:
            # if its not in the subpath, use the absolute path
            fname = path_abs
    else:
        raise ValueError("PATH_MODE must be either 'relative' or 'absolute")

    return fname.as_posix()


# actual dbg function
@typing.overload
def dbg() -> _NoExpPassedSentinel: ...
@typing.overload
def dbg(
    exp: _NoExpPassedSentinel,
    formatter: typing.Optional[typing.Callable[[typing.Any], str]] = None,
    val_joiner: str = DEFAULT_VAL_JOINER,
) -> _NoExpPassedSentinel: ...
@typing.overload
def dbg(
    exp: _ExpType,
    formatter: typing.Optional[typing.Callable[[typing.Any], str]] = None,
    val_joiner: str = DEFAULT_VAL_JOINER,
) -> _ExpType: ...
def dbg(
    exp: typing.Union[_ExpType, _NoExpPassedSentinel] = _NoExpPassed,
    formatter: typing.Optional[typing.Callable[[typing.Any], str]] = None,
    val_joiner: str = DEFAULT_VAL_JOINER,
) -> typing.Union[_ExpType, _NoExpPassedSentinel]:
    """Call dbg with any variable or expression.

    Calling dbg will print to stderr the current filename and lineno,
    as well as the passed expression and what the expression evaluates to:

            from muutils.dbg import dbg

            a = 2
            b = 5

            dbg(a+b)

            def square(x: int) -> int:
                    return x * x

            dbg(square(a))

    """
    global _COUNTER

    # get the context
    fname: str = "unknown"
    line_exp: str = "unknown"
    for frame in inspect.stack():
        if frame.code_context is None:
            continue
        line: str = frame.code_context[0]
        if "dbg" in line:
            start: int = line.find("(") + 1
            end: int = line.rfind(")")
            if end == -1:
                end = len(line)

            fname = f"{_process_path(Path(frame.filename))}:{frame.lineno}"
            # special case for jupyter notebooks
            if fname.startswith("/tmp/ipykernel_"):
                fname = f"<ipykernel>:{frame.lineno}"

            line_exp = line[start:end]

            break

    # assemble the message
    msg: str
    if exp is _NoExpPassed:
        # if no expression is passed, just show location and counter value
        msg = f"[ {fname} ] <dbg {_COUNTER}>"
        _COUNTER += 1
    else:
        # if expression passed, format its value and show location, expr, and value
        exp_val: str = formatter(exp) if formatter else repr(exp)
        msg = f"[ {fname} ] {line_exp}{val_joiner}{exp_val}"

    # print the message
    print(
        msg,
        file=sys.stderr,
    )

    # return the expression itself
    return exp


# formatted `dbg_*` functions with their helpers

DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS: typing.Dict[str, typing.Union[bool, int, str]] = (
    dict(
        fmt="unicode",
        precision=2,
        stats=True,
        shape=True,
        dtype=True,
        device=True,
        requires_grad=True,
        sparkline=True,
        sparkline_bins=7,
        sparkline_logy=False,
        colored=True,
        eq_char="=",
    )
)


DBG_TENSOR_VAL_JOINER: str = ": "


def tensor_info(tensor: typing.Any) -> str:
    from muutils.tensor_info import array_summary

    return array_summary(tensor, **DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS)


dbg_tensor = functools.partial(
    dbg, formatter=tensor_info, val_joiner=DBG_TENSOR_VAL_JOINER
)
