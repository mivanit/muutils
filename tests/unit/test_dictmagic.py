from __future__ import annotations
from typing import Dict

import pytest

from muutils.dictmagic import (
    condense_nested_dicts,
    condense_nested_dicts_matching_values,
    condense_tensor_dict,
    dotlist_to_nested_dict,
    is_numeric_consecutive,
    kwargs_to_nested_dict,
    nested_dict_to_dotlist,
    tuple_dims_replace,
    update_with_nested_dict,
)
from muutils.json_serialize import SerializableDataclass, serializable_dataclass


def test_dotlist_to_nested_dict():
    # Positive case
    assert dotlist_to_nested_dict({"a.b.c": 1, "a.b.d": 2, "a.e": 3}) == {
        "a": {"b": {"c": 1, "d": 2}, "e": 3}
    }

    # Negative case
    with pytest.raises(TypeError):
        dotlist_to_nested_dict({1: 1})  # type: ignore[dict-item]

    # Test with different separator
    assert dotlist_to_nested_dict({"a/b/c": 1, "a/b/d": 2, "a/e": 3}, sep="/") == {
        "a": {"b": {"c": 1, "d": 2}, "e": 3}
    }


def test_update_with_nested_dict():
    # Positive case
    assert update_with_nested_dict({"a": {"b": 1}, "c": -1}, {"a": {"b": 2}}) == {
        "a": {"b": 2},
        "c": -1,
    }

    # Case where the key is not present in original dict
    assert update_with_nested_dict({"a": {"b": 1}, "c": -1}, {"d": 3}) == {
        "a": {"b": 1},
        "c": -1,
        "d": 3,
    }

    # Case where a nested value is overridden
    assert update_with_nested_dict(
        {"a": {"b": 1, "d": 3}, "c": -1}, {"a": {"b": 2}}
    ) == {"a": {"b": 2, "d": 3}, "c": -1}

    # Case where the dict we are trying to update does not exist
    assert update_with_nested_dict({"a": 1}, {"b": {"c": 2}}) == {"a": 1, "b": {"c": 2}}


def test_kwargs_to_nested_dict():
    # Positive case
    assert kwargs_to_nested_dict({"a.b.c": 1, "a.b.d": 2, "a.e": 3}) == {
        "a": {"b": {"c": 1, "d": 2}, "e": 3}
    }

    # Case where strip_prefix is not None
    assert kwargs_to_nested_dict(
        {"prefix.a.b.c": 1, "prefix.a.b.d": 2, "prefix.a.e": 3}, strip_prefix="prefix."
    ) == {"a": {"b": {"c": 1, "d": 2}, "e": 3}}

    # Negative case
    with pytest.raises(ValueError):
        kwargs_to_nested_dict(
            {"a.b.c": 1, "a.b.d": 2, "a.e": 3},
            strip_prefix="prefix.",
            when_unknown_prefix="raise",
        )

    # Case where -- and - prefix
    assert kwargs_to_nested_dict(
        {"--a.b.c": 1, "--a.b.d": 2, "a.e": 3},
        strip_prefix="--",
        when_unknown_prefix="ignore",
    ) == {"a": {"b": {"c": 1, "d": 2}, "e": 3}}

    # Case where -- and - prefix with warning
    with pytest.warns(UserWarning):
        kwargs_to_nested_dict(
            {"--a.b.c": 1, "-a.b.d": 2, "a.e": 3},
            strip_prefix="-",
            when_unknown_prefix="warn",
        )


def test_kwargs_to_nested_dict_transform_key():
    # Case where transform_key is not None, changing dashes to underscores
    assert kwargs_to_nested_dict(
        {"a-b-c": 1, "a-b-d": 2, "a-e": 3}, transform_key=lambda x: x.replace("-", "_")
    ) == {"a_b_c": 1, "a_b_d": 2, "a_e": 3}

    # Case where strip_prefix and transform_key are both used
    assert kwargs_to_nested_dict(
        {"prefix.a-b-c": 1, "prefix.a-b-d": 2, "prefix.a-e": 3},
        strip_prefix="prefix.",
        transform_key=lambda x: x.replace("-", "_"),
    ) == {"a_b_c": 1, "a_b_d": 2, "a_e": 3}

    # Case where strip_prefix, transform_key and when_unknown_prefix='raise' are all used
    with pytest.raises(ValueError):
        kwargs_to_nested_dict(
            {"a-b-c": 1, "prefix.a-b-d": 2, "prefix.a-e": 3},
            strip_prefix="prefix.",
            transform_key=lambda x: x.replace("-", "_"),
            when_unknown_prefix="raise",
        )

    # Case where strip_prefix, transform_key and when_unknown_prefix='warn' are all used
    with pytest.warns(UserWarning):
        assert kwargs_to_nested_dict(
            {"a-b-c": 1, "prefix.a-b-d": 2, "prefix.a-e": 3},
            strip_prefix="prefix.",
            transform_key=lambda x: x.replace("-", "_"),
            when_unknown_prefix="warn",
        ) == {"a_b_c": 1, "a_b_d": 2, "a_e": 3}


@serializable_dataclass
class ChildData(SerializableDataclass):
    x: int
    y: int


@serializable_dataclass
class ParentData(SerializableDataclass):
    a: int
    b: ChildData


def test_update_from_nested_dict():
    parent = ParentData(a=1, b=ChildData(x=2, y=3))
    update_data = {"a": 5, "b": {"x": 6}}
    parent.update_from_nested_dict(update_data)

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 3

    update_data2 = {"b": {"y": 7}}
    parent.update_from_nested_dict(update_data2)

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 7


def test_update_from_dotlists():
    parent = ParentData(a=1, b=ChildData(x=2, y=3))
    update_data = {"a": 5, "b.x": 6}
    parent.update_from_nested_dict(dotlist_to_nested_dict(update_data))

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 3

    update_data2 = {"b.y": 7}
    parent.update_from_nested_dict(dotlist_to_nested_dict(update_data2))

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 7


# Tests for is_numeric_consecutive
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["1", "2", "3"], True),
        (["1", "3", "2"], True),
        (["1", "4", "2"], False),
        ([], False),
        (["a", "2", "3"], False),
    ],
)
def test_is_numeric_consecutive(test_input, expected):
    assert is_numeric_consecutive(test_input) == expected


# Tests for condense_nested_dicts
def test_condense_nested_dicts_single_level():
    data = {"1": "a", "2": "a", "3": "b"}
    expected = {"[1-2]": "a", "3": "b"}
    assert condense_nested_dicts(data) == expected


def test_condense_nested_dicts_nested():
    data = {"1": {"1": "a", "2": "a"}, "2": "b"}
    expected = {"1": {"[1-2]": "a"}, "2": "b"}
    assert condense_nested_dicts(data) == expected


def test_condense_nested_dicts_non_numeric():
    data = {"a": "a", "b": "a", "c": "b"}
    assert condense_nested_dicts(data, condense_matching_values=False) == data
    assert condense_nested_dicts(data, condense_matching_values=True) == {
        "[a, b]": "a",
        "c": "b",
    }


def test_condense_nested_dicts_mixed_keys():
    data = {"1": "a", "2": "a", "a": "b"}
    assert condense_nested_dicts(data) == {"[1, 2]": "a", "a": "b"}


# Mocking a Tensor-like object for use in tests
class MockTensor:
    def __init__(self, shape):
        self.shape = shape


# Test cases for `tuple_dims_replace`
@pytest.mark.parametrize(
    "input_tuple,dims_names_map,expected",
    [
        ((1, 2, 3), {1: "A", 2: "B"}, ("A", "B", 3)),
        ((4, 5, 6), {}, (4, 5, 6)),
        ((7, 8), None, (7, 8)),
        ((1, 2, 3), {3: "C"}, (1, 2, "C")),
    ],
)
def test_tuple_dims_replace(input_tuple, dims_names_map, expected):
    assert tuple_dims_replace(input_tuple, dims_names_map) == expected


@pytest.fixture
def tensor_data():
    # Mock tensor data simulating different shapes
    return {
        "tensor1": MockTensor((10, 256, 256)),
        "tensor2": MockTensor((10, 256, 256)),
        "tensor3": MockTensor((10, 512, 256)),
    }


def test_condense_tensor_dict_basic(tensor_data):
    assert condense_tensor_dict(
        tensor_data,
        drop_batch_dims=1,
        condense_matching_values=False,
    ) == {
        "tensor1": "(256, 256)",
        "tensor2": "(256, 256)",
        "tensor3": "(512, 256)",
    }

    assert condense_tensor_dict(
        tensor_data,
        drop_batch_dims=1,
        condense_matching_values=True,
    ) == {
        "[tensor1, tensor2]": "(256, 256)",
        "tensor3": "(512, 256)",
    }


def test_condense_tensor_dict_shapes_convert(tensor_data):
    # Returning the actual shape tuple
    shapes_convert = lambda x: x  # noqa: E731
    assert condense_tensor_dict(
        tensor_data,
        shapes_convert=shapes_convert,
        drop_batch_dims=1,
        condense_matching_values=False,
    ) == {
        "tensor1": (256, 256),
        "tensor2": (256, 256),
        "tensor3": (512, 256),
    }

    assert condense_tensor_dict(
        tensor_data,
        shapes_convert=shapes_convert,
        drop_batch_dims=1,
        condense_matching_values=True,
    ) == {
        "[tensor1, tensor2]": (256, 256),
        "tensor3": (512, 256),
    }


def test_condense_tensor_dict_named_dims(tensor_data):
    assert condense_tensor_dict(
        tensor_data,
        dims_names_map={10: "B", 256: "A", 512: "C"},
        condense_matching_values=False,
    ) == {
        "tensor1": "(B, A, A)",
        "tensor2": "(B, A, A)",
        "tensor3": "(B, C, A)",
    }

    assert condense_tensor_dict(
        tensor_data,
        dims_names_map={10: "B", 256: "A", 512: "C"},
        condense_matching_values=True,
    ) == {"[tensor1, tensor2]": "(B, A, A)", "tensor3": "(B, C, A)"}


@pytest.mark.parametrize(
    "input_data,expected,fallback_mapping",
    [
        # Test 1: Simple dictionary with no identical values
        ({"a": 1, "b": 2}, {"a": 1, "b": 2}, None),
        # Test 2: Dictionary with identical values
        ({"a": 1, "b": 1, "c": 2}, {"[a, b]": 1, "c": 2}, None),
        # Test 3: Nested dictionary with identical values
        ({"a": {"x": 1, "y": 1}, "b": 2}, {"a": {"[x, y]": 1}, "b": 2}, None),
        # Test 4: Nested dictionaries with and without identical values
        (
            {"a": {"x": 1, "y": 2}, "b": {"x": 1, "z": 3}, "c": 1},
            {"a": {"x": 1, "y": 2}, "b": {"x": 1, "z": 3}, "c": 1},
            None,
        ),
        # Test 5: Dictionary with unhashable values and no fallback mapping
        # This case is expected to fail without a fallback mapping, hence not included when using str as fallback
        # Test 6: Dictionary with unhashable values and a fallback mapping as str
        (
            {"a": [1, 2], "b": [1, 2], "c": "test"},
            {"[a, b]": "[1, 2]", "c": "test"},
            str,
        ),
    ],
)
def test_condense_nested_dicts_matching_values(input_data, expected, fallback_mapping):
    if fallback_mapping is not None:
        result = condense_nested_dicts_matching_values(input_data, fallback_mapping)
    else:
        result = condense_nested_dicts_matching_values(input_data)
    assert result == expected, f"Expected {expected}, got {result}"


# "ndtd" = `nested_dict_to_dotlist`
def test_nested_dict_to_dotlist_basic():
    nested_dict = {"a": {"b": {"c": 1, "d": 2}, "e": 3}}
    expected_dotlist = {"a.b.c": 1, "a.b.d": 2, "a.e": 3}
    assert nested_dict_to_dotlist(nested_dict) == expected_dotlist


def test_nested_dict_to_dotlist_empty():
    nested_dict: dict = {}
    expected_dotlist: dict = {}
    result = nested_dict_to_dotlist(nested_dict)
    assert result == expected_dotlist


def test_nested_dict_to_dotlist_single_level():
    nested_dict: Dict[str, int] = {"a": 1, "b": 2, "c": 3}
    expected_dotlist: Dict[str, int] = {"a": 1, "b": 2, "c": 3}
    assert nested_dict_to_dotlist(nested_dict) == expected_dotlist


def test_nested_dict_to_dotlist_with_list():
    nested_dict: dict = {"a": [1, 2, {"b": 3}], "c": 4}
    expected_dotlist: Dict[str, int] = {"a.0": 1, "a.1": 2, "a.2.b": 3, "c": 4}
    assert nested_dict_to_dotlist(nested_dict, allow_lists=True) == expected_dotlist


def test_nested_dict_to_dotlist_nested_empty():
    nested_dict: dict = {"a": {"b": {}}}
    expected_dotlist: dict = {"a.b": {}}
    assert nested_dict_to_dotlist(nested_dict) == expected_dotlist


def test_round_trip_conversion():
    original: dict = {"a": {"b": {"c": 1, "d": 2}, "e": 3}}
    dotlist = nested_dict_to_dotlist(original)
    result = dotlist_to_nested_dict(dotlist)
    assert result == original
