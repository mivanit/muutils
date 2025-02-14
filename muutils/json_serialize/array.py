"""this utilities module handles serialization and loading of numpy and torch arrays as json

- `array_list_meta` is less efficient (arrays are stored as nested lists), but preserves both metadata and human readability.
- `array_b64_meta` is the most efficient, but is not human readable.
- `external` is mostly for use in [`ZANJ`](https://github.com/mivanit/ZANJ)

"""

from __future__ import annotations

import base64
import typing
import warnings
from typing import Any, Iterable, Literal, Optional, Sequence

try:
    import numpy as np
except ImportError as e:
    warnings.warn(
        f"numpy is not installed, array serialization will not work: \n{e}",
        ImportWarning,
    )

from muutils.json_serialize.util import _FORMAT_KEY, JSONitem

# pylint: disable=unused-argument

ArrayMode = Literal[
    "list",
    "array_list_meta",
    "array_hex_meta",
    "array_b64_meta",
    "external",
    "zero_dim",
]


def array_n_elements(arr) -> int:  # type: ignore[name-defined]
    """get the number of elements in an array"""
    if isinstance(arr, np.ndarray):
        return arr.size
    elif str(type(arr)) == "<class 'torch.Tensor'>":
        return arr.nelement()
    else:
        raise TypeError(f"invalid type: {type(arr)}")


def arr_metadata(arr) -> dict[str, list[int] | str | int]:
    """get metadata for a numpy array"""
    return {
        "shape": list(arr.shape),
        "dtype": (
            arr.dtype.__name__ if hasattr(arr.dtype, "__name__") else str(arr.dtype)
        ),
        "n_elements": array_n_elements(arr),
    }


def serialize_array(
    jser: "JsonSerializer",  # type: ignore[name-defined] # noqa: F821
    arr: np.ndarray,
    path: str | Sequence[str | int],
    array_mode: ArrayMode | None = None,
) -> JSONitem:
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
    arr_np: np.ndarray = arr if isinstance(arr, np.ndarray) else np.array(arr)

    # handle zero-dimensional arrays
    if len(arr.shape) == 0:
        return {
            _FORMAT_KEY: f"{arr_type}:zero_dim",
            "data": arr.item(),
            **arr_metadata(arr),
        }

    if array_mode == "array_list_meta":
        return {
            _FORMAT_KEY: f"{arr_type}:array_list_meta",
            "data": arr_np.tolist(),
            **arr_metadata(arr_np),
        }
    elif array_mode == "list":
        return arr_np.tolist()
    elif array_mode == "array_hex_meta":
        return {
            _FORMAT_KEY: f"{arr_type}:array_hex_meta",
            "data": arr_np.tobytes().hex(),
            **arr_metadata(arr_np),
        }
    elif array_mode == "array_b64_meta":
        return {
            _FORMAT_KEY: f"{arr_type}:array_b64_meta",
            "data": base64.b64encode(arr_np.tobytes()).decode(),
            **arr_metadata(arr_np),
        }
    else:
        raise KeyError(f"invalid array_mode: {array_mode}")


def infer_array_mode(arr: JSONitem) -> ArrayMode:
    """given a serialized array, infer the mode

    assumes the array was serialized via `serialize_array()`
    """
    if isinstance(arr, typing.Mapping):
        fmt: str = arr.get(_FORMAT_KEY, "")  # type: ignore
        if fmt.endswith(":array_list_meta"):
            if not isinstance(arr["data"], Iterable):
                raise ValueError(f"invalid list format: {type(arr['data']) = }\t{arr}")
            return "array_list_meta"
        elif fmt.endswith(":array_hex_meta"):
            if not isinstance(arr["data"], str):
                raise ValueError(f"invalid hex format: {type(arr['data']) = }\t{arr}")
            return "array_hex_meta"
        elif fmt.endswith(":array_b64_meta"):
            if not isinstance(arr["data"], str):
                raise ValueError(f"invalid b64 format: {type(arr['data']) = }\t{arr}")
            return "array_b64_meta"
        elif fmt.endswith(":external"):
            return "external"
        elif fmt.endswith(":zero_dim"):
            return "zero_dim"
        else:
            raise ValueError(f"invalid format: {arr}")
    elif isinstance(arr, list):
        return "list"
    else:
        raise ValueError(f"cannot infer array_mode from\t{type(arr) = }\n{arr = }")


def load_array(arr: JSONitem, array_mode: Optional[ArrayMode] = None) -> Any:
    """load a json-serialized array, infer the mode if not specified"""
    # return arr if its already a numpy array
    if isinstance(arr, np.ndarray) and array_mode is None:
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
        assert isinstance(
            arr, typing.Mapping
        ), f"invalid list format: {type(arr) = }\n{arr = }"
        data = np.array(arr["data"], dtype=arr["dtype"])  # type: ignore
        if tuple(arr["shape"]) != tuple(data.shape):  # type: ignore
            raise ValueError(f"invalid shape: {arr}")
        return data

    elif array_mode == "array_hex_meta":
        assert isinstance(
            arr, typing.Mapping
        ), f"invalid list format: {type(arr) = }\n{arr = }"
        data = np.frombuffer(bytes.fromhex(arr["data"]), dtype=arr["dtype"])  # type: ignore
        return data.reshape(arr["shape"])  # type: ignore

    elif array_mode == "array_b64_meta":
        assert isinstance(
            arr, typing.Mapping
        ), f"invalid list format: {type(arr) = }\n{arr = }"
        data = np.frombuffer(base64.b64decode(arr["data"]), dtype=arr["dtype"])  # type: ignore
        return data.reshape(arr["shape"])  # type: ignore

    elif array_mode == "list":
        assert isinstance(
            arr, typing.Sequence
        ), f"invalid list format: {type(arr) = }\n{arr = }"
        return np.array(arr)  # type: ignore
    elif array_mode == "external":
        # assume ZANJ has taken care of it
        assert isinstance(arr, typing.Mapping)
        if "data" not in arr:
            raise KeyError(
                f"invalid external array, expected key 'data', got keys: '{list(arr.keys())}' and arr: {arr}"
            )
        return arr["data"]
    elif array_mode == "zero_dim":
        assert isinstance(arr, typing.Mapping)
        data = np.array(arr["data"])
        if tuple(arr["shape"]) != tuple(data.shape):  # type: ignore
            raise ValueError(f"invalid shape: {arr}")
        return data
    else:
        raise ValueError(f"invalid array_mode: {array_mode}")
