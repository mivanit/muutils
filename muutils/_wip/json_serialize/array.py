import functools
import json
from pathlib import Path
from types import GenericAlias
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union, Callable, Literal, Iterable
from dataclasses import dataclass, is_dataclass, asdict
from collections import namedtuple
import inspect
import typing
import warnings

import numpy as np

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, isinstance_namedtuple, try_catch
from muutils.tensor_utils import NDArray


ArrayMode = Literal["list", "array_list_meta", "array_hex_meta", "external"]

def serialize_array(arr: NDArray, array_mode: ArrayMode = "array_list_meta") -> JSONitem:
    """serialize a numpy or pytorch array in one of several modes

    if the object is zero-dimensional, simply get the unique item

    `array_mode: ArrayMode` can be one of:
    - `list`: serialize as a list of values, no metadata (equivalent to `arr.tolist()`)
    - `array_list_meta`: serialize dict with metadata, actual list under the key `data`
    - `array_hex_meta`: serialize dict with metadata, actual hex string under the key `data`
	# - `external`: reference to external file

    for `array_list_meta` and `array_hex_meta`, the output will look like
    ```
    {
        "__format__": <array_list_meta|array_hex_meta>,
        "shape": arr.shape,
        "dtype": str(arr.dtype),
        "data": <arr.tolist()|arr.tobytes().hex()>,
    }
    ```

    # Parameters:
     - `arr : Any` array to serialize
     - `array_mode : ArrayMode` mode in which to serialize the array  
       (defaults to `"array_list_meta"`)  
    
    # Returns:
     - `JSONitem` 
       json serialized array

    # Raises:
     - `KeyError` : if the array mode is not valid
    """    

    if len(arr.shape) == 0:
        return arr.item()
    
    if array_mode == "array_list_meta":
        return {
            "__format__": "array_list_meta",
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "data": arr.tolist(),
        }
    elif array_mode == "list":
        return arr.tolist()
    elif array_mode == "array_hex_meta":
        return {
            "__format__": "array_hex_meta",
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "data": arr.tobytes().hex(),
        }
    else:
        raise KeyError(f"invalid array_mode: {array_mode}")

def infer_array_mode(arr: JSONitem) -> ArrayMode:
    """given a serialized array, infer the mode
    
    assumes the array was serialized via `serialize_array()`
    """
    if isinstance(arr, dict):
        fmt: Optional[str] = arr.get("__format__", None)
        if fmt == "array_list_meta":
            if type(arr["data"]) != list:
                raise ValueError(f"invalid list format: {arr}")
            return fmt
        elif fmt == "array_hex_meta":
            if type(arr["data"]) != str:
                raise ValueError(f"invalid hex format: {arr}")
            return fmt
        elif fmt == "external":
            if ("$ref" not in arr) or (type(arr["$ref"]) != str):
                raise ValueError(f"invalid external format: {arr}")
            return fmt
        else:
            raise ValueError(f"invalid format: {arr}")

    elif isinstance(arr, list):
        return "list"
    else:
        raise ValueError(f"cannot infer array_mode from {arr}")

def load_array(arr: JSONitem, array_mode: Optional[ArrayMode] = None) -> Any:
    """load a json-serialized array, infer the mode if not specified"""
    # try to infer the array_mode
    array_mode_inferred: ArrayMode = infer_array_mode(arr)
    if array_mode is None:
        array_mode = array_mode_inferred
    elif array_mode != array_mode_inferred:
        warnings.warn(f"array_mode {array_mode} does not match inferred array_mode {array_mode_inferred}")        

    # actually load the array
    if array_mode == "array_list_meta":
        data = np.array(arr["data"], dtype=arr["dtype"])
        if tuple(arr["shape"]) != tuple(data.shape):
            raise ValueError(f"invalid shape: {arr}")
        return data
    elif array_mode == "array_hex_meta":
        data = np.frombuffer(bytes.fromhex(arr["data"]), dtype=arr["dtype"])
        return data.reshape(arr["shape"])
    elif array_mode == "list":
        return np.array(arr)
    else:
        raise ValueError(f"invalid array_mode: {array_mode}")
