"""utilities for json_serialize"""

from __future__ import annotations

import dataclasses
import functools
import inspect
import sys
import typing
import warnings
from typing import Any, Callable, Iterable, Union

_NUMPY_WORKING: bool
try:
    _NUMPY_WORKING = True
except ImportError:
    warnings.warn("numpy not found, cannot serialize numpy arrays!")
    _NUMPY_WORKING = False


BaseType = Union[
    bool,
    int,
    float,
    str,
    None,
]

JSONitem = Union[
    BaseType,
    # mypy doesn't like recursive types, so we just go down a few levels manually
    typing.List[Union[BaseType, typing.List[Any], typing.Dict[str, Any]]],
    typing.Dict[str, Union[BaseType, typing.List[Any], typing.Dict[str, Any]]],
]
JSONdict = typing.Dict[str, JSONitem]

Hashableitem = Union[bool, int, float, str, tuple]


_FORMAT_KEY: str = "__muutils_format__"
_REF_KEY: str = "$ref"

# or if python version <3.9
if typing.TYPE_CHECKING or sys.version_info < (3, 9):
    MonoTuple = typing.Sequence
else:

    class MonoTuple:
        """tuple type hint, but for a tuple of any length with all the same type"""

        __slots__ = ()

        def __new__(cls, *args, **kwargs):
            raise TypeError("Type MonoTuple cannot be instantiated.")

        def __init_subclass__(cls, *args, **kwargs):
            raise TypeError(f"Cannot subclass {cls.__module__}")

        # idk why mypy thinks there is no such function in typing
        @typing._tp_cache  # type: ignore
        def __class_getitem__(cls, params):
            if getattr(params, "__origin__", None) == typing.Union:
                return typing.GenericAlias(tuple, (params, Ellipsis))
            elif isinstance(params, type):
                typing.GenericAlias(tuple, (params, Ellipsis))
            # test if has len and is iterable
            elif isinstance(params, Iterable):
                if len(params) == 0:
                    return tuple
                elif len(params) == 1:
                    return typing.GenericAlias(tuple, (params[0], Ellipsis))
            else:
                raise TypeError(f"MonoTuple expects 1 type argument, got {params = }")


class UniversalContainer:
    """contains everything -- `x in UniversalContainer()` is always True"""

    def __contains__(self, x: Any) -> bool:
        return True


def isinstance_namedtuple(x: Any) -> bool:
    """checks if `x` is a `namedtuple`

    credit to https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
    """
    t: type = type(x)
    b: tuple = t.__bases__
    if len(b) != 1 or (b[0] is not tuple):
        return False
    f: Any = getattr(t, "_fields", None)
    if not isinstance(f, tuple):
        return False
    return all(isinstance(n, str) for n in f)


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
    if isinstance(obj, typing.Mapping):
        return tuple((k, _recursive_hashify(v)) for k, v in obj.items())
    elif isinstance(obj, (tuple, list, Iterable)):
        return tuple(_recursive_hashify(v) for v in obj)
    elif isinstance(obj, (bool, int, float, str)):
        return obj
    else:
        if force:
            return str(obj)
        else:
            raise ValueError(f"cannot hashify:\n{obj}")


class SerializationException(Exception):
    pass


def string_as_lines(s: str | None) -> list[str]:
    """for easier reading of long strings in json, split up by newlines

    sort of like how jupyter notebooks do it
    """
    if s is None:
        return list()
    else:
        return s.splitlines(keepends=False)


def safe_getsource(func) -> list[str]:
    try:
        return string_as_lines(inspect.getsource(func))
    except Exception as e:
        return string_as_lines(f"Error: Unable to retrieve source code:\n{e}")


# credit to https://stackoverflow.com/questions/51743827/how-to-compare-equality-of-dataclasses-holding-numpy-ndarray-boola-b-raises
def array_safe_eq(a: Any, b: Any) -> bool:
    """check if two objects are equal, account for if numpy arrays or torch tensors"""
    if a is b:
        return True

    if type(a) is not type(b):
        return False

    if (
        str(type(a)) == "<class 'numpy.ndarray'>"
        and str(type(b)) == "<class 'numpy.ndarray'>"
    ) or (
        str(type(a)) == "<class 'torch.Tensor'>"
        and str(type(b)) == "<class 'torch.Tensor'>"
    ):
        return (a == b).all()

    if (
        str(type(a)) == "<class 'pandas.core.frame.DataFrame'>"
        and str(type(b)) == "<class 'pandas.core.frame.DataFrame'>"
    ):
        return a.equals(b)

    if isinstance(a, typing.Sequence) and isinstance(b, typing.Sequence):
        if len(a) == 0 and len(b) == 0:
            return True
        return len(a) == len(b) and all(array_safe_eq(a1, b1) for a1, b1 in zip(a, b))

    if isinstance(a, (dict, typing.Mapping)) and isinstance(b, (dict, typing.Mapping)):
        return len(a) == len(b) and all(
            array_safe_eq(k1, k2) and array_safe_eq(a[k1], b[k2])
            for k1, k2 in zip(a.keys(), b.keys())
        )

    try:
        return bool(a == b)
    except (TypeError, ValueError) as e:
        warnings.warn(f"Cannot compare {a} and {b} for equality\n{e}")
        return NotImplemented  # type: ignore[return-value]


def dc_eq(
    dc1,
    dc2,
    except_when_class_mismatch: bool = False,
    false_when_class_mismatch: bool = True,
    except_when_field_mismatch: bool = False,
) -> bool:
    """
    checks if two dataclasses which (might) hold numpy arrays are equal

    # Parameters:

    - `dc1`: the first dataclass
    - `dc2`: the second dataclass
    - `except_when_class_mismatch: bool`
        if `True`, will throw `TypeError` if the classes are different.
        if not, will return false by default or attempt to compare the fields if `false_when_class_mismatch` is `False`
        (default: `False`)
    - `false_when_class_mismatch: bool`
        only relevant if `except_when_class_mismatch` is `False`.
        if `True`, will return `False` if the classes are different.
        if `False`, will attempt to compare the fields.
    - `except_when_field_mismatch: bool`
        only relevant if `except_when_class_mismatch` is `False` and `false_when_class_mismatch` is `False`.
        if `True`, will throw `TypeError` if the fields are different.
        (default: `True`)

    # Returns:
    - `bool`: True if the dataclasses are equal, False otherwise

    # Raises:
    - `TypeError`: if the dataclasses are of different classes
    - `AttributeError`: if the dataclasses have different fields

    # TODO: after "except when class mismatch" is False, shouldn't we then go to "field keys match"?
    ```
              [START]
                 ▼
           ┌───────────┐  ┌─────────┐
           │dc1 is dc2?├─►│ classes │
           └──┬────────┘No│ match?  │
      ────    │           ├─────────┤
     (True)◄──┘Yes        │No       │Yes
      ────                ▼         ▼
          ┌────────────────┐ ┌────────────┐
          │ except when    │ │ fields keys│
          │ class mismatch?│ │ match?     │
          ├───────────┬────┘ ├───────┬────┘
          │Yes        │No    │No     │Yes
          ▼           ▼      ▼       ▼
     ───────────  ┌──────────┐  ┌────────┐
    { raise     } │ except   │  │ field  │
    { TypeError } │ when     │  │ values │
     ───────────  │ field    │  │ match? │
                  │ mismatch?│  ├────┬───┘
                  ├───────┬──┘  │    │Yes
                  │Yes    │No   │No  ▼
                  ▼       ▼     │   ────
     ───────────────     ─────  │  (True)
    { raise         }   (False)◄┘   ────
    { AttributeError}    ─────
     ───────────────
    ```

    """
    if dc1 is dc2:
        return True

    if dc1.__class__ is not dc2.__class__:
        if except_when_class_mismatch:
            # if the classes don't match, raise an error
            raise TypeError(
                f"Cannot compare dataclasses of different classes: `{dc1.__class__}` and `{dc2.__class__}`"
            )
        if except_when_field_mismatch:
            dc1_fields: set = set([fld.name for fld in dataclasses.fields(dc1)])
            dc2_fields: set = set([fld.name for fld in dataclasses.fields(dc2)])
            fields_match: bool = set(dc1_fields) == set(dc2_fields)
            if not fields_match:
                # if the fields match, keep going
                raise AttributeError(
                    f"dataclasses {dc1} and {dc2} have different fields: `{dc1_fields}` and `{dc2_fields}`"
                )
        return False

    return all(
        array_safe_eq(getattr(dc1, fld.name), getattr(dc2, fld.name))
        for fld in dataclasses.fields(dc1)
        if fld.compare
    )
