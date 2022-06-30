import functools
import pdb
from typing import *
from dataclasses import is_dataclass, asdict
from collections import namedtuple
import inspect


def isinstance_namedtuple(x):
	"""checks if `x` is a `namedtuple`

	credit to https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
	"""
	t = type(x)
	b = t.__bases__
	if len(b) != 1 or b[0] != tuple:
		return False
	f = getattr(t, "_fields", None)
	if not isinstance(f, tuple):
		return False
	return all(type(n) == str for n in f)


def try_catch(func: Callable):

	@functools.wraps(func)
	def newfunc(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			return f'{e.__class__.__name__}: {e}'
	
	return newfunc

SERIALIZER_SPECIAL_KEYS: List[str] = [
	"__name__",
	"__doc__",
	"__module__",
	"__class__",
	"__dict__",
	"__annotations__",
]

SERIALIZER_SPECIAL_FUNCS: Dict[str, Callable] = {
	"str": str,
	"type": try_catch(lambda x: type(x).__name__),
	"repr": try_catch(lambda x: repr(x)),
	"code": try_catch(lambda x: inspect.getsource(x)),
	"sourcefile": try_catch(lambda x: inspect.getsourcefile(x)),
}


def json_serialize(
	obj: Any,
	depth: int = -1,
	do_numpy: bool = True,
	do_torch: bool = True,
	except_mode: Literal["ignore", "warn", "except"] = "except",
) -> Any:

	newdepth: int = depth - 1
	try:
		# check for special `serialize` method
		if hasattr(obj, "serialize"):
			# print(f'\n### using custom serialize: {str(obj) = }\n')
			return json_serialize(obj.serialize())

		# if `None`, return `None`
		if obj is None:
			return None

		# if primitive type, just add it
		if isinstance(obj, (bool, int, float, str)):
			return obj

		# if max depth is reached, return the object as a string and dont recurse
		if depth == 0:
			return str(obj)

		if isinstance(obj, dict):
			# print(f'\n### reading obj as dict: {str(obj)}')
			# if dict, recurse
			out_dict: Dict[str, Any] = dict()
			for k, v in obj.items():
				out_dict[str(k)] = json_serialize(v, newdepth)
			return out_dict

		elif isinstance_namedtuple(obj):
			# if namedtuple, treat as dict
			return json_serialize(dict(obj._asdict()), newdepth)

		elif is_dataclass(obj):
			# if dataclass, treat as dict
			# print(f'\n### reading obj as dataclass: {str(obj)}')
			return {k: json_serialize(getattr(obj, k)) for k in obj.__dataclass_fields__}

		elif isinstance(obj, (set, list, tuple)) or isinstance(obj, Iterable):
			# if iterable, recurse
			# print(f'\n### reading obj as iterable: {str(obj)}')
			return [json_serialize(x, newdepth) for x in obj]
		else:
			# check for numpy and torch
			if do_numpy:
				try:
					import numpy as np

					if isinstance(obj, np.ndarray):
						return obj.tolist()
				except ImportError:
					pass
			if do_torch:
				try:
					import torch

					if isinstance(obj, torch.Tensor):
						return obj.detach().cpu().numpy().tolist()
				except ImportError:
					pass

			# if not basic type, serialize it however we can
			return {
				**{k: str(getattr(obj, k, None)) for k in SERIALIZER_SPECIAL_KEYS},
				**{k: str(f(obj)) for k, f in SERIALIZER_SPECIAL_FUNCS.items()},
			}
	except Exception as e:
		if except_mode == "except":
			raise e
		elif except_mode == "warn":
			print(f"!!! error serializing {obj}: {e}")

		return str(obj)
