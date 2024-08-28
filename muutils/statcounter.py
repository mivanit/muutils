"""`StatCounter` class for counting and calculating statistics on numbers

cleaner and more efficient than just using a `Counter` or array"""

from __future__ import annotations

import json
import math
from collections import Counter
from functools import cached_property
from itertools import chain
from typing import Callable, Optional, Sequence, Union


# _GeneralArray = Union[np.ndarray, "torch.Tensor"]
NumericSequence = Sequence[Union[float, int, "NumericSequence"]]

# pylint: disable=abstract-method

# misc
# ==================================================


def universal_flatten(
    arr: Union[NumericSequence, float, int], require_rectangular: bool = True
) -> NumericSequence:
    """flattens any iterable"""

    # mypy complains that the sequence has no attribute "flatten"
    if hasattr(arr, "flatten") and callable(arr.flatten):  # type: ignore
        return arr.flatten()  # type: ignore
    elif isinstance(arr, Sequence):
        elements_iterable: list[bool] = [isinstance(x, Sequence) for x in arr]
        if require_rectangular and (all(elements_iterable) != any(elements_iterable)):
            raise ValueError("arr contains mixed iterable and non-iterable elements")
        if any(elements_iterable):
            return list(chain.from_iterable(universal_flatten(x) for x in arr))  # type: ignore[misc]
        else:
            return arr
    else:
        return [arr]


# StatCounter
# ==================================================


class StatCounter(Counter):
    """`Counter`, but with some stat calculation methods which assume the keys are numerical

    works best when the keys are `int`s
    """

    def validate(self) -> bool:
        """validate the counter as being all floats or ints"""
        return all(isinstance(k, (bool, int, float, type(None))) for k in self.keys())

    def min(self):
        "minimum value"
        return min(x for x, v in self.items() if v > 0)

    def max(self):
        "maximum value"
        return max(x for x, v in self.items() if v > 0)

    def total(self):
        """Sum of the counts"""
        return sum(self.values())

    @cached_property
    def keys_sorted(self) -> list:
        """return the keys"""
        return sorted(list(self.keys()))

    def percentile(self, p: float):
        """return the value at the given percentile

        this could be log time if we did binary search, but that would be a lot of added complexity
        """

        if p < 0 or p > 1:
            raise ValueError(f"percentile must be between 0 and 1: {p}")
        # flip for speed
        sorted_keys: list[float] = [float(x) for x in self.keys_sorted]
        sort: int = 1
        if p > 0.51:
            sort = -1
            p = 1 - p

        sorted_keys = sorted_keys[::sort]
        real_target: float = p * (self.total() - 1)

        n_target_f: int = math.floor(real_target)
        n_target_c: int = math.ceil(real_target)

        n_sofar: float = -1

        # print(f'{p = } {real_target = } {n_target_f = } {n_target_c = }')

        for i, k in enumerate(sorted_keys):
            n_sofar += self[k]

            # print(f'{k = } {n_sofar = }')

            if n_sofar > n_target_f:
                return k

            elif n_sofar == n_target_f:
                if n_sofar == n_target_c:
                    return k
                else:
                    # print(
                    #     sorted_keys[i], (n_sofar + 1 - real_target),
                    #     sorted_keys[i + 1], (real_target - n_sofar),
                    # )
                    return sorted_keys[i] * (n_sofar + 1 - real_target) + sorted_keys[
                        i + 1
                    ] * (real_target - n_sofar)
            else:
                continue

        raise ValueError(f"percentile {p} not found???")

    def median(self) -> float:
        return self.percentile(0.5)

    def mean(self) -> float:
        """return the mean of the values"""
        return float(sum(k * c for k, c in self.items()) / self.total())

    def mode(self) -> float:
        return self.most_common()[0][0]

    def std(self) -> float:
        """return the standard deviation of the values"""
        mean: float = self.mean()
        deviations: float = sum(c * (k - mean) ** 2 for k, c in self.items())

        return (deviations / self.total()) ** 0.5

    def summary(
        self,
        typecast: Callable = lambda x: x,
        *,
        extra_percentiles: Optional[list[float]] = None,
    ) -> dict[str, Union[float, int]]:
        """return a summary of the stats, without the raw data. human readable and small"""
        # common stats that always work
        output: dict = dict(
            total_items=self.total(),
            n_keys=len(self.keys()),
            mode=self.mode(),
        )

        if self.total() > 0:
            if self.validate():
                # if its a numeric counter, we can do some stats
                output = {
                    **output,
                    **dict(
                        mean=float(self.mean()),
                        std=float(self.std()),
                        min=typecast(self.min()),
                        q1=typecast(self.percentile(0.25)),
                        median=typecast(self.median()),
                        q3=typecast(self.percentile(0.75)),
                        max=typecast(self.max()),
                    ),
                }

                if extra_percentiles is not None:
                    for p in extra_percentiles:
                        output[f"percentile_{p}"] = typecast(self.percentile(p))
            else:
                # if its not, we can only do the simpler things
                # mean mode and total are done in the initial declaration of `output`
                pass

        return output

    def serialize(
        self,
        typecast: Callable = lambda x: x,
        *,
        extra_percentiles: Optional[list[float]] = None,
    ) -> dict:
        """return a json-serializable version of the counter

        includes both the output of `summary` and the raw data:

        ```json
        {
            "StatCounter": { <keys, values from raw data> },
            "summary": self.summary(typecast, extra_percentiles=extra_percentiles),
        }

        """

        return {
            "StatCounter": {
                typecast(k): v
                for k, v in sorted(dict(self).items(), key=lambda x: x[0])
            },
            "summary": self.summary(typecast, extra_percentiles=extra_percentiles),
        }

    def __str__(self) -> str:
        "summary as json with 2 space indent, good for printing"
        return json.dumps(self.summary(), indent=2)

    def __repr__(self) -> str:
        return json.dumps(self.serialize(), indent=2)

    @classmethod
    def load(cls, data: dict) -> "StatCounter":
        "load from a the output of `StatCounter.serialize`"
        if "StatCounter" in data:
            loadme = data["StatCounter"]
        else:
            loadme = data

        return cls({float(k): v for k, v in loadme.items()})

    @classmethod
    def from_list_arrays(
        cls,
        arr,
        map_func: Callable = float,
    ) -> "StatCounter":
        """calls `map_func` on each element of `universal_flatten(arr)`"""
        return cls([map_func(x) for x in universal_flatten(arr)])
