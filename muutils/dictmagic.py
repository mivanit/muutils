from collections import defaultdict
from typing import Any, Callable, Generic, TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DefaulterDict(dict[_KT, _VT], Generic[_KT, _VT]):
    """like a defaultdict, but default_factory is passed the key as an argument"""

    def __init__(self, default_factory: Callable[[_KT], _VT], *args, **kwargs):
        if args:
            raise TypeError(
                f"DefaulterDict does not support positional arguments: *args = {args}"
            )
        super().__init__(**kwargs)
        self.default_factory: Callable[[_KT], _VT] = default_factory

    def __getitem__(self, k: _KT) -> _VT:
        if k in self:
            return dict.__getitem__(self, k)
        else:
            return self.default_factory(k)


def _recursive_defaultdict_ctor() -> defaultdict:
    return defaultdict(_recursive_defaultdict_ctor)


def defaultdict_to_dict_recursive(dd: defaultdict | DefaulterDict) -> dict:
    """Convert a defaultdict or DefaulterDict to a normal dict, recursively"""
    return {
        key: (
            defaultdict_to_dict_recursive(value)
            if isinstance(value, (defaultdict, DefaulterDict))
            else value
        )
        for key, value in dd.items()
    }


def dotlist_to_nested_dict(dot_dict: dict[str, Any], sep: str = ".") -> dict[str, Any]:
    """Convert a dict with dot-separated keys to a nested dict

    Example:
    >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})
    {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
    """
    nested_dict: defaultdict = _recursive_defaultdict_ctor()
    for key, value in dot_dict.items():
        if not isinstance(key, str):
            raise TypeError(f"key must be a string, got {type(key)}")
        keys: list[str] = key.split(sep)
        current: defaultdict = nested_dict
        # iterate over the keys except the last one
        for sub_key in keys[:-1]:
            current = current[sub_key]
        current[keys[-1]] = value
    return defaultdict_to_dict_recursive(nested_dict)
