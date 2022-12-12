import sys
import json
import typing


import numpy as np
import torch

# pylint: disable=protected-access


def annotated_array_factory(
        array_type: typing.Literal[torch.Tensor, np.ndarray],
        name: str = "ATensor",
    ) -> type:

    class BaseTensor(array_type):
        """tensor type with annotation for shape and dim names"""

        __slots__ = ()

        def __new__(cls, *args, **kwargs):
            raise TypeError("Type ATensor cannot be instantiated.")

        def __init_subclass__(cls, *args, **kwargs):
            raise TypeError(f"Cannot subclass {cls.__module__}.Annotated")

        @typing._tp_cache
        def __class_getitem__(cls, params):
            if isinstance(params, type):
                return typing._AnnotatedAlias(array_type, {"type": params})
            elif len(params) == 0:
                return array_type
            else:
                return typing._AnnotatedAlias(array_type, params)

    BaseTensor.__name__ = name

    return BaseTensor

class ATensor(torch.Tensor):
    @typing._tp_cache
    def __class_getitem__(cls, params):
        raise NotImplementedError()

ATensor = annotated_array_factory(torch.Tensor, "ATensor")

class NDArray(np.ndarray):
    @typing._tp_cache
    def __class_getitem__(cls, params):
        raise NotImplementedError()

NDArray = annotated_array_factory(np.ndarray, "NDArray")



DTYPE_LIST: list = [
    *[
        bool, int, float,
    ],
    *[
        # ----------
        # pytorch
        # ----------
        # floats
        torch.float, torch.float32, torch.float64, torch.half, torch.double, torch.bfloat16,
        # complex
        torch.complex64, torch.complex128,
        # ints
        torch.int, torch.int8, torch.int16, torch.int32, torch.int64, torch.long, torch.short,
        # simplest
        torch.uint8, torch.bool,
    ],
    *[
        # ----------
        # numpy
        # ----------
        # floats
        np.float_, np.float16, np.float32, np.float64, np.half, np.float, np.double,
        # complex
        np.complex64, np.complex128,
        # ints
        np.int8, np.int16, np.int32, np.int64, np.int, np.long, np.short,
        # simplest
        np.uint8, np.bool,
    ]
]

DTYPE_MAP: dict = {
    str(x) : x
    for x in DTYPE_LIST
}



TORCH_OPTIMIZERS_MAP: dict[str, torch.optim.Optimizer] = {
    "Adagrad" : torch.optim.Adagrad,
    "Adam" : torch.optim.Adam,
    "AdamW" : torch.optim.AdamW,
    "SparseAdam" : torch.optim.SparseAdam,
    "Adamax" : torch.optim.Adamax,
    "ASGD" : torch.optim.ASGD,
    "LBFGS" : torch.optim.LBFGS,
    "NAdam" : torch.optim.NAdam,
    "RAdam" : torch.optim.RAdam,
    "RMSprop" : torch.optim.RMSprop,
    "Rprop" : torch.optim.Rprop,
    "SGD" : torch.optim.SGD,
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

def lpad_array(array: ATensor["token"], padded_length: int, pad_value: float = 0.0) -> NDArray:
    """pad a 1-d array on the left with pad_value to length `padded_length`"""
    return np.concatenate([
        np.full((padded_length - array.shape[0],), pad_value, dtype=array.dtype),
        array,
    ])

def rpad_array(array: ATensor["token"], pad_length: int, pad_value: float = 0.0) -> NDArray:
    """pad a 1-d array on the right with pad_value to length `pad_length`"""
    return np.concatenate([
        array,
        np.full((pad_length - array.shape[0],), pad_value, dtype=array.dtype),
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
