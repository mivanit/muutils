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
import re

# type defs
_ExpType = typing.TypeVar("_ExpType")
_ExpType_dict = typing.TypeVar(
    "_ExpType_dict", bound=typing.Dict[typing.Any, typing.Any]
)
_ExpType_list = typing.TypeVar("_ExpType_list", bound=typing.List[typing.Any])


# TypedDict definitions for configuration dictionaries
class DBGDictDefaultsType(typing.TypedDict):
    key_types: bool
    val_types: bool
    max_len: int
    indent: str
    max_depth: int


class DBGListDefaultsType(typing.TypedDict):
    max_len: int
    summary_show_types: bool


class DBGTensorArraySummaryDefaultsType(typing.TypedDict):
    fmt: typing.Literal["unicode", "latex", "ascii"]
    precision: int
    stats: bool
    shape: bool
    dtype: bool
    device: bool
    requires_grad: bool
    sparkline: bool
    sparkline_bins: int
    sparkline_logy: typing.Union[None, bool]
    colored: bool
    eq_char: str


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
    line_exp: str = "unknown"
    current_file: str = "unknown"
    dbg_frame: typing.Optional[inspect.FrameInfo] = None
    for frame in inspect.stack():
        if frame.code_context is None:
            continue
        line: str = frame.code_context[0]
        if "dbg" in line:
            current_file = _process_path(Path(frame.filename))
            dbg_frame = frame
            start: int = line.find("(") + 1
            end: int = line.rfind(")")
            if end == -1:
                end = len(line)
            line_exp = line[start:end]
            break

    fname: str = "unknown"
    if current_file.startswith("/tmp/ipykernel_"):
        stack: list[inspect.FrameInfo] = inspect.stack()
        filtered_functions: list[str] = []
        # this loop will find, in this order:
        # - the dbg function call
        # - the functions we care about displaying
        # - `<module>`
        # - a bunch of jupyter internals we don't care about
        for frame_info in stack:
            if _process_path(Path(frame_info.filename)) != current_file:
                continue
            if frame_info.function == "<module>":
                break
            if frame_info.function.startswith("dbg"):
                continue
            filtered_functions.append(frame_info.function)
        if dbg_frame is not None:
            filtered_functions.append(f"<ipykernel>:{dbg_frame.lineno}")
        else:
            filtered_functions.append(current_file)
        filtered_functions.reverse()
        fname = " -> ".join(filtered_functions)
    elif dbg_frame is not None:
        fname = f"{current_file}:{dbg_frame.lineno}"

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

DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS: DBGTensorArraySummaryDefaultsType = {
    "fmt": "unicode",
    "precision": 2,
    "stats": True,
    "shape": True,
    "dtype": True,
    "device": True,
    "requires_grad": True,
    "sparkline": True,
    "sparkline_bins": 7,
    "sparkline_logy": None,  # None means auto-detect
    "colored": True,
    "eq_char": "=",
}


DBG_TENSOR_VAL_JOINER: str = ": "


def tensor_info(tensor: typing.Any) -> str:
    from muutils.tensor_info import array_summary

    # TODO: explicitly pass args to avoid type: ignore (mypy can't match overloads with **TypedDict spread)
    return array_summary(tensor, as_list=False, **DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS)  # type: ignore[call-overload]


DBG_DICT_DEFAULTS: DBGDictDefaultsType = {
    "key_types": True,
    "val_types": True,
    "max_len": 32,
    "indent": "  ",
    "max_depth": 3,
}

DBG_LIST_DEFAULTS: DBGListDefaultsType = {
    "max_len": 16,
    "summary_show_types": True,
}


def list_info(
    lst: typing.List[typing.Any],
) -> str:
    len_l: int = len(lst)
    output: str
    if len_l > DBG_LIST_DEFAULTS["max_len"]:
        output = f"<list of len()={len_l}"
        if DBG_LIST_DEFAULTS["summary_show_types"]:
            val_types: typing.Set[str] = set(type(x).__name__ for x in lst)
            output += f", types={{{', '.join(sorted(val_types))}}}"
        output += ">"
    else:
        output = "[" + ", ".join(repr(x) for x in lst) + "]"

    return output


TENSOR_STR_TYPES: typing.Set[str] = {
    "<class 'torch.Tensor'>",
    "<class 'numpy.ndarray'>",
}


def dict_info(
    d: typing.Dict[typing.Any, typing.Any],
    depth: int = 0,
) -> str:
    len_d: int = len(d)
    indent: str = DBG_DICT_DEFAULTS["indent"]

    # summary line
    output: str = f"{indent * depth}<dict of len()={len_d}"

    if DBG_DICT_DEFAULTS["key_types"] and len_d > 0:
        key_types: typing.Set[str] = set(type(k).__name__ for k in d.keys())
        key_types_str: str = "{" + ", ".join(sorted(key_types)) + "}"
        output += f", key_types={key_types_str}"

    if DBG_DICT_DEFAULTS["val_types"] and len_d > 0:
        val_types: typing.Set[str] = set(type(v).__name__ for v in d.values())
        val_types_str: str = "{" + ", ".join(sorted(val_types)) + "}"
        output += f", val_types={val_types_str}"

    output += ">"

    # keys/values if not to deep and not too many
    if depth < DBG_DICT_DEFAULTS["max_depth"]:
        if len_d > 0 and len_d < DBG_DICT_DEFAULTS["max_len"]:
            for k, v in d.items():
                key_str: str = repr(k) if not isinstance(k, str) else k

                val_str: str
                val_type_str: str = str(type(v))
                if isinstance(v, dict):
                    val_str = dict_info(v, depth + 1)
                elif val_type_str in TENSOR_STR_TYPES:
                    val_str = tensor_info(v)
                elif isinstance(v, list):
                    val_str = list_info(v)
                else:
                    val_str = repr(v)

                output += (
                    f"\n{indent * (depth + 1)}{key_str}{DBG_TENSOR_VAL_JOINER}{val_str}"
                )

    return output


def info_auto(
    obj: typing.Any,
) -> str:
    """Automatically format an object for debugging."""
    if isinstance(obj, dict):
        return dict_info(obj)
    elif isinstance(obj, list):
        return list_info(obj)
    elif str(type(obj)) in TENSOR_STR_TYPES:
        return tensor_info(obj)
    else:
        return repr(obj)


def dbg_tensor(
    tensor: _ExpType,  # numpy array or torch tensor
) -> _ExpType:
    """dbg function for tensors, using tensor_info formatter."""
    return dbg(
        tensor,
        formatter=tensor_info,
        val_joiner=DBG_TENSOR_VAL_JOINER,
    )


def dbg_dict(
    d: _ExpType_dict,
) -> _ExpType_dict:
    """dbg function for dictionaries, using dict_info formatter."""
    return dbg(
        d,
        formatter=dict_info,
        val_joiner=DBG_TENSOR_VAL_JOINER,
    )


def dbg_auto(
    obj: _ExpType,
) -> _ExpType:
    """dbg function for automatic formatting based on type."""
    return dbg(
        obj,
        formatter=info_auto,
        val_joiner=DBG_TENSOR_VAL_JOINER,
    )


def _normalize_for_loose(text: str) -> str:
    """Normalize text for loose matching by replacing non-alphanumeric chars with spaces."""
    normalized: str = re.sub(r"[^a-zA-Z0-9]+", " ", text)
    return " ".join(normalized.split())


def _compile_pattern(
    pattern: str | re.Pattern[str],
    *,
    cased: bool = False,
    loose: bool = False,
) -> re.Pattern[str]:
    """Compile pattern with appropriate flags for case sensitivity and loose matching."""
    if isinstance(pattern, re.Pattern):
        return pattern

    # Start with no flags for case-insensitive default
    flags: int = 0
    if not cased:
        flags |= re.IGNORECASE

    if loose:
        pattern = _normalize_for_loose(pattern)

    return re.compile(pattern, flags)


def grep_repr(
    obj: typing.Any,
    pattern: str | re.Pattern[str],
    *,
    char_context: int | None = 20,
    line_context: int | None = None,
    before_context: int = 0,
    after_context: int = 0,
    context: int | None = None,
    max_count: int | None = None,
    cased: bool = False,
    loose: bool = False,
    line_numbers: bool = False,
    highlight: bool = True,
    color: str = "31",
    separator: str = "--",
    quiet: bool = False,
) -> typing.List[str] | None:
    """grep-like search on ``repr(obj)`` with improved grep-style options.

    By default, string patterns are case-insensitive. Pre-compiled regex
    patterns use their own flags.

    Parameters:
    - obj: Object to search (its repr() string is scanned)
    - pattern: Regular expression pattern (string or pre-compiled)
    - char_context: Characters of context before/after each match (default: 20)
    - line_context: Lines of context before/after; overrides char_context
    - before_context: Lines of context before match (like grep -B)
    - after_context: Lines of context after match (like grep -A)
    - context: Lines of context before AND after (like grep -C)
    - max_count: Stop after this many matches
    - cased: Force case-sensitive search for string patterns
    - loose: Normalize spaces/punctuation for flexible matching
    - line_numbers: Show line numbers in output
    - highlight: Wrap matches with ANSI color codes
    - color: ANSI color code (default: "31" for red)
    - separator: Separator between multiple matches
    - quiet: Return results instead of printing

    Returns:
    - None if quiet=False (prints to stdout)
    - List[str] if quiet=True (returns formatted output lines)
    """
    # Handle context parameter shortcuts
    if context is not None:
        before_context = after_context = context

    # Prepare text and pattern
    text: str = repr(obj)
    if loose:
        text = _normalize_for_loose(text)

    regex: re.Pattern[str] = _compile_pattern(pattern, cased=cased, loose=loose)

    def _color_match(segment: str) -> str:
        if not highlight:
            return segment
        return regex.sub(lambda m: f"\033[1;{color}m{m.group(0)}\033[0m", segment)

    output_lines: list[str] = []
    match_count: int = 0

    # Determine if we're using line-based context
    using_line_context = (
        line_context is not None or before_context > 0 or after_context > 0
    )

    if using_line_context:
        lines: list[str] = text.splitlines()
        line_starts: list[int] = []
        pos: int = 0
        for line in lines:
            line_starts.append(pos)
            pos += len(line) + 1  # +1 for newline

        processed_lines: set[int] = set()

        for match in regex.finditer(text):
            if max_count is not None and match_count >= max_count:
                break

            # Find which line contains this match
            match_line = max(
                i for i, start in enumerate(line_starts) if start <= match.start()
            )

            # Calculate context range
            ctx_before: int
            ctx_after: int
            if line_context is not None:
                ctx_before = ctx_after = line_context
            else:
                ctx_before, ctx_after = before_context, after_context

            start_line: int = max(0, match_line - ctx_before)
            end_line: int = min(len(lines), match_line + ctx_after + 1)

            # Avoid duplicate output for overlapping contexts
            line_range: set[int] = set(range(start_line, end_line))
            if line_range & processed_lines:
                continue
            processed_lines.update(line_range)

            # Format the context block
            context_lines: list[str] = []
            for i in range(start_line, end_line):
                line_text = lines[i]
                if line_numbers:
                    line_prefix = f"{i + 1}:"
                    line_text = f"{line_prefix}{line_text}"
                context_lines.append(_color_match(line_text))

            if output_lines and separator:
                output_lines.append(separator)
            output_lines.extend(context_lines)
            match_count += 1

    else:
        # Character-based context
        ctx: int = 0 if char_context is None else char_context

        for match in regex.finditer(text):
            if max_count is not None and match_count >= max_count:
                break

            start: int = max(0, match.start() - ctx)
            end: int = min(len(text), match.end() + ctx)
            snippet: str = text[start:end]

            if output_lines and separator:
                output_lines.append(separator)
            output_lines.append(_color_match(snippet))
            match_count += 1

    if quiet:
        return output_lines
    else:
        for line in output_lines:
            print(line)
        return None
