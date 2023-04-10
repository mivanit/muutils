import typing
import warnings
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


def kwargs_to_nested_dict(
    kwargs_dict: dict[str, Any],
    sep: str = ".",
    strip_prefix: str | None = None,
    when_unknown_prefix: typing.Literal["raise", "warn", "ignore"] = "warn",
) -> dict[str, Any]:
    """given kwargs from fire, convert them to a nested dict

    if strip_prefix is not None, then all keys must start with the prefix. by default,
    will warn if an unknown prefix is found, but can be set to raise an error or ignore it:
    `when_unknown_prefix: typing.Literal["raise", "warn", "ignore"]`

    Example:
    ```python
    def main(**kwargs):
        print(kwargs_to_nested_dict(kwargs))
    fire.Fire(main)
    ```
    running the above script will give:
    ```bash
    $ python test.py --a.b.c=1 --a.b.d=2 --a.e=3
    {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
    ```
    """
    filtered_kwargs: dict[str, Any] = dict()
    for key, value in kwargs_dict.items():
        if strip_prefix is not None:
            if not key.startswith(strip_prefix):
                if when_unknown_prefix == "raise":
                    raise ValueError(f"key {key} does not start with {strip_prefix}")
                elif when_unknown_prefix == "warn":
                    warnings.warn(f"key {key} does not start with {strip_prefix}")
                elif when_unknown_prefix == "ignore":
                    pass
                else:
                    raise ValueError(
                        f"when_unknown_prefix must be one of 'raise', 'warn', or 'ignore', got {when_unknown_prefix}"
                    )
            key = key.removeprefix(strip_prefix)
        filtered_kwargs[key] = value

    return dotlist_to_nested_dict(filtered_kwargs, sep=sep)
