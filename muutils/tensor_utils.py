import json
import typing
import torch

# pylint: disable=protected-access

class ATensor(torch.Tensor):
    """tensor type with annotation for shape and dim names"""

    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        raise TypeError("Type ATensor cannot be instantiated.")

    def __init_subclass__(cls, *args, **kwargs):
        raise TypeError(f"Cannot subclass {cls.__module__}.Annotated")

    @typing._tp_cache
    def __class_getitem__(cls, params):
        if len(params) == 0:
            return torch.Tensor
        else:
            return typing._AnnotatedAlias(torch.Tensor, params)


def lpad_tensor(tensor: torch.Tensor, padded_length: int, pad_value: float = 0.0) -> torch.Tensor:
	"""pad a 1-d tensor on the left with pad_value to length `padded_length`"""
	return torch.cat([
		torch.full((padded_length - tensor.shape[0],), pad_value, dtype=tensor.dtype, device=tensor.device),
		tensor,
	])

def rpad_tensor(tensor: torch.Tensor, pad_length: int, pad_value: float = 0.0) -> torch.Tensor:
	"""pad a 1-d tensor on the right with pad_value to length `pad_length`"""
	return torch.cat([
		tensor,
		torch.full((pad_length - tensor.shape[0],), pad_value, dtype=tensor.dtype, device=tensor.device),
	])


