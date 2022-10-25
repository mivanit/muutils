import functools
import json
from pathlib import Path
from types import GenericAlias
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union, Callable, Literal, Iterable
from dataclasses import dataclass, is_dataclass, asdict
from collections import namedtuple
import inspect
import typing
import warnings

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, ErrorMode, isinstance_namedtuple, try_catch, _recursive_hashify
from muutils._wip.json_serialize.array import serialize_array, ArrayMode


SERIALIZER_SPECIAL_KEYS: List[str] = [
    "__name__",
    "__doc__",
    "__module__",
    "__class__",
    "__dict__",
    "__annotations__",
]

SERIALIZER_SPECIAL_FUNCS: Dict[str, Callable] = {
    "str": str,
    "dir": dir,
    "type": try_catch(lambda x: str(type(x).__name__)),
    "repr": try_catch(lambda x: repr(x)),
    "code": try_catch(lambda x: inspect.getsource(x)),
    "sourcefile": try_catch(lambda x: inspect.getsourcefile(x)),
}

ErrorMode = Literal["ignore", "warn", "except"]

SERIALIZE_DIRECT_AS_STR: set[str] = {
    "<class 'torch.device'>", "<class 'torch.dtype'>",
}

# SerializerHandler = NamedTuple("SerializerHandler", [
#     # (self_config, object) -> whether to use this handler
#     ("check", Callable[["JsonSerializer", Any], bool]), 
#     ("serialize", Callable[
#         # (self_config, object, depth) -> serialized object  
# 		["JsonSerializer", Any, int], 
# 		JSONitem
# 	]),
#     ("desc", str),
# ])

@dataclass
class SerializerHandler:
    """a handler for a specific type of object
    
    # Parameters:
        - `check : Callable[[JsonSerializer, Any], bool]` takes a JsonSerializer and an object, returns whether to use this handler
        - `serialize : Callable[[JsonSerializer, Any, int], JSONitem]` takes a JsonSerializer, an object, and the current depth, returns the serialized object
        - `desc : str` description of the handler (optional)
    """    

    # (self_config, object) -> whether to use this handler
    check: Callable[["JsonSerializer", Any], bool]
    # (self_config, object, depth) -> serialized object
    serialize: Callable[["JsonSerializer", Any, int], JSONitem]
    desc: str = "(no description)"

DEFAULT_HANDLERS: MonoTuple[SerializerHandler] = (
    # TODO: allow for custom serialization handler name
    SerializerHandler(
        check = lambda self, obj: hasattr(obj, "serialize") and callable(obj.serialize),
        serialize = lambda self, obj: obj.serialize(),
        desc = ".serialize override",
    ),
    SerializerHandler(
        check = lambda self, obj: isinstance(obj, (bool, int, float, str)),
        serialize = lambda self, obj: obj,
        desc = "base types",
    ),
    SerializerHandler(
        check = lambda self, obj: isinstance(obj, dict),
        serialize = lambda self, obj: {str(k): self.json_serialize(v) for k, v in obj.items()},
        desc = "dictionaries",
    ),
    SerializerHandler(
        check = lambda self, obj: isinstance_namedtuple(obj),
        serialize = lambda self, obj: self.json_serialize(dict(obj._asdict())),
        desc = "namedtuple -> dict",
    ),
    SerializerHandler(
        check = lambda self, obj: is_dataclass(obj),
        serialize = lambda self, obj: {
            k: self.json_serialize(getattr(obj, k))
            for k in obj.__dataclass_fields__
        },
        desc = "dataclass -> dict",
    ),
    SerializerHandler(
        check = lambda self, obj: isinstance(obj, Path),
        serialize = lambda self, obj: obj.as_posix(),
        desc = "path -> str",
    ),
    SerializerHandler(
        check = lambda self, obj: str(type(obj)) in SERIALIZE_DIRECT_AS_STR,
        serialize = lambda self, obj: str(obj),
        desc = "obj -> str(obj)",
    ),
    SerializerHandler(
        check = lambda self, obj: str(type(obj)) == "<class 'numpy.ndarray'>",
        serialize = lambda self, obj: serialize_array(self, obj),
        desc = "numpy.ndarray",
    ),
    SerializerHandler(
        check = lambda self, obj: str(type(obj)) == "<class 'torch.Tensor'>",
        serialize = lambda self, obj: serialize_array(self, obj.detach().cpu().numpy()),
        desc = "torch.Tensor",
    ),
    SerializerHandler(
        check = lambda self, obj: isinstance(obj, (set, list, tuple)) or isinstance(obj, Iterable),
        serialize = lambda self, obj: [self.json_serialize(x) for x in obj],
        desc = "(set, list, tuple, Iterable) -> list",
    ),
    SerializerHandler(
        check = lambda self, obj: True,
        serialize = lambda self, obj: {
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
        depth: int = -1,
    ) -> JSONitem:

        newdepth: int = depth - 1
        try:
            for handler in self.handlers:
                if handler.check(self, obj):
                    return handler.serialize(self, obj, newdepth)

            raise ValueError(f"no handler found for object with {type(obj) = }")

        except Exception as e:
            if self.error_mode == "except":
                raise e
            elif self.error_mode == "warn":
                warnings.warn(f"error serializing, will return as string\n{obj = }\nexception = {e}")

            return repr(obj)

    def hashify(self, obj: Any, force: bool = True) -> Hashableitem:
        """try to turn any object into something hashable"""
        data = self.json_serialize(obj, depth=-1)

        # recursive hashify, turning dicts and lists into tuples
        return _recursive_hashify(data, force=force)



def json_serialize(obj: Any) -> JSONitem:
    """serialize object to json-serializable object with default config"""
    return JsonSerializer().json_serialize(obj)