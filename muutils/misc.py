import typing

def sanitize_fname(fname: str) -> str:
	"""sanitize a filename for use in a path"""
	fname_sanitized: str = ''
	for char in fname:
		if char.isalnum():
			fname_sanitized += char
		elif char in ("-", "_", "."):
			fname_sanitized += char
		else:
			fname_sanitized += ""

	return fname_sanitized


def freeze(obj: typing.Any) -> typing.Any:

	def new_setattr(self, name, value):
		raise AttributeError(f"{self.__class__.__name__} is frozen")
	
	obj.__setattr__ = new_setattr

	return obj 