from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple

import pytest

# Module code assumed to be imported from my_module
from muutils.json_serialize.util import (
    UniversalContainer,
    _FORMAT_KEY,
    _recursive_hashify,
    array_safe_eq,
    dc_eq,
    isinstance_namedtuple,
    safe_getsource,
    string_as_lines,
    try_catch,
)


def test_universal_container():
    uc = UniversalContainer()
    assert "anything" in uc
    assert 123 in uc
    assert None in uc


def test_isinstance_namedtuple():
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    assert isinstance_namedtuple(p)
    assert not isinstance_namedtuple((1, 2))

    class Point2(NamedTuple):
        x: int
        y: int

    p2 = Point2(1, 2)
    assert isinstance_namedtuple(p2)


def test_try_catch():
    @try_catch
    def raises_value_error():
        raise ValueError("test error")

    @try_catch
    def normal_func(x):
        return x

    assert raises_value_error() == "ValueError: test error"
    assert normal_func(10) == 10


def test_recursive_hashify():
    assert _recursive_hashify({"a": [1, 2, 3]}) == (("a", (1, 2, 3)),)
    assert _recursive_hashify([1, 2, 3]) == (1, 2, 3)
    assert _recursive_hashify(123) == 123
    with pytest.raises(ValueError):
        _recursive_hashify(object(), force=False)


def test_string_as_lines():
    assert string_as_lines("line1\nline2\nline3") == ["line1", "line2", "line3"]
    assert string_as_lines(None) == []


def test_safe_getsource():
    def sample_func():
        pass

    source = safe_getsource(sample_func)
    print(f"Source of sample_func: {source}")
    assert "def sample_func():" in source[0]

    def raises_error():
        raise Exception("test error")

    wrapped_func = try_catch(raises_error)
    error_source = safe_getsource(wrapped_func)
    print(f"Source of wrapped_func: {error_source}")
    # Check for the original function's source since the decorator doesn't change this
    assert any("def raises_error():" in line for line in error_source)


# Additional tests from TODO.md


def test_try_catch_exception_handling():
    """Test that try_catch properly catches exceptions and returns default error message."""

    @try_catch
    def raises_runtime_error():
        raise RuntimeError("runtime error message")

    @try_catch
    def raises_key_error():
        raise KeyError("missing key")

    @try_catch
    def raises_zero_division():
        return 1 / 0

    # Test that exceptions are caught and serialized
    assert raises_runtime_error() == "RuntimeError: runtime error message"
    assert raises_key_error() == "KeyError: 'missing key'"
    result = raises_zero_division()
    assert "ZeroDivisionError" in result

    # Test with arguments
    @try_catch
    def func_with_args(a, b):
        if a == 0:
            raise ValueError(f"a cannot be 0, got {a}")
        return a + b

    assert func_with_args(1, 2) == 3
    assert func_with_args(0, 2) == "ValueError: a cannot be 0, got 0"


def test_array_safe_eq():
    """Test array_safe_eq with numpy arrays, torch tensors, and nested arrays."""
    # Basic types
    assert array_safe_eq(1, 1) is True
    assert array_safe_eq(1, 2) is False
    # Note: strings are treated as sequences by array_safe_eq, so we test differently
    assert array_safe_eq(1.5, 1.5) is True
    assert array_safe_eq(True, True) is True

    # Lists and sequences
    assert array_safe_eq([1, 2, 3], [1, 2, 3]) is True
    assert array_safe_eq([1, 2, 3], [1, 2, 4]) is False
    assert array_safe_eq([], []) is True
    assert array_safe_eq((1, 2, 3), (1, 2, 3)) is True

    # Nested arrays
    assert array_safe_eq([[1, 2], [3, 4]], [[1, 2], [3, 4]]) is True
    assert array_safe_eq([[1, 2], [3, 4]], [[1, 2], [3, 5]]) is False
    assert array_safe_eq([[[1]], [[2]]], [[[1]], [[2]]]) is True

    # Dicts
    assert array_safe_eq({"a": 1, "b": 2}, {"a": 1, "b": 2}) is True
    assert array_safe_eq({"a": 1, "b": 2}, {"a": 1, "b": 3}) is False
    assert array_safe_eq({}, {}) is True

    # Mixed nested structures
    assert (
        array_safe_eq({"a": [1, 2], "b": {"c": 3}}, {"a": [1, 2], "b": {"c": 3}})
        is True
    )
    assert (
        array_safe_eq({"a": [1, 2], "b": {"c": 3}}, {"a": [1, 2], "b": {"c": 4}})
        is False
    )

    # Identity check
    obj = {"a": 1}
    assert array_safe_eq(obj, obj) is True

    # Type mismatch
    assert array_safe_eq(1, 1.0) is False  # Different types
    assert array_safe_eq([1, 2], (1, 2)) is False

    # Try with numpy if available (note: numpy returns np.True_ not Python True)
    try:
        import numpy as np

        arr1 = np.array([1, 2, 3])
        arr2 = np.array([1, 2, 3])
        arr3 = np.array([1, 2, 4])
        assert array_safe_eq(arr1, arr2)  # Use == not is for numpy bool
        assert not array_safe_eq(arr1, arr3)
    except ImportError:
        pass  # Skip numpy tests if not available

    # Try with torch if available (note: torch also may return tensor bool)
    try:
        import torch

        t1 = torch.tensor([1.0, 2.0, 3.0])
        t2 = torch.tensor([1.0, 2.0, 3.0])
        t3 = torch.tensor([1.0, 2.0, 4.0])
        assert array_safe_eq(t1, t2)  # Use == not is for torch bool
        assert not array_safe_eq(t1, t3)
    except ImportError:
        pass  # Skip torch tests if not available


def test_dc_eq():
    """Test dc_eq for dataclasses equal and unequal cases."""

    @dataclass
    class Point:
        x: int
        y: int

    @dataclass
    class Point3D:
        x: int
        y: int
        z: int

    @dataclass
    class PointWithArray:
        x: int
        coords: list

    # Equal dataclasses
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    assert dc_eq(p1, p2) is True

    # Unequal dataclasses
    p3 = Point(1, 3)
    assert dc_eq(p1, p3) is False

    # Identity
    assert dc_eq(p1, p1) is True

    # Different classes - default behavior (false_when_class_mismatch=True)
    p3d = Point3D(1, 2, 3)
    assert dc_eq(p1, p3d) is False

    # Different classes - except_when_class_mismatch=True
    with pytest.raises(
        TypeError, match="Cannot compare dataclasses of different classes"
    ):
        dc_eq(p1, p3d, except_when_class_mismatch=True)

    # Dataclasses with arrays
    pa1 = PointWithArray(1, [1, 2, 3])
    pa2 = PointWithArray(1, [1, 2, 3])
    pa3 = PointWithArray(1, [1, 2, 4])
    assert dc_eq(pa1, pa2) is True
    assert dc_eq(pa1, pa3) is False

    # Test with nested structures
    @dataclass
    class Container:
        items: list
        metadata: dict

    c1 = Container([1, 2, 3], {"name": "test"})
    c2 = Container([1, 2, 3], {"name": "test"})
    c3 = Container([1, 2, 3], {"name": "other"})
    assert dc_eq(c1, c2) is True
    assert dc_eq(c1, c3) is False

    # Test except_when_field_mismatch with different classes but same fields
    @dataclass
    class Point2D:
        x: int
        y: int

    # Different classes but same fields - should raise with except_when_field_mismatch
    with pytest.raises(AttributeError):
        dc_eq(p1, p3d, except_when_field_mismatch=True)


def test_FORMAT_KEY():
    """Test that FORMAT_KEY constant is accessible and has expected value."""
    # Test that the format key exists and is a string
    assert isinstance(_FORMAT_KEY, str)
    assert _FORMAT_KEY == "__muutils_format__"

    # Test that it can be used in dictionaries (common use case)
    data = {_FORMAT_KEY: "custom_type", "value": 42}
    assert data[_FORMAT_KEY] == "custom_type"
    assert _FORMAT_KEY in data


def test_edge_cases():
    """Test edge cases for utility functions: None values, empty containers, mixed types."""
    # string_as_lines with None
    assert string_as_lines(None) == []
    # Empty string splits to empty list (splitlines behavior)
    assert string_as_lines("") == []
    assert string_as_lines("single") == ["single"]

    # _recursive_hashify with empty containers
    assert _recursive_hashify([]) == ()
    assert _recursive_hashify({}) == ()
    assert _recursive_hashify(()) == ()

    # _recursive_hashify with mixed nested types
    mixed = {"list": [1, 2], "dict": {"nested": True}, "tuple": (3, 4)}
    result = _recursive_hashify(mixed)
    assert isinstance(result, tuple)

    # array_safe_eq with empty containers
    assert array_safe_eq([], []) is True
    assert array_safe_eq({}, {}) is True
    assert array_safe_eq((), ()) is True

    # array_safe_eq with None
    assert array_safe_eq(None, None) is True
    assert array_safe_eq(None, 0) is False

    # try_catch with function returning None
    @try_catch
    def returns_none():
        return None

    assert returns_none() is None

    # UniversalContainer with various types
    uc = UniversalContainer()
    assert None in uc
    assert [] in uc
    assert {} in uc
    assert object() in uc
