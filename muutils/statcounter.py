import json
import math
from collections import Counter
from functools import cached_property
from itertools import chain
from types import NoneType
from typing import Callable, Iterable, Optional, Sequence, Union

import numpy as np

# import pdb


# TODO: mypy complains that "torch" is not defined
# _GeneralArray = Union[np.ndarray, "torch.Tensor"]
_GeneralArray = np.ndarray

GeneralSequence = Union[Sequence, _GeneralArray]

# pylint: disable=abstract-method

# misc
# ==================================================


def universal_flatten(
    arr: GeneralSequence, require_rectangular: bool = True
) -> GeneralSequence:
    """flattens any iterable"""

    # mypy complains that the sequence has no attribute "flatten"
    if hasattr(arr, "flatten") and callable(arr.flatten):  # type: ignore
        return arr.flatten()  # type: ignore
    elif not isinstance(arr, Iterable):
        return arr
    else:
        elements_iterable: list[bool] = [isinstance(x, Iterable) for x in arr]
        if require_rectangular and (all(elements_iterable) != any(elements_iterable)):
            raise ValueError("arr contains mixed iterable and non-iterable elements")
        if any(elements_iterable):
            return list(chain.from_iterable(universal_flatten(x) for x in arr))
        else:
            return arr


def compute_rsquared(actual: np.ndarray, predicted: np.ndarray) -> float:
    assert actual.shape == predicted.shape

    actual_mean: float = np.mean(actual)

    ss_res: float = np.sum((actual - predicted) ** 2.0)
    ss_tot: float = np.sum((actual - actual_mean) ** 2.0)

    return 1 - ss_res / ss_tot


# StatCounter
# ==================================================


class StatCounter(Counter):
    """counter, but with some stat calculation methods which assume the keys are numbers

    works best when the keys are ints
    """

    def validate(self) -> bool:
        """validate the counter as being all floats or ints"""
        return all(isinstance(k, (bool, int, float, NoneType)) for k in self.keys())

    def min(self):
        return min(x for x, v in self.items() if v > 0)

    def max(self):
        return max(x for x, v in self.items() if v > 0)

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
        return {
            "StatCounter": {
                typecast(k): v
                for k, v in sorted(dict(self).items(), key=lambda x: x[0])
            },
            "summary": self.summary(typecast, extra_percentiles=extra_percentiles),
        }

    def __str__(self) -> str:
        return json.dumps(self.summary(), indent=2)

    def __repr__(self) -> str:
        return json.dumps(self.serialize(), indent=2)

    @classmethod
    def load(cls, data: dict) -> "StatCounter":
        if "StatCounter" in data:
            loadme = data["StatCounter"]
        else:
            loadme = data

        return cls({float(k): v for k, v in loadme.items()})

    @classmethod
    def from_list_arrays(
        cls,
        arr: _GeneralArray,
        map_func: Callable = float,
    ) -> "StatCounter":
        """calls `map_func` on each element of `universal_flatten(arr)`"""
        return cls([map_func(x) for x in universal_flatten(arr)])


# testing
# ==================================================


def _compute_err(a: float, b: float, /) -> dict[str, float]:
    return dict(
        num_a=float(a),
        num_b=float(b),
        diff=float(b - a),
        frac_err=float((b - a) / a),
    )


def _compare_np_custom(arr: np.ndarray) -> dict[str, dict]:
    counter: StatCounter = StatCounter(arr)
    return dict(
        mean=_compute_err(counter.mean(), np.mean(arr)),
        std=_compute_err(counter.std(), np.std(arr)),
        min=_compute_err(counter.min(), np.min(arr)),
        q1=_compute_err(counter.percentile(0.25), np.percentile(arr, 25)),
        median=_compute_err(counter.median(), np.median(arr)),
        q3=_compute_err(counter.percentile(0.75), np.percentile(arr, 75)),
        max=_compute_err(counter.max(), np.max(arr)),
    )


def _test_statscounter():
    arrs: list[np.ndarray] = [
        np.array([0, 1]),
        np.array([1, 2]),
        np.random.randint(0, 10, size=100),
        np.random.randint(-5, 15, size=10),
        np.array([-5, -4, -1, 1, 1, 3, 3, 5, 11, 12]),
        np.random.randint(-5, 15, size=10000),
        np.random.randint(0, 100, size=100),
        np.random.randint(0, 1000, size=10000),
    ]

    for i, j in np.random.randint(1, 100, size=(50, 2)):
        if i > j:
            i, j = j, i

        arrs.append(np.random.randint(i, j, size=1000))

    import json

    for a in arrs:
        r = _compare_np_custom(a)

        if any(x["diff"] > 0.00000000001 for x in r.values()):
            print("!!!!!!!!!!!!!!!!!!!!")
            print(f"errs for rantint array: {a.shape = } {np.min(a) =} {np.max(a) =}")
            print(json.dumps(r, indent=2))
        # s = StatCounter(a)
        # print(s.total(), s)
        # print(sorted(list(s.elements())))


# if __name__ == '__main__':
#     _test_statscounter()
