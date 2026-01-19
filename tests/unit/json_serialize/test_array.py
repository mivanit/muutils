import numpy as np
import pytest

from muutils.json_serialize import JsonSerializer
from muutils.json_serialize.array import (
    ArrayMode,
    ArrayModeWithMeta,
    arr_metadata,
    array_n_elements,
    load_array,
    serialize_array,
)
from muutils.json_serialize.types import _FORMAT_KEY

# pylint: disable=missing-class-docstring


class TestArray:
    def setup_method(self):
        self.array_1d = np.array([1, 2, 3])
        self.array_2d = np.array([[1, 2], [3, 4]])
        self.array_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=np.int64)
        self.array_zero_dim = np.array(42)
        self.jser = JsonSerializer(array_mode="list")

    def test_array_n_elements(self):
        assert array_n_elements(self.array_1d) == 3
        assert array_n_elements(self.array_2d) == 4
        assert array_n_elements(self.array_3d) == 8
        assert array_n_elements(self.array_zero_dim) == 1

    def test_arr_metadata(self):
        metadata = arr_metadata(self.array_3d)
        assert metadata["shape"] == [2, 2, 2]
        assert metadata["dtype"] == "int64"
        assert metadata["n_elements"] == 8

    @pytest.mark.parametrize(
        "array_mode,expected_type",
        [
            ("list", list),
            ("array_list_meta", dict),
            ("array_hex_meta", dict),
            ("array_b64_meta", dict),
        ],
    )
    def test_serialize_array(self, array_mode: ArrayMode, expected_type: type):
        result = serialize_array(
            self.jser, self.array_2d, "test_path", array_mode=array_mode
        )
        assert isinstance(result, expected_type)

    def test_load_array(self):
        serialized_array = serialize_array(
            self.jser, self.array_3d, "test_path", array_mode="array_list_meta"
        )
        loaded_array = load_array(serialized_array, array_mode="array_list_meta")
        assert np.array_equal(loaded_array, self.array_3d)

    @pytest.mark.parametrize(
        "array_mode",
        ["list", "array_list_meta", "array_hex_meta", "array_b64_meta"],
    )
    def test_serialize_load_integration(self, array_mode: ArrayMode):
        for array in [self.array_1d, self.array_2d, self.array_3d]:
            serialized_array = serialize_array(
                self.jser,
                array,
                "test_path",
                array_mode=array_mode,
            )
            # The overload combinations for serialize_array -> load_array are complex
            # since array_mode determines both the serialized type and load method
            loaded_array = load_array(serialized_array, array_mode=array_mode)  # type: ignore[call-overload, arg-type]
            assert np.array_equal(loaded_array, array)

    def test_serialize_load_list(self):
        """Test serialize/load with 'list' mode - separate function for type safety."""
        for array in [self.array_1d, self.array_2d, self.array_3d]:
            serialized_array = serialize_array(
                self.jser, array, "test_path", array_mode="list"
            )
            loaded_array = load_array(serialized_array, array_mode="list")
            assert np.array_equal(loaded_array, array)

    def test_serialize_load_array_list_meta(self):
        """Test serialize/load with 'array_list_meta' mode - separate function for type safety."""
        for array in [self.array_1d, self.array_2d, self.array_3d]:
            serialized_array = serialize_array(
                self.jser, array, "test_path", array_mode="array_list_meta"
            )
            loaded_array = load_array(serialized_array, array_mode="array_list_meta")
            assert np.array_equal(loaded_array, array)

    def test_serialize_load_array_hex_meta(self):
        """Test serialize/load with 'array_hex_meta' mode - separate function for type safety."""
        for array in [self.array_1d, self.array_2d, self.array_3d]:
            serialized_array = serialize_array(
                self.jser, array, "test_path", array_mode="array_hex_meta"
            )
            loaded_array = load_array(serialized_array, array_mode="array_hex_meta")
            assert np.array_equal(loaded_array, array)

    def test_serialize_load_array_b64_meta(self):
        """Test serialize/load with 'array_b64_meta' mode - separate function for type safety."""
        for array in [self.array_1d, self.array_2d, self.array_3d]:
            serialized_array = serialize_array(
                self.jser, array, "test_path", array_mode="array_b64_meta"
            )
            loaded_array = load_array(serialized_array, array_mode="array_b64_meta")
            assert np.array_equal(loaded_array, array)

    # TODO: do we even want to support "list" mode for zero-dim arrays?
    @pytest.mark.parametrize(
        "array_mode",
        ["array_list_meta", "array_hex_meta", "array_b64_meta"],
    )
    def test_serialize_load_zero_dim(self, array_mode: ArrayModeWithMeta):
        serialized_array = serialize_array(
            self.jser,
            self.array_zero_dim,
            "test_path",
            array_mode=array_mode,
        )
        loaded_array = load_array(serialized_array)
        assert np.array_equal(loaded_array, self.array_zero_dim)


@pytest.mark.parametrize(
    "mode", ["array_list_meta", "array_hex_meta", "array_b64_meta"]
)
def test_array_shape_dtype_preservation(mode: ArrayModeWithMeta):
    """Test that various shapes and dtypes are preserved through serialization."""
    # Test different shapes
    shapes_and_arrays = [
        (np.array([1, 2, 3], dtype=np.int32), "1D int32"),
        (np.array([[1.5, 2.5], [3.5, 4.5]], dtype=np.float32), "2D float32"),
        (np.array([[[1]], [[2]]], dtype=np.int8), "3D int8"),
        (np.array([[[[1, 2, 3, 4]]]], dtype=np.int16), "4D int16"),
    ]

    # Test different dtypes
    dtype_tests = [
        (np.array([1, 2, 3], dtype=np.int8), np.int8),
        (np.array([1, 2, 3], dtype=np.int16), np.int16),
        (np.array([1, 2, 3], dtype=np.int32), np.int32),
        (np.array([1, 2, 3], dtype=np.int64), np.int64),
        (np.array([1.0, 2.0, 3.0], dtype=np.float16), np.float16),
        (np.array([1.0, 2.0, 3.0], dtype=np.float32), np.float32),
        (np.array([1.0, 2.0, 3.0], dtype=np.float64), np.float64),
        (np.array([True, False, True], dtype=np.bool_), np.bool_),
    ]

    jser = JsonSerializer(array_mode="array_list_meta")

    # Test shapes preservation
    for arr, description in shapes_and_arrays:
        serialized = serialize_array(jser, arr, "test", array_mode=mode)
        loaded = load_array(serialized)
        assert loaded.shape == arr.shape, f"Shape mismatch for {description} in {mode}"
        assert loaded.dtype == arr.dtype, f"Dtype mismatch for {description} in {mode}"
        assert np.array_equal(loaded, arr), f"Data mismatch for {description} in {mode}"

    # Test dtypes preservation
    for arr, expected_dtype in dtype_tests:
        serialized = serialize_array(jser, arr, "test", array_mode=mode)
        loaded = load_array(serialized)
        assert loaded.dtype == expected_dtype, f"Dtype not preserved: {mode}"
        assert np.array_equal(loaded, arr), f"Data not preserved: {mode}"


def test_array_serialization_handlers():
    """Test integration with JsonSerializer - ensure arrays are serialized correctly when part of larger objects."""
    # Test that JsonSerializer properly handles arrays in different contexts
    jser = JsonSerializer(array_mode="array_list_meta")

    # Array in a dict
    data_dict = {
        "metadata": {"name": "test"},
        "array": np.array([1, 2, 3, 4]),
        "nested": {"inner_array": np.array([[1, 2], [3, 4]])},
    }

    serialized = jser.json_serialize(data_dict)
    assert isinstance(serialized, dict)
    serialized_array = serialized["array"]
    assert isinstance(serialized_array, dict)
    assert _FORMAT_KEY in serialized_array
    assert serialized_array["shape"] == [4]

    # Array in a list
    data_list = [
        {"value": 1},
        np.array([10, 20, 30]),
        {"value": 2, "data": np.array([[1, 2]])},
    ]

    serialized_list = jser.json_serialize(data_list)
    assert isinstance(serialized_list, list)
    serialized_list_item = serialized_list[1]
    assert isinstance(serialized_list_item, dict)
    assert _FORMAT_KEY in serialized_list_item

    # Test different array modes
    for mode in ["list", "array_list_meta", "array_hex_meta", "array_b64_meta"]:
        jser_mode = JsonSerializer(array_mode=mode)  # type: ignore[arg-type]
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        result = jser_mode.json_serialize(arr)

        if mode == "list":
            assert isinstance(result, list)
        else:
            assert isinstance(result, dict)
            assert _FORMAT_KEY in result


@pytest.mark.parametrize(
    "mode", ["array_list_meta", "array_hex_meta", "array_b64_meta"]
)
def test_array_edge_cases(mode: ArrayModeWithMeta):
    """Test edge cases: empty arrays, unusual dtypes, and boundary conditions."""
    jser = JsonSerializer(array_mode="array_list_meta")

    # Empty arrays with different shapes
    empty_1d = np.array([], dtype=np.int32)
    empty_2d = np.array([[], []], dtype=np.float32).reshape(2, 0)
    empty_3d = np.array([[]], dtype=np.int64).reshape(1, 1, 0)

    for empty_arr in [empty_1d, empty_2d, empty_3d]:
        serialized = serialize_array(jser, empty_arr, "test", array_mode=mode)
        loaded = load_array(serialized)
        assert loaded.shape == empty_arr.shape
        assert loaded.dtype == empty_arr.dtype
        assert np.array_equal(loaded, empty_arr)

    # Complex dtypes
    complex_arr = np.array([1 + 2j, 3 + 4j, 5 + 6j], dtype=np.complex64)
    serialized = serialize_array(
        jser, complex_arr, "test", array_mode="array_list_meta"
    )
    loaded = load_array(serialized)
    assert loaded.dtype == np.complex64
    assert np.array_equal(loaded, complex_arr)

    # Large arrays (test that serialization doesn't break)
    large_arr = np.random.rand(100, 100)
    serialized = serialize_array(jser, large_arr, "test", array_mode=mode)
    loaded = load_array(serialized)
    assert np.allclose(loaded, large_arr)

    # Arrays with special values
    special_arr = np.array([np.inf, -np.inf, np.nan, 0.0, -0.0], dtype=np.float64)
    serialized = serialize_array(jser, special_arr, "test", array_mode=mode)
    loaded = load_array(serialized)
    # Use special comparison for NaN
    assert np.isnan(loaded[2]) and np.isnan(special_arr[2])
    assert np.array_equal(loaded[:2], special_arr[:2])  # inf values
    assert np.array_equal(loaded[3:], special_arr[3:])  # zeros
