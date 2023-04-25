import abc
import typing
from typing import Any, Type, TypeVar

import torch

from muutils.json_serialize import SerializableDataclass
from muutils.json_serialize.json_serialize import ObjectPath
from muutils.json_serialize.util import safe_getsource, string_as_lines
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
    """a model that has a configuration, for saving with ZANJ

    ```python
    @set_config_class(YourConfig)
    class YourModule(ConfiguredModel[YourConfig]):
        def __init__(self, cfg: YourConfig):
            super().__init__(cfg)
    ```

    `__init__()` must initialize the model from a config object only, and call
    `super().__init__(zanj_model_config)`

    If you are inheriting from another class + ConfiguredModel,
    ConfiguredModel must be the first class in the inheritance list
    """

    # dont set this directly, use `set_config_class()` decorator
    _config_class: type | None = None
    zanj_config_class = property(lambda self: type(self)._config_class)

    def __init__(self, zanj_model_config: T_config, **kwargs):
        super().__init__(**kwargs)
        if self.zanj_config_class is None:
            raise NotImplementedError("you need to set `config_class` for your model")
        if not isinstance(zanj_model_config, self.zanj_config_class):  # type: ignore
            raise TypeError(
                f"config must be an instance of {self.zanj_config_class = }, got {type(zanj_model_config) = }"
            )

        self.zanj_model_config: T_config = zanj_model_config
        self.training_records: dict | None = None

    def serialize(
        self, path: ObjectPath = tuple(), zanj: ZANJ | None = None
    ) -> dict[str, Any]:
        if zanj is None:
            zanj = ZANJ()
        obj = dict(
            zanj_model_config=self.zanj_model_config.serialize(),
            meta=dict(
                class_name=self.__class__.__name__,
                class_doc=string_as_lines(self.__class__.__doc__),
                class_source=safe_getsource(self.__class__),
                module_name=self.__class__.__module__,
                module_mro=[str(x) for x in self.__class__.__mro__],
                num_params=num_params(self),
                as_str=string_as_lines(str(self)),
            ),
            training_records=self.training_records,
            state_dict=self.state_dict(),
            __format__=self.__class__.__name__,
        )
        return obj

    def save(self, file_path: str, zanj: ZANJ | None = None):
        if zanj is None:
            zanj = ZANJ()
        zanj.save(self.serialize(), file_path)

    def _load_state_dict_wrapper(
        self,
        state_dict: dict[str, torch.Tensor],
        **kwargs,
    ):
        """wrapper for `load_state_dict()` in case you need to override it"""
        assert len(kwargs) == 0, f"got unexpected kwargs: {kwargs}"
        return self.load_state_dict(state_dict)

    @classmethod
    def load(
        cls, obj: dict[str, Any], path: ObjectPath, zanj: ZANJ | None = None
    ) -> "ConfiguredModel":
        """load a model from a serialized object"""

        if zanj is None:
            zanj = ZANJ()

        # get the config
        zanj_model_config: T_config = cls._config_class.load(obj["zanj_model_config"])  # type: ignore

        # get the training records
        training_records: typing.Any = load_item_recursive(
            obj.get("training_records", None),
            tuple(path) + ("training_records",),
            zanj,
        )

        # initialize the model
        model: "ConfiguredModel" = cls(zanj_model_config)

        # load the state dict
        tensored_state_dict: dict[str, torch.Tensor] = load_item_recursive(
            obj["state_dict"],
            tuple(path) + ("state_dict",),
            zanj,
        )

        model._load_state_dict_wrapper(
            tensored_state_dict,
            **zanj.custom_settings.get("_load_state_dict_wrapper", dict()),
        )

        # set the training records
        model.training_records = training_records

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


class ConfigMismatchException(ValueError):
    def __init__(self, msg: str, diff):
        super().__init__(msg)
        self.diff = diff

    def __str__(self):
        return f"{super().__str__()}: {self.diff}"


def assert_model_cfg_equality(model_a: ConfiguredModel, model_b: ConfiguredModel):
    """check both models are correct instances and have the same config

    Raises:
        ConfigMismatchException: if the configs don't match, e.diff will contain the diff
    """
    assert isinstance(model_a, ConfiguredModel), "model_a must be a ConfiguredModel"
    assert isinstance(
        model_a.zanj_model_config, SerializableDataclass
    ), "model_a must have a zanj_model_config"
    assert isinstance(model_b, ConfiguredModel), "model_b must be a ConfiguredModel"
    assert isinstance(
        model_b.zanj_model_config, SerializableDataclass
    ), "model_b must have a zanj_model_config"

    cls_type: type = type(model_a.zanj_model_config)

    if not (model_a.zanj_model_config == model_b.zanj_model_config):
        raise ConfigMismatchException(
            f"configs of type {type(model_a.zanj_model_config)}, {type(model_b.zanj_model_config)} don't match",
            diff=cls_type.diff(model_a.zanj_model_config, model_b.zanj_model_config),
        )


def assert_model_exact_equality(model_a: ConfiguredModel, model_b: ConfiguredModel):
    """check the models are exactly equal, including state dict contents"""
    assert_model_cfg_equality(model_a, model_b)

    model_a_sd_keys: set[str] = set(model_a.state_dict().keys())
    model_b_sd_keys: set[str] = set(model_b.state_dict().keys())
    assert (
        model_a_sd_keys == model_b_sd_keys
    ), f"state dict keys don't match: {model_a_sd_keys - model_b_sd_keys} / {model_b_sd_keys - model_a_sd_keys}"
    keys_failed: list[str] = list()
    for k, v_a in model_a.state_dict().items():
        v_b = model_b.state_dict()[k]
        if not (v_a == v_b).all():
            # if not torch.allclose(v, v_load):
            keys_failed.append(k)
            print(f"failed {k}")
        else:
            print(f"passed {k}")
    assert (
        len(keys_failed) == 0
    ), f"{len(keys_failed)} / {len(model_a_sd_keys)} state dict elements don't match: {keys_failed}"
