"""for storing/retrieving an item externally in a ZANJ archive"""

import json
from typing import IO, Any, Callable, Literal, NamedTuple, get_args

import numpy as np

from muutils.json_serialize.util import JSONitem
from muutils.json_serialize.json_serialize import JsonSerializer
from muutils.tensor_utils import NDArray

# this is to make type checking work -- it will later be overridden
_ZANJ_pre = Any

ZANJ_MAIN: str = "__zanj__.json"
ZANJ_META: str = "__zanj_meta__.json"

ExternalItemType = Literal["ndarray", "jsonl"]

ExternalItemType_vals = get_args(ExternalItemType)

ExternalItem = NamedTuple(
    "ExternalItem",
    [
        ("item_type", ExternalItemType),
        ("data", Any),
        ("path", list[str | int]),  # object path
    ],
)

EXTERNAL_ITEMS_EXTENSIONS: dict[ExternalItemType, str] = {
    "ndarray": "npy",
    "jsonl": "jsonl",
}

EXTERNAL_ITEMS_EXTENSIONS_INV: dict[str, ExternalItemType] = {
    ext: item_type for item_type, ext in EXTERNAL_ITEMS_EXTENSIONS.items()
}


def load_ndarray(zanj: "LoadedZANJ", fp: IO[bytes]) -> NDArray:
    return np.load(fp)


def load_jsonl(zanj: "LoadedZANJ", fp: IO[bytes]) -> list[JSONitem]:
    return [json.loads(line) for line in fp]


EXTERNAL_LOAD_FUNCS: dict[ExternalItemType, Callable[[_ZANJ_pre, IO[bytes]], Any]] = {
    "ndarray": load_ndarray,
    "jsonl": load_jsonl,
}


def GET_EXTERNAL_LOAD_FUNC(item_type: str) -> Callable[[_ZANJ_pre, IO[bytes]], Any]:
    if item_type not in EXTERNAL_LOAD_FUNCS:
        raise ValueError(f"unknown external item type: {item_type}")
    return EXTERNAL_LOAD_FUNCS[item_type]