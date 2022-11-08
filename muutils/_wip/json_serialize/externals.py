"""for storing/retrieving an item externally in a ZANJ archive"""

import json
import typing
from typing import Literal, NamedTuple, Sequence, IO, Callable, Any, Iterable

import numpy as np
import pandas as pd

from muutils._wip.json_serialize.util import JSONitem 
from muutils.tensor_utils import NDArray


ExternalItemType = Literal["nparray", "jsonl"]

ExternalItem = NamedTuple(
	"ExternalItem",
	[
		("item_type", ExternalItemType),
		("data", Any),
		("path", list[str|int])
	],
)

EXTERNAL_ITEMS_EXTENSIONS: dict[ExternalItemType, str] = {
	"nparray": "npy",
	"jsonl": "jsonl",
}


def store_nparray(self, fp: IO[bytes], data: NDArray) -> None:
	np.lib.format.write_array(
		fp = fp, 
		array = np.asanyarray(data),
		allow_pickle=False,
	)

def store_jsonl(self, fp: IO[bytes], data: Sequence[JSONitem]) -> None:

	if isinstance(data, pd.DataFrame):
		data_new = data.to_dict(orient="records")
	else:
		data_new = data

	for item in data_new:
		fp.write(json.dumps(item).encode("utf-8"))
		fp.write("\n".encode("utf-8"))

EXTERNAL_STORE_FUNCS: dict[ExternalItemType, Callable[[IO[bytes], Any], None]] = {
	"nparray": store_nparray,
	"jsonl": store_jsonl,
}


def load_nparray(self, fp: IO[bytes]) -> NDArray:
	return np.load(fp)

def load_jsonl(self, fp: IO[bytes]) -> Iterable[JSONitem]:
	for line in fp:
		yield json.loads(line)

EXTERNAL_LOAD_FUNCS: dict[ExternalItemType, Callable[[IO[bytes]], Any]] = {
	"nparray": load_nparray,
	"jsonl": load_jsonl,
}


