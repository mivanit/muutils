"""utilities for working with tensors and arrays.

notably:

- `TYPE_TO_JAX_DTYPE` : a mapping from python, numpy, and torch types to `jaxtyping` types
- `DTYPE_MAP` mapping string representations of types to their type
- `TORCH_DTYPE_MAP` mapping string representations of types to torch types
- `compare_state_dicts` for comparing two state dicts and giving a detailed error message on whether if was keys, shapes, or values that didn't match

"""

from __future__ import annotations

import json
import typing

import jaxtyping
import numpy as np
import torch

from muutils.errormode import ErrorMode
from muutils.dictmagic import dotlist_to_nested_dict

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
    np.float16: jaxtyping.Float,
    np.float32: jaxtyping.Float,
    np.float64: jaxtyping.Float,
    np.half: jaxtyping.Float,
    np.single: jaxtyping.Float,
    np.double: jaxtyping.Float,
    # numpy int
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
"dict mapping python, numpy, and torch types to `jaxtyping` types"

if np.version.version < "2.0.0":
    TYPE_TO_JAX_DTYPE[np.float_] = jaxtyping.Float
    TYPE_TO_JAX_DTYPE[np.int_] = jaxtyping.Int


# TODO: add proper type annotations to this signature
# TODO: maybe get rid of this altogether?
def jaxtype_factory(
    name: str,
    array_type: type,
    default_jax_dtype=jaxtyping.Float,
    legacy_mode: typing.Union[ErrorMode, str] = ErrorMode.WARN,
) -> type:
    """usage:
    ```
    ATensor = jaxtype_factory("ATensor", torch.Tensor, jaxtyping.Float)
    x: ATensor["dim1 dim2", np.float32]
    ```
    """
    legacy_mode_ = ErrorMode.from_any(legacy_mode)

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
            return "\n".join(
                f"{k} = {v}"
                for k, v in {
                    "cls.__name__": cls.__name__,
                    "cls.__doc__": cls.__doc__,
                    "params": params,
                    "type(params)": type(params),
                }.items()
            )

        @typing._tp_cache  # type: ignore
        def __class_getitem__(cls, params: typing.Union[str, tuple]) -> type:  # type: ignore
            # MyTensor["dim1 dim2"]
            if isinstance(params, str):
                return default_jax_dtype[array_type, params]

            elif isinstance(params, tuple):
                if len(params) != 2:
                    raise Exception(
                        f"unexpected type for params, expected tuple of length 2 here:\n{cls.param_info(params)}"
                    )

                if isinstance(params[0], str):
                    # MyTensor["dim1 dim2", int]
                    return TYPE_TO_JAX_DTYPE[params[1]][array_type, params[0]]

                elif isinstance(params[0], tuple):
                    legacy_mode_.process(
                        f"legacy type annotation was used:\n{cls.param_info(params) = }",
                        except_cls=Exception,
                    )
                    # MyTensor[("dim1", "dim2"), int]
                    shape_anot: list[str] = list()
                    for x in params[0]:
                        if isinstance(x, str):
                            shape_anot.append(x)
                        elif isinstance(x, int):
                            shape_anot.append(str(x))
                        elif isinstance(x, tuple):
                            shape_anot.append("".join(str(y) for y in x))
                        else:
                            raise Exception(
                                f"unexpected type for params, expected first part to be str, int, or tuple:\n{cls.param_info(params)}"
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


def numpy_to_torch_dtype(dtype: typing.Union[np.dtype, torch.dtype]) -> torch.dtype:
    """convert numpy dtype to torch dtype"""
    if isinstance(dtype, torch.dtype):
        return dtype
    else:
        return torch.from_numpy(np.array(0, dtype=dtype)).dtype


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
        np.longlong,
        np.short,
        # simplest
        np.uint8,
        np.bool_,
    ],
]
"list of all the python, numpy, and torch numerical types I could think of"

if np.version.version < "2.0.0":
    DTYPE_LIST.extend([np.float_, np.int_])

DTYPE_MAP: dict = {
    **{str(x): x for x in DTYPE_LIST},
    **{dtype.__name__: dtype for dtype in DTYPE_LIST if dtype.__module__ == "numpy"},
}
"mapping from string representations of types to their type"

TORCH_DTYPE_MAP: dict = {
    key: numpy_to_torch_dtype(dtype) for key, dtype in DTYPE_MAP.items()
}
"mapping from string representations of types to specifically torch types"

# no idea why we have to do this, smh
DTYPE_MAP["bool"] = np.bool_
TORCH_DTYPE_MAP["bool"] = torch.bool


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
    tensor: jaxtyping.Shaped[torch.Tensor, "dim1"],  # noqa: F821
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False,
) -> jaxtyping.Shaped[torch.Tensor, "padded_length"]:  # noqa: F821
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
    """pad a 1-d tensor on the left with pad_value to length `padded_length`"""
    return pad_tensor(tensor, padded_length, pad_value, rpad=False)


def rpad_tensor(
    tensor: torch.Tensor, pad_length: int, pad_value: float = 0.0
) -> torch.Tensor:
    """pad a 1-d tensor on the right with pad_value to length `pad_length`"""
    return pad_tensor(tensor, pad_length, pad_value, rpad=True)


def pad_array(
    array: jaxtyping.Shaped[np.ndarray, "dim1"],  # noqa: F821
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False,
) -> jaxtyping.Shaped[np.ndarray, "padded_length"]:  # noqa: F821
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


def get_dict_shapes(d: dict[str, "torch.Tensor"]) -> dict[str, tuple[int, ...]]:
    """given a state dict or cache dict, compute the shapes and put them in a nested dict"""
    return dotlist_to_nested_dict({k: tuple(v.shape) for k, v in d.items()})


def string_dict_shapes(d: dict[str, "torch.Tensor"]) -> str:
    """printable version of get_dict_shapes"""
    return json.dumps(
        dotlist_to_nested_dict(
            {
                k: str(
                    tuple(v.shape)
                )  # to string, since indent wont play nice with tuples
                for k, v in d.items()
            }
        ),
        indent=2,
    )


class StateDictCompareError(AssertionError):
    """raised when state dicts don't match"""

    pass


class StateDictKeysError(StateDictCompareError):
    """raised when state dict keys don't match"""

    pass


class StateDictShapeError(StateDictCompareError):
    """raised when state dict shapes don't match"""

    pass


class StateDictValueError(StateDictCompareError):
    """raised when state dict values don't match"""

    pass


def compare_state_dicts(
    d1: dict, d2: dict, rtol: float = 1e-5, atol: float = 1e-8, verbose: bool = True
) -> None:
    """compare two dicts of tensors

    # Parameters:

     - `d1 : dict`
     - `d2 : dict`
     - `rtol : float`
       (defaults to `1e-5`)
     - `atol : float`
       (defaults to `1e-8`)
     - `verbose : bool`
       (defaults to `True`)

    # Raises:

     - `StateDictKeysError` : keys don't match
     - `StateDictShapeError` : shapes don't match (but keys do)
     - `StateDictValueError` : values don't match (but keys and shapes do)
    """
    # check keys match
    d1_keys: set = set(d1.keys())
    d2_keys: set = set(d2.keys())
    symmetric_diff: set = set.symmetric_difference(d1_keys, d2_keys)
    keys_diff_1: set = d1_keys - d2_keys
    keys_diff_2: set = d2_keys - d1_keys
    # sort sets for easier debugging
    symmetric_diff = set(sorted(symmetric_diff))
    keys_diff_1 = set(sorted(keys_diff_1))
    keys_diff_2 = set(sorted(keys_diff_2))
    diff_shapes_1: str = (
        string_dict_shapes({k: d1[k] for k in keys_diff_1})
        if verbose
        else "(verbose = False)"
    )
    diff_shapes_2: str = (
        string_dict_shapes({k: d2[k] for k in keys_diff_2})
        if verbose
        else "(verbose = False)"
    )
    if not len(symmetric_diff) == 0:
        raise StateDictKeysError(
            f"state dicts do not match:\n{symmetric_diff = }\n{keys_diff_1 = }\n{keys_diff_2 = }\nd1_shapes = {diff_shapes_1}\nd2_shapes = {diff_shapes_2}"
        )

    # check tensors match
    shape_failed: list[str] = list()
    vals_failed: list[str] = list()
    for k, v1 in d1.items():
        v2 = d2[k]
        # check shapes first
        if not v1.shape == v2.shape:
            shape_failed.append(k)
        else:
            # if shapes match, check values
            if not torch.allclose(v1, v2, rtol=rtol, atol=atol):
                vals_failed.append(k)

    str_shape_failed: str = (
        string_dict_shapes({k: d1[k] for k in shape_failed}) if verbose else ""
    )
    str_vals_failed: str = (
        string_dict_shapes({k: d1[k] for k in vals_failed}) if verbose else ""
    )

    if not len(shape_failed) == 0:
        raise StateDictShapeError(
            f"{len(shape_failed)} / {len(d1)} state dict elements don't match in shape:\n{shape_failed = }\n{str_shape_failed}"
        )
    if not len(vals_failed) == 0:
        raise StateDictValueError(
            f"{len(vals_failed)} / {len(d1)} state dict elements don't match in values:\n{vals_failed = }\n{str_vals_failed}"
        )
