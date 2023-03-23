import abc
import typing
from dataclasses import dataclass, field
from typing import Type, Any, Callable, Iterable, TypeVar

import torch

from muutils.json_serialize import BASE_HANDLERS, JSONitem, JsonSerializer
from muutils.json_serialize.util import JSONdict
from muutils.zanj import ZANJ
from muutils.zanj.loading import LoadedZANJ

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

    unique: list[torch.nn.Parameter] = list(
        {p.data_ptr(): p for p in parameters}.values()
    )

    return sum(p.numel() for p in unique)


def get_device(
    m: torch.nn.Module,
) -> tuple[bool, torch.device | dict[str, torch.device],]:
    """get the current devices"""

    devs: dict[str, torch.device] = {name: p.device for name, p in m.named_parameters()}

    # check if all devices are the same
    dev_uni: torch.device = list(devs.values())[0]

    if all(dev == dev_uni for dev in devs.values()):
        return True, dev_uni
    else:
        return False, devs


# "error: Only concrete class can be given where Type[Abstract] is expected"
# this is a mypy issue, see
# https://github.com/python/mypy/issues/5374
# https://github.com/python/mypy/issues/4717
@dataclass  # type: ignore
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
    def load(cls, obj: JSONdict) -> "ModelConfig":
        """load a model config from a serialized object"""
        raise NotImplementedError()

    @abc.abstractmethod
    def serialize(self, jser: JsonSerializer | None = None) -> JSONitem:
        """serialize this object to JSON"""
        raise NotImplementedError()


T_config = TypeVar("T_config", bound=ModelConfig)


class ConfiguredModel(
    torch.nn.Module,
    typing.Generic[T_config],
    metaclass=abc.ABCMeta,
):
    """a model that has a configuration

    `__init__()` must initialize the model from a config object only, and call
    `super().__init__(config)`
    """

    _config_class: type | None = None
    config_class = property(lambda self: type(self)._config_class)

    def __init__(self, config: T_config):
        super().__init__()
        print(f"{self.config_class = } {type(self.config_class) = }")
        if self.config_class is None:
            raise NotImplementedError("you need to set `config_class` for your model")
        if not isinstance(config, self.config_class):  # type: ignore
            raise TypeError(
                f"config must be an instance of {self.config_class = }, got {type(config) = }"
            )

        self.config: T_config = config

    def save(self, file_path: str, zanj: ZANJ | None) -> None:
        """save the model to a file"""
        if zanj is None:
            zanj = ZANJ()

        zanj.save(
            obj=dict(
                model=self,
                config=self.config,
                meta=dict(
                    class_name=self.__class__.__name__,
                    module_name=self.__class__.__module__,
                    num_params=num_params(self),
                ),
            ),
            file_path=file_path,
        )

    @classmethod
    def load(cls, obj: dict[str, Any] | LoadedZANJ) -> "ConfiguredModel":
        """load a model from a serialized object"""

        # get the config
        config: T_config = cls.config_class.load(obj["config"])

        # initialize the model
        model: "ConfiguredModel" = cls(config)

        # load the state dict
        model.load_state_dict(obj["model"]["state_dict"])

        return model

    @classmethod
    def load_file(cls, file_path: str, zanj: ZANJ | None = None) -> "ConfiguredModel":
        """load a model from a file"""
        if zanj is None:
            zanj = ZANJ()

        return cls.load(zanj.read(file_path, externals_mode="full"))


def set_config_class(
    config_class: Type[ModelConfig],
) -> typing.Callable[[Type[ConfiguredModel]], Type[ConfiguredModel]]:

    if not issubclass(config_class, ModelConfig):
        raise TypeError(f"{config_class} must be a subclass of ModelConfig")

    def wrapper(cls: Type[ConfiguredModel]) -> Type[ConfiguredModel]:
        cls._config_class = config_class
        return cls

    return wrapper
