"""base types, lets us avoid import cycles"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Union, Tuple

if TYPE_CHECKING:
    from muutils.json_serialize.util import JSONitem


BaseType = Union[
    bool,
    int,
    float,
    str,
    None,
]

Hashableitem = Union[BaseType, Tuple["Hashableitem", ...]]


_FORMAT_KEY: Literal["__muutils_format__"] = "__muutils_format__"
_REF_KEY: Literal["$ref"] = "$ref"


# TypedDicts for serialized set/frozenset - using Total=False workaround for 3.8 compat
# These are used by @overload signatures for better type narrowing
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class _SerializedSet(TypedDict):
    """TypedDict for serialized set objects."""

    __muutils_format__: Literal["set"]
    data: List["JSONitem"]


class _SerializedFrozenset(TypedDict):
    """TypedDict for serialized frozenset objects."""

    __muutils_format__: Literal["frozenset"]
    data: List["JSONitem"]
