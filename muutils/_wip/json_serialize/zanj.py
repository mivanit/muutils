"""
an HDF5/exdir file alternative, which uses json for attributes, allows serialization of arbitrary data

for large arrays, the output is a .tar.gz file with most data in a json file, but with sufficiently large arrays stored in binary .npy files
"""

import functools
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union, Callable, Literal, Iterable
import tarfile


from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, ArrayMode, ErrorMode, isinstance_namedtuple, try_catch, _recursive_hashify
from muutils._wip.json_serialize.array import serialize_array
from muutils._wip.json_serialize.json_serialize import json_serialize, SerializerHandler, DEFAULT_HANDLERS
from muutils.tensor_utils import NDArray


def _external_array_serialize(self: "ZANJ", arr: NDArray) -> JSONitem:
	"""_summary_
	
	_extended_summary_
	
	# Parameters:
	 - `self : ZANJ`   
	   _description_
	 - `arr : NDArray`   
	   _description_
	
	# Returns:
	 - `JSONitem` 
	   json data with reference

	# Modifies:
	 - stores a file in the ZANJ archive
	"""	


class ZANJ():
	"""Zip up: Arrays in Numpy, JSON for everything else
	
	given an arbitrary object, zip it up into a tar.gz file, with arrays stored in .npy files, and everything else stored in a json file

	- numpy (or pytorch) arrays are stored in paths according to their name and structure in the object
	- everything else about the object is stored in a json file `zanj.json` in the root of the archive, via `muutils.json_serialize.JsonSerializer`
	- metadata about ZANJ configuration, and optionally packages and versions, is stored in a `__zanj_meta__.json` file in the root of the archive	
	
	create a ZANJ-class via `z_cls = ZANJ().create(obj)`, and save/read instances of the object via `z_cls.save(obj, path)`, `z_cls.load(path)`. be sure to pass an **instance** of the object, to make sure that the attributes of the class can be correctly recognized
	
	"""

	def __init__(
		self,
		error_mode: ErrorMode = "except",
		array_threshold: int = 256,
		handlers_pre: MonoTuple[SerializerHandler] = tuple(),
		handlers_default: MonoTuple[SerializerHandler] = DEFAULT_HANDLERS,	
	) -> None:

		self.error_mode: ErrorMode = error_mode
		self.array_threshold: int = array_threshold
		self.handlers_pre: MonoTuple[SerializerHandler] = handlers_pre
		self.handlers_default: MonoTuple[SerializerHandler] = handlers_default

	
	def create(self, cls: type) -> type:
		"""create a ZANJ class for a given class"""

		# create a new class
		class ZANJ_cls(cls):
			f"""a ZANJ class for {cls.__name__}"""

			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)

			def save(self, path: Union[str, Path]):
				"""save the object to a ZANJ archive"""
				raise NotImplementedError()

			def read(path: Union[str, Path]):
				"""load the object from a ZANJ archive"""
				raise NotImplementedError()

		ZANJ_cls.__name__ = f"ZANJ_{cls.__name__}"



def serialize_array_external(jser: JsonSerializer, arr: NDArray, path: Path) -> JSONitem:
	"""serialize an array to an external file, return a reference to the file"""
	path.parent.mkdir(parents=True, exist_ok=True)
	np.save(path, arr)
	return {
		"__format__": "external",
		"$ref": jser.get_relative_path(path),
	}
		for `external`, the output will look like
	```
	{
		"__format__": "external",
		"shape": arr.shape, # optional
		"dtype": str(arr.dtype), # optional
		"$ref": <path to npy file>
	}
	```



	