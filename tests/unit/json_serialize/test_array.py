import numpy as np
import pytest

from muutils.json_serialize import JsonSerializer
from muutils.json_serialize.array import (
    ArrayMode,
    arr_metadata,
    array_n_elements,
    load_array,
    serialize_array,
)

# pylint: disable=missing-class-docstring


class TestYourModule:
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

    def test_serialize_load_integration(self):
        for array_mode in [
            "list",
            "array_list_meta",
            "array_hex_meta",
            "array_b64_meta",
        ]:
            for array in [self.array_1d, self.array_2d, self.array_3d]:
                serialized_array = serialize_array(
                    self.jser,
                    array,
                    "test_path",
                    array_mode=array_mode,  # type: ignore[arg-type]
                )
                loaded_array = load_array(serialized_array, array_mode=array_mode)  # type: ignore[arg-type]
                assert np.array_equal(loaded_array, array)

    def test_serialize_load_zero_dim(self):
        for array_mode in [
            "list",
            "array_list_meta",
            "array_hex_meta",
            "array_b64_meta",
        ]:
            serialized_array = serialize_array(
                self.jser,
                self.array_zero_dim,
                "test_path",
                array_mode=array_mode,  # type: ignore[arg-type]
            )
            loaded_array = load_array(serialized_array)
            assert np.array_equal(loaded_array, self.array_zero_dim)
