import abc
import typing
from dataclasses import dataclass

import torch

from muutils.json_serialize import JSONitem
from muutils._wip.json_serialize.zanj import ZANJ


def num_params(m: torch.nn.Module, only_trainable: bool = True):
	"""return total number of parameters in a model
	
	- only counting shared parameters once
	- if `only_trainable` is False, will include parameters with `requires_grad = False`

	https://stackoverflow.com/questions/49201236/check-the-total-number-of-parameters-in-a-pytorch-model
	"""
	parameters: list[torch.nn.Parameter] = list(m.parameters())
	if only_trainable:
		parameters = [p for p in parameters if p.requires_grad]
	unique: list[torch.nn.Parameter] = {p.data_ptr(): p for p in parameters}.values()
	return sum(p.numel() for p in unique)


@dataclass
class ModelConfig(metaclass=abc.ABCMeta):
	"""configuration for a pytorch model
	
	- needs to implement: 
	  - `get_init_kwargs()`, which will return a dict of the arguments used to initialize the model
	  - `load()`, a class method which will load a model from a serialized object (JSONitem)
	- allows better loading and saving to ZANJ
	- more consistent reproducibility of models

	used in `ConfiguredModel` class
	"""

	@classmethod
	@abc.abstractclassmethod
	def load(cls, obj: JSONitem) -> "ModelConfig":
		"""load a model config from a serialized object"""
		raise NotImplementedError

	@abc.abstractmethod
	def get_init_kwargs(self) -> dict:
		"""get the kwargs used to initialize the model"""
		raise NotImplementedError

T_config = typing.TypeVar("T_config", bound=ModelConfig)
class ConfiguredModel(torch.nn.Module, typing.Generic[T_config], metaclass=abc.ABCMeta):
	"""a model that has a configuration
	
	`__init__()` must initialize the model from a config object only, and call
	`super().__init__(config)`
	"""

	def __init__(self, config: T_config):
		super().__init__()
		self.config: T_config = config

	def save(self, file_path: str, zanj: ZANJ|None) -> None:
		"""save the model to a file"""
		if zanj is None:
			zanj = ZANJ()
		
		zanj.save(
			obj = dict(
				model = self,
				config = self.config,
				meta = dict(
					class_name = self.__class__.__name__,
					module_name = self.__class__.__module__,
					num_params = num_params(self),
				),
			), 
			file_path = file_path,
		)

	@classmethod
	def load(cls, obj: JSONitem) -> "ConfiguredModel":
		"""load a model from a serialized object"""
		
		# get the config
		config: T_config = T_config.load(obj["config"])

		# initialize the model
		model: "ConfiguredModel" = cls(config)

		# load the state dict
		model.load_state_dict(obj["model"]["state_dict"])

	@classmethod
	def load_file(cls, file_path: str, zanj: ZANJ|None) -> "ConfiguredModel":
		"""load a model from a file"""
		if zanj is None:
			zanj = ZANJ()
		
		return cls.load(zanj.read(file_path))