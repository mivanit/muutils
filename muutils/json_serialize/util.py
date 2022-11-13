import functools
import json
from pathlib import Path
import types
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union, Callable, Literal, Iterable
from dataclasses import dataclass, is_dataclass, asdict
from collections import namedtuple
import inspect
import typing
import warnings


_NUMPY_WORKING: bool
try:
    import numpy as np
    _NUMPY_WORKING = True
except ImportError:
    warnings.warn("numpy not found, cannot serialize numpy arrays!")
    _NUMPY_WORKING = False

ErrorMode = Literal["ignore", "warn", "except"]
TypeErrorMode = Union[ErrorMode, Literal["try_convert"]]


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
        if isinstance(params, (type, types.UnionType)):
            return types.GenericAlias(tuple, (params, Ellipsis))
        # test if has len and is iterable
        elif isinstance(params, Iterable):
            if len(params) == 0:
                return tuple
            elif len(params) == 1:
                return types.GenericAlias(tuple, (params[0], Ellipsis))
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



def _recursive_hashify(obj: Any, force: bool = True) -> Hashableitem:
    if isinstance(obj, dict):
        return tuple(
            (k, _recursive_hashify(v)) 
            for k, v in obj.items()
        )
    elif isinstance(obj, (tuple, list, Iterable)):
        return tuple(
            _recursive_hashify(v)
            for v in obj
        )
    elif isinstance(obj, (bool, int, float, str)):
        return obj
    else:
        if force:
            return str(obj)
        else:
            raise ValueError(f"cannot hashify:\n{obj}")



class SerializationException(Exception):
    pass


def string_as_lines(s: str) -> list[str]:
    """for easier reading of long strings in json, split up by newlines
    
    sort of like how jupyter notebooks do it
    """

    return s.splitlines(keepends=False)