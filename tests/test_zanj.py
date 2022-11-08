import typing

import numpy as np
# import pandas as pd
# import torch

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



def test_torch():

	SimpleNetwork = torch.nn.Sequential(
		torch.nn.Linear(128, 32),
		torch.nn.ReLU(),
		torch.nn.Linear(32, 2),
		torch.nn.Softmax(dim=1),
	)

	print(SimpleNetwork)


	print(f"{dir(SimpleNetwork) = }")


	# ZANJ.save


if __name__ == "__main__":
	import fire
	fire.Fire(dict(
		numpy=test_numpy,
		torch=test_torch,
	))