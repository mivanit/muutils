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
from muutils.zanj.externals import ExternalItemType, ExternalItem, EXTERNAL_ITEMS_EXTENSIONS

def jsonl_metadata(data: list[JSONitem]) -> dict:
	"""metadata about a jsonl object"""
	return {
		"data[0]": data[0],
		"len(data)": len(data),
	}


def store_ndarray(self, fp: IO[bytes], data: NDArray) -> None:
	"""store numpy array to given file as .npy"""
	np.lib.format.write_array(
		fp = fp, 
		array = np.asanyarray(data),
		allow_pickle=False,
	)

def store_jsonl(self, fp: IO[bytes], data: Sequence[JSONitem]) -> None:
	"""store sequence to given file as .jsonl"""

	for item in data:
		fp.write(json.dumps(item).encode("utf-8"))
		fp.write("\n".encode("utf-8"))

EXTERNAL_STORE_FUNCS: dict[ExternalItemType, Callable[[IO[bytes], Any], None]] = {
	"ndarray": store_ndarray,
	"jsonl": store_jsonl,
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
	archive_path: str = f"{joined_path}.{EXTERNAL_ITEMS_EXTENSIONS[item_type]}"

	if archive_path in jser._externals:
		raise ValueError(f"external path {archive_path} already exists!")
	if any([p.startswith(joined_path) for p in jser._externals.keys()]):
		raise ValueError(f"external path {joined_path} is a prefix of another path!")

	# process the data if needed, assemble metadata
	data_new: Any = data
	output: dict = {
		"__format__": f"external:{EXTERNAL_ITEMS_EXTENSIONS[item_type]}",
		"$ref": archive_path,
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
	jser._externals[archive_path] = ExternalItem(
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




DEFAULT_SERIALIZER_HANDLERS_ZANJ: MonoTuple[SerializerHandler] = (
	(
		SerializerHandler(
			check = lambda self, obj, path: (
				isinstance(obj, np.ndarray) 
				and obj.size >= self.external_array_threshold
			),
			serialize_func = lambda self, obj, path: zanj_external_serialize(self, obj, path, item_type="ndarray"),
			desc = "external:ndarray",
		),
		SerializerHandler(
			check = lambda self, obj, path: (
				str(type(obj)) == "<class 'torch.Tensor'>" 
				and int(obj.nelement()) >= self.external_array_threshold
			),
			serialize_func = lambda self, obj, path: zanj_external_serialize(self, obj, path, item_type="ndarray"),
			desc = "external:ndarray:torchtensor",
		),
		SerializerHandler(
			check = lambda self, obj, path: isinstance(obj, (list, tuple, pd.DataFrame)) and len(obj) >= self.external_table_threshold,
			serialize_func = lambda self, obj, path: zanj_external_serialize(self, obj, path, item_type="jsonl"),
			desc = "external:jsonl",
		),
		SerializerHandler(
			check = lambda self, obj, path: "<class 'torch.nn.modules.module.Module'>" in [str(t) for t in obj.__class__.__mro__],
			serialize_func = lambda self, obj, path: zanj_serialize_torchmodule(self, obj, path),
			desc = "torch.nn.Module",
		),
	)
	+ DEFAULT_HANDLERS
)