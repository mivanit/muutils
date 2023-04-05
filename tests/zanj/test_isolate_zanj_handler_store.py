import json
import zipfile
from pathlib import Path

import numpy as np

from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)
from muutils.zanj import ZANJ
from muutils.zanj.loading import LOADER_MAP

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


print(list(LOADER_MAP.keys()))


@serializable_dataclass
class ModelCfg(SerializableDataclass):
    name: str
    num_layers: int
    hidden_size: int
    dropout: float


print(list(LOADER_MAP.keys()))


def test_isolate_handlers():
    instance = ModelCfg("lstm", 3, 128, 0.1)

    print(list(LOADER_MAP.keys()))

    z = ZANJ()
    path = TEST_DATA_PATH / "00-test_isolate_handlers.zanj"
    z.save(instance, path)
    recovered = z.read(path)
    assert instance == recovered

    assert "Basic(SerializableDataclass)" in LOADER_MAP
    assert "ModelCfg(SerializableDataclass)" in LOADER_MAP

    # check they are in the zanj file
    with zipfile.ZipFile(path, "r") as zfile:
        zmeta = json.load(zfile.open("__zanj_meta__.json", "r"))
        assert "Basic(SerializableDataclass)" in zmeta["zanj_cfg"]["load_handlers"]
        assert "ModelCfg(SerializableDataclass)" in zmeta["zanj_cfg"]["load_handlers"]


if __name__ == "__main__":
    test_isolate_handlers()
