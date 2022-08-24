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

DTYPE_MAP: dict[str, torch.dtype] = {
    str(x) : x
    for x in [
        torch.float, torch.float32, torch.float64, torch.half, torch.bfloat16, 
        torch.complex64, torch.complex128,
        torch.int, torch.int8, torch.int16, torch.int32, torch.int64, torch.long, torch.short,
        torch.uint8, torch.bool,
    ]
}


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



def split_sequences(
		sequences: typing.Iterator[ATensor["token"]],
		min_length: int = 1,
		max_length: int|None = None,
        lpad_to: int|None = None,
	) -> typing.Iterator[ATensor["token"]]:
    """split a list of sequences into a list of sequences with length in [min_length, max_length]
    
    mostly for feeding data into transformers"""

    if max_length is None:
        max_length = max(len(seq) for seq in sequences)

    for seq in sequences:
        for i in range(len(seq)):
            if i < min_length:
                continue
            
            start_idx: int = max(0, i - max_length)
            
            if lpad_to is None:
                yield seq[start_idx:i+1]
            else:
                yield torch.cat([
                    torch.full((padded_length - tensor.shape[0],), pad_value, dtype=tensor.dtype, device=tensor.device),
                    tensor,
                ])
