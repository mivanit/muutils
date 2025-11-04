"""this utilities module handles serialization and loading of numpy and torch arrays as json

- `array_list_meta` is less efficient (arrays are stored as nested lists), but preserves both metadata and human readability.
- `array_b64_meta` is the most efficient, but is not human readable.
- `external` is mostly for use in [`ZANJ`](https://github.com/mivanit/ZANJ)

"""

from __future__ import annotations

import base64
import typing
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Literal,
    Optional,
    Sequence,
    TypedDict,
    Union,
    overload,
)

try:
    import numpy as np
except ImportError as e:
    warnings.warn(
        f"numpy is not installed, array serialization will not work: \n{e}",
        ImportWarning,
    )

if TYPE_CHECKING:
    import numpy as np
    import torch
    from muutils.json_serialize.json_serialize import JsonSerializer

from muutils.json_serialize.types import _FORMAT_KEY  # pyright: ignore[reportPrivateUsage]

# TYPING: pyright complains way too much here
# pyright: reportCallIssue=false,reportArgumentType=false,reportUnknownVariableType=false,reportUnknownMemberType=false

# Recursive type for nested numeric lists (output of arr.tolist())
NumericList = typing.Union[
    typing.List[typing.Union[int, float, bool]],
    typing.List["NumericList"],
]

ArrayMode = Literal[
    "list",
    "array_list_meta",
    "array_hex_meta",
    "array_b64_meta",
    "external",
    "zero_dim",
]


def array_n_elements(arr: Any) -> int:  # type: ignore[name-defined]  # pyright: ignore[reportAny]
    """get the number of elements in an array"""
    if isinstance(arr, np.ndarray):
        return arr.size
    elif str(type(arr)) == "<class 'torch.Tensor'>":  # pyright: ignore[reportUnknownArgumentType, reportAny]
        assert hasattr(arr, "nelement"), (
            "torch Tensor does not have nelement() method? this should not happen"
        )  # pyright: ignore[reportAny]
        return arr.nelement()  # pyright: ignore[reportAny]
    else:
        raise TypeError(f"invalid type: {type(arr)}")  # pyright: ignore[reportAny]


class ArrayMetadata(TypedDict):
    """Metadata for a numpy/torch array"""

    shape: list[int]
    dtype: str
    n_elements: int


class SerializedArrayWithMeta(TypedDict):
    """Serialized array with metadata (for array_list_meta, array_hex_meta, array_b64_meta, zero_dim modes)"""

    __muutils_format__: str
    data: typing.Union[
        NumericList, str, int, float, bool
    ]  # list, hex str, b64 str, or scalar for zero_dim
    shape: list[int]
    dtype: str
    n_elements: int


def arr_metadata(arr: Any) -> ArrayMetadata:  # pyright: ignore[reportAny]
    """get metadata for a numpy array"""
    return {
        "shape": list(arr.shape),  # pyright: ignore[reportAny]
        "dtype": (
            arr.dtype.__name__ if hasattr(arr.dtype, "__name__") else str(arr.dtype)  # pyright: ignore[reportAny]
        ),
        "n_elements": array_n_elements(arr),
    }


def serialize_array(
    jser: "JsonSerializer",  # type: ignore[name-defined] # noqa: F821
    arr: "Union[np.ndarray, torch.Tensor]",
    path: str | Sequence[str | int],  # pyright: ignore[reportUnusedParameter]
    array_mode: ArrayMode | None = None,
) -> SerializedArrayWithMeta | NumericList:
    """serialize a numpy or pytorch array in one of several modes

    if the object is zero-dimensional, simply get the unique item

    `array_mode: ArrayMode` can be one of:
    - `list`: serialize as a list of values, no metadata (equivalent to `arr.tolist()`)
    - `array_list_meta`: serialize dict with metadata, actual list under the key `data`
    - `array_hex_meta`: serialize dict with metadata, actual hex string under the key `data`
    - `array_b64_meta`: serialize dict with metadata, actual base64 string under the key `data`

    for `array_list_meta`, `array_hex_meta`, and `array_b64_meta`, the serialized object is:
    ```
    {
        _FORMAT_KEY: <array_list_meta|array_hex_meta>,
        "shape": arr.shape,
        "dtype": str(arr.dtype),
        "data": <arr.tolist()|arr.tobytes().hex()|base64.b64encode(arr.tobytes()).decode()>,
    }
    ```

    # Parameters:
     - `arr : Any` array to serialize
     - `array_mode : ArrayMode` mode in which to serialize the array
       (defaults to `None` and inheriting from `jser: JsonSerializer`)

    # Returns:
     - `JSONitem`
       json serialized array

    # Raises:
     - `KeyError` : if the array mode is not valid
    """

    if array_mode is None:
        array_mode = jser.array_mode

    arr_type: str = f"{type(arr).__module__}.{type(arr).__name__}"
    arr_np: np.ndarray = arr if isinstance(arr, np.ndarray) else np.array(arr)  # pyright: ignore[reportUnnecessaryIsInstance]

    # Handle list mode first (no metadata needed)
    if array_mode == "list":
        return arr_np.tolist()  # pyright: ignore[reportAny]

    # For all other modes, compute metadata once
    metadata: ArrayMetadata = arr_metadata(arr if len(arr.shape) == 0 else arr_np)

    # TYPING: ty<=0.0.1a24 does not appear to support unpacking TypedDicts, so we do things manually. change it back later maybe?

    # handle zero-dimensional arrays
    if len(arr.shape) == 0:
        return SerializedArrayWithMeta(
            __muutils_format__=f"{arr_type}:zero_dim",
            data=arr.item(),  # pyright: ignore[reportAny]
            shape=metadata["shape"],
            dtype=metadata["dtype"],
            n_elements=metadata["n_elements"],
        )

    # Handle the metadata modes
    if array_mode == "array_list_meta":
        return SerializedArrayWithMeta(
            __muutils_format__=f"{arr_type}:array_list_meta",
            data=arr_np.tolist(),  # pyright: ignore[reportAny]
            shape=metadata["shape"],
            dtype=metadata["dtype"],
            n_elements=metadata["n_elements"],
        )
    elif array_mode == "array_hex_meta":
        return SerializedArrayWithMeta(
            __muutils_format__=f"{arr_type}:array_hex_meta",
            data=arr_np.tobytes().hex(),
            shape=metadata["shape"],
            dtype=metadata["dtype"],
            n_elements=metadata["n_elements"],
        )
    elif array_mode == "array_b64_meta":
        return SerializedArrayWithMeta(
            __muutils_format__=f"{arr_type}:array_b64_meta",
            data=base64.b64encode(arr_np.tobytes()).decode(),
            shape=metadata["shape"],
            dtype=metadata["dtype"],
            n_elements=metadata["n_elements"],
        )
    else:
        raise KeyError(f"invalid array_mode: {array_mode}")


@overload
def infer_array_mode(
    arr: SerializedArrayWithMeta,
) -> Literal[
    "array_list_meta",
    "array_hex_meta",
    "array_b64_meta",
    "external",
    "zero_dim",
]: ...
@overload
def infer_array_mode(arr: NumericList) -> Literal["list"]: ...
def infer_array_mode(
    arr: Union[SerializedArrayWithMeta, NumericList],
) -> ArrayMode:
    """given a serialized array, infer the mode

    assumes the array was serialized via `serialize_array()`
    """
    return_mode: ArrayMode
    if isinstance(arr, typing.Mapping):
        # _FORMAT_KEY always maps to a string
        fmt: str = arr.get(_FORMAT_KEY, "")  # type: ignore
        if fmt.endswith(":array_list_meta"):
            if not isinstance(arr["data"], Iterable):
                raise ValueError(f"invalid list format: {type(arr['data']) = }\t{arr}")
            return_mode = "array_list_meta"
        elif fmt.endswith(":array_hex_meta"):
            if not isinstance(arr["data"], str):
                raise ValueError(f"invalid hex format: {type(arr['data']) = }\t{arr}")
            return_mode = "array_hex_meta"
        elif fmt.endswith(":array_b64_meta"):
            if not isinstance(arr["data"], str):
                raise ValueError(f"invalid b64 format: {type(arr['data']) = }\t{arr}")
            return_mode = "array_b64_meta"
        elif fmt.endswith(":external"):
            return_mode = "external"
        elif fmt.endswith(":zero_dim"):
            return_mode = "zero_dim"
        else:
            raise ValueError(f"invalid format: {arr}")
    elif isinstance(arr, list):  # pyright: ignore[reportUnnecessaryIsInstance]
        return_mode = "list"
    else:
        raise ValueError(f"cannot infer array_mode from\t{type(arr) = }\n{arr = }")  # pyright: ignore[reportUnreachable]

    return return_mode


@overload
def load_array(
    arr: SerializedArrayWithMeta,
    array_mode: Optional[
        Literal[
            "array_list_meta",
            "array_hex_meta",
            "array_b64_meta",
            "external",
            "zero_dim",
        ]
    ] = None,
) -> np.ndarray: ...
@overload
def load_array(
    arr: NumericList,
    array_mode: Optional[Literal["list"]] = None,
) -> np.ndarray: ...
@overload
def load_array(
    arr: np.ndarray,
    array_mode: None = None,
) -> np.ndarray: ...
def load_array(
    arr: Union[SerializedArrayWithMeta, np.ndarray, NumericList],
    array_mode: Optional[ArrayMode] = None,
) -> np.ndarray:
    """load a json-serialized array, infer the mode if not specified"""
    # return arr if its already a numpy array
    if isinstance(arr, np.ndarray):
        assert array_mode is None, (
            "array_mode should not be specified when loading a numpy array, since that is a no-op"
        )
        return arr

    # try to infer the array_mode
    array_mode_inferred: ArrayMode = infer_array_mode(arr)
    if array_mode is None:
        array_mode = array_mode_inferred
    elif array_mode != array_mode_inferred:
        warnings.warn(
            f"array_mode {array_mode} does not match inferred array_mode {array_mode_inferred}"
        )

    # actually load the array
    if array_mode == "array_list_meta":
        assert isinstance(arr, typing.Mapping), (
            f"invalid list format: {type(arr) = }\n{arr = }"
        )
        data = np.array(arr["data"], dtype=arr["dtype"])  # type: ignore
        if tuple(arr["shape"]) != tuple(data.shape):  # type: ignore
            raise ValueError(f"invalid shape: {arr}")
        return data

    elif array_mode == "array_hex_meta":
        assert isinstance(arr, typing.Mapping), (
            f"invalid list format: {type(arr) = }\n{arr = }"
        )
        data = np.frombuffer(bytes.fromhex(arr["data"]), dtype=arr["dtype"])  # type: ignore
        return data.reshape(arr["shape"])  # type: ignore

    elif array_mode == "array_b64_meta":
        assert isinstance(arr, typing.Mapping), (
            f"invalid list format: {type(arr) = }\n{arr = }"
        )
        data = np.frombuffer(base64.b64decode(arr["data"]), dtype=arr["dtype"])  # type: ignore
        return data.reshape(arr["shape"])  # type: ignore

    elif array_mode == "list":
        assert isinstance(arr, typing.Sequence), (
            f"invalid list format: {type(arr) = }\n{arr = }"
        )
        return np.array(arr)  # type: ignore
    elif array_mode == "external":
        assert isinstance(arr, typing.Mapping)
        if "data" not in arr:
            raise KeyError(  # pyright: ignore[reportUnreachable]
                f"invalid external array, expected key 'data', got keys: '{list(arr.keys())}' and arr: {arr}"
            )
        # we can ignore here since we assume ZANJ has taken care of it
        return arr["data"]  # type: ignore[return-value] # pyright: ignore[reportReturnType]
    elif array_mode == "zero_dim":
        assert isinstance(arr, typing.Mapping)
        data = np.array(arr["data"])
        if tuple(arr["shape"]) != tuple(data.shape):  # type: ignore
            raise ValueError(f"invalid shape: {arr}")
        return data
    else:
        raise ValueError(f"invalid array_mode: {array_mode}")  # pyright: ignore[reportUnreachable]
