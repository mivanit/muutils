import abc
import typing
from typing import Callable, Iterable, Any
from dataclasses import dataclass, field

import torch

from muutils.json_serialize import JSONitem, JsonSerializer, BASE_HANDLERS
from muutils.zanj import ZANJ

# pylint: disable=protected-access

KWArgs = Any

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


def get_device(m: torch.nn.Module) -> tuple[
		bool,
		torch.device|dict[str, torch.device],
	]:
	"""get the current devices"""
	
	devs: dict[str, torch.device] = {
		name: p.device
		for name, p in m.named_parameters()
	}

	# check if all devices are the same
	dev_uni: torch.device = list(devs.values())[0]

	if all(dev == dev_uni for dev in devs.values()):
		return True, dev_uni
	else:
		return False, devs




OptimizerFactoryFunction = Callable[
	[Iterable[torch.nn.parameter.Parameter], KWArgs], 
	torch.optim.Optimizer
]
LRschedulerFactoryFunction = Callable[
	[torch.optim.Optimizer, KWArgs], 
	torch.optim.lr_scheduler._LRScheduler
]
LossFactoryFunction = Callable[
	[KWArgs], 
	torch.nn.modules.loss._Loss
]

TrainingTuple = typing.NamedTuple(
	"TrainingTuple",
	(
		("optimizer", torch.optim.Optimizer),
		("lr_scheduler", torch.optim.lr_scheduler._LRScheduler),
		("loss", torch.nn.modules.loss._Loss),
	),
)

@dataclass(kw_only=True)
class TrainConfig:
	"""training configuration for a pytorch model (specifically LLMs)"""
	__format__: str = field(default="zanj.torchutil.TrainConfig", init=False)

	batch_size: int
	epochs: int = 1
	optimizer_factory: OptimizerFactoryFunction
	optimizer_kwargs: dict[str, Any] = field(default_factory=dict)
	lr_scheduler_factory: LRschedulerFactoryFunction|None
	lr_scheduler_kwargs: dict[str, Any] = field(default_factory=dict)
	# loss_factory: LossFactoryFunction
	# loss_kwargs: dict[str, Any] = field(default_factory=dict)

	def get_all(
			self, 
			model: torch.nn.Module,
		) -> TrainingTuple:
		"""get the optimizer, learning rate scheduler, and loss for the model from the config"""

		# optimizer from model
		optimizer: torch.optim.Optimizer = self.optimizer_factory(model.parameters(), **self.optimizer_kwargs)

		# lr scheduler from optimizer
		lr_scheduler: torch.optim.lr_scheduler._LRScheduler
		if self.lr_scheduler_factory is None:
			# if its none, use constant LR
			lr_scheduler = torch.optim.lr_scheduler.ConstantLR(optimizer, factor = 1.0, total_iters = 0)
		else:
			lr_scheduler = self.lr_scheduler_factory(optimizer, **self.lr_scheduler_kwargs)

		# loss
		# loss: torch.nn.modules.loss._Loss = self.loss_factory(**self.loss_kwargs)
		loss = None
		
		return TrainingTuple(optimizer = optimizer, lr_scheduler = lr_scheduler, loss = loss)

	def serialize(self, jser: JsonSerializer|None = None) -> JSONitem:
		"""serialize this object to JSON"""
		if jser is None:
			jser = JsonSerializer(handlers_default=BASE_HANDLERS) # only allow base handlers, for reproducibility

		# handle `None` scheduler
		_SER_lr_scheduler_factory: dict[str, Any]|None
		if self.lr_scheduler_factory is not None:
			_SER_lr_scheduler_factory = {
				"__name__": self.lr_scheduler_factory.__name__,
				"__module__": self.lr_scheduler_factory.__module__,
			}
		else:
			_SER_lr_scheduler_factory = None

		return {
			"__format__": self.__format__,
			"batch_size": self.batch_size,
			"epochs": self.epochs,
			"optimizer_factory": {
				"__name__": self.optimizer_factory.__name__,
				"__module__": self.optimizer_factory.__module__,
			},
			"optimizer_kwargs" : jser.json_serialize(self.optimizer_kwargs),
			"lr_scheduler_factory": _SER_lr_scheduler_factory,
			"lr_scheduler_kwargs" : jser.json_serialize(self.lr_scheduler_kwargs),
			"loss_factory": {
				"__name__": self.loss_factory.__name__,
				"__module__": self.loss_factory.__module__,
			},
			"loss_kwargs" : jser.json_serialize(self.loss_kwargs),
		}
		

	@classmethod
	def load(cls, data: JSONitem) -> "TrainConfig":
		"""load a TrainConfig from a serialized object
		
		TODO: support loading custom optimizers, lr schedulers, and losses
		"""

		# optimizer
		assert (
			"optimizer_factory" in data
			and "__name__" in data["optimizer_factory"]
			and "__module__" in data["optimizer_factory"]
			and data["optimizer_factory"]["__module__"].startswith("torch.optim")
		), "optimizer_factory must be a dict with __name__ and __module__ keys, and be a member of torch.optim"

		optimizer_factory: OptimizerFactoryFunction = getattr(torch.optim, data["optimizer_factory"]["__name__"])

		# lr scheduler
		if data["lr_scheduler_factory"] is None:
			lr_scheduler_factory: LRschedulerFactoryFunction|None = None
		else:
			lr_scheduler_factory: LRschedulerFactoryFunction = getattr(torch.optim.lr_scheduler, data["lr_scheduler_factory"]["__name__"])

		# loss
		loss_factory: LossFactoryFunction = getattr(torch.nn.modules.loss, data["loss_factory"]["__name__"])

		return cls(
			batch_size = data["batch_size"],
			epochs = data["epochs"],
			optimizer_factory = optimizer_factory,
			optimizer_kwargs = data["optimizer_kwargs"],
			lr_scheduler_factory = lr_scheduler_factory,
			lr_scheduler_kwargs = data["lr_scheduler_kwargs"],
			loss_factory = loss_factory,
			loss_kwargs = data["loss_kwargs"],
		)




@dataclass
class ModelConfig(metaclass=abc.ABCMeta):
	"""configuration for a pytorch model
	
	- needs to implement: 
	  - `load()`, a class method which will load a model from a serialized object (JSONitem)
	- allows better loading and saving to ZANJ
	- more consistent reproducibility of models

	used in `ConfiguredModel` class

	TODO: automatic mapping of loss functions and optimizers (string to class)
	"""

	@classmethod
	@abc.abstractclassmethod
	def load(cls, obj: JSONitem) -> "ModelConfig":
		"""load a model config from a serialized object"""
		raise NotImplementedError()

	@abc.abstractmethod
	def serialize(self, jser: JsonSerializer|None = None) -> JSONitem:
		"""serialize this object to JSON"""
		raise NotImplementedError()

T_config = typing.TypeVar("T_config", bound=ModelConfig)
class ConfiguredModel(
		torch.nn.Module, 
		typing.Generic[T_config], 
		metaclass=abc.ABCMeta,
	):
	"""a model that has a configuration
	
	`__init__()` must initialize the model from a config object only, and call
	`super().__init__(config)`
	"""
	
	_config_class: type|None = None
	config_class = property(lambda self: type(self)._config_class)

	def __init__(self, config: T_config):
		super().__init__()
		print(f"{self.config_class = } {type(self.config_class) = }")
		if self.config_class is None:
			raise NotImplementedError("you need to set `config_class` for your model")
		if not isinstance(config, self.config_class): # type: ignore
			raise TypeError(f"config must be an instance of {self.config_class = }, got {type(config) = }")

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
		config: T_config = cls.config_class.load(obj["config"])

		# initialize the model
		model: "ConfiguredModel" = cls(config)

		# load the state dict
		model.load_state_dict(obj["model"]["state_dict"])

	@classmethod
	def load_file(cls, file_path: str, zanj: ZANJ|None = None) -> "ConfiguredModel":
		"""load a model from a file"""
		if zanj is None:
			zanj = ZANJ()
		
		return cls.load(zanj.read(file_path, externals_mode="full"))

def set_config_class( 
		config_class: type,
	) -> typing.Callable[[type], type]:

	if not issubclass(config_class, ModelConfig):
		raise TypeError(f"{config_class} must be a subclass of ModelConfig")

	def wrapper(cls: type) -> type:
		cls._config_class = config_class
		return cls

	return wrapper