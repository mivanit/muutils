from itertools import chain
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")


def group_by_equivalence(
    items_in: Sequence[T],
    eq_func: Callable[[T, T], bool],
) -> list[list[T]]:
    """group items by assuming that `eq_func` implies an equivalence relation but might not be transitive

    so, if f(a,b) and f(b,c) then f(a,c) might be false, but we still want to put [a,b,c] in the same class
    """

    items: list[T] = list(items_in)
    output: list[list[T]] = list()

    while items:
        x: T = items.pop()

        # try to add to an existing class
        found_classes: list[int] = list()
        for i, c in enumerate(output):
            if any(eq_func(x, y) for y in c):
                found_classes.append(i)

        # if one class found, add to it
        if len(found_classes) == 1:
            output[found_classes.pop()].append(x)

        elif len(found_classes) > 1:
            # if multiple classes found, merge the classes

            # first sort the ones to be merged
            output_new: list[list[T]] = list()
            to_merge: list[list[T]] = list()
            for i, c in enumerate(output):
                if i in found_classes:
                    to_merge.append(c)
                else:
                    output_new.append(c)

            # then merge them back in, along with the element `x`
            merged: list[T] = list(chain.from_iterable(to_merge))
            merged.append(x)

            output_new.append(merged)

        # if no class found, make a new one
        else:
            output.append([x])

    return output
