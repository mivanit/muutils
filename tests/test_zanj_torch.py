from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pytest

from muutils.zanj import ZANJ
from muutils.json_serialize import JSONitem, serializable_dataclass, SerializableDataclass, serializable_field
from muutils.zanj.loading import LOADER_HANDLERS, LOADER_MAP, register_loader_handler

np.random.seed(0)

TEST_DATA_PATH: Path = Path("tests/junk_data")


def test_torch_configmodel():
    import torch

    from muutils.zanj.torchutil import ConfiguredModel, set_config_class

    @serializable_dataclass
    class MyGPTConfig(SerializableDataclass):
        """basic test GPT config"""

        n_layers: int
        n_heads: int
        embedding_size: int
        n_positions: int
        n_vocab: int

        loss_factory: torch.nn.modules.loss._Loss = serializable_field(
            default_factory=lambda: torch.nn.CrossEntropyLoss,
            serialization_fn=lambda x: x.__name__,
            loading_fn=lambda x: getattr(torch.nn, x["loss_factory"]),
        )

        loss_kwargs: dict = serializable_field(default_factory=dict)

        @property
        def loss(self):
            return self.loss_factory(**self.loss_kwargs)

        optim_factory: torch.optim.Optimizer = serializable_field(
            default_factory=lambda: torch.optim.Adam,
            serialization_fn=lambda x: x.__name__,
            loading_fn=lambda x: getattr(torch.optim, x["optim_factory"]),
        )

        optim_kwargs: dict = serializable_field(default_factory=dict)

        @property
        def optim(self, model):
            return self.optim_factory(model.parameters(), **self.optim_kwargs)


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
        loss_factory=torch.nn.CrossEntropyLoss,
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

    assert model.config == model2.config
    
    for k, v in model.state_dict().items():
        assert torch.allclose(model.state_dict()[k], model2.state_dict()[k])


    model3: MyGPT = ZANJ().read(fname)
    print(f"loaded model from {fname}")
    print(f"{model3.config = }")

    assert model.config == model3.config

    for k, v in model.state_dict().items():
        assert torch.allclose(model.state_dict()[k], model3.state_dict()[k])
