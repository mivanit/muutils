import typing

import numpy as np
import pandas as pd
import torch

from muutils._wip.json_serialize.zanj import ZANJ


SimpleNetwork = torch.nn.Sequential(
	torch.nn.Linear(128, 32),
	torch.nn.ReLU(),
	torch.nn.Linear(32, 2),
	torch.nn.Softmax(dim=1),
)

print(SimpleNetwork)


