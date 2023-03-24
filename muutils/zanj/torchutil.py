import abc
import typing
from typing import Any, Type, TypeVar

import torch

from muutils.json_serialize import SerializableDataclass
from muutils.json_serialize.json_serialize import ObjectPath
from muutils.zanj import ZANJ, register_loader_handler
from muutils.zanj.loading import LoaderHandler, load_item_recursive

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


T_config = TypeVar("T_config", bound=SerializableDataclass)


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
        if self.config_class is None:
            raise NotImplementedError("you need to set `config_class` for your model")
        if not isinstance(config, self.config_class):  # type: ignore
            raise TypeError(
                f"config must be an instance of {self.config_class = }, got {type(config) = }"
            )

        self.config: T_config = config

    def serialize(
        self, path: ObjectPath = tuple(), zanj: ZANJ | None = None
    ) -> dict[str, Any]:
        if zanj is None:
            zanj = ZANJ()
        obj = dict(
            config=self.config.serialize(),
            meta=dict(
                class_name=self.__class__.__name__,
                class_doc=self.__class__.__doc__,
                module_name=self.__class__.__module__,
                module_mro=[str(x) for x in self.__class__.__mro__],
                num_params=num_params(self),
            ),
            state_dict=self.state_dict(),
            __format__=self.__class__.__name__,
        )
        return obj

    @classmethod
    def load(
        cls, obj: dict[str, Any], path: ObjectPath, zanj: ZANJ | None = None
    ) -> "ConfiguredModel":
        """load a model from a serialized object"""

        if zanj is None:
            zanj = ZANJ()

        # get the config
        config: T_config = cls._config_class.load(obj["config"])  # type: ignore

        # initialize the model
        model: "ConfiguredModel" = cls(config)

        # load the state dict
        tensored_state_dict: dict[str, torch.Tensor] = load_item_recursive(
            obj["state_dict"],
            tuple(path) + ("state_dict",),
            zanj,
        )

        model.load_state_dict(tensored_state_dict)

        return model

    @classmethod
    def load_file(cls, file_path: str, zanj: ZANJ | None = None) -> "ConfiguredModel":
        """load a model from a file"""
        if zanj is None:
            zanj = ZANJ()

        mdl = zanj.read(file_path)
        assert isinstance(mdl, cls), f"loaded object must be a {cls}, got {type(mdl)}"
        return mdl

    @classmethod
    def get_handler(cls) -> LoaderHandler:
        cls_name: str = str(cls.__name__)
        return LoaderHandler(
            check=lambda json_item, path=None, z=None: (  # type: ignore
                isinstance(json_item, dict)
                and "__format__" in json_item
                and json_item["__format__"].startswith(cls_name)
            ),
            load=lambda json_item, path=None, z=None: cls.load(json_item, path, z),  # type: ignore
            uid=cls_name,
            source_pckg=cls.__module__,
            desc=f"{cls.__module__} {cls_name} loader via muutils.zanj.torchutil.ConfiguredModel",
        )


def set_config_class(
    config_class: Type[SerializableDataclass],
) -> typing.Callable[[Type[ConfiguredModel]], Type[ConfiguredModel]]:
    if not issubclass(config_class, SerializableDataclass):
        raise TypeError(f"{config_class} must be a subclass of SerializableDataclass")

    def wrapper(cls: Type[ConfiguredModel]) -> Type[ConfiguredModel]:
        # set the config class
        cls._config_class = config_class

        # register the handlers
        register_loader_handler(cls.get_handler())

        # return the new class
        return cls

    return wrapper
