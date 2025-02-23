from __future__ import annotations

import jaxtyping
import numpy as np
import pytest
import torch

from muutils.tensor_utils import (
    DTYPE_MAP,
    TORCH_DTYPE_MAP,
    StateDictKeysError,
    StateDictShapeError,
    compare_state_dicts,
    get_dict_shapes,
    jaxtype_factory,
    lpad_array,
    lpad_tensor,
    numpy_to_torch_dtype,
    pad_array,
    pad_tensor,
    rpad_array,
    rpad_tensor,
)


def test_jaxtype_factory():
    ATensor = jaxtype_factory(
        "ATensor", torch.Tensor, jaxtyping.Float, legacy_mode="ignore"
    )
    assert ATensor.__name__ == "ATensor"
    assert "default_jax_dtype = <class 'jaxtyping.Float'" in ATensor.__doc__  # type: ignore[operator]
    assert "array_type = <class 'torch.Tensor'>" in ATensor.__doc__  # type: ignore[operator]

    x = ATensor[(1, 2, 3), np.float32]  # type: ignore[index]
    print(x)
    y = ATensor["dim1 dim2", np.float32]  # type: ignore[index]
    print(y)


def test_numpy_to_torch_dtype():
    # TODO: type ignores here should not be necessary?
    assert numpy_to_torch_dtype(np.float32) == torch.float32  # type: ignore[arg-type]
    assert numpy_to_torch_dtype(np.int32) == torch.int32  # type: ignore[arg-type]
    assert numpy_to_torch_dtype(torch.float32) == torch.float32


def test_dtype_maps():
    assert len(DTYPE_MAP) == len(TORCH_DTYPE_MAP)
    for key in DTYPE_MAP:
        assert key in TORCH_DTYPE_MAP
        assert numpy_to_torch_dtype(DTYPE_MAP[key]) == TORCH_DTYPE_MAP[key]


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

    d2["a"] = torch.tensor([7, 8, 9, 10])
    with pytest.raises(StateDictShapeError):
        compare_state_dicts(d1, d2)  # This should raise an exception

    d2["c"] = torch.tensor([10, 11, 12])
    with pytest.raises(StateDictKeysError):
        compare_state_dicts(d1, d2)  # This should raise an exception


def test_get_dict_shapes():
    x = {"a": torch.rand(2, 3), "b": torch.rand(1, 3, 5), "c": torch.rand(2)}
    x_shapes = get_dict_shapes(x)
    assert x_shapes == {"a": (2, 3), "b": (1, 3, 5), "c": (2,)}
