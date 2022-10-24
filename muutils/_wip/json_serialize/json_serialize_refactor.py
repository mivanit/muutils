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

# TODO: this isnt done yet


_NUMPY_WORKING: bool
try:
    import numpy as np
    _NUMPY_WORKING = True
except ImportError:
    warnings.warn("numpy not found, cannot serialize numpy arrays!")
    _NUMPY_WORKING = False

JSONitem = Union[bool, int, float, str, list, dict, None]
Hashableitem = Union[bool, int, float, str, tuple]

class MonoTuple:
	"""tuple type hint, but for a tuple of any length with all the same type"""
	__slots__ = ()

	def __new__(cls, *args, **kwargs):
		raise TypeError("Type MonoTuple cannot be instantiated.")

	def __init_subclass__(cls, *args, **kwargs):
		raise TypeError(f"Cannot subclass {cls.__module__}")

	@typing._tp_cache
	def __class_getitem__(cls, params):
		if len(params) == 0:
			return tuple
		elif len(params) == 1:
			return GenericAlias(tuple, (params[0], Ellipsis))
		else:
			raise TypeError(f"MonoTuple expects 1 type argument, got {len(params) = } \n\t{params = }")


class UniversalContainer:
    """contains everything -- `x in UniversalContainer()` is always True"""
    def __contains__(self, x: Any) -> bool:
        return True


def isinstance_namedtuple(x):
    """checks if `x` is a `namedtuple`

    credit to https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
    """
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, "_fields", None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def try_catch(func: Callable):
    """wraps the function to catch exceptions, returns serialized error message on exception
    
    returned func will return normal result on success, or error message on exception
    """
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"{e.__class__.__name__}: {e}"

    return newfunc


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

ArrayMode = Literal["list", "array_list_meta", "array_hex_meta"]


def serialize_array(arr: Any, array_mode: ArrayMode = "array_list_meta") -> JSONitem:
    """serialize a numpy or pytorch array in one of several modes

    if the object is zero-dimensional, simply get the unique item

    `array_mode: ArrayMode` can be one of:
    - `list`: serialize as a list of values, no metadata (equivalent to `arr.tolist()`)
    - `array_list_meta`: serialize dict with metadata, actual list under the key `data`
    - `array_hex_meta`: serialize dict with metadata, actual hex string under the key `data`

    for the latter two, the output will look like
    ```
    {
        "__format__": <array_list_meta|array_hex_meta>,
        "shape": arr.shape,
        "dtype": str(arr.dtype),
        "data": <arr.tolist()|arr.tobytes().hex()>,
    }
    ```

    # Parameters:
     - `arr : Any` array to serialize
     - `array_mode : ArrayMode` mode in which to serialize the array  
       (defaults to `"array_list_meta"`)  
    
    # Returns:
     - `JSONitem` 
       json serialized array
    
    # Raises:
     - `KeyError` : if the array mode is not valid
    """    

    if len(arr.shape) == 0:
        return arr.item()
    
    if array_mode == "array_list_meta":
        return {
            "__format__": "array_list_meta",
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "data": arr.tolist(),
        }
    elif array_mode == "list":
        return arr.tolist()
    elif array_mode == "array_hex_meta":
        return {
            "__format__": "array_hex_meta",
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "data": arr.tobytes().hex(),
        }
    else:
        raise KeyError(f"invalid array_mode: {array_mode}")

def infer_array_mode(arr: JSONitem) -> ArrayMode:
    """given a serialized array, infer the mode
    
    assumes the array was serialized via `serialize_array()`
    """
    if isinstance(arr, dict):
        fmt: Optional[str] = arr.get("__format__", None)
        if fmt == "array_list_meta":
            if type(arr["data"]) != list:
                raise ValueError(f"invalid list format: {arr}")
            return fmt
        elif fmt == "array_hex_meta":
            if type(arr["data"]) != str:
                raise ValueError(f"invalid hex format: {arr}")
            return fmt
        else:
            raise ValueError(f"invalid format: {arr}")

    elif isinstance(arr, list):
        return "list"
    else:
        raise ValueError(f"cannot infer array_mode from {arr}")

def load_array(arr: JSONitem, array_mode: Optional[ArrayMode] = None) -> Any:
    """load a json-serialized array, infer the mode if not specified"""
    # try to infer the array_mode
    array_mode_inferred: ArrayMode = infer_array_mode(arr)
    if array_mode is None:
        array_mode = array_mode_inferred
    elif array_mode != array_mode_inferred:
        warnings.warn(f"array_mode {array_mode} does not match inferred array_mode {array_mode_inferred}")        

    # actually load the array
    if array_mode == "array_list_meta":
        data = np.array(arr["data"], dtype=arr["dtype"])
        if tuple(arr["shape"]) != tuple(data.shape):
            raise ValueError(f"invalid shape: {arr}")
        return data
    elif array_mode == "array_hex_meta":
        data = np.frombuffer(bytes.fromhex(arr["data"]), dtype=arr["dtype"])
        return data.reshape(arr["shape"])
    elif array_mode == "list":
        return np.array(arr)
    else:
        raise ValueError(f"invalid array_mode: {array_mode}")

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


