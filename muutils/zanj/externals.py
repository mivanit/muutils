"""for storing/retrieving an item externally in a ZANJ archive"""

import json
import typing
from typing import Literal, NamedTuple, Sequence, IO, Callable, Any, Iterable

import numpy as np
import pandas as pd

from muutils.json_serialize.util import JSONitem 
from muutils.tensor_utils import NDArray


ExternalItemType = Literal["ndarray", "jsonl"]

ExternalItem = NamedTuple(
	"ExternalItem",
	[
		("item_type", ExternalItemType),
		("data", Any),
		("path", list[str|int])
	],
)

EXTERNAL_ITEMS_EXTENSIONS: dict[ExternalItemType, str] = {
	"ndarray": "npy",
	"jsonl": "jsonl",
}



