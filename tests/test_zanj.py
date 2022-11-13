import typing
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

from muutils.json_serialize.zanj import ZANJ

np.random.seed(0)

def test_numpy():

	data = dict(
		name="testing zanj",
		some_array=np.random.rand(128, 128),
		some_other_array=np.random.rand(16, 64),
		small_array=np.random.rand(4, 4),
	)

	ZANJ().save(data, "junk_data/test_numpy.zanj")

def test_jsonl():

	data = dict(
		name="testing zanj jsonl",
		iris_data=pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv'),
		brain_data=pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/brain_networks.csv'),
		some_array=np.random.rand(128, 128),
	)

	ZANJ().save(data, "junk_data/test_jsonl.zanj")

def test_torch_simple():
	import torch

	SimpleNetwork = torch.nn.Sequential(
		torch.nn.Linear(128, 32),
		torch.nn.ReLU(),
		torch.nn.Linear(32, 2),
		torch.nn.Softmax(dim=1),
	)

	# print(SimpleNetwork)


	# print(f"{dir(SimpleNetwork) = }")

	# print(f"{SimpleNetwork.__class__ = }")
	# print(f"{[str(x) for x in SimpleNetwork.__class__.__bases__] = }")


	ZANJ().save(SimpleNetwork, "junk_data/test_torch.zanj")


def test_torch_configmodel():
	import torch

	from muutils.json_serialize.torchutil import ModelConfig, ConfiguredModel

	@dataclass
	class MyGPTConfig(ModelConfig):
		"""basic test GPT config"""
		n_layers: int
		n_heads: int
		embedding_size: int
		n_positions: int
		n_vocab: int

		def get_init_kwargs(self) -> dict:
			"""just return all the attributes of the dataclass"""
			return asdict(self)
		
		@classmethod
		def load(cls, obj: dict) -> "MyGPTConfig":
			"""load the model from a path"""
			return cls(**data)

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


	fname: str = "junk_data/test_torch_configmodel.zanj"
	ZANJ().save(model, fname)

	print(f"saved model to {fname}")
	print(f"{model.config = }")

	# try to load the model
	model2: MyGPT = ZANJ().read(fname)
	print(f"loaded model from {fname}")
	print(f"{model2.config = }")



	




if __name__ == "__main__":
	import fire
	fire.Fire(dict(
		numpy=test_numpy,
		jsonl=test_jsonl,
		torch_simple=test_torch_simple,
		torch=test_torch_configmodel,
		all=lambda: [
			test_numpy(), test_jsonl(), 
			test_torch_simple(), test_torch_configmodel(),
		],
	))