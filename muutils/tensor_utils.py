import typing
import warnings

import jaxtyping
import numpy as np
import torch

# pylint: disable=missing-class-docstring


TYPE_TO_JAX_DTYPE: dict = {
    float: jaxtyping.Float,
    int: jaxtyping.Int,
    jaxtyping.Float: jaxtyping.Float,
    jaxtyping.Int: jaxtyping.Int,
    # bool
    bool: jaxtyping.Bool,
    jaxtyping.Bool: jaxtyping.Bool,
    np.bool_: jaxtyping.Bool,
    torch.bool: jaxtyping.Bool,
    # numpy float
    np.float_: jaxtyping.Float,
    np.float16: jaxtyping.Float,
    np.float32: jaxtyping.Float,
    np.float64: jaxtyping.Float,
    np.half: jaxtyping.Float,
    np.single: jaxtyping.Float,
    np.double: jaxtyping.Float,
    # numpy int
    np.int_: jaxtyping.Int,
    np.int8: jaxtyping.Int,
    np.int16: jaxtyping.Int,
    np.int32: jaxtyping.Int,
    np.int64: jaxtyping.Int,
    np.longlong: jaxtyping.Int,
    np.short: jaxtyping.Int,
    np.uint8: jaxtyping.Int,
    # torch float
    torch.float: jaxtyping.Float,
    torch.float16: jaxtyping.Float,
    torch.float32: jaxtyping.Float,
    torch.float64: jaxtyping.Float,
    torch.half: jaxtyping.Float,
    torch.double: jaxtyping.Float,
    torch.bfloat16: jaxtyping.Float,
    # torch int
    torch.int: jaxtyping.Int,
    torch.int8: jaxtyping.Int,
    torch.int16: jaxtyping.Int,
    torch.int32: jaxtyping.Int,
    torch.int64: jaxtyping.Int,
    torch.long: jaxtyping.Int,
    torch.short: jaxtyping.Int,
}


# TODO: add proper type annotations to this signature
def jaxtype_factory(
    name: str,
    array_type: type,
    default_jax_dtype=jaxtyping.Float,
    legacy_mode: typing.Literal["error", "warn", "ignore"] = "warn",
) -> type:
    class _BaseArray:
        """jaxtyping shorthand
        (backwards compatible with older versions of muutils.tensor_utils)

        default_jax_dtype = {default_jax_dtype}
        array_type = {array_type}
        """

        def __new__(cls, *args, **kwargs):
            raise TypeError("Type FArray cannot be instantiated.")

        def __init_subclass__(cls, *args, **kwargs):
            raise TypeError(f"Cannot subclass {cls.__name__}")

        @classmethod
        def param_info(cls, params) -> str:
            """useful for error printing"""
            return str(
                {
                    "cls.__name__": cls.__name__,
                    "cls.__doc__": cls.__doc__,
                    "params": params,
                    "type(params)": type(params),
                }
            )

        @typing._tp_cache  # type: ignore
        def __class_getitem__(cls, params):
            # MyTensor["dim1 dim2"]
            if isinstance(params, str):
                return default_jax_dtype[array_type, params]

            elif isinstance(params, tuple):
                if len(params) != 2:
                    raise Exception(
                        f"unexpected type for params:\n{cls.param_info(params)}"
                    )

                if isinstance(params[0], str):
                    # MyTensor["dim1 dim2", int]
                    return TYPE_TO_JAX_DTYPE[params[1]][array_type, params[0]]

                elif isinstance(params[0], tuple):
                    if legacy_mode == "error":
                        raise Exception(
                            f"legacy mode is set to error, but legacy type was used:\n{cls.param_info(params)}"
                        )
                    elif legacy_mode == "warn":
                        warnings.warn(
                            f"legacy type annotation was used:\n{cls.param_info(params)}"
                        )
                    # MyTensor[("dim1", "dim2"), int]
                    shape_anot: list[str] = list()
                    for x in params[0]:
                        if isinstance(x, (str, int)):
                            shape_anot.append(x)
                        elif isinstance(x, tuple):
                            shape_anot.append("".join(str(y) for y in x))
                        else:
                            raise Exception(
                                f"unexpected type for params:\n{cls.param_info(params)}"
                            )

                    return TYPE_TO_JAX_DTYPE[params[1]][
                        array_type, " ".join(shape_anot)
                    ]
            else:
                raise Exception(
                    f"unexpected type for params:\n{cls.param_info(params)}"
                )

    _BaseArray.__name__ = name

    if _BaseArray.__doc__ is None:
        _BaseArray.__doc__ = "{default_jax_dtype = }\n{array_type = }"

    _BaseArray.__doc__ = _BaseArray.__doc__.format(
        default_jax_dtype=repr(default_jax_dtype),
        array_type=repr(array_type),
    )

    return _BaseArray


if typing.TYPE_CHECKING:
    # these class definitions are only used here to make pylint happy,
    # but they make mypy unhappy and there is no way to only run if not mypy
    # so, later on we have more ignores
    class ATensor(torch.Tensor):
        @typing._tp_cache  # type: ignore
        def __class_getitem__(cls, params):
            raise NotImplementedError()

    class NDArray(torch.Tensor):
        @typing._tp_cache  # type: ignore
        def __class_getitem__(cls, params):
            raise NotImplementedError()


ATensor = jaxtype_factory("ATensor", torch.Tensor, jaxtyping.Float)  # type: ignore[misc, assignment]

NDArray = jaxtype_factory("NDArray", np.ndarray, jaxtyping.Float)  # type: ignore[misc, assignment]


DTYPE_LIST: list = [
    *[
        bool,
        int,
        float,
    ],
    *[
        # ----------
        # pytorch
        # ----------
        # floats
        torch.float,
        torch.float32,
        torch.float64,
        torch.half,
        torch.double,
        torch.bfloat16,
        # complex
        torch.complex64,
        torch.complex128,
        # ints
        torch.int,
        torch.int8,
        torch.int16,
        torch.int32,
        torch.int64,
        torch.long,
        torch.short,
        # simplest
        torch.uint8,
        torch.bool,
    ],
    *[
        # ----------
        # numpy
        # ----------
        # floats
        np.float_,
        np.float16,
        np.float32,
        np.float64,
        np.half,
        np.single,
        np.double,
        # complex
        np.complex64,
        np.complex128,
        # ints
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.int_,
        np.longlong,
        np.short,
        # simplest
        np.uint8,
        np.bool_,
    ],
]

DTYPE_MAP: dict = {str(x): x for x in DTYPE_LIST}


TORCH_OPTIMIZERS_MAP: dict[str, typing.Type[torch.optim.Optimizer]] = {
    "Adagrad": torch.optim.Adagrad,
    "Adam": torch.optim.Adam,
    "AdamW": torch.optim.AdamW,
    "SparseAdam": torch.optim.SparseAdam,
    "Adamax": torch.optim.Adamax,
    "ASGD": torch.optim.ASGD,
    "LBFGS": torch.optim.LBFGS,
    "NAdam": torch.optim.NAdam,
    "RAdam": torch.optim.RAdam,
    "RMSprop": torch.optim.RMSprop,
    "Rprop": torch.optim.Rprop,
    "SGD": torch.optim.SGD,
}


def pad_tensor(
    tensor: jaxtyping.Shaped[torch.Tensor, "dim1"],
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False,
) -> jaxtyping.Shaped[torch.Tensor, "padded_length"]:
    """pad a 1-d tensor on the left with pad_value to length `padded_length`

    set `rpad = True` to pad on the right instead"""

    temp: list[torch.Tensor] = [
        torch.full(
            (padded_length - tensor.shape[0],),
            pad_value,
            dtype=tensor.dtype,
            device=tensor.device,
        ),
        tensor,
    ]

    if rpad:
        temp.reverse()

    return torch.cat(temp)


def lpad_tensor(
    tensor: torch.Tensor, padded_length: int, pad_value: float = 0.0
) -> torch.Tensor:
    return pad_tensor(tensor, padded_length, pad_value, rpad=False)


def rpad_tensor(
    tensor: torch.Tensor, pad_length: int, pad_value: float = 0.0
) -> torch.Tensor:
    """pad a 1-d tensor on the right with pad_value to length `pad_length`"""
    return pad_tensor(tensor, pad_length, pad_value, rpad=True)


def pad_array(
    array: jaxtyping.Shaped[np.ndarray, "dim1"],
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False,
) -> jaxtyping.Shaped[np.ndarray, "padded_length"]:
    """pad a 1-d array on the left with pad_value to length `padded_length`

    set `rpad = True` to pad on the right instead"""

    temp: list[np.ndarray] = [
        np.full(
            (padded_length - array.shape[0],),
            pad_value,
            dtype=array.dtype,
        ),
        array,
    ]

    if rpad:
        temp.reverse()

    return np.concatenate(temp)


def lpad_array(
    array: np.ndarray, padded_length: int, pad_value: float = 0.0
) -> np.ndarray:
    """pad a 1-d array on the left with pad_value to length `padded_length`"""
    return pad_array(array, padded_length, pad_value, rpad=False)


def rpad_array(
    array: np.ndarray, pad_length: int, pad_value: float = 0.0
) -> np.ndarray:
    """pad a 1-d array on the right with pad_value to length `pad_length`"""
    return pad_array(array, pad_length, pad_value, rpad=True)
