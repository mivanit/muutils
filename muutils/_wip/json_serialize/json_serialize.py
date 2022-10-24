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

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, isinstance_namedtuple, try_catch


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

SerializerHandler = NamedTuple("SerializerHandler", [
    ("check", Callable[[Any], bool]), # whether to use this handler
    ("serialize", Callable[
		[Any, int, ArrayMode, ErrorMode, MonoTuple["SerializerHandler"]], # object, depth, array_mode, error_mode, handlers  
		JSONitem
	]), # how to serialize
])

DEFAULT_HANDLERS: MonoTuple[SerializerHandler] = (
    # base types
    SerializerHandler(
        lambda obj: isinstance(obj, (bool, int, float, str)),
        lambda obj: obj,
    ),
    SerializerHandler(
        lambda obj: isinstance(obj, dict),
        lambda obj: {str(k): json_serialize_handled(v) for k, v in obj.items()},
    ),
    SerializerHandler(
        isinstance_namedtuple,
        lambda obj: json_serialize_handled(dict(obj._asdict())),
    ),
    SerializerHandler(
        is_dataclass,
        lambda obj: {
            k: json_serialize_handled(getattr(obj, k)) 
            for k in obj.__dataclass_fields__
        },
    ),
    SerializerHandler(
        lambda obj: isinstance(obj, Path),
        lambda obj: obj.as_posix(),
    ),
    SerializerHandler(
        lambda obj: str(type(obj)) in SERIALIZE_DIRECT_AS_STR,
        lambda obj: str(obj),
    ),
    SerializerHandler(
        lambda obj: str(type(obj)) == "<class 'numpy.ndarray'>",
        lambda obj: serialize_array(obj),
    ),
    SerializerHandler(
        lambda obj: str(type(obj)) == "<class 'torch.Tensor'>",
        lambda obj: serialize_array(obj.detach().cpu().numpy()),
    ),
    SerializerHandler(
        lambda obj: isinstance(obj, (set, list, tuple)) or isinstance(obj, Iterable),
        lambda obj: [json_serialize_handled(x) for x in obj],
    ),
    SerializerHandler(
        lambda obj: True,
        lambda obj: {
            **{k: str(getattr(obj, k, None)) for k in SERIALIZER_SPECIAL_KEYS},
            **{k: f(obj) for k, f in SERIALIZER_SPECIAL_FUNCS.items()},
        },
    ),
)


@dataclass
class JsonSerializer:
    pass
    


def json_serialize_handled(
    obj: Any,
    depth: int = -1,
    array_mode: ArrayMode = "array_list_meta",
    error_mode: ErrorMode = "except",
    handlers: tuple[SerializerHandler, ...] = tuple(),
    **kwargs,
) -> JSONitem:


    if len(kwargs) > 0:
        warnings.warn(f"unused kwargs: {kwargs}")

    newdepth: int = depth - 1
    try:
        handlers
        
    except Exception as e:
        if error_mode == "except":
            raise e
        elif error_mode == "warn":
            warnings.warn(f"error serializing, will return as string\n{obj = }\nexception = {e}")

        return repr(obj)


