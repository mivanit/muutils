"""submodule for serializing things to json in a recoverable way

you can throw *any* object into `muutils.json_serialize.json_serialize`
and it will return a `JSONitem`, meaning a bool, int, float, str, None, list of `JSONitem`s, or a dict mappting to `JSONitem`.

The goal of this is if you want to just be able to store something as relatively human-readable JSON, and don't care as much about recovering it, you can throw it into `json_serialize` and it will just work. If you want to do so in a recoverable way, check out [`ZANJ`](https://github.com/mivanit/ZANJ).

it will do so by looking in `DEFAULT_HANDLERS`, which will keep it as-is if its already valid, then try to find a `.serialize()` method on the object, and then have a bunch of special cases. You can add handlers by initializing a `JsonSerializer` object and passing a sequence of them to `handlers_pre`

additionally, `SerializeableDataclass` is a special kind of dataclass where you specify how to serialize each field, and a `.serialize()` method is automatically added to the class. This is done by using the `serializable_dataclass` decorator, inheriting from `SerializeableDataclass`, and `serializable_field` in place of `dataclasses.field` when defining non-standard fields.

This module plays nicely with and is a dependency of the [`ZANJ`](https://github.com/mivanit/ZANJ) library, which extends this to support saving things to disk in a more efficient way than just plain json (arrays are saved as npy files, for example), and automatically detecting how to load saved objects into their original classes.

"""

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
