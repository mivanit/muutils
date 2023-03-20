from dataclasses import asdict, dataclass
from pathlib import Path
import typing
import json

import numpy as np
import pandas as pd
import pytest

from muutils.json_serialize.json_serialize import JsonSerializer
from muutils.json_serialize.util import JSONdict
from muutils.zanj import ZANJ
from muutils.json_serialize import JSONitem

np.random.seed(0)

def _assert_mappings_equal(m1, m2) -> bool:
    shared_keys = set(m1.keys()) & set(m2.keys())

    for k in shared_keys:
        assert k in m1
        assert k in m2

        v1 = m1[k]
        v2 = m2[k]

        if isinstance(v1, typing.Mapping):
            assert isinstance(v2, typing.Mapping)
            _assert_mappings_equal(v1, v2)
        else:
            if isinstance(v1, Iterable):
                assert isinstance(v2, Iterable)
                assert len(v1) == len(v2), f"{len(v1)} != {len(v2)}"

                tval = v1 == v2

                if hasattr(tval, "all") and callable(tval.all):
                    assert v1.shape == v2.shape, f"{v1.shape} != {v2.shape}"
                    assert tval.all()
                else:
                    if isinstance(tval, Iterable):
                        assert all(tval)
                    else:
                        assert isinstance(tval, bool)
                        assert tval
            else:
                assert tval

    return True

TEST_DATA_PATH: Path = Path("tests/junk_data")

def array_meta(x: typing.Any) -> dict:
    if isinstance(x, np.ndarray):
        return dict(
            shape=list(x.shape),
            dtype=str(x.dtype),
            contents=str(x),
        )
    else:
        return dict(
            type=type(x).__name__,
            contents=str(x),
        )


def test_numpy():
    data = dict(
        name="testing zanj",
        some_array=np.random.rand(128, 128),
        some_other_array=np.random.rand(16, 64),
        small_array=np.random.rand(4, 4),
    )
    fname: Path = TEST_DATA_PATH / "test_numpy.zanj"
    z: ZANJ = ZANJ()
    z.save(data, fname)
    recovered_data = z.read(fname)

    print(f"{list(data.keys()) = }")
    print(f"{list(recovered_data.keys()) = }")
    original_vals: dict = {k: array_meta(v) for k,v in data.items()}
    print(json.dumps(original_vals, indent=2))
    recovered_vals: dict = {k: array_meta(v) for k,v in recovered_data.items()}
    print(json.dumps(recovered_vals, indent=2))


    assert sorted(list(data.keys())) == sorted(list(recovered_data.keys()))
    # assert all([type(data[k]) == type(recovered_data[k]) for k in data.keys()])

    assert all(
        [
            data["name"] == recovered_data["name"],
            np.allclose(data["some_array"], recovered_data["some_array"]),
            np.allclose(data["some_other_array"], recovered_data["some_other_array"]),
            np.allclose(data["small_array"], recovered_data["small_array"]),
        ]
    ), f"assert failed:\n{data = }\n{recovered_data = }"


def test_jsonl():
    data = dict(
        name="testing zanj jsonl",
        iris_data=pd.read_csv(
            "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        ),
        brain_data=pd.read_csv(
            "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/brain_networks.csv"
        ),
        some_array=np.random.rand(128, 128),
    )
    fname: Path = TEST_DATA_PATH / "test_jsonl.zanj"
    z: ZANJ = ZANJ()
    z.save(data, fname)
    recovered_data = z.read(fname)

    assert sorted(list(data.keys())) == sorted(list(recovered_data.keys()))
    # assert all([type(data[k]) == type(recovered_data[k]) for k in data.keys()])

    assert all(
        [
            data["name"] == recovered_data["name"],
            np.allclose(data["some_array"], recovered_data["some_array"]),
            data["iris_data"].equals(recovered_data["iris_data"]),
            data["brain_data"].equals(recovered_data["brain_data"]),
        ]
    )


def test_torch_simple():
    import torch

    SimpleNetwork = torch.nn.Sequential(
        torch.nn.Linear(128, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 2),
        torch.nn.Softmax(dim=1),
    )
    fname: Path = TEST_DATA_PATH / "test_torch.zanj"
    z: ZANJ = ZANJ()
    z.save(SimpleNetwork, fname)
    recovered_data = z.read(fname)

    assert SimpleNetwork == recovered_data


@pytest.mark.skip(reason="TODO")
def test_torch_configmodel():
    import torch

    from muutils.zanj.torchutil import ConfiguredModel, ModelConfig, set_config_class

    @dataclass
    class MyGPTConfig(ModelConfig):
        """basic test GPT config"""

        n_layers: int
        n_heads: int
        embedding_size: int
        n_positions: int
        n_vocab: int

        # override here is returning `MyGPTConfig` instead of `ModelConfig`
        @classmethod
        def load(cls, obj: JSONdict) -> "MyGPTConfig":  # type: ignore[override]
            """load the model from a path"""
            return cls(**obj)  # type: ignore[arg-type]

        def serialize(self, jser: JsonSerializer | None = None) -> JSONitem:
            """serialize the model to a path"""
            return asdict(self)

    @set_config_class(MyGPTConfig)
    class MyGPT(ConfiguredModel[MyGPTConfig]):
        """basic GPT model"""

        def __init__(self, config: MyGPTConfig):
            super().__init__(config)

            # implementation of a GPT style model with decoders only

            self.transformer = torch.nn.Transformer(
                d_model=config.embedding_size,
                nhead=config.n_heads,
                num_encoder_layers=0,
                num_decoder_layers=config.n_layers,
            )

        def forward(self, x):
            return self.transformer(x)

    config: MyGPTConfig = MyGPTConfig(
        n_layers=2,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
    )

    model: MyGPT = MyGPT(config)

    fname: Path = TEST_DATA_PATH / "test_torch_configmodel.zanj"
    ZANJ().save(model, fname)

    print(f"saved model to {fname}")
    print(f"{model.config = }")

    # try to load the model
    model2: MyGPT = MyGPT.load_file(fname)
    print(f"loaded model from {fname}")
    print(f"{model2.config = }")


if __name__ == "__main__":
    import fire  # type: ignore[import]

    fire.Fire(
        dict(
            numpy=test_numpy,
            jsonl=test_jsonl,
            torch_simple=test_torch_simple,
            torch=test_torch_configmodel,
            all=lambda: [
                test_numpy(),
                test_jsonl(),
                test_torch_simple(),
                test_torch_configmodel(),
            ],
        )
    )
