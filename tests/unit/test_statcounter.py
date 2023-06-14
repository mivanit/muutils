import numpy as np

from muutils.statcounter import _compare_np_custom

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
