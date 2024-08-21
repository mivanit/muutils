from __future__ import annotations

from typing import (
    Iterable,
    Any,
    Generator,
    Callable,
    Union,
)

import typing
from typing import (
    Literal,
    Mapping,
)


WhenMissing = Literal["except", "skip", "include"]


def empty_sequence_if_attr_false(
    itr: Iterable[Any],
    attr_owner: Any,
    attr_name: str,
) -> Iterable[Any]:
    """Returns `itr` if `attr_owner` has the attribute `attr_name` and it boolean casts to `True`. Returns an empty sequence otherwise.

    Particularly useful for optionally inserting delimiters into a sequence depending on an `TokenizerElement` attribute.

    # Parameters:
    - `itr: Iterable[Any]`
        The iterable to return if the attribute is `True`.
    - `attr_owner: Any`
        The object to check for the attribute.
    - `attr_name: str`
        The name of the attribute to check.

    # Returns:
    - `itr: Iterable` if `attr_owner` has the attribute `attr_name` and it boolean casts to `True`, otherwise an empty sequence.
    - `()` an empty sequence if the attribute is `False` or not present.
    """
    return itr if bool(getattr(attr_owner, attr_name, False)) else ()


def flatten(it: Iterable[Any], levels_to_flatten: int | None = None) -> Generator:
    """
    Flattens an arbitrarily nested iterable.
    Flattens all iterable data types except for `str` and `bytes`.

    # Returns
    Generator over the flattened sequence.

    # Parameters
    - `it`: Any arbitrarily nested iterable.
    - `levels_to_flatten`: Number of levels to flatten by, starting at the outermost layer. If `None`, performs full flattening.
    """
    for x in it:
        # TODO: swap type check with more general check for __iter__() or __next__() or whatever
        if (
            hasattr(x, "__iter__")
            and not isinstance(x, (str, bytes))
            and (levels_to_flatten is None or levels_to_flatten > 0)
        ):
            yield from flatten(
                x, None if levels_to_flatten is None else levels_to_flatten - 1
            )
        else:
            yield x


# string-like operations on lists
# --------------------------------------------------------------------------------


def list_split(lst: list, val: Any) -> list[list]:
    """split a list into sublists by `val`. similar to "a_b_c".split("_")

    ```python
    >>> list_split([1,2,3,0,4,5,0,6], 0)
    [[1, 2, 3], [4, 5], [6]]
    >>> list_split([0,1,2,3], 0)
    [[], [1, 2, 3]]
    >>> list_split([1,2,3], 0)
    [[1, 2, 3]]
    >>> list_split([], 0)
    [[]]
    ```

    """

    if len(lst) == 0:
        return [[]]

    output: list[list] = [
        [],
    ]

    for x in lst:
        if x == val:
            output.append([])
        else:
            output[-1].append(x)
    return output


def list_join(lst: list, factory: Callable) -> list:
    """add a *new* instance of `factory()` between each element of `lst`

    ```python
    >>> list_join([1,2,3], lambda : 0)
    [1,0,2,0,3]
    >>> list_join([1,2,3], lambda: [time.sleep(0.1), time.time()][1])
    [1, 1600000000.0, 2, 1600000000.1, 3]
    ```
    """

    if len(lst) == 0:
        return []

    output: list = [
        lst[0],
    ]

    for x in lst[1:]:
        output.append(factory())
        output.append(x)

    return output


# applying mappings
# --------------------------------------------------------------------------------

_AM_K = typing.TypeVar("_AM_K")
_AM_V = typing.TypeVar("_AM_V")


def apply_mapping(
    mapping: Mapping[_AM_K, _AM_V],
    iter: Iterable[_AM_K],
    when_missing: WhenMissing = "skip",
) -> list[Union[_AM_K, _AM_V]]:
    """Given an iterable and a mapping, apply the mapping to the iterable with certain options

    Gotcha: if `when_missing` is invalid, this is totally fine until a missing key is actually encountered.

    Note: you can use this with `muutils.kappa.Kappa` if you want to pass a function instead of a dict

    # Parameters:
     - `mapping : Mapping[_AM_K, _AM_V]`
        must have `__contains__` and `__getitem__`, both of which take `_AM_K` and the latter returns `_AM_V`
     - `iter : Iterable[_AM_K]`
        the iterable to apply the mapping to
     - `when_missing : WhenMissing`
        what to do when a key is missing from the mapping -- this is what distinguishes this function from `map`
        you can choose from `"skip"`, `"include"` (without converting), and `"except"`
       (defaults to `"skip"`)

    # Returns:
    return type is one of:
     - `list[_AM_V]` if `when_missing` is `"skip"` or `"except"`
     - `list[Union[_AM_K, _AM_V]]` if `when_missing` is `"include"`

    # Raises:
     - `KeyError` : if the item is missing from the mapping and `when_missing` is `"except"`
     - `ValueError` : if `when_missing` is invalid
    """
    output: list[Union[_AM_K, _AM_V]] = list()
    item: _AM_K
    for item in iter:
        if item in mapping:
            output.append(mapping[item])
            continue
        if when_missing == "skip":
            continue
        elif when_missing == "include":
            output.append(item)
        elif when_missing == "except":
            raise KeyError(f"item {item} is missing from mapping {mapping}")
        else:
            raise ValueError(
                f"invalid value for {when_missing = }\n{item = }\n{mapping = }"
            )
    return output


def apply_mapping_chain(
    mapping: Mapping[_AM_K, Iterable[_AM_V]],
    iter: Iterable[_AM_K],
    when_missing: WhenMissing = "skip",
) -> list[Union[_AM_K, _AM_V]]:
    """Given an iterable and a mapping, chain the mappings together

    Gotcha: if `when_missing` is invalid, this is totally fine until a missing key is actually encountered.

    Note: you can use this with `muutils.kappa.Kappa` if you want to pass a function instead of a dict

    # Parameters:
    - `mapping : Mapping[_AM_K, Iterable[_AM_V]]`
        must have `__contains__` and `__getitem__`, both of which take `_AM_K` and the latter returns `Iterable[_AM_V]`
    - `iter : Iterable[_AM_K]`
        the iterable to apply the mapping to
    - `when_missing : WhenMissing`
        what to do when a key is missing from the mapping -- this is what distinguishes this function from `map`
        you can choose from `"skip"`, `"include"` (without converting), and `"except"`
    (defaults to `"skip"`)

    # Returns:
    return type is one of:
     - `list[_AM_V]` if `when_missing` is `"skip"` or `"except"`
     - `list[Union[_AM_K, _AM_V]]` if `when_missing` is `"include"`

    # Raises:
    - `KeyError` : if the item is missing from the mapping and `when_missing` is `"except"`
    - `ValueError` : if `when_missing` is invalid

    """
    output: list[Union[_AM_K, _AM_V]] = list()
    item: _AM_K
    for item in iter:
        if item in mapping:
            output.extend(mapping[item])
            continue
        if when_missing == "skip":
            continue
        elif when_missing == "include":
            output.append(item)
        elif when_missing == "except":
            raise KeyError(f"item {item} is missing from mapping {mapping}")
        else:
            raise ValueError(
                f"invalid value for {when_missing = }\n{item = }\n{mapping = }"
            )
    return output
