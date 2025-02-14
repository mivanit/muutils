"""provides the basic framework for json serialization of objects

notably:

- `SerializerHandler` defines how to serialize a specific type of object
- `JsonSerializer` handles configuration for which handlers to use
- `json_serialize` provides the default configuration if you don't care -- call it on any object!

"""

from __future__ import annotations

import inspect
import warnings
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Set, Union

from muutils.errormode import ErrorMode

try:
    from muutils.json_serialize.array import ArrayMode, serialize_array
except ImportError as e:
    ArrayMode = str  # type: ignore[misc]
    serialize_array = lambda *args, **kwargs: None  # noqa: E731
    warnings.warn(
        f"muutils.json_serialize.array could not be imported probably because missing numpy, array serialization will not work: \n{e}",
        ImportWarning,
    )

from muutils.json_serialize.util import (
    _FORMAT_KEY,
    Hashableitem,
    JSONitem,
    MonoTuple,
    SerializationException,
    _recursive_hashify,
    isinstance_namedtuple,
    safe_getsource,
    string_as_lines,
    try_catch,
)

# pylint: disable=protected-access

SERIALIZER_SPECIAL_KEYS: MonoTuple[str] = (
    "__name__",
    "__doc__",
    "__module__",
    "__class__",
    "__dict__",
    "__annotations__",
)

SERIALIZER_SPECIAL_FUNCS: dict[str, Callable] = {
    "str": str,
    "dir": dir,
    "type": try_catch(lambda x: str(type(x).__name__)),
    "repr": try_catch(lambda x: repr(x)),
    "code": try_catch(lambda x: inspect.getsource(x)),
    "sourcefile": try_catch(lambda x: inspect.getsourcefile(x)),
}

SERIALIZE_DIRECT_AS_STR: Set[str] = {
    "<class 'torch.device'>",
    "<class 'torch.dtype'>",
}

ObjectPath = MonoTuple[Union[str, int]]


@dataclass
class SerializerHandler:
    """a handler for a specific type of object

    # Parameters:
        - `check : Callable[[JsonSerializer, Any], bool]` takes a JsonSerializer and an object, returns whether to use this handler
        - `serialize : Callable[[JsonSerializer, Any, ObjectPath], JSONitem]` takes a JsonSerializer, an object, and the current path, returns the serialized object
        - `desc : str` description of the handler (optional)
    """

    # (self_config, object) -> whether to use this handler
    check: Callable[["JsonSerializer", Any, ObjectPath], bool]
    # (self_config, object, path) -> serialized object
    serialize_func: Callable[["JsonSerializer", Any, ObjectPath], JSONitem]
    # unique identifier for the handler
    uid: str
    # description of this serializer
    desc: str

    def serialize(self) -> dict:
        """serialize the handler info"""
        return {
            # get the code and doc of the check function
            "check": {
                "code": safe_getsource(self.check),
                "doc": string_as_lines(self.check.__doc__),
            },
            # get the code and doc of the load function
            "serialize_func": {
                "code": safe_getsource(self.serialize_func),
                "doc": string_as_lines(self.serialize_func.__doc__),
            },
            # get the uid, source_pckg, priority, and desc
            "uid": str(self.uid),
            "source_pckg": getattr(self.serialize_func, "source_pckg", None),
            "__module__": getattr(self.serialize_func, "__module__", None),
            "desc": str(self.desc),
        }


BASE_HANDLERS: MonoTuple[SerializerHandler] = (
    SerializerHandler(
        check=lambda self, obj, path: isinstance(
            obj, (bool, int, float, str, type(None))
        ),
        serialize_func=lambda self, obj, path: obj,
        uid="base types",
        desc="base types (bool, int, float, str, None)",
    ),
    SerializerHandler(
        check=lambda self, obj, path: isinstance(obj, Mapping),
        serialize_func=lambda self, obj, path: {
            str(k): self.json_serialize(v, tuple(path) + (k,)) for k, v in obj.items()
        },
        uid="dictionaries",
        desc="dictionaries",
    ),
    SerializerHandler(
        check=lambda self, obj, path: isinstance(obj, (list, tuple)),
        serialize_func=lambda self, obj, path: [
            self.json_serialize(x, tuple(path) + (i,)) for i, x in enumerate(obj)
        ],
        uid="(list, tuple) -> list",
        desc="lists and tuples as lists",
    ),
)


def _serialize_override_serialize_func(
    self: "JsonSerializer", obj: Any, path: ObjectPath
) -> JSONitem:
    # obj_cls: type = type(obj)
    # if hasattr(obj_cls, "_register_self") and callable(obj_cls._register_self):
    #     obj_cls._register_self()

    # get the serialized object
    return obj.serialize()


DEFAULT_HANDLERS: MonoTuple[SerializerHandler] = tuple(BASE_HANDLERS) + (
    SerializerHandler(
        # TODO: allow for custom serialization handler name
        check=lambda self, obj, path: hasattr(obj, "serialize")
        and callable(obj.serialize),
        serialize_func=_serialize_override_serialize_func,
        uid=".serialize override",
        desc="objects with .serialize method",
    ),
    SerializerHandler(
        check=lambda self, obj, path: isinstance_namedtuple(obj),
        serialize_func=lambda self, obj, path: self.json_serialize(dict(obj._asdict())),
        uid="namedtuple -> dict",
        desc="namedtuples as dicts",
    ),
    SerializerHandler(
        check=lambda self, obj, path: is_dataclass(obj),
        serialize_func=lambda self, obj, path: {
            k: self.json_serialize(getattr(obj, k), tuple(path) + (k,))
            for k in obj.__dataclass_fields__
        },
        uid="dataclass -> dict",
        desc="dataclasses as dicts",
    ),
    SerializerHandler(
        check=lambda self, obj, path: isinstance(obj, Path),
        serialize_func=lambda self, obj, path: obj.as_posix(),
        uid="path -> str",
        desc="Path objects as posix strings",
    ),
    SerializerHandler(
        check=lambda self, obj, path: str(type(obj)) in SERIALIZE_DIRECT_AS_STR,
        serialize_func=lambda self, obj, path: str(obj),
        uid="obj -> str(obj)",
        desc="directly serialize objects in `SERIALIZE_DIRECT_AS_STR` to strings",
    ),
    SerializerHandler(
        check=lambda self, obj, path: str(type(obj)) == "<class 'numpy.ndarray'>",
        serialize_func=lambda self, obj, path: serialize_array(self, obj, path=path),
        uid="numpy.ndarray",
        desc="numpy arrays",
    ),
    SerializerHandler(
        check=lambda self, obj, path: str(type(obj)) == "<class 'torch.Tensor'>",
        serialize_func=lambda self, obj, path: serialize_array(
            self, obj.detach().cpu(), path=path
        ),
        uid="torch.Tensor",
        desc="pytorch tensors",
    ),
    SerializerHandler(
        check=lambda self, obj, path: (
            str(type(obj)) == "<class 'pandas.core.frame.DataFrame'>"
        ),
        serialize_func=lambda self, obj, path: {
            _FORMAT_KEY: "pandas.DataFrame",
            "columns": obj.columns.tolist(),
            "data": obj.to_dict(orient="records"),
            "path": path,  # type: ignore
        },
        uid="pandas.DataFrame",
        desc="pandas DataFrames",
    ),
    SerializerHandler(
        check=lambda self, obj, path: isinstance(obj, (set, list, tuple))
        or isinstance(obj, Iterable),
        serialize_func=lambda self, obj, path: [
            self.json_serialize(x, tuple(path) + (i,)) for i, x in enumerate(obj)
        ],
        uid="(set, list, tuple, Iterable) -> list",
        desc="sets, lists, tuples, and Iterables as lists",
    ),
    SerializerHandler(
        check=lambda self, obj, path: True,
        serialize_func=lambda self, obj, path: {
            **{k: str(getattr(obj, k, None)) for k in SERIALIZER_SPECIAL_KEYS},
            **{k: f(obj) for k, f in SERIALIZER_SPECIAL_FUNCS.items()},
        },
        uid="fallback",
        desc="fallback handler -- serialize object attributes and special functions as strings",
    ),
)


class JsonSerializer:
    """Json serialization class (holds configs)

    # Parameters:
    - `array_mode : ArrayMode`
    how to write arrays
    (defaults to `"array_list_meta"`)
    - `error_mode : ErrorMode`
    what to do when we can't serialize an object (will use repr as fallback if "ignore" or "warn")
    (defaults to `"except"`)
    - `handlers_pre : MonoTuple[SerializerHandler]`
    handlers to use before the default handlers
    (defaults to `tuple()`)
    - `handlers_default : MonoTuple[SerializerHandler]`
    default handlers to use
    (defaults to `DEFAULT_HANDLERS`)
    - `write_only_format : bool`
    changes _FORMAT_KEY keys in output to "__write_format__" (when you want to serialize something in a way that zanj won't try to recover the object when loading)
    (defaults to `False`)

    # Raises:
    - `ValueError`: on init, if `args` is not empty
    - `SerializationException`: on `json_serialize()`, if any error occurs when trying to serialize an object and `error_mode` is set to `ErrorMode.EXCEPT"`

    """

    def __init__(
        self,
        *args,
        array_mode: ArrayMode = "array_list_meta",
        error_mode: ErrorMode = ErrorMode.EXCEPT,
        handlers_pre: MonoTuple[SerializerHandler] = tuple(),
        handlers_default: MonoTuple[SerializerHandler] = DEFAULT_HANDLERS,
        write_only_format: bool = False,
    ):
        if len(args) > 0:
            raise ValueError(
                f"JsonSerializer takes no positional arguments!\n{args = }"
            )

        self.array_mode: ArrayMode = array_mode
        self.error_mode: ErrorMode = ErrorMode.from_any(error_mode)
        self.write_only_format: bool = write_only_format
        # join up the handlers
        self.handlers: MonoTuple[SerializerHandler] = tuple(handlers_pre) + tuple(
            handlers_default
        )

    def json_serialize(
        self,
        obj: Any,
        path: ObjectPath = tuple(),
    ) -> JSONitem:
        try:
            for handler in self.handlers:
                if handler.check(self, obj, path):
                    output: JSONitem = handler.serialize_func(self, obj, path)
                    if self.write_only_format:
                        if isinstance(output, dict) and _FORMAT_KEY in output:
                            new_fmt: JSONitem = output.pop(_FORMAT_KEY)
                            output["__write_format__"] = new_fmt
                    return output

            raise ValueError(f"no handler found for object with {type(obj) = }")

        except Exception as e:
            if self.error_mode == "except":
                obj_str: str = repr(obj)
                if len(obj_str) > 1000:
                    obj_str = obj_str[:1000] + "..."
                raise SerializationException(
                    f"error serializing at {path = } with last handler: '{handler.uid}'\nfrom: {e}\nobj: {obj_str}"
                ) from e
            elif self.error_mode == "warn":
                warnings.warn(
                    f"error serializing at {path = }, will return as string\n{obj = }\nexception = {e}"
                )

            return repr(obj)

    def hashify(
        self,
        obj: Any,
        path: ObjectPath = tuple(),
        force: bool = True,
    ) -> Hashableitem:
        """try to turn any object into something hashable"""
        data = self.json_serialize(obj, path=path)

        # recursive hashify, turning dicts and lists into tuples
        return _recursive_hashify(data, force=force)


GLOBAL_JSON_SERIALIZER: JsonSerializer = JsonSerializer()


def json_serialize(obj: Any, path: ObjectPath = tuple()) -> JSONitem:
    """serialize object to json-serializable object with default config"""
    return GLOBAL_JSON_SERIALIZER.json_serialize(obj, path=path)
