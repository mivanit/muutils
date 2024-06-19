from __future__ import annotations

import numpy as np

from muutils.statcounter import StatCounter


def _compute_err(a: float, b: float, /) -> dict[str, float]:
    return dict(
        num_a=float(a),
        num_b=float(b),
        diff=float(b - a),
        # frac_err=float((b - a) / a), # this causes division by zero, whatever
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


EPSILON: float = 1e-8


def test_statcounter() -> None:
    arrs: list[np.ndarray] = [
        np.array([0, 1]),
        np.array([1, 2]),
        np.random.randint(0, 10, size=10),
        np.random.randint(-5, 15, size=10),
        np.array([-5, -4, -1, 1, 1, 3, 3, 5, 11, 12]),
        np.random.randint(-5, 15, size=100),
        np.random.randint(0, 100, size=100),
        np.random.randint(0, 1000, size=100),
    ]

    # for i, j in np.random.randint(1, 100, size=(50, 2)):
    #     if i > j:
    #         i, j = j, i

    #     arrs.append(np.random.randint(i, j, size=1000))

    for a in arrs:
        r = _compare_np_custom(a)

        assert all(
            [x["diff"] < EPSILON for x in r.values()]
        ), f"errs for rantint array: {a.shape = } {np.min(a) = } {np.max(a) = } data = {r}"
        # s = StatCounter(a)
        # print(s.total(), s)
        # print(sorted(list(s.elements())))
