from __future__ import annotations

from muutils.json_serialize.array import arr_metadata, load_array
from muutils.json_serialize.json_serialize import (
    BASE_HANDLERS,
    JsonSerializer,
    json_serialize,
)
from muutils.json_serialize.serializable_dataclass import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)
from muutils.json_serialize.util import try_catch, JSONitem, dc_eq

__all__ = [
    # submodules
    "array",
    "json_serialize",
    "serializable_dataclass",
    "serializable_field",
    "util",
    # imports
    "arr_metadata",
    "load_array",
    "BASE_HANDLERS",
    "JSONitem",
    "JsonSerializer",
    "json_serialize",
    "try_catch",
    "JSONitem",
    "dc_eq",
    "serializable_dataclass",
    "serializable_field",
    "SerializableDataclass",
]
