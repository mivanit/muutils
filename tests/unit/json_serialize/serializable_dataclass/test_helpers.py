from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch

from muutils.json_serialize.serializable_dataclass import array_safe_eq, dc_eq


def test_array_safe_eq():
    assert array_safe_eq(np.array([1, 2, 3]), np.array([1, 2, 3]))
    assert not array_safe_eq(np.array([1, 2, 3]), np.array([4, 5, 6]))
    assert array_safe_eq(torch.tensor([1, 2, 3]), torch.tensor([1, 2, 3]))
    assert not array_safe_eq(torch.tensor([1, 2, 3]), torch.tensor([4, 5, 6]))


def test_dc_eq_case1():
    @dataclass(eq=False)
    class TestClass:
        a: int
        b: np.ndarray
        c: torch.Tensor
        e: list[int]
        f: dict[str, int]

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

    assert dc_eq(instance1, instance2)


def test_dc_eq_case2():
    @dataclass(eq=False)
    class TestClass:
        a: int
        b: np.ndarray
        c: torch.Tensor
        e: list[int]
        f: dict[str, int]

    instance1 = TestClass(
        a=1,
        b=np.array([1, 2, 3]),
        c=torch.tensor([1, 2, 3]),
        e=[1, 2, 3],
        f={"key1": 1, "key2": 2},
    )

    instance2 = TestClass(
        a=1,
        b=np.array([4, 5, 6]),
        c=torch.tensor([1, 2, 3]),
        e=[1, 2, 3],
        f={"key1": 1, "key2": 2},
    )

    assert not dc_eq(instance1, instance2)


def test_dc_eq_case3():
    @dataclass(eq=False)
    class TestClass:
        a: int
        b: np.ndarray
        c: torch.Tensor
        e: list[int]
        f: dict[str, int]

    instance1 = TestClass(
        a=1,
        b=np.array([1, 2, 3]),
        c=torch.tensor([1, 2, 3]),
        e=[1, 2, 3],
        f={"key1": 1, "key2": 2},
    )

    instance2 = TestClass(
        a=2,
        b=np.array([1, 2, 3]),
        c=torch.tensor([1, 2, 3]),
        e=[1, 2, 3],
        f={"key1": 1, "key2": 2},
    )

    assert not dc_eq(instance1, instance2)
