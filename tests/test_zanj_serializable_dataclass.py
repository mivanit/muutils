from pathlib import Path

import numpy as np
import pandas as pd
import torch

from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)
from muutils.zanj import ZANJ

np.random.seed(0)

# pylint: disable=missing-function-docstring,missing-class-docstring

TEST_DATA_PATH: Path = Path("tests/junk_data")


@serializable_dataclass
class Basic(SerializableDataclass):
    a: str
    q: int = 42
    c: list[int] = serializable_field(default_factory=list)


def test_Basic():
    instance = Basic("hello", 42, [1, 2, 3])

    z = ZANJ()
    path = TEST_DATA_PATH / "test_Basic.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class Nested(SerializableDataclass):
    name: str
    basic: Basic
    val: float


def test_Nested():
    instance = Nested("hello", Basic("hello", 42, [1, 2, 3]), 3.14)

    z = ZANJ()
    path = TEST_DATA_PATH / "test_Nested.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class Nested_with_container(SerializableDataclass):
    name: str
    basic: Basic
    val: float
    container: list[Nested] = serializable_field(
        default_factory=list,
        serialization_fn=lambda c: [n.serialize() for n in c],
        loading_fn=lambda data: [Nested.load(n) for n in data["container"]],
    )


def test_Nested_with_container():
    instance = Nested_with_container(
        "hello",
        basic=Basic("hello", 42, [1, 2, 3]),
        val=3.14,
        container=[
            Nested("n1", Basic("n1_b", 123, [4, 5, 7]), 2.71),
            Nested("n2", Basic("n2_b", 456, [7, 8, 9]), 6.28),
        ],
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_Nested_with_container.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class sdc_with_np_array(SerializableDataclass):
    name: str
    arr1: np.ndarray
    arr2: np.ndarray


def test_sdc_with_np_array_small():
    instance = sdc_with_np_array("small arrays", np.random.rand(10), np.random.rand(20))

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_with_np_array.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


def test_sdc_with_np_array():
    instance = sdc_with_np_array(
        "bigger arrays", np.random.rand(128, 128), np.random.rand(256, 256)
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_with_np_array.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class sdc_with_torch_tensor(SerializableDataclass):
    name: str
    tensor1: torch.Tensor
    tensor2: torch.Tensor


def test_sdc_tensor_small():
    instance = sdc_with_torch_tensor("small tensors", torch.rand(8), torch.rand(16))

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_tensor_small.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


def test_sdc_tensor():
    instance = sdc_with_torch_tensor(
        "bigger tensors", torch.rand(128, 128), torch.rand(256, 256)
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_tensor.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class sdc_with_df(SerializableDataclass):
    name: str
    iris_data: pd.DataFrame
    brain_data: pd.DataFrame


def test_sdc_with_df():
    instance = sdc_with_df(
        "downloaded_data",
        iris_data=pd.read_csv("tests/input_data/iris.csv"),
        brain_data=pd.read_csv("tests/input_data/brain_networks.csv"),
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_with_df.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass(kw_only=True)
class sdc_complicated(SerializableDataclass):
    name: str
    arr1: np.ndarray
    arr2: np.ndarray
    iris_data: pd.DataFrame
    brain_data: pd.DataFrame
    container: list[Nested]

    tensor: torch.Tensor


def test_sdc_complicated():
    instance = sdc_complicated(
        name="complicated data",
        arr1=np.random.rand(128, 128),
        arr2=np.random.rand(256, 256),
        iris_data=pd.read_csv("tests/input_data/iris.csv"),
        brain_data=pd.read_csv("tests/input_data/brain_networks.csv"),
        container=[
            Nested(
                f"n-{n}",
                Basic(f"n-{n}_b", n * 10 + 1, [n + 1, n + 2, n + 10]),
                n * np.pi,
            )
            for n in range(10)
        ],
        tensor=torch.rand(512, 512),
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_complicated.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class sdc_container_explicit(SerializableDataclass):
    name: str
    container: list[Nested] = serializable_field(
        default_factory=list,
        serialization_fn=lambda c: [n.serialize() for n in c],
        loading_fn=lambda data: [Nested.load(n) for n in data["container"]],
    )


def test_sdc_container_explicit():
    instance = sdc_container_explicit(
        "container explicit",
        container=[
            Nested(
                f"n-{n}",
                Basic(f"n-{n}_b", n * 10 + 1, [n + 1, n + 2, n + 10]),
                n * np.pi,
            )
            for n in range(10)
        ],
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_sdc_container_explicit.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered


@serializable_dataclass
class ModelCfg(SerializableDataclass):
    name: str
    num_layers: int
    hidden_size: int
    dropout: float

@serializable_dataclass
class OptimizerCfg(SerializableDataclass):
    name: str
    lr: float
    weight_decay: float

class CustomCfg:
    def __init__(self, x: int, y: str):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def serialize(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def load(cls, data):
        return cls(**{
            "x": data["x"],
            "y": data["y"],
        })

@serializable_dataclass
class MyCfgHolder(SerializableDataclass):
    model: ModelCfg
    optimizer: OptimizerCfg
    custom: CustomCfg


def test_config_holder():
    instance = MyCfgHolder(
        ModelCfg("lstm", 3, 128, 0.1),
        OptimizerCfg("adam", 0.001, 0.0001),
        CustomCfg(42, "forty-two"),
    )

    z = ZANJ()
    path = TEST_DATA_PATH / "test_config_holder.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered