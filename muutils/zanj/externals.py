"""for storing/retrieving an item externally in a ZANJ archive"""

import json
from typing import IO, Any, Callable, Literal, NamedTuple, get_args

import numpy as np

from muutils.json_serialize.json_serialize import ObjectPath
from muutils.json_serialize.util import JSONitem

# this is to make type checking work -- it will later be overridden
_ZANJ_pre = Any

ZANJ_MAIN: str = "__zanj__.json"
ZANJ_META: str = "__zanj_meta__.json"

ExternalItemType = Literal["jsonl", "npy"]

ExternalItemType_vals = get_args(ExternalItemType)

ExternalItem = NamedTuple(
    "ExternalItem",
    [
        ("item_type", ExternalItemType),
        ("data", Any),
        ("path", ObjectPath),
    ],
)


def load_jsonl(zanj: "LoadedZANJ", fp: IO[bytes]) -> list[JSONitem]:  # type: ignore[name-defined]
    return [json.loads(line) for line in fp]


def load_npy(zanj: "LoadedZANJ", fp: IO[bytes]) -> np.ndarray:  # type: ignore[name-defined]
    return np.load(fp)


EXTERNAL_LOAD_FUNCS: dict[ExternalItemType, Callable[[_ZANJ_pre, IO[bytes]], Any]] = {
    "jsonl": load_jsonl,
    "npy": load_npy,
}


def GET_EXTERNAL_LOAD_FUNC(item_type: str) -> Callable[[_ZANJ_pre, IO[bytes]], Any]:
    if item_type not in EXTERNAL_LOAD_FUNCS:
        raise ValueError(
            f"unknown external item type: {item_type}, needs to be one of {EXTERNAL_LOAD_FUNCS.keys()}"
        )
    # safe to ignore since we just checked
    return EXTERNAL_LOAD_FUNCS[item_type]  # type: ignore[index]
