import dataclasses

import numpy as np
import pytest
import torch

from muutils.json_serialize.serializable_dataclass import (
    array_safe_eq,
    dc_eq,
    serializable_field,
)


@dataclasses.dataclass(eq=False)
class TestClass:
    a: int
    b: np.ndarray = serializable_field()
    c: torch.Tensor = serializable_field()
    e: list[int] = serializable_field()
    f: dict[str, int] = serializable_field()


instance1 = TestClass(
    a=1,
    b=np.array([1, 2, 3]),
    c=torch.tensor([1, 2, 3]),
    e=[1, 2, 3],
    f={"key1": 1, "key2": 2},
)

instance2 = TestClass(
    a=1,
    b=np.array([1, 2, 3]),
    c=torch.tensor([1, 2, 3]),
    e=[1, 2, 3],
    f={"key1": 1, "key2": 2},
)


def test_array_safe_eq():
    assert array_safe_eq(np.array([1, 2, 3]), np.array([1, 2, 3]))
    assert not array_safe_eq(np.array([1, 2, 3]), np.array([4, 5, 6]))
    assert array_safe_eq(torch.tensor([1, 2, 3]), torch.tensor([1, 2, 3]))
    assert not array_safe_eq(torch.tensor([1, 2, 3]), torch.tensor([4, 5, 6]))


@pytest.mark.parametrize(
    "instance1, instance2, expected",
    [
        (instance1, instance2, True),
        (
            instance1,
            TestClass(
                a=1,
                b=np.array([4, 5, 6]),
                c=torch.tensor([1, 2, 3]),
                e=[1, 2, 3],
                f={"key1": 1, "key2": 2},
            ),
            False,
        ),
        (
            instance1,
            TestClass(
                a=2,
                b=np.array([1, 2, 3]),
                c=torch.tensor([1, 2, 3]),
                e=[1, 2, 3],
                f={"key1": 1, "key2": 2},
            ),
            False,
        ),
    ],
)
def test_dc_eq(instance1, instance2, expected):
    assert dc_eq(instance1, instance2) == expected
