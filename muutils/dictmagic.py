"""making working with dictionaries easier

- `DefaulterDict`: like a defaultdict, but default_factory is passed the key as an argument
- various methods for working wit dotlist-nested dicts, converting to and from them
- `condense_nested_dicts`: condense a nested dict, by condensing numeric or matching keys with matching values to ranges
- `condense_tensor_dict`: convert a dictionary of tensors to a dictionary of shapes
- `kwargs_to_nested_dict`: given kwargs from fire, convert them to a nested dict
"""

from __future__ import annotations

import typing
import warnings
from collections import defaultdict
from typing import (
    Any,
    Callable,
    Generic,
    Hashable,
    Iterable,
    Literal,
    Optional,
    TypeVar,
    Union,
)

from muutils.errormode import ErrorMode

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DefaulterDict(typing.Dict[_KT, _VT], Generic[_KT, _VT]):
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
            v: _VT = self.default_factory(k)
            dict.__setitem__(self, k, v)
            return v


def _recursive_defaultdict_ctor() -> defaultdict:
    return defaultdict(_recursive_defaultdict_ctor)


def defaultdict_to_dict_recursive(dd: Union[defaultdict, DefaulterDict]) -> dict:
    """Convert a defaultdict or DefaulterDict to a normal dict, recursively"""
    return {
        key: (
            defaultdict_to_dict_recursive(value)
            if isinstance(value, (defaultdict, DefaulterDict))
            else value
        )
        for key, value in dd.items()
    }


def dotlist_to_nested_dict(
    dot_dict: typing.Dict[str, Any], sep: str = "."
) -> typing.Dict[str, Any]:
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


def nested_dict_to_dotlist(
    nested_dict: typing.Dict[str, Any],
    sep: str = ".",
    allow_lists: bool = False,
) -> dict[str, Any]:
    def _recurse(current: Any, parent_key: str = "") -> typing.Dict[str, Any]:
        items: dict = dict()

        new_key: str
        if isinstance(current, dict):
            # dict case
            if not current and parent_key:
                items[parent_key] = current
            else:
                for k, v in current.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    items.update(_recurse(v, new_key))

        elif allow_lists and isinstance(current, list):
            # list case
            for i, item in enumerate(current):
                new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                items.update(_recurse(item, new_key))

        else:
            # anything else (write value)
            items[parent_key] = current

        return items

    return _recurse(nested_dict)


def update_with_nested_dict(
    original: dict[str, Any],
    update: dict[str, Any],
) -> dict[str, Any]:
    """Update a dict with a nested dict

    Example:
    >>> update_with_nested_dict({'a': {'b': 1}, "c": -1}, {'a': {"b": 2}})
    {'a': {'b': 2}, 'c': -1}

    # Arguments
    - `original: dict[str, Any]`
        the dict to update (will be modified in-place)
    - `update: dict[str, Any]`
        the dict to update with

    # Returns
    - `dict`
        the updated dict
    """
    for key, value in update.items():
        if key in original:
            if isinstance(original[key], dict) and isinstance(value, dict):
                update_with_nested_dict(original[key], value)
            else:
                original[key] = value
        else:
            original[key] = value

    return original


def kwargs_to_nested_dict(
    kwargs_dict: dict[str, Any],
    sep: str = ".",
    strip_prefix: Optional[str] = None,
    when_unknown_prefix: Union[ErrorMode, str] = ErrorMode.WARN,
    transform_key: Optional[Callable[[str], str]] = None,
) -> dict[str, Any]:
    """given kwargs from fire, convert them to a nested dict

    if strip_prefix is not None, then all keys must start with the prefix. by default,
    will warn if an unknown prefix is found, but can be set to raise an error or ignore it:
    `when_unknown_prefix: ErrorMode`

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

    # Arguments
    - `kwargs_dict: dict[str, Any]`
        the kwargs dict to convert
    - `sep: str = "."`
        the separator to use for nested keys
    - `strip_prefix: Optional[str] = None`
        if not None, then all keys must start with this prefix
    - `when_unknown_prefix: ErrorMode = ErrorMode.WARN`
        what to do when an unknown prefix is found
    - `transform_key: Callable[[str], str] | None = None`
        a function to apply to each key before adding it to the dict (applied after stripping the prefix)
    """
    when_unknown_prefix_ = ErrorMode.from_any(when_unknown_prefix)
    filtered_kwargs: dict[str, Any] = dict()
    for key, value in kwargs_dict.items():
        if strip_prefix is not None:
            if not key.startswith(strip_prefix):
                when_unknown_prefix_.process(
                    f"key '{key}' does not start with '{strip_prefix}'",
                    except_cls=ValueError,
                )
            else:
                key = key[len(strip_prefix) :]

        if transform_key is not None:
            key = transform_key(key)

        filtered_kwargs[key] = value

    return dotlist_to_nested_dict(filtered_kwargs, sep=sep)


def is_numeric_consecutive(lst: list[str]) -> bool:
    """Check if the list of keys is numeric and consecutive."""
    try:
        numbers: list[int] = [int(x) for x in lst]
        return sorted(numbers) == list(range(min(numbers), max(numbers) + 1))
    except ValueError:
        return False


def condense_nested_dicts_numeric_keys(
    data: dict[str, Any],
) -> dict[str, Any]:
    """condense a nested dict, by condensing numeric keys with matching values to ranges

    # Examples:
    ```python
    >>> condense_nested_dicts_numeric_keys({'1': 1, '2': 1, '3': 1, '4': 2, '5': 2, '6': 2})
    {'[1-3]': 1, '[4-6]': 2}
    >>> condense_nested_dicts_numeric_keys({'1': {'1': 'a', '2': 'a'}, '2': 'b'})
    {"1": {"[1-2]": "a"}, "2": "b"}
    ```
    """

    if not isinstance(data, dict):
        return data

    # Process each sub-dictionary
    for key, value in list(data.items()):
        data[key] = condense_nested_dicts_numeric_keys(value)

    # Find all numeric, consecutive keys
    if is_numeric_consecutive(list(data.keys())):
        keys: list[str] = sorted(data.keys(), key=lambda x: int(x))
    else:
        return data

    # output dict
    condensed_data: dict[str, Any] = {}

    # Identify ranges of identical values and condense
    i: int = 0
    while i < len(keys):
        j: int = i
        while j + 1 < len(keys) and data[keys[j]] == data[keys[j + 1]]:
            j += 1
        if j > i:  # Found consecutive keys with identical values
            condensed_key: str = f"[{keys[i]}-{keys[j]}]"
            condensed_data[condensed_key] = data[keys[i]]
            i = j + 1
        else:
            condensed_data[keys[i]] = data[keys[i]]
            i += 1

    return condensed_data


def condense_nested_dicts_matching_values(
    data: dict[str, Any],
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None,
) -> dict[str, Any]:
    """condense a nested dict, by condensing keys with matching values

    # Examples: TODO

    # Parameters:
     - `data : dict[str, Any]`
        data to process
     - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
        a function to apply to each value before adding it to the dict (if it's not hashable)
        (defaults to `None`)

    """

    if isinstance(data, dict):
        data = {
            key: condense_nested_dicts_matching_values(
                value, val_condense_fallback_mapping
            )
            for key, value in data.items()
        }
    else:
        return data

    # Find all identical values and condense by stitching together keys
    values_grouped: defaultdict[Any, list[str]] = defaultdict(list)
    data_persist: dict[str, Any] = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            try:
                values_grouped[value].append(key)
            except TypeError:
                # If the value is unhashable, use a fallback mapping to find a hashable representation
                if val_condense_fallback_mapping is not None:
                    values_grouped[val_condense_fallback_mapping(value)].append(key)
                else:
                    data_persist[key] = value
        else:
            data_persist[key] = value

    condensed_data = data_persist
    for value, keys in values_grouped.items():
        if len(keys) > 1:
            merged_key = f"[{', '.join(keys)}]"  # Choose an appropriate method to represent merged keys
            condensed_data[merged_key] = value
        else:
            condensed_data[keys[0]] = value

    return condensed_data


def condense_nested_dicts(
    data: dict[str, Any],
    condense_numeric_keys: bool = True,
    condense_matching_values: bool = True,
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None,
) -> dict[str, Any]:
    """condense a nested dict, by condensing numeric or matching keys with matching values to ranges

    combines the functionality of `condense_nested_dicts_numeric_keys()` and `condense_nested_dicts_matching_values()`

    # NOTE: this process is not meant to be reversible, and is intended for pretty-printing and visualization purposes
    it's not reversible because types are lost to make the printing pretty

    # Parameters:
     - `data : dict[str, Any]`
        data to process
     - `condense_numeric_keys : bool`
        whether to condense numeric keys (e.g. "1", "2", "3") to ranges (e.g. "[1-3]")
       (defaults to `True`)
     - `condense_matching_values : bool`
        whether to condense keys with matching values
       (defaults to `True`)
     - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
        a function to apply to each value before adding it to the dict (if it's not hashable)
       (defaults to `None`)

    """

    condensed_data: dict = data
    if condense_numeric_keys:
        condensed_data = condense_nested_dicts_numeric_keys(condensed_data)
    if condense_matching_values:
        condensed_data = condense_nested_dicts_matching_values(
            condensed_data, val_condense_fallback_mapping
        )
    return condensed_data


def tuple_dims_replace(
    t: tuple[int, ...], dims_names_map: Optional[dict[int, str]] = None
) -> tuple[Union[int, str], ...]:
    if dims_names_map is None:
        return t
    else:
        return tuple(dims_names_map.get(x, x) for x in t)


TensorDict = typing.Dict[str, "torch.Tensor|np.ndarray"]  # type: ignore[name-defined] # noqa: F821
TensorIterable = Iterable[typing.Tuple[str, "torch.Tensor|np.ndarray"]]  # type: ignore[name-defined] # noqa: F821
TensorDictFormats = Literal["dict", "json", "yaml", "yml"]


def _default_shapes_convert(x: tuple) -> str:
    return str(x).replace('"', "").replace("'", "")


def condense_tensor_dict(
    data: TensorDict | TensorIterable,
    fmt: TensorDictFormats = "dict",
    *args,
    shapes_convert: Callable[[tuple], Any] = _default_shapes_convert,
    drop_batch_dims: int = 0,
    sep: str = ".",
    dims_names_map: Optional[dict[int, str]] = None,
    condense_numeric_keys: bool = True,
    condense_matching_values: bool = True,
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None,
    return_format: Optional[TensorDictFormats] = None,
) -> Union[str, dict[str, str | tuple[int, ...]]]:
    """Convert a dictionary of tensors to a dictionary of shapes.

    by default, values are converted to strings of their shapes (for nice printing).
    If you want the actual shapes, set `shapes_convert = lambda x: x` or `shapes_convert = None`.

    # Parameters:
     - `data : dict[str, "torch.Tensor|np.ndarray"] | Iterable[tuple[str, "torch.Tensor|np.ndarray"]]`
        a either a `TensorDict` dict from strings to tensors, or an `TensorIterable` iterable of (key, tensor) pairs (like you might get from a `dict().items())` )
     - `fmt : TensorDictFormats`
        format to return the result in -- either a dict, or dump to json/yaml directly for pretty printing. will crash if yaml is not installed.
        (defaults to `'dict'`)
     - `shapes_convert : Callable[[tuple], Any]`
        conversion of a shape tuple to a string or other format (defaults to turning it into a string and removing quotes)
        (defaults to `lambdax:str(x).replace('"', '').replace("'", '')`)
     - `drop_batch_dims : int`
        number of leading dimensions to drop from the shape
        (defaults to `0`)
     - `sep : str`
        separator to use for nested keys
        (defaults to `'.'`)
     - `dims_names_map : dict[int, str] | None`
        convert certain dimension values in shape. not perfect, can be buggy
        (defaults to `None`)
     - `condense_numeric_keys : bool`
        whether to condense numeric keys (e.g. "1", "2", "3") to ranges (e.g. "[1-3]"), passed on to `condense_nested_dicts`
        (defaults to `True`)
     - `condense_matching_values : bool`
        whether to condense keys with matching values, passed on to `condense_nested_dicts`
        (defaults to `True`)
     - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
        a function to apply to each value before adding it to the dict (if it's not hashable), passed on to `condense_nested_dicts`
        (defaults to `None`)
     - `return_format : TensorDictFormats | None`
        legacy alias for `fmt` kwarg

    # Returns:
     - `str|dict[str, str|tuple[int, ...]]`
        dict if `return_format='dict'`, a string for `json` or `yaml` output

    # Examples:
    ```python
    >>> model = transformer_lens.HookedTransformer.from_pretrained("gpt2")
    >>> print(condense_tensor_dict(model.named_parameters(), return_format='yaml'))
    ```
    ```yaml
    embed:
      W_E: (50257, 768)
    pos_embed:
      W_pos: (1024, 768)
    blocks:
      '[0-11]':
        attn:
          '[W_Q, W_K, W_V]': (12, 768, 64)
          W_O: (12, 64, 768)
          '[b_Q, b_K, b_V]': (12, 64)
          b_O: (768,)
        mlp:
          W_in: (768, 3072)
          b_in: (3072,)
          W_out: (3072, 768)
          b_out: (768,)
    unembed:
      W_U: (768, 50257)
      b_U: (50257,)
    ```

    # Raises:
     - `ValueError` :  if `return_format` is not one of 'dict', 'json', or 'yaml', or if you try to use 'yaml' output without having PyYAML installed
    """

    # handle arg processing:
    # ----------------------------------------------------------------------
    # make all args except data and format keyword-only
    assert len(args) == 0, f"unexpected positional args: {args}"
    # handle legacy return_format
    if return_format is not None:
        warnings.warn(
            "return_format is deprecated, use fmt instead",
            DeprecationWarning,
        )
        fmt = return_format

    # identity function for shapes_convert if not provided
    if shapes_convert is None:
        shapes_convert = lambda x: x  # noqa: E731

    # convert to iterable
    data_items: "Iterable[tuple[str, Union[torch.Tensor,np.ndarray]]]" = (  # type: ignore # noqa: F821
        data.items() if hasattr(data, "items") and callable(data.items) else data  # type: ignore
    )

    # get shapes
    data_shapes: dict[str, Union[str, tuple[int, ...]]] = {
        k: shapes_convert(
            tuple_dims_replace(
                tuple(v.shape)[drop_batch_dims:],
                dims_names_map,
            )
        )
        for k, v in data_items
    }

    # nest the dict
    data_nested: dict[str, Any] = dotlist_to_nested_dict(data_shapes, sep=sep)

    # condense the nested dict
    data_condensed: dict[str, Union[str, tuple[int, ...]]] = condense_nested_dicts(
        data=data_nested,
        condense_numeric_keys=condense_numeric_keys,
        condense_matching_values=condense_matching_values,
        val_condense_fallback_mapping=val_condense_fallback_mapping,
    )

    # return in the specified format
    fmt_lower: str = fmt.lower()
    if fmt_lower == "dict":
        return data_condensed
    elif fmt_lower == "json":
        import json

        return json.dumps(data_condensed, indent=2)
    elif fmt_lower in ["yaml", "yml"]:
        try:
            import yaml  # type: ignore[import-untyped]

            return yaml.dump(data_condensed, sort_keys=False)
        except ImportError as e:
            raise ValueError("PyYAML is required for YAML output") from e
    else:
        raise ValueError(f"Invalid return format: {fmt}")
