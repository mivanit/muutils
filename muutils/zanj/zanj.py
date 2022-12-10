"""
an HDF5/exdir file alternative, which uses json for attributes, allows serialization of arbitrary data

for large arrays, the output is a .tar.gz file with most data in a json file, but with sufficiently large arrays stored in binary .npy files


"ZANJ" is an acronym that the AI tool [Elicit](https://elicit.org) came up with for me. not to be confused with:

- https://en.wikipedia.org/wiki/Zanj
- https://www.plutojournals.com/zanj/

"""

import os
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

from muutils.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, ErrorMode, isinstance_namedtuple, try_catch, _recursive_hashify, string_as_lines
from muutils.json_serialize.array import serialize_array, ArrayMode, arr_metadata
from muutils.json_serialize.json_serialize import JsonSerializer, json_serialize, SerializerHandler, DEFAULT_HANDLERS, ObjectPath
from muutils.tensor_utils import NDArray
from muutils.sysinfo import SysInfo
from muutils.zanj.externals import ExternalItemType, ExternalItem, EXTERNAL_ITEMS_EXTENSIONS, ZANJ_MAIN, ZANJ_META
from muutils.zanj.serializing import EXTERNAL_STORE_FUNCS, DEFAULT_SERIALIZER_HANDLERS_ZANJ
from muutils.zanj.loading import EXTERNAL_LOAD_FUNCS, LoaderHandler, ZANJLoaderHandler, DEFAULT_LOADER_HANDLERS, DEFAULT_LOADER_HANDLERS_ZANJ, ZANJLoaderTreeNode, LazyExternalLoader, LoadedZANJ, ExternalsLoadingMode

# pylint: disable=protected-access

ZANJitem = Union[
	JSONitem,
	NDArray,
	pd.DataFrame,
]

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

		# make directory
		os.makedirs(os.path.dirname(file_path), exist_ok=True)

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
			# why force zip64? numpy.savez does it
			with zipf.open(key, 'w', force_zip64=True) as fp:
				EXTERNAL_STORE_FUNCS[ext_type](self, fp, ext_data)

		zipf.close()

		# clear the externals, again
		self._externals: dict[str, Any] = dict()

		return file_path

	def read(
			self, 
			path: Union[str, Path], 
			externals_mode: ExternalsLoadingMode = "lazy",
			loader_handlers: MonoTuple[ZANJLoaderHandler] = DEFAULT_LOADER_HANDLERS_ZANJ,
		) -> LoadedZANJ:
		"""load the object from a ZANJ archive"""
		return LoadedZANJ(
			path = path,
			zanj = self,
			externals_mode = externals_mode,
			loader_handlers = loader_handlers,
		)
		