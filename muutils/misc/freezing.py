from __future__ import annotations
from typing import Any, TypeVar, overload


class FrozenDict(dict):
    def __setitem__(self, key, value):
        raise AttributeError("dict is frozen")

    def __delitem__(self, key):
        raise AttributeError("dict is frozen")


class FrozenList(list):
    def __setitem__(self, index, value):
        raise AttributeError("list is frozen")

    def __delitem__(self, index):
        raise AttributeError("list is frozen")

    def append(self, value):
        raise AttributeError("list is frozen")

    def extend(self, iterable):
        raise AttributeError("list is frozen")

    def insert(self, index, value):
        raise AttributeError("list is frozen")

    def remove(self, value):
        raise AttributeError("list is frozen")

    def pop(self, index=-1):
        raise AttributeError("list is frozen")

    def clear(self):
        raise AttributeError("list is frozen")


FreezeMe = TypeVar("FreezeMe")


@overload
def freeze(instance: dict) -> FrozenDict: ...
@overload
def freeze(instance: list) -> FrozenList: ...
@overload
def freeze(instance: tuple) -> tuple: ...
@overload
def freeze(instance: set) -> frozenset: ...
@overload
def freeze(instance: FreezeMe) -> FreezeMe: ...
def freeze(instance: Any) -> Any:
    """recursively freeze an object in-place so that its attributes and elements cannot be changed

    messy in the sense that sometimes the object is modified in place, but you can't rely on that. always use the return value.

    the [gelidum](https://github.com/diegojromerolopez/gelidum/) package is a more complete implementation of this idea

    """

    # mark as frozen
    if hasattr(instance, "_IS_FROZEN"):
        if instance._IS_FROZEN:
            return instance

    # try to mark as frozen
    try:
        instance._IS_FROZEN = True  # type: ignore[attr-defined]
    except AttributeError:
        pass

    # skip basic types, weird things, or already frozen things
    if isinstance(instance, (bool, int, float, str, bytes)):
        pass

    elif isinstance(instance, (type(None), type(Ellipsis))):
        pass

    elif isinstance(instance, (FrozenList, FrozenDict, frozenset)):
        pass

    # handle containers
    elif isinstance(instance, list):
        for i in range(len(instance)):
            instance[i] = freeze(instance[i])
        instance = FrozenList(instance)

    elif isinstance(instance, tuple):
        instance = tuple(freeze(item) for item in instance)

    elif isinstance(instance, set):
        instance = frozenset({freeze(item) for item in instance})  # type: ignore[assignment]

    elif isinstance(instance, dict):
        for key, value in instance.items():
            instance[key] = freeze(value)
        instance = FrozenDict(instance)

    # handle custom classes
    else:
        # set everything in the __dict__ to frozen
        instance.__dict__ = freeze(instance.__dict__)  # type: ignore[assignment]

        # create a new class which inherits from the original class
        class FrozenClass(instance.__class__):  # type: ignore[name-defined]
            def __setattr__(self, name, value):
                raise AttributeError("class is frozen")

        FrozenClass.__name__ = f"FrozenClass__{instance.__class__.__name__}"
        FrozenClass.__module__ = instance.__class__.__module__
        FrozenClass.__doc__ = instance.__class__.__doc__

        # set the instance's class to the new class
        try:
            instance.__class__ = FrozenClass
        except TypeError as e:
            raise TypeError(
                f"Cannot freeze:\n{instance = }\n{instance.__class__ = }\n{FrozenClass = }"
            ) from e

    return instance
