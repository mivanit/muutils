from __future__ import annotations

import json
from typing import Any, Mapping, Protocol

from muutils.json_serialize import json_serialize

# takes message, level, other data, and outputs message with appropriate header
# HeaderFunction = Callable[[str, int, Any], str]


class HeaderFunction(Protocol):
    def __call__(self, msg: Any, lvl: int, **kwargs) -> str: ...


def md_header_function(
    msg: Any,
    lvl: int,
    stream: str | None = None,
    indent_lvl: str = "  ",
    extra_indent: str = "",
    **kwargs,
) -> str:
    """standard header function. will output

    - `# {msg}`

            for levels in [0, 9]

    - `## {msg}`

            for levels in [10, 19], and so on

    - `[{stream}] # {msg}`

            for a non-`None` stream, with level headers as before

    - `!WARNING! [{stream}] {msg}`

            for level in [-9, -1]

    - `!!WARNING!! [{stream}] {msg}`

            for level in [-19, -10] and so on

    """
    stream_prefix: str = ""
    if stream is not None:
        stream_prefix = f"[{stream}] "

    lvl_div_10: int = lvl // 10

    msg_processed: str
    if isinstance(msg, Mapping):
        msg_processed = ", ".join([f"{k}: {json_serialize(v)}" for k, v in msg.items()])
    else:
        msg_processed = json.dumps(json_serialize(msg))

    if lvl >= 0:
        return f"{extra_indent}{indent_lvl * (lvl_div_10 - 1)}{stream_prefix}#{'#' * lvl_div_10 if lvl else ''} {msg_processed}"
    else:
        exclamation_pts: str = "!" * (abs(lvl) // 10)
        return f"{extra_indent}{exclamation_pts}WARNING{exclamation_pts} {stream_prefix} {msg_processed}"


HEADER_FUNCTIONS: dict[str, HeaderFunction] = {
    "md": md_header_function,
}
