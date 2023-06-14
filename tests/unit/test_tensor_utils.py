import pytest
import numpy as np
import torch
import jaxtyping

from muutils.tensor_utils import (
    jaxtype_factory, numpy_to_torch_dtype, pad_tensor, lpad_tensor,
	rpad_tensor, pad_array, lpad_array, rpad_array, compare_state_dicts,
    numpy_to_torch_dtype,
    TORCH_DTYPE_MAP,
    DTYPE_MAP,    
)

def test_jaxtype_factory():
    ATensor = jaxtype_factory("ATensor", torch.Tensor, jaxtyping.Float)
    assert ATensor.__name__ == "ATensor"
    assert "default_jax_dtype = <class 'jaxtyping.Float'" in ATensor.__doc__
    assert "array_type = <class 'torch.Tensor'>" in ATensor.__doc__


def test_numpy_to_torch_dtype():
    assert numpy_to_torch_dtype(np.float32) == torch.float32
    assert numpy_to_torch_dtype(np.int32) == torch.int32
    assert numpy_to_torch_dtype(torch.float32) == torch.float32

def test_dtype_maps():
    assert len(DTYPE_MAP) == len(TORCH_DTYPE_MAP)
    for key in DTYPE_MAP:
        assert key in TORCH_DTYPE_MAP
        assert numpy_to_torch_dtype(DTYPE_MAP[key]) == TORCH_DTYPE_MAP[key]


def test_numpy_to_torch_dtype():
    assert numpy_to_torch_dtype(np.float32) == torch.float32
    assert numpy_to_torch_dtype(torch.float32) == torch.float32

def test_pad_tensor():
    tensor = torch.tensor([1, 2, 3])
    assert torch.all(pad_tensor(tensor, 5) == torch.tensor([0, 0, 1, 2, 3]))
    assert torch.all(lpad_tensor(tensor, 5) == torch.tensor([0, 0, 1, 2, 3]))
    assert torch.all(rpad_tensor(tensor, 5) == torch.tensor([1, 2, 3, 0, 0]))

def test_pad_array():
    array = np.array([1, 2, 3])
    assert np.array_equal(pad_array(array, 5), np.array([0, 0, 1, 2, 3]))
    assert np.array_equal(lpad_array(array, 5), np.array([0, 0, 1, 2, 3]))
    assert np.array_equal(rpad_array(array, 5), np.array([1, 2, 3, 0, 0]))

def test_compare_state_dicts():
    d1 = {"a": torch.tensor([1, 2, 3]), "b": torch.tensor([4, 5, 6])}
    d2 = {"a": torch.tensor([1, 2, 3]), "b": torch.tensor([4, 5, 6])}
    compare_state_dicts(d1, d2)  # This should not raise an exception

    d2["a"] = torch.tensor([7, 8, 9])
    with pytest.raises(AssertionError):
        compare_state_dicts(d1, d2)  # This should raise an exception
