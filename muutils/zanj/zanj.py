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
import inspect

import numpy as np
import pandas as pd

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, ErrorMode, isinstance_namedtuple, try_catch, _recursive_hashify, string_as_lines
from muutils._wip.json_serialize.array import serialize_array, ArrayMode, arr_metadata
from muutils._wip.json_serialize.json_serialize import JsonSerializer, json_serialize, SerializerHandler, DEFAULT_HANDLERS, ObjectPath
from muutils._wip.json_serialize.externals import ExternalItemType, ExternalItem, EXTERNAL_ITEMS_EXTENSIONS, EXTERNAL_STORE_FUNCS, EXTERNAL_LOAD_FUNCS
from muutils.tensor_utils import NDArray
from muutils.sysinfo import SysInfo

# pylint: disable=protected-access

ZANJitem = Union[
	JSONitem,
	NDArray,
	pd.DataFrame,
]

ExternalsLoadingMode = Literal["lazy", "full"]



def jsonl_metadata(data: list[JSONitem]) -> dict:
	return {
		"data[0]": data[0],
		"len(data)": len(data),
	}


def zanj_external_serialize(
		jser: "ZANJ", 
		data: Any, 
		path: ObjectPath,
		item_type: ExternalItemType,
	) -> JSONitem:
	"""stores a numpy array or jsonl externally in a ZANJ object
	
	# Parameters:
	 - `jser : ZANJ`
	 - `arr : NDArray`
	
	# Returns:
	 - `JSONitem` 
	   json data with reference

	# Modifies:
	 - modifies `jser._externals`
	"""	
	# get the path, make sure its unique
	joined_path: str = "/".join([str(p) for p in path])
	if joined_path in jser._externals:
		raise ValueError(f"external path {joined_path} already exists!")

	# process the data if needed, assemble metadata
	data_new: Any = data
	output: dict = {
		"__format__": f"external:{EXTERNAL_ITEMS_EXTENSIONS[item_type]}",
		"$ref": joined_path,
	}
	if item_type == "ndarray":
		# check type
		data_type_str: str = str(type(data))
		if data_type_str == "<class 'torch.Tensor'>":
			# detach and convert
			data_new = data.detach().cpu().numpy()		
		elif data_type_str == "<class 'numpy.ndarray'>":
			pass
		else:
			# if not a numpy array, except
			raise TypeError(f"expected numpy.ndarray, got {data_type_str}")
		# get metadata
		output.update(arr_metadata(data))
	elif item_type.startswith("jsonl"):
		if isinstance(data, pd.DataFrame):
			output["columns"] = data.columns.tolist()
			data_new = data.to_dict(orient="records")
		elif isinstance(data, (list, tuple, Iterable)):
			data_new = [
				jser.json_serialize(item, path + (i,))
				for i, item in enumerate(data)
			]
		else:
			raise TypeError(f"expected list or pd.DataFrame, got {type(data)}")
			
		output.update(jsonl_metadata(data_new))
			
	# store the item for external serialization
	jser._externals[joined_path] = ExternalItem(
		item_type=item_type,
		data=data_new,
		path=path,
	)

	return output

def zanj_serialize_torchmodule(
		jser: "ZANJ",
		data: "torch.nn.Module",
		path: ObjectPath,
	) -> JSONitem:
	"""serialize a torch module to zanj
	
	we want to save:
	- class name, docstring, __mro__
	- code of `.forward()` method
	- code of `.__init__()` method
	- state dict, in accordance with zanj parameters for storing arrays
	- `_modules` with modules as strings
	- __dict__ with values printed (not fully serialized)
	"""

	output: dict = {
		"__format__" : "torchmodule",
		"__class__" : str(data.__class__.__name__),
		"__doc__" : string_as_lines(data.__doc__),
		"__mro__" : [str(c.__name__) for c in data.__class__.__mro__],
		"__init__" : string_as_lines(inspect.getsource(data.__init__)),
		"forward" : string_as_lines(inspect.getsource(data.forward)),
		"state_dict" : jser.json_serialize(data.state_dict(), path + ("state_dict",)),
		"_modules" : {k: str(v) for k, v in data._modules.items()},
		"__dict__" : {k: str(v) for k, v in data.__dict__.items()},
	}

	return jser.json_serialize(output)


ZANJ_MAIN: str = "__zanj__.json"
ZANJ_META: str = "__zanj_meta__.json"


DEFAULT_SERIALIZER_HANDLERS_ZANJ: MonoTuple[SerializerHandler] = (
	(
		SerializerHandler(
			check = lambda self, obj, path: (
				isinstance(obj, np.ndarray) 
				and obj.size >= self.external_array_threshold
			),
			serialize = lambda self, obj, path: zanj_external_serialize(self, obj, path, item_type="ndarray"),
			desc = "external:ndarray",
		),
		SerializerHandler(
			check = lambda self, obj, path: (
				str(type(obj)) == "<class 'torch.Tensor'>" 
				and int(obj.nelement()) >= self.external_array_threshold
			),
			serialize = lambda self, obj, path: zanj_external_serialize(self, obj, path, item_type="ndarray"),
			desc = "external:ndarray:torchtensor",
		),
		SerializerHandler(
			check = lambda self, obj, path: isinstance(obj, (list, tuple, pd.DataFrame)) and len(obj) >= self.external_table_threshold,
			serialize = lambda self, obj, path: zanj_external_serialize(self, obj, path, item_type="jsonl"),
			desc = "external:jsonl",
		),
		SerializerHandler(
			check = lambda self, obj, path: "<class 'torch.nn.modules.module.Module'>" in [str(t) for t in obj.__class__.__mro__],
			serialize = lambda self, obj, path: zanj_serialize_torchmodule(self, obj, path),
			desc = "torch.nn.Module",
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
	# TODO: add name/unique identifier, `desc` should be human-readable and more detailed
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
		internal_array_mode: ArrayMode = "array_list_meta",
		external_array_threshold: int = 64,
		external_table_threshold: int = 64,
		compress: bool|int = True,
		handlers_pre: MonoTuple[SerializerHandler] = tuple(),
		handlers_default: MonoTuple[SerializerHandler] = DEFAULT_SERIALIZER_HANDLERS_ZANJ,	
	) -> None:
		super().__init__(
			array_mode = internal_array_mode,		
			error_mode = error_mode,
			handlers_pre = handlers_pre,
			handlers_default = handlers_default,
		)

		self.external_array_threshold: int = external_array_threshold
		self.external_table_threshold: int = external_table_threshold

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
		for key, item in self._externals.items():
			data = item.data
			output[key] = {
				"item_type": item.item_type,
				"path": item.path,
				"type(data)": str(type(data)),
				"len(data)": len(data),
			}

			if item.item_type == "ndarray":
				output[key].update(arr_metadata(data))
			elif item.item_type.startswith("jsonl"):
				output[key]["data[0]"] = data[0]
		
		return output

	def meta(self) -> JSONitem:
		"""return the metadata of the ZANJ archive"""

		return json_serialize(dict(
			# configuration of this ZANJ instance
			zanj_cfg = dict(
				error_mode = str(self.error_mode),
				array_mode = str(self.array_mode),
				external_array_threshold = self.external_array_threshold,
				external_table_threshold = self.external_table_threshold,
				compress = self.compress,
				handlers_desc = [str(h.desc) for h in self.handlers],
			),
			# system info (python, pip packages, torch & cuda, platform info, git info)
			sysinfo = SysInfo.get_all(include=("python", "pytorch")),
			externals_info = self.externals_info(),
		))


	def save(self, obj: Any, file_path: str|Path) -> str:
		"""save the object to a ZANJ archive. returns the path to the archive"""

		# adjust extension
		file_path = str(file_path)
		if not file_path.endswith(".zanj"):
			file_path += ".zanj"

		# clear the externals!
		self._externals = dict()

		# serialize the object -- this will populate self._externals
		json_data: JSONitem = self.json_serialize(obj)

		# open the zip file
		zipf: zipfile.ZipFile = zipfile.ZipFile(file=file_path, mode="w", compression=self.compress)

		# store base json data and metadata
		zipf.writestr(ZANJ_MAIN, json.dumps(json_data, indent="\t"))
		zipf.writestr(ZANJ_META, json.dumps(self.meta(), indent="\t"))

		# store externals
		for key, (ext_type, ext_data, ext_path) in self._externals.items():
			fname: str = f"{key}.{EXTERNAL_ITEMS_EXTENSIONS[ext_type]}"
			# why force zip64? numpy.savez does it
			with zipf.open(fname, 'w', force_zip64=True) as fp:
				EXTERNAL_STORE_FUNCS[ext_type](self, fp, ext_data)

		zipf.close()

		# clear the externals, again
		self._externals: dict[str, Any] = dict()

		return file_path

	def read(self, path: Union[str, Path], externals_mode: ExternalsLoadingMode = "lazy") -> Any:
		"""load the object from a ZANJ archive"""
		



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
				or (isinstance(self._data, dict) and isinstance(key, str))
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
		loader_handlers: MonoTuple[ZANJLoaderHandler],
		externals_mode: ExternalsLoadingMode = "lazy",
	) -> None:

		self._path: str = str(path)
		self._zanj: ZANJ = zanj
		self._externals_mode: ExternalsLoadingMode = externals_mode

		self._zipf: zipfile.ZipFile = zipfile.ZipFile(file=self._path, mode="r")

		self._meta: JSONitem = json.load(self._zipf.open(ZANJ_META, "rt"))
		self._json_data: ZANJLoaderTreeNode = ZANJLoaderTreeNode(
			_parent = self,
			_data = json.load(self._zipf.open(ZANJ_MAIN, "rt"))
		)

		self._externals: LazyExternalLoader|dict
		if externals_mode == "lazy":
			self._externals = LazyExternalLoader(
				zipf=self._zipf,
				zanj_meta=self._meta,
			)
		elif externals_mode == "full":
			self._externals = {
				key : self._load_external(key, val)
				for key, val in self._meta["externals_info"].items()
			}

		
	
	def __getitem__(self, key: str) -> Any:
		"""get the value of the given key"""



