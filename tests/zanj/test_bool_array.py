from pathlib import Path

import numpy as np
import torch

from muutils.json_serialize import SerializableDataclass, serializable_dataclass
from muutils.zanj import ZANJ

TEST_DATA_PATH: Path = Path("tests/junk_data")


@serializable_dataclass
class MyClass_list(SerializableDataclass):
    name: str
    arr_1: list
    arr_2: list


@serializable_dataclass
class MyClass_np(SerializableDataclass):
    name: str
    arr_1: np.ndarray
    arr_2: np.ndarray


@serializable_dataclass
class MyClass_torch(SerializableDataclass):
    name: str
    arr_1: torch.Tensor
    arr_2: torch.Tensor


def test_list_bool_array():
    fname: Path = TEST_DATA_PATH / "test_list_bool_array.zanj"
    c: MyClass_list = MyClass_list(
        name="test",
        arr_1=[True, False, True],
        arr_2=[True, False, True],
    )

    z = ZANJ()

    z.save(c, fname)

    c2: MyClass_list = z.read(fname)

    assert c == c2


def test_np_bool_array():
    fname: Path = TEST_DATA_PATH / "test_np_bool_array.zanj"
    c: MyClass_np = MyClass_np(
        name="test",
        arr_1=np.array([True, False, True]),
        arr_2=np.array([True, False, True]),
    )

    z = ZANJ()

    z.save(c, fname)

    c2: MyClass_np = z.read(fname)

    assert c2.arr_1.dtype == np.bool_
    assert c2.arr_2.dtype == np.bool_

    assert c == c2


def test_torch_bool_array():
    fname: Path = TEST_DATA_PATH / "test_torch_bool_array.zanj"
    c: MyClass_torch = MyClass_torch(
        name="test",
        arr_1=torch.tensor([True, False, True]),
        arr_2=torch.tensor([True, False, True]),
    )

    z = ZANJ()

    z.save(c, fname)

    c2: MyClass_torch = z.read(fname)

    assert c2.arr_1.dtype == torch.bool
    assert c2.arr_2.dtype == torch.bool

    assert c == c2
