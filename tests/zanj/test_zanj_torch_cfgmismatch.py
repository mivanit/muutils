from typing import Any

import torch

from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)
from muutils.zanj.torchutil import (
    ConfigMismatchException,
    ConfiguredModel,
    assert_model_cfg_equality,
    set_config_class,
)

# Assuming required imports and classes are present (including ConfiguredModel, MyGPTConfig, and MyGPT)


@serializable_dataclass
class MyGPTConfig(SerializableDataclass):
    """basic test GPT config"""

    n_layers: int
    n_heads: int
    embedding_size: int
    n_positions: int
    n_vocab: int
    junk_data: Any = serializable_field(default_factory=dict)


@set_config_class(MyGPTConfig)
class MyGPT(ConfiguredModel[MyGPTConfig]):
    """basic "GPT" model"""

    def __init__(self, config: MyGPTConfig):
        super().__init__(config)
        self.transformer = torch.nn.Linear(config.embedding_size, config.n_vocab)

    def forward(self, x):
        return self.transformer(x)


def test_config_mismatch_exception_direct():
    msg = "Configs don't match"
    diff = {"model_cfg": {"are_weights_processed": {"self": False, "other": True}}}

    exc = ConfigMismatchException(msg, diff)
    assert exc.diff == diff
    assert (
        str(exc)
        == r"Configs don't match: {'model_cfg': {'are_weights_processed': {'self': False, 'other': True}}}"
    )


def test_equal_configs():
    config = MyGPTConfig(
        n_layers=2,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
        junk_data={"a": 1, "b": 2},
    )

    model_a = MyGPT(config)
    model_b = MyGPT(config)

    assert_model_cfg_equality(model_a, model_b)


def test_unequal_configs():
    config_a = MyGPTConfig(
        n_layers=2,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
        junk_data={"a": 1, "b": 2},
    )
    # a different config
    config_b = MyGPTConfig(
        n_layers=3,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
        junk_data={"a": 7, "something": "or other"},
    )

    model_a = MyGPT(config_a)
    model_b = MyGPT(config_b)

    try:
        assert_model_cfg_equality(model_a, model_b)
    except ConfigMismatchException as exc:
        assert exc.diff == {
            "n_layers": {"self": 2, "other": 3},
            "junk_data": {
                "self": {"a": 1, "b": 2},
                "other": {"a": 7, "something": "or other"},
            },
        }
    else:
        raise AssertionError("Expected a ConfigMismatchException!")


def test_unequal_configs_2():
    config_a = MyGPTConfig(
        n_layers=2,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
        junk_data={"a": 1, "b": 2},
    )
    # a different config
    config_b = MyGPTConfig(
        n_layers=3,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
        junk_data="this isnt even a dict lol",
    )

    model_a = MyGPT(config_a)
    model_b = MyGPT(config_b)

    try:
        assert_model_cfg_equality(model_a, model_b)
    except ConfigMismatchException as exc:
        assert exc.diff == {
            "n_layers": {"self": 2, "other": 3},
            "junk_data": {
                "self": {"a": 1, "b": 2},
                "other": "this isnt even a dict lol",
            },
        }
    else:
        raise AssertionError("Expected a ConfigMismatchException!")


def test_incorrect_instance():
    config = MyGPTConfig(
        n_layers=2,
        n_heads=2,
        embedding_size=16,
        n_positions=16,
        n_vocab=128,
    )

    model_a = MyGPT(config)
    model_b = "Not a ConfiguredModel instance"

    try:
        assert_model_cfg_equality(model_a, model_b)  # type: ignore
    except AssertionError as exc:
        assert str(exc) == "model_b must be a ConfiguredModel"
