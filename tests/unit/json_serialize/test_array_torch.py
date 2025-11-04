import numpy as np
import pytest
import torch

from muutils.json_serialize import JsonSerializer
from muutils.json_serialize.array import (
    ArrayMode,
    arr_metadata,
    array_n_elements,
    load_array,
    serialize_array,
)
from muutils.json_serialize.types import _FORMAT_KEY  # pyright: ignore[reportPrivateUsage]

# pylint: disable=missing-class-docstring


_WITH_META_ARRAY_MODES: list[ArrayMode] = [
    "array_list_meta",
    "array_hex_meta",
    "array_b64_meta",
]


def test_arr_metadata_torch():
    """Test arr_metadata() with torch tensors."""
    # 1D tensor
    tensor_1d = torch.tensor([1, 2, 3, 4, 5])
    metadata_1d = arr_metadata(tensor_1d)
    assert metadata_1d["shape"] == [5]
    assert "int64" in metadata_1d["dtype"]  # Could be "torch.int64" or "int64"
    assert metadata_1d["n_elements"] == 5

    # 2D tensor
    tensor_2d = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)
    metadata_2d = arr_metadata(tensor_2d)
    assert metadata_2d["shape"] == [2, 2]
    assert "float32" in metadata_2d["dtype"]
    assert metadata_2d["n_elements"] == 4

    # 3D tensor
    tensor_3d = torch.randn(3, 4, 5, dtype=torch.float64)
    metadata_3d = arr_metadata(tensor_3d)
    assert metadata_3d["shape"] == [3, 4, 5]
    assert "float64" in metadata_3d["dtype"]
    assert metadata_3d["n_elements"] == 60

    # Zero-dimensional tensor
    tensor_0d = torch.tensor(42)
    metadata_0d = arr_metadata(tensor_0d)
    assert metadata_0d["shape"] == []
    assert metadata_0d["n_elements"] == 1


def test_array_n_elements_torch():
    """Test array_n_elements() with torch tensors."""
    assert array_n_elements(torch.tensor([1, 2, 3])) == 3
    assert array_n_elements(torch.tensor([[1, 2], [3, 4]])) == 4
    assert array_n_elements(torch.randn(2, 3, 4)) == 24
    assert array_n_elements(torch.tensor(42)) == 1


def test_serialize_load_torch_tensors():
    """Test round-trip serialization of torch tensors."""
    jser = JsonSerializer(array_mode="array_list_meta")

    # Test various tensor types
    tensors = [
        torch.tensor([1, 2, 3, 4], dtype=torch.int32),
        torch.tensor([[1.5, 2.5], [3.5, 4.5]], dtype=torch.float32),
        torch.tensor([[[1, 2]], [[3, 4]]], dtype=torch.int64),
        torch.tensor([True, False, True], dtype=torch.bool),
    ]

    for tensor in tensors:
        for mode in _WITH_META_ARRAY_MODES:
            serialized = serialize_array(jser, tensor, "test", array_mode=mode)  # type: ignore[arg-type]
            loaded = load_array(serialized)

            # Convert to numpy for comparison
            tensor_np = tensor.cpu().numpy()
            assert np.array_equal(loaded, tensor_np)
            assert loaded.shape == tuple(tensor.shape)


def test_torch_shape_dtype_preservation():
    """Test that various torch tensor shapes and dtypes are preserved."""
    jser = JsonSerializer(array_mode="array_list_meta")

    # Different dtypes
    dtype_tests = [
        (torch.tensor([1, 2, 3], dtype=torch.int8), torch.int8),
        (torch.tensor([1, 2, 3], dtype=torch.int16), torch.int16),
        (torch.tensor([1, 2, 3], dtype=torch.int32), torch.int32),
        (torch.tensor([1, 2, 3], dtype=torch.int64), torch.int64),
        (torch.tensor([1.0, 2.0, 3.0], dtype=torch.float16), torch.float16),
        (torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32), torch.float32),
        (torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64), torch.float64),
        (torch.tensor([True, False, True], dtype=torch.bool), torch.bool),
    ]

    for tensor, _expected_dtype in dtype_tests:
        for mode in _WITH_META_ARRAY_MODES:
            serialized = serialize_array(jser, tensor, "test", array_mode=mode)  # type: ignore[arg-type]
            loaded = load_array(serialized)

            # Convert for comparison
            tensor_np = tensor.cpu().numpy()
            assert np.array_equal(loaded, tensor_np)
            assert loaded.dtype.name == tensor_np.dtype.name


def test_torch_zero_dim_tensor():
    """Test zero-dimensional torch tensors."""
    jser = JsonSerializer(array_mode="array_list_meta")

    tensor_0d = torch.tensor(42)

    for mode in _WITH_META_ARRAY_MODES:
        serialized = serialize_array(jser, tensor_0d, "test", array_mode=mode)  # type: ignore[arg-type]
        loaded = load_array(serialized)

        # Zero-dim tensors have special handling
        assert loaded.shape == tensor_0d.shape
        assert np.array_equal(loaded, tensor_0d.cpu().numpy())


def test_torch_edge_cases():
    """Test edge cases with torch tensors."""
    jser = JsonSerializer(array_mode="array_list_meta")

    # Empty tensors
    empty_1d = torch.tensor([], dtype=torch.float32)
    serialized = serialize_array(jser, empty_1d, "test", array_mode="array_list_meta")
    loaded = load_array(serialized)
    assert loaded.shape == (0,)

    # Tensors with special values
    special_tensor = torch.tensor(
        [float("inf"), float("-inf"), float("nan"), 0.0, -0.0]
    )
    for mode in _WITH_META_ARRAY_MODES:
        serialized = serialize_array(jser, special_tensor, "test", array_mode=mode)  # type: ignore[arg-type]
        loaded = load_array(serialized)

        # Check special values
        assert np.isinf(loaded[0]) and loaded[0] > 0  # pyright: ignore[reportAny]
        assert np.isinf(loaded[1]) and loaded[1] < 0  # pyright: ignore[reportAny]
        assert np.isnan(loaded[2])  # pyright: ignore[reportAny]

    # Large tensor
    large_tensor = torch.randn(100, 100)
    serialized = serialize_array(
        jser, large_tensor, "test", array_mode="array_b64_meta"
    )
    loaded = load_array(serialized)
    assert np.allclose(loaded, large_tensor.cpu().numpy())


def test_torch_gpu_tensors():
    """Test serialization of GPU tensors (if CUDA is available)."""
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")

    jser = JsonSerializer(array_mode="array_list_meta")

    # Create GPU tensor
    tensor_gpu = torch.tensor([1, 2, 3, 4], dtype=torch.float32, device="cuda")

    for mode in _WITH_META_ARRAY_MODES:
        # Need to move to CPU first for numpy conversion
        tensor_cpu_torch = tensor_gpu.cpu()
        serialized = serialize_array(jser, tensor_cpu_torch, "test", array_mode=mode)  # type: ignore[arg-type]
        loaded = load_array(serialized)

        # Should match the CPU version
        tensor_cpu = tensor_gpu.cpu().numpy()
        assert np.array_equal(loaded, tensor_cpu)


def test_torch_serialization_integration():
    """Test torch tensors integrated with JsonSerializer in complex structures."""
    jser = JsonSerializer(array_mode="array_list_meta")

    # Mixed structure with torch tensors
    data = {
        "model_weights": torch.randn(10, 5),
        "biases": torch.randn(5),
        "metadata": {"epochs": 10, "lr": 0.001},
        "history": [
            {"loss": torch.tensor(0.5), "accuracy": torch.tensor(0.95)},
            {"loss": torch.tensor(0.3), "accuracy": torch.tensor(0.97)},
        ],
    }

    serialized = jser.json_serialize(data)
    assert isinstance(serialized, dict)

    # Check structure is preserved
    assert isinstance(serialized["model_weights"], dict)
    assert _FORMAT_KEY in serialized["model_weights"]
    assert serialized["model_weights"]["shape"] == [10, 5]

    assert isinstance(serialized["biases"], dict)
    assert serialized["biases"]["shape"] == [5]

    assert serialized["metadata"]["epochs"] == 10  # pyright: ignore[reportArgumentType, reportCallIssue, reportIndexIssue, reportOptionalSubscript]

    # Check nested tensors
    assert isinstance(serialized["history"][0]["loss"], dict)  # pyright: ignore[reportArgumentType, reportCallIssue, reportIndexIssue, reportOptionalSubscript]
    assert _FORMAT_KEY in serialized["history"][0]["loss"]  # pyright: ignore[reportArgumentType, reportCallIssue, reportIndexIssue, reportOptionalSubscript, reportOperatorIssue]


def test_mixed_numpy_torch():
    """Test that both numpy arrays and torch tensors can coexist in serialization."""
    jser = JsonSerializer(array_mode="array_list_meta")

    data = {
        "numpy_array": np.array([1, 2, 3]),
        "torch_tensor": torch.tensor([4, 5, 6]),
        "nested": {
            "np": np.array([[1, 2]]),
            "torch": torch.tensor([[3, 4]]),
        },
    }

    serialized = jser.json_serialize(data)
    assert isinstance(serialized, dict)

    # Both should be serialized as dicts with metadata
    assert isinstance(serialized["numpy_array"], dict)
    assert isinstance(serialized["torch_tensor"], dict)
    assert _FORMAT_KEY in serialized["numpy_array"]
    assert _FORMAT_KEY in serialized["torch_tensor"]

    # Check format strings identify the type
    assert "numpy" in serialized["numpy_array"][_FORMAT_KEY]  # pyright: ignore[reportOperatorIssue]
    assert "torch" in serialized["torch_tensor"][_FORMAT_KEY]  # pyright: ignore[reportOperatorIssue]
