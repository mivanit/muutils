"""
an HDF5/exdir file alternative, which uses json for attributes, allows serialization of arbitrary data

for large arrays, the output is a .tar.gz file with most data in a json file, but with sufficiently large arrays stored in binary .npy files


"ZANJ" is an acronym that the AI tool [Elicit](https://elicit.org) came up with for me. not to be confused with:

- https://en.wikipedia.org/wiki/Zanj
- https://www.plutojournals.com/zanj/

"""

from dataclasses import dataclass
import functools
import json
from pathlib import Path
import typing
from typing import IO, Any, Dict, List, NamedTuple, Optional, Sequence, Tuple, Type, Union, Callable, Literal, Iterable
import zipfile

import numpy as np
import pandas as pd

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, ErrorMode, isinstance_namedtuple, try_catch, _recursive_hashify
from muutils._wip.json_serialize.array import serialize_array, ArrayMode
from muutils._wip.json_serialize.json_serialize import JsonSerializer, json_serialize, SerializerHandler, DEFAULT_HANDLERS, ObjectPath
from muutils._wip.json_serialize.externals import ExternalItemType, ExternalItem, EXTERNAL_ITEMS_EXTENSIONS, EXTERNAL_STORE_FUNCS, EXTERNAL_LOAD_FUNCS
from muutils.tensor_utils import NDArray
from muutils.sysinfo import SysInfo

# pylint: disable=protected-access

def zanj_external_serialize(
		jser: "ZANJ", 
		arr: NDArray, 
		path: MonoTuple[str|int],
		item_type: ExternalItemType,
	) -> JSONitem:
	"""stores a numpy array externally in a ZANJ object
	
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
	
	jser._externals[joined_path] = ExternalItem(
		item_type=item_type,
		data=arr,
		path=path,
	)

	return {
		"__format__": f"external:{EXTERNAL_ITEMS_EXTENSIONS[item_type]}",
		"$ref": joined_path,
	}

ZANJ_MAIN: str = "zanj.json"
ZANJ_META: str = "__zanj_meta__.json"


DEFAULT_SERIALIZER_HANDLERS_ZANJ: MonoTuple[SerializerHandler] = (
	(
		SerializerHandler(
			check = lambda self, obj, path: isinstance(obj, np.ndarray) and obj.size >= self.array_threshold,
			serialize = lambda self, obj, path: zanj_external_serialize(self, obj, path, "nparray"),
			desc = "external.nparray",
		),
		SerializerHandler(
			check = lambda self, obj, path: isinstance(obj, (list, tuple, pd.DataFrame)) and len(obj) >= self.table_threshold,
			serialize = lambda self, obj, path: zanj_external_serialize(self, obj, path, "jsonl"),
			desc = "external.jsonl",
		),
	)
	+ DEFAULT_HANDLERS
)




@dataclass
class LoaderHandler:
	"""handler for loading an object from a json file"""
	# (json_data, path) -> whether to use this handler
	check: Callable[[JSONitem, ObjectPath], bool]
	# function to load the object
	load: Callable[[JSONitem, ObjectPath], Any]
	# description of the handler
	desc: str = "(no description)"

@dataclass
class ZANJLoaderHandler:
	"""handler for loading an object from a ZANJ archive (takes ZANJ object as first arg)"""
	# (zanj_obi, json_data, path) -> whether to use this handler
	check: Callable[["ZANJ", JSONitem, ObjectPath], bool]
	# function to load the object (zanj_obj, json_data, path) -> loaded_obj
	load: Callable[["ZANJ", JSONitem, ObjectPath], Any]
	# description of the handler
	desc: str = "(no description)"

	@classmethod
	def from_LoaderHandler(cls, lh: LoaderHandler):
		"""wrap a standard LoaderHandler to make it compatible with ZANJ"""
		return cls(
			check = lambda zanj, json_item, path: lh.check(json_item, path),
			load = lambda zanj, json_item, path: lh.load(json_item, path),
			desc = lh.desc,
		)

DEFAULT_LOADER_HANDLERS: tuple[LoaderHandler] = (
	LoaderHandler(
		check = lambda json_item, path: (
			isinstance(json_item, dict)
			and "__format__" in json_item
			and json_item["__format__"] == "array_list_meta"
		),
		load = lambda json_item, path: (
			np.array(json_item["data"], dtype=json_item["dtype"]).reshape(json_item["shape"])
		),
		desc = "array_list_meta loader",
	),
	LoaderHandler(
		check = lambda json_item, path: (
			isinstance(json_item, dict)
			and "__format__" in json_item
			and json_item["__format__"] == "array_hex_meta"
		),
		load = lambda json_item, path: (
			np.frombuffer(bytes.fromhex(json_item["data"]), dtype=json_item["dtype"]).reshape(json_item["shape"])
		),
		desc = "array_hex_meta loader",
	),
)


DEFAULT_LOADER_HANDLERS_ZANJ: tuple[ZANJLoaderHandler] = (
	ZANJLoaderHandler(
		check = lambda zanj, json_item, path: (
			isinstance(json_item, dict)
			and "__format__" in json_item
			and json_item["__format__"].startswith("external:")
		),
		load = lambda zanj, json_item, path: (
			zanj._externals[json_item["key"]]
		)
	),
) + tuple(
	ZANJLoaderHandler.from_LoaderHandler(lh) 
	for lh in DEFAULT_LOADER_HANDLERS
)



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
		table_threshold: int = 256,
		compress: bool|int = True,
		handlers_pre: MonoTuple[SerializerHandler] = tuple(),
		handlers_default: MonoTuple[SerializerHandler] = DEFAULT_HANDLERS,	
	) -> None:
		super().__init__(
			array_mode = "external",
			error_mode = error_mode,
			handlers_pre = handlers_pre,
			handlers_default = handlers_default,
		)

		self.array_threshold: int = array_threshold
		self.table_threshold: int = table_threshold

		# process compression to int if bool given
		self.compress = compress
		if isinstance(compress, bool):
			if compress:
				self.compress = zipfile.ZIP_DEFLATED
			else:
				self.compress = zipfile.ZIP_STORED

		# create the externals, leave it empty
		self._externals: dict[str, ExternalItem] = dict()

	def externals_info(self) -> dict[dict]:
		"""return information about the current externals"""
		output: dict[dict] = dict()

		key: str; item: ExternalItem
		for key, item in self._externals:
			data = item.data
			output[key] = {
				"item_type": item.item_type,
				"type(data)": type(data),
				"len(data)": len(data),
			}

			if item.item_type == "nparray":
				output[key]["data.shape"] = data.shape
				output[key]["data.dtype"] = data.dtype
				output[key]["data.size"] = item.size
			elif item.item_type == "jsonl":
				output[key]["data[0]"] = data[0]
		
		return output

	def meta(self) -> JSONitem:
		"""return the metadata of the ZANJ archive"""

		return dict(
			# configuration of this ZANJ instance
			zanj_cfg = dict(
				error_mode = str(self.error_mode),
				array_threshold = self.array_threshold,
				table_threshold = self.table_threshold,
				compress = self.compress,
				handlers_desc = [str(h.desc) for h in self.handlers],
			),
			# system info (python, pip packages, torch & cuda, platform info, git info)
			sysinfo = SysInfo.get_all(),
			externals_info = self.externals_info(),
		)


	def save(self, file_path: str|Path, obj: Any) -> str:
		"""save the object to a ZANJ archive. returns the path to the archive"""

		# make a path
		file_path: str = f"{file_path}.zanj"

		# clear the externals!
		self._externals = dict()

		# serialize the object -- this will populate self._externals
		json_data: JSONitem = self.json_serialize(obj, path=tuple())

		# open the zip file
		zipf: zipfile.ZipFile = zipfile.ZipFile(file=file_path, mode="w", compression=self.compress)

		# store json data
		with zipf.open(ZANJ_MAIN, "wt") as fp:
			json.dump(json_data, fp, indent="\t")
		
		# store zanj metadata
		with zipf.open(ZANJ_META, "wt") as fp:
			json.dump(self.meta(), fp, indent="\t")

		# store externals
		for key, (ext_type, ext_data) in self._externals.items():
			fname: str = f"{key}.{EXTERNAL_ITEMS_EXTENSIONS[ext_type]}"
			# why force zip64? numpy.savez does it
			with zipf.open(fname, 'wb', force_zip64=True) as fp:
				EXTERNAL_STORE_FUNCS[ext_type](fp, ext_data)

		zipf.close()

		# clear the externals, again
		self._externals: dict[str, Any] = dict()

		return file_path

	def read(self, path: Union[str, Path], mmap_mode: str|None = None):
		"""load the object from a ZANJ archive"""
		raise NotImplementedError()



@dataclass
class ZANJLoaderTreeNode:
	"""acts like a regular dictionary or list, but applies loaders to items
	
	does this by passing `_parent` down the stack, whenever you get an item from the container.
	"""
	_parent: "LoadedZANJ"
	_data: dict[str, JSONitem]|list[JSONitem]

	def __getitem__(self, key: str|int) -> Any:
		# get value, check key types
		val: JSONitem
		if (
				(isinstance(self._data, list) and isinstance(key, int))
				and (isinstance(self._data, dict) and isinstance(key, str))
			):
			val = self._data[key]
		else:
			raise KeyError(f"invalid key type {type(key) = }, {key = } for {self._data = } with {type(self._data) = }")

		# get value or dereference
		if key == "$ref":
			val = self._parent._externals[val]
		else:
			val = self._data[key]

		if isinstance(val, (dict,list)):
			return ZANJLoaderTreeNode(_parent=self._parent, _data=val)
		else:
			return val

class LazyExternalLoader:
	"""lazy load np arrays or jsonl files, similar tp NpzFile from np.lib
	
	initialize with zipfile object and zanj metadata (for list of externals)
	"""

	def __init__(
			self,
			zipf: zipfile.ZipFile,
			zanj_meta: JSONitem,
		):
		self._zipf: zipfile.ZipFile = zipf
		self._zanj_meta: JSONitem = zanj_meta
		# (path, item_type) pairs
		self._externals_types: dict[str, str] = {
			key : val.item_type
			for key, val in zanj_meta["externals_info"].items()
		}

		# validate by checking each external file exists
		for key, item_type in self._externals_types.items():
			fname: str = f"{key}.{EXTERNAL_ITEMS_EXTENSIONS[item_type]}"
			if fname not in zipf.namelist():
				raise ValueError(f"external file {fname} not found in archive")


	def __getitem__(self, key: str) -> Any:
		if key in self._externals_types:
			path, item_type = key
			with self._zipf.open(path, "rb") as fp:
				return EXTERNAL_LOAD_FUNCS[item_type](fp)



class LoadedZANJ:
	"""object loaded from ZANJ archive. acts like a dict."""
	def __init__(
		self,
		# config
		path: str|Path,
		zanj: ZANJ,
		mmap_mode: str|None,
		loader_handlers: MonoTuple[ZANJLoaderHandler],
	) -> None:

		self._path: str = str(path)
		self._zanj: ZANJ = zanj
		self._zipf: zipfile.ZipFile = zipfile.ZipFile(file=self._path, mode="r")
		self._mmap_mode: str|None = mmap_mode

		self._meta: JSONitem = json.load(self._zipf.open(ZANJ_META, "rt"))

		self._json_data: ZANJLoaderTreeNode = ZANJLoaderTreeNode(
			_parent = self,
			_data = json.load(self._zipf.open(ZANJ_MAIN, "rt"))
		)
		self._externals: np.lib.format.NpzFile = np.lib.format.NpzFile(

		)
		
	
	def __getitem__(self, key: str) -> Any:
		"""get the value of the given key"""



