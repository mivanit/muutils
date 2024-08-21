from __future__ import annotations

from typing import (
    Iterable,
    Any,
    Generator,
    Callable,
)


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


def list_split(lst: list, val) -> list[list]:
    """split a list into n sublists. similar to "a_b_c".split("_")"""

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
    """add a *new* instance of `val` between each element of `lst`

    ```
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
