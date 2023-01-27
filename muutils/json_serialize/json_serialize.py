import json
import functools
from pathlib import Path
import types
import typing
from typing import Any, Callable, Literal, Iterable
from dataclasses import dataclass, is_dataclass, asdict
from collections import namedtuple
import inspect
import warnings

from muutils.json_serialize.util import (
    JSONitem, Hashableitem, MonoTuple, UniversalContainer, ErrorMode, 
    isinstance_namedtuple, try_catch, _recursive_hashify, 
    SerializationException,
)
from muutils.json_serialize.array import serialize_array, ArrayMode

SERIALIZER_SPECIAL_KEYS: tuple[str] = (
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

SERIALIZE_DIRECT_AS_STR: set[str] = {
    "<class 'torch.device'>", "<class 'torch.dtype'>",
}

ObjectPath = MonoTuple[str|int]

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
    # optional description of how this serializer works
    desc: str = "(no description)"

BASE_HANDLERS: MonoTuple[SerializerHandler] = (
    SerializerHandler(
        check = lambda self, obj, path: isinstance(obj, (bool, int, float, str,  types.NoneType)),
        serialize_func = lambda self, obj, path: obj,
        desc = "base types",
    ),
    SerializerHandler(
        check = lambda self, obj, path: isinstance(obj, dict),
        serialize_func = lambda self, obj, path: {
            str(k): self.json_serialize(v, path + (k,)) 
            for k, v in obj.items()
        },
        desc = "dictionaries",
    ),
        SerializerHandler(
        check = lambda self, obj, path: isinstance(obj, (list, tuple)),
        serialize_func = lambda self, obj, path: [self.json_serialize(x, path + (i,)) for i, x in enumerate(obj)],
        desc = "(list, tuple) -> list",
    ),
)


DEFAULT_HANDLERS: MonoTuple[SerializerHandler] = BASE_HANDLERS + (
    SerializerHandler(
        # TODO: allow for custom serialization handler name
        check = lambda self, obj, path: hasattr(obj, "serialize") and callable(obj.serialize),
        serialize_func = lambda self, obj, path: obj.serialize(),
        desc = ".serialize override",
    ),
    SerializerHandler(
        check = lambda self, obj, path: isinstance_namedtuple(obj),
        serialize_func = lambda self, obj, path: self.json_serialize(dict(obj._asdict())),
        desc = "namedtuple -> dict",
    ),
    SerializerHandler(
        check = lambda self, obj, path: is_dataclass(obj),
        serialize_func = lambda self, obj, path: {
            k: self.json_serialize(getattr(obj, k), path + (k,))
            for k in obj.__dataclass_fields__
        },
        desc = "dataclass -> dict",
    ),
    SerializerHandler(
        check = lambda self, obj, path: isinstance(obj, Path),
        serialize_func = lambda self, obj, path: obj.as_posix(),
        desc = "path -> str",
    ),
    SerializerHandler(
        check = lambda self, obj, path: str(type(obj)) in SERIALIZE_DIRECT_AS_STR,
        serialize_func = lambda self, obj, path: str(obj),
        desc = "obj -> str(obj)",
    ),
    SerializerHandler(
        check = lambda self, obj, path: str(type(obj)) == "<class 'numpy.ndarray'>",
        serialize_func = lambda self, obj, path: serialize_array(self, obj, path=path),
        desc = "numpy.ndarray",
    ),
    SerializerHandler(
        check = lambda self, obj, path: str(type(obj)) == "<class 'torch.Tensor'>",
        serialize_func = lambda self, obj, path: serialize_array(self, obj.detach().cpu().numpy(), path=path),
        desc = "torch.Tensor",
    ),
    SerializerHandler(
        check = lambda self, obj, path: str(type(obj)) == "<class 'pandas.core.frame.DataFrame'>",
        serialize_func = lambda self, obj, path: obj.to_dict(orient="records"),
        desc = "pandas.DataFrame",
    ),
    SerializerHandler(
        check = lambda self, obj, path: isinstance(obj, (set, list, tuple)) or isinstance(obj, Iterable),
        serialize_func = lambda self, obj, path: [self.json_serialize(x, path + (i,)) for i, x in enumerate(obj)],
        desc = "(set, list, tuple, Iterable) -> list",
    ),
    SerializerHandler(
        check = lambda self, obj, path: True,
        serialize_func = lambda self, obj, path: {
            **{k: str(getattr(obj, k, None)) for k in SERIALIZER_SPECIAL_KEYS},
            **{k: f(obj) for k, f in SERIALIZER_SPECIAL_FUNCS.items()},
        },
        desc = "fallback",
    ),
)


class JsonSerializer:
    """Json serialization class (holds configs)"""

    def __init__(
            self,
            *args,
            array_mode: ArrayMode = "array_list_meta",
            error_mode: ErrorMode = "except",
            handlers_pre: MonoTuple[SerializerHandler] = tuple(),
            handlers_default: MonoTuple[SerializerHandler] = DEFAULT_HANDLERS,
        ):

        if len(args) > 0:
            raise ValueError(f"JsonSerializer takes no positional arguments!\n{args = }")
        
        self.array_mode: ArrayMode = array_mode
        self.error_mode: ErrorMode = error_mode
        # join up the handlers
        self.handlers: MonoTuple[SerializerHandler] = handlers_pre + handlers_default
    
    def json_serialize(
        self,
        obj: Any,
        path: ObjectPath = tuple(),
    ) -> JSONitem:

        try:
            for handler in self.handlers:
                if handler.check(self, obj, path):
                    return handler.serialize_func(self, obj, path)

            raise ValueError(f"no handler found for object with {type(obj) = }")

        except Exception as e:
            if self.error_mode == "except":                
                obj_str: str = repr(obj)
                if len(obj_str) > 1000:
                    obj_str = obj_str[:1000] + "..."
                raise SerializationException(f"error serializing at {path = } with last handler desc: '{handler.desc}'\nfrom: {e}\nobj: {obj_str}") from e
            elif self.error_mode == "warn":
                warnings.warn(f"error serializing at {path = }, will return as string\n{obj = }\nexception = {e}")

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



def json_serialize(obj: Any, path: ObjectPath = tuple()) -> JSONitem:
    """serialize object to json-serializable object with default config"""
    return JsonSerializer().json_serialize(obj, path=path)