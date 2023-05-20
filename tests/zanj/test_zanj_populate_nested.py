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
class BasicZanj(SerializableDataclass):
    some_string: str
    arr_numbers: np.ndarray

@serializable_dataclass
class Nested(SerializableDataclass):
    name: str
    lst_basic: list[BasicZanj] = serializable_field(
        serialization_fn=lambda x: [b.serialize() for b in x],
        loading_fn=lambda x: [BasicZanj.load(b) for b in x],
	)

def test_nested_populate():
    instance = Nested(
        name="hello", 
        lst_basic=[
            BasicZanj(
				some_string = f"hello_{i}",
				arr_numbers = np.random.rand(20),
            )
            for i in range(20)
		]
	)

    z = ZANJ(
        external_array_threshold=10,
        external_list_threshold=10,
	)
    path = TEST_DATA_PATH / "test_nested_populate.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered
