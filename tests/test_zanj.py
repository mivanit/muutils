import typing

import numpy as np
import pandas as pd

from muutils._wip.json_serialize.zanj import ZANJ

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

def test_torch():
	import torch

	SimpleNetwork = torch.nn.Sequential(
		torch.nn.Linear(128, 32),
		torch.nn.ReLU(),
		torch.nn.Linear(32, 2),
		torch.nn.Softmax(dim=1),
	)

	print(SimpleNetwork)


	print(f"{dir(SimpleNetwork) = }")

	print(f"{SimpleNetwork.__class__ = }")
	print(f"{[str(x) for x in SimpleNetwork.__class__.__bases__] = }")


	ZANJ().save(SimpleNetwork, "junk_data/test_torch.zanj")


if __name__ == "__main__":
	import fire
	fire.Fire(dict(
		numpy=test_numpy,
		jsonl=test_jsonl,
		torch=test_torch,
		all=lambda: [test_numpy(), test_jsonl(), test_torch()],
	))