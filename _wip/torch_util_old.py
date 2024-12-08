import typing
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

import torch

from muutils.json_serialize import BASE_HANDLERS, JSONitem, JsonSerializer

KWArgs = Any

OptimizerFactoryFunction = Callable[
    [Iterable[torch.nn.parameter.Parameter], KWArgs], torch.optim.Optimizer
]
LRschedulerFactoryFunction = Callable[
    [torch.optim.Optimizer, KWArgs], torch.optim.lr_scheduler._LRScheduler
]
LossFactoryFunction = Callable[[KWArgs], torch.nn.modules.loss._Loss]

TrainingTuple = typing.NamedTuple(
    "TrainingTuple",
    (
        ("optimizer", torch.optim.Optimizer),
        ("lr_scheduler", torch.optim.lr_scheduler._LRScheduler),
        ("loss", torch.nn.modules.loss._Loss),
    ),
)


# TODO: this is very broken, and not really using it anywhere. deprecate?


@dataclass(kw_only=True)
class TrainConfig:
    """training configuration for a pytorch model (specifically LLMs)"""

    # not sure what was happening here:
    # error: Incompatible types in assignment (expression has type "str", base class "object" defined the type as "Callable[[object, str], str]")
    __format__: str = field(default="zanj.torchutil.TrainConfig", init=False)  # type: ignore

    batch_size: int
    epochs: int = 1
    optimizer_factory: OptimizerFactoryFunction
    optimizer_kwargs: dict[str, Any] = field(default_factory=dict)
    lr_scheduler_factory: LRschedulerFactoryFunction | None
    lr_scheduler_kwargs: dict[str, Any] = field(default_factory=dict)
    # loss_factory: LossFactoryFunction
    # loss_kwargs: dict[str, Any] = field(default_factory=dict)

    def get_all(
        self,
        model: torch.nn.Module,
    ) -> TrainingTuple:
        """get the optimizer, learning rate scheduler, and loss for the model from the config"""

        raise NotImplementedError("TODO: implement this")

        # optimizer from model
        optimizer: torch.optim.Optimizer = self.optimizer_factory(
            model.parameters(), **self.optimizer_kwargs
        )

        # lr scheduler from optimizer
        lr_scheduler: torch.optim.lr_scheduler._LRScheduler
        if self.lr_scheduler_factory is None:
            # if its none, use constant LR
            lr_scheduler = torch.optim.lr_scheduler.ConstantLR(
                optimizer, factor=1.0, total_iters=0
            )
        else:
            lr_scheduler = self.lr_scheduler_factory(
                optimizer, **self.lr_scheduler_kwargs
            )

        # loss
        # loss: torch.nn.modules.loss._Loss = self.loss_factory(**self.loss_kwargs)
        loss = None

        return TrainingTuple(optimizer=optimizer, lr_scheduler=lr_scheduler, loss=loss)

    def serialize(self, jser: JsonSerializer | None = None) -> JSONitem:
        """serialize this object to JSON"""

        raise NotImplementedError("TODO: implement this")

        if jser is None:
            jser = JsonSerializer(
                handlers_default=BASE_HANDLERS
            )  # only allow base handlers, for reproducibility

        # handle `None` scheduler
        _SER_lr_scheduler_factory: dict[str, Any] | None
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
            "optimizer_kwargs": jser.json_serialize(self.optimizer_kwargs),
            "lr_scheduler_factory": _SER_lr_scheduler_factory,
            "lr_scheduler_kwargs": jser.json_serialize(self.lr_scheduler_kwargs),
            "loss_factory": {
                "__name__": self.loss_factory.__name__,
                "__module__": self.loss_factory.__module__,
            },
            "loss_kwargs": jser.json_serialize(self.loss_kwargs),
        }

    @classmethod
    def load(cls, data: dict[str, Any]) -> "TrainConfig":
        """load a TrainConfig from a serialized object

        TODO: support loading custom optimizers, lr schedulers, and losses
        """
        raise NotImplementedError("TODO: implement this")

        # optimizer
        assert (
            "optimizer_factory" in data
            and "__name__" in data["optimizer_factory"]
            and "__module__" in data["optimizer_factory"]
            and data["optimizer_factory"]["__module__"].startswith("torch.optim")
        ), "optimizer_factory must be a dict with __name__ and __module__ keys, and be a member of torch.optim"

        optimizer_factory: OptimizerFactoryFunction = getattr(
            torch.optim, data["optimizer_factory"]["__name__"]
        )

        # lr scheduler
        lr_scheduler_factory: LRschedulerFactoryFunction | None
        if data["lr_scheduler_factory"] is None:
            lr_scheduler_factory = None
        else:
            lr_scheduler_factory = getattr(
                torch.optim.lr_scheduler, data["lr_scheduler_factory"]["__name__"]
            )

        # loss
        loss_factory: LossFactoryFunction = getattr(
            torch.nn.modules.loss, data["loss_factory"]["__name__"]
        )

        return cls(
            batch_size=data["batch_size"],
            epochs=data["epochs"],
            optimizer_factory=optimizer_factory,
            optimizer_kwargs=data["optimizer_kwargs"],
            lr_scheduler_factory=lr_scheduler_factory,
            lr_scheduler_kwargs=data["lr_scheduler_kwargs"],
            loss_factory=loss_factory,
            loss_kwargs=data["loss_kwargs"],
        )


def zanj_serialize_torchmodule(
    jser: _ZANJ_pre,
    data: "torch.nn.Module",  # type: ignore
    path: ObjectPath,
) -> JSONitem:
    """serialize a torch module to zanj

    we want to save:
    - class name, docstring, __mro__
    - code of `.forward()` method
    - code of `.__init__()` method
    - state dict, in accordance with zanj parameters for storing arrays
    - `_modules` with modules as strings
    - __dict__ with values printed (not fully serialized)
    """

    # check torch is installed
    try:
        import torch
    except ImportError:
        raise ImportError(
            "torch is not installed! how do you expect to serialize torch modules?"
        )

    # check type
    if not isinstance(data, torch.nn.Module):
        raise TypeError(f"expected torch.nn.Module, got {type(data)}")

    # serialize the output
    output: dict = {
        "__format__": "torchmodule",
        "__class__": str(data.__class__.__name__),
        "__doc__": string_as_lines(data.__doc__),
        "__mro__": [str(c.__name__) for c in data.__class__.__mro__],
        "__init__": string_as_lines(inspect.getsource(data.__init__)),  # type: ignore[misc]
        "forward": string_as_lines(inspect.getsource(data.forward)),
        "state_dict": jser.json_serialize(
            data.state_dict(), tuple(path) + ("state_dict",)
        ),
        "_modules": {k: str(v) for k, v in data._modules.items()},
        "__dict__": {k: str(v) for k, v in data.__dict__.items()},
    }

    return jser.json_serialize(output)
