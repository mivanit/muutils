"""
an HDF5/exdir file alternative, which uses json for attributes, allows serialization of arbitrary data

for large arrays, the output is a .tar.gz file with most data in a json file, but with sufficiently large arrays stored in binary .npy files
"""

from dataclasses import dataclass
import functools
import json
from pathlib import Path
import typing
from typing import IO, Any, Dict, List, NamedTuple, Optional, Sequence, Tuple, Type, Union, Callable, Literal, Iterable
import zipfile

import numpy as np

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, ArrayMode, ErrorMode, isinstance_namedtuple, try_catch, _recursive_hashify
from muutils._wip.json_serialize.array import serialize_array
from muutils._wip.json_serialize.json_serialize import JsonSerializer, json_serialize, SerializerHandler, DEFAULT_HANDLERS
from muutils.tensor_utils import NDArray


ExternalItemType = Literal["nparray", "jsonl"]

ExternalItem = NamedTuple(
	"ExternalItem",
	[
		("item_type", ExternalItemType),
		("data", Any),
	],
)

@dataclass
class ExternalItem:
	_type: ExternalItemType|None = None

	def store(fp: IO[bytes]) -> None:
		raise NotImplementedError()
	
	def load(fp: IO[bytes]) -> Any:
		raise NotImplementedError()

@dataclass
class ExternalItem_NDArray(ExternalItem):
	_type: Literal["nparray"] = "nparray"

	def store(self, fp: IO[bytes], data: NDArray) -> None:
		np.lib.format.write_array(
			fp = fp,
			array = np.asanyarray(data),
			allow_pickle=False,
		)

	def load(self, fp: IO[bytes]) -> NDArray:
		return np.load(fp)

@dataclass
class ExternalItem_JsonL(ExternalItem):
	_type: Literal["jsonl"] = "jsonl"

	def store(self, fp: IO[bytes], data: Sequence[JSONitem]) -> None:
		for item in data:
			fp.write(json.dumps(item).encode("utf-8"))
			fp.write("\n".encode("utf-8"))

	def load(self, fp: IO[bytes]) -> Iterable[JSONitem]:
		for line in fp:
			yield json.loads(line)


ExternalItemSerializers: dict[str, ExternalItem] = {
	"nparray": ExternalItem_NDArray(),
	"jsonl": ExternalItem_JsonL(),
}


def _external_serialize(
		jser: "ZANJ", 
		arr: NDArray, 
		path: MonoTuple[str|int],
		item_type: ExternalItemType,
	) -> JSONitem:
	"""_summary_
	
	
	
	# Parameters:
	 - `jser : ZANJ`
	 - `arr : NDArray`
	
	# Returns:
	 - `JSONitem` 
	   json data with reference

	# Modifies:
	 - modifies `jser._externals`
	"""	

	joined_path: str = "/".join([str(p) for p in path])

	if joined_path in jser._externals:
		raise ValueError(f"external path {joined_path} already exists!")
	
	jser._externals[joined_path] = ExternalItem(item_type, arr)

	return {
		"__format__": "external.",
		"$ref": joined_path,
	}

class ZANJ(JsonSerializer):
	"""Zip up: Arrays in Numpy, JSON for everything else
	
	given an arbitrary object, throw into a zip file, with arrays stored in .npy files, and everything else stored in a json file

	(basically npz file with augemented json)

	# TODO: large tables in JSONL format

	- numpy (or pytorch) arrays are stored in paths according to their name and structure in the object
	- everything else about the object is stored in a json file `zanj.json` in the root of the archive, via `muutils.json_serialize.JsonSerializer`
	- metadata about ZANJ configuration, and optionally packages and versions, is stored in a `__zanj_meta__.json` file in the root of the archive	
	
	create a ZANJ-class via `z_cls = ZANJ().create(obj)`, and save/read instances of the object via `z_cls.save(obj, path)`, `z_cls.load(path)`. be sure to pass an **instance** of the object, to make sure that the attributes of the class can be correctly recognized
	
	"""

	def __init__(
		self,
		error_mode: ErrorMode = "except",
		array_threshold: int = 256,
		compress: bool|int = True,
		handlers_pre: MonoTuple[SerializerHandler] = tuple(),
		handlers_default: MonoTuple[SerializerHandler] = DEFAULT_HANDLERS,	
	) -> None:

		self.error_mode: ErrorMode = error_mode
		self.array_threshold: int = array_threshold
		self.handlers_pre: MonoTuple[SerializerHandler] = handlers_pre
		self.handlers_default: MonoTuple[SerializerHandler] = handlers_default

		# process compression to int if bool given
		self.compress = compress
		if isinstance(compress, bool):
			if compress:
				self.compress = zipfile.ZIP_DEFLATED
			else:
				self.compress = zipfile.ZIP_STORED


	def save(self, file_path: str|Path, obj: Any) -> None:
		"""save the object to a ZANJ archive"""

		self._externals: dict[str, Any] = dict()

		# serialize the object -- this will populate self._externals
		json_data: JSONitem = self.json_serialize(obj, path=tuple())

		zipf = zipfile.ZipFile(file=file, mode="w", compression=self.compress)

		for key, (ext_type, ext_data) in self._externals.items():
			fname = key + '.npy'
			val = np.asanyarray(val)
			# why force zip64? numpy.savez does it
			with zipf.open(fname, 'w', force_zip64=True) as fid:
				np.lib.format.write_array(
					fp = fid, 
					array = val,
					allow_pickle=False,
				)

		zipf.close()


			raise NotImplementedError()

		def read(path: Union[str, Path]):
			"""load the object from a ZANJ archive"""
			raise NotImplementedError()




	