"""base types, lets us avoid import cycles"""

from __future__ import annotations

from typing import Final, Union


BaseType = Union[
    bool,
    int,
    float,
    str,
    None,
]

Hashableitem = Union[bool, int, float, str, tuple]  # pyright: ignore[reportMissingTypeArgument]


_FORMAT_KEY: Final[str] = "__muutils_format__"
_REF_KEY: Final[str] = "$ref"
