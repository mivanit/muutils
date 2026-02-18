"""Tests for muutils.json_serialize.json_serialize module.

IMPORTANT: This tests the core json_serialize functionality. Array-specific tests are in test_array.py,
and utility function tests are in test_util.py. We focus on JsonSerializer class and handler system here.
"""

from __future__ import annotations

import warnings
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from muutils.errormode import ErrorMode
from muutils.json_serialize.json_serialize import (
    BASE_HANDLERS,
    DEFAULT_HANDLERS,
    JsonSerializer,
    SerializerHandler,
    json_serialize,
)
from muutils.json_serialize.types import _FORMAT_KEY
from muutils.json_serialize.util import SerializationException


# ============================================================================
# Test classes and fixtures
# ============================================================================


@dataclass
class SimpleDataclass:
    """Simple dataclass for testing."""

    x: int
    y: str
    z: bool = True


@dataclass
class NestedDataclass:
    """Nested dataclass for testing."""

    simple: SimpleDataclass
    data: dict[str, Any]


class ClassWithSerialize:
    """Class with custom serialize method."""

    def __init__(self, value: int):
        self.value = value
        self.name = "test"

    def serialize(self) -> dict:
        """Custom serialization."""
        return {"custom_value": self.value * 2, "custom_name": self.name.upper()}


class UnserializableClass:
    """Class that can't be easily serialized."""

    def __init__(self):
        self.data = "test"


# ============================================================================
# Tests for basic type serialization
# ============================================================================


def test_json_serialize_basic_types():
    """Test serialization of basic Python types: int, float, str, bool, None, list, dict."""
    serializer = JsonSerializer()

    # Test primitives
    assert serializer.json_serialize(42) == 42
    assert serializer.json_serialize(3.14) == 3.14
    assert serializer.json_serialize("hello") == "hello"
    assert serializer.json_serialize(True) is True
    assert serializer.json_serialize(False) is False
    assert serializer.json_serialize(None) is None

    # Test list
    result = serializer.json_serialize([1, 2, 3])
    assert result == [1, 2, 3]
    assert isinstance(result, list)

    # Test dict
    result = serializer.json_serialize({"a": 1, "b": 2})
    assert result == {"a": 1, "b": 2}
    assert isinstance(result, dict)

    # Test empty containers
    assert serializer.json_serialize([]) == []
    assert serializer.json_serialize({}) == {}


def test_json_serialize_function():
    """Test the module-level json_serialize function with default config."""
    # Test that it works with basic types
    assert json_serialize(42) == 42
    assert json_serialize("test") == "test"
    assert json_serialize([1, 2, 3]) == [1, 2, 3]
    assert json_serialize({"key": "value"}) == {"key": "value"}

    # Test with more complex types
    obj = SimpleDataclass(x=10, y="hello", z=False)
    result = json_serialize(obj)
    assert result == {"x": 10, "y": "hello", "z": False}


# ============================================================================
# Tests for .serialize() method override
# ============================================================================


def test_json_serialize_serialize_method():
    """Test objects with .serialize() method are handled correctly."""
    serializer = JsonSerializer()

    obj = ClassWithSerialize(value=5)
    result = serializer.json_serialize(obj)
    assert isinstance(result, dict)

    # Should use the custom serialize method
    assert result == {"custom_value": 10, "custom_name": "TEST"}
    assert result["custom_value"] == obj.value * 2  # ty: ignore[invalid-argument-type, invalid-key]
    assert result["custom_name"] == obj.name.upper()  # ty: ignore[invalid-argument-type, invalid-key]


def test_serialize_method_priority():
    """Test that .serialize() method takes priority over other handlers."""
    serializer = JsonSerializer()

    # Even though this is a dataclass, the .serialize() method should take priority
    @dataclass
    class DataclassWithSerialize:
        x: int
        y: int

        def serialize(self) -> dict:
            return {"sum": self.x + self.y}

    obj = DataclassWithSerialize(x=3, y=7)
    result = serializer.json_serialize(obj)
    assert isinstance(result, dict)

    # Should use custom serialize, not dataclass handler
    assert result == {"sum": 10}
    assert "x" not in result
    assert "y" not in result


# ============================================================================
# Tests for custom handlers
# ============================================================================


def test_JsonSerializer_custom_handlers():
    """Test adding custom pre/post handlers and verify execution order."""
    # Create a custom handler that captures specific types
    custom_check_count = {"count": 0}
    custom_serialize_count = {"count": 0}

    def custom_check(self, obj, path):
        custom_check_count["count"] += 1
        return isinstance(obj, str) and obj.startswith("CUSTOM:")

    def custom_serialize(self, obj, path):
        custom_serialize_count["count"] += 1
        return {"custom": True, "value": obj[7:]}  # Remove "CUSTOM:" prefix

    custom_handler = SerializerHandler(
        check=custom_check,
        serialize_func=custom_serialize,
        uid="custom_string_handler",
        desc="Custom handler for strings starting with CUSTOM:",
    )

    # Create serializer with custom handler in handlers_pre (before defaults)
    serializer = JsonSerializer(handlers_pre=(custom_handler,))

    # Test that custom handler is used
    result = serializer.json_serialize("CUSTOM:test")
    assert result == {"custom": True, "value": "test"}
    assert custom_serialize_count["count"] == 1

    # Test that normal strings still work (use default handler)
    result = serializer.json_serialize("normal string")
    assert result == "normal string"


def test_custom_handler_execution_order():
    """Test that handlers_pre are executed before default handlers."""
    executed_handlers = []

    def tracking_check(handler_name):
        def check(self, obj, path):
            executed_handlers.append(handler_name)
            return isinstance(obj, dict) and "_test_marker" in obj

        return check

    def tracking_serialize(handler_name):
        def serialize(self, obj, path):
            return {"handled_by": handler_name}

        return serialize

    handler1 = SerializerHandler(
        check=tracking_check("handler1"),
        serialize_func=tracking_serialize("handler1"),
        uid="handler1",
        desc="First custom handler",
    )

    handler2 = SerializerHandler(
        check=tracking_check("handler2"),
        serialize_func=tracking_serialize("handler2"),
        uid="handler2",
        desc="Second custom handler",
    )

    serializer = JsonSerializer(handlers_pre=(handler1, handler2))

    test_obj = {"_test_marker": True}
    result = serializer.json_serialize(test_obj)

    # First handler that matches should be used (handler1)
    assert result == {"handled_by": "handler1"}
    assert executed_handlers[0] == "handler1"


# ============================================================================
# Tests for DEFAULT_HANDLERS
# ============================================================================


def test_DEFAULT_HANDLERS():
    """Test that all default type handlers serialize correctly."""
    serializer = JsonSerializer()

    # Test dataclass
    dc = SimpleDataclass(x=1, y="test", z=False)
    result = serializer.json_serialize(dc)
    assert result == {"x": 1, "y": "test", "z": False}

    # Test namedtuple - should serialize as dict
    Point = namedtuple("Point", ["x", "y"])
    point = Point(10, 20)
    result = serializer.json_serialize(point)
    assert result == {"x": 10, "y": 20}
    assert isinstance(result, dict)

    # Test Path
    path = Path("/home/user/test.txt")
    result = serializer.json_serialize(path)
    assert result == "/home/user/test.txt"
    assert isinstance(result, str)

    # Test set (should become dict with _FORMAT_KEY)
    result = serializer.json_serialize({1, 2, 3})
    assert isinstance(result, dict)
    assert result[_FORMAT_KEY] == "set"
    assert isinstance(result["data"], list)
    assert set(result["data"]) == {1, 2, 3}

    # Test tuple (should become list)
    result = serializer.json_serialize((1, 2, 3))
    assert result == [1, 2, 3]
    assert isinstance(result, list)


def test_BASE_HANDLERS():
    """Test that BASE_HANDLERS work correctly (primitives, dicts, lists, tuples)."""
    serializer = JsonSerializer(handlers_default=BASE_HANDLERS)

    # Base handlers should handle primitives
    assert serializer.json_serialize(42) == 42
    assert serializer.json_serialize("test") == "test"
    assert serializer.json_serialize(True) is True
    assert serializer.json_serialize(None) is None

    # Base handlers should handle dicts and lists
    assert serializer.json_serialize([1, 2, 3]) == [1, 2, 3]
    assert serializer.json_serialize({"a": 1}) == {"a": 1}
    assert serializer.json_serialize((1, 2)) == [1, 2]


def test_fallback_handler():
    """Test that the fallback handler works for unserializable objects."""
    serializer = JsonSerializer()

    obj = UnserializableClass()
    result = serializer.json_serialize(obj)

    # Fallback handler should return dict with special keys
    assert isinstance(result, dict)
    assert "__name__" in result
    assert "__module__" in result
    assert "type" in result
    assert "repr" in result


# ============================================================================
# Tests for nested structures
# ============================================================================


def test_nested_structures():
    """Test serialization of mixed types and nested dicts/lists."""
    serializer = JsonSerializer()

    # Nested dicts and lists
    nested = {"outer": {"inner": [1, 2, {"deep": "value"}]}}
    result = serializer.json_serialize(nested)
    assert result == {"outer": {"inner": [1, 2, {"deep": "value"}]}}

    # List of dicts
    list_of_dicts = [{"a": 1}, {"b": 2}, {"c": 3}]
    result = serializer.json_serialize(list_of_dicts)
    assert result == [{"a": 1}, {"b": 2}, {"c": 3}]

    # Dict of lists
    dict_of_lists = {"nums": [1, 2, 3], "strs": ["a", "b", "c"]}
    result = serializer.json_serialize(dict_of_lists)
    assert result == {"nums": [1, 2, 3], "strs": ["a", "b", "c"]}


def test_nested_dataclasses():
    """Test serialization of nested dataclasses."""
    serializer = JsonSerializer()

    simple = SimpleDataclass(x=5, y="inner", z=True)
    nested = NestedDataclass(simple=simple, data={"key": "value"})

    result = serializer.json_serialize(nested)
    assert result == {
        "simple": {"x": 5, "y": "inner", "z": True},
        "data": {"key": "value"},
    }


def test_deeply_nested_structure():
    """Test very deeply nested structures."""
    serializer = JsonSerializer()

    deep = {"l1": {"l2": {"l3": {"l4": {"l5": [1, 2, 3]}}}}}
    result = serializer.json_serialize(deep)
    assert result == {"l1": {"l2": {"l3": {"l4": {"l5": [1, 2, 3]}}}}}


def test_mixed_types_nested():
    """Test nested structures with mixed types (dataclass, dict, list, primitives)."""
    serializer = JsonSerializer()

    dc = SimpleDataclass(x=100, y="test", z=False)
    mixed = {
        "dataclass": dc,
        "list": [1, 2, dc],
        "nested": {"inner_dc": dc, "values": [10, 20]},
        "primitive": 42,
    }

    result = serializer.json_serialize(mixed)
    expected_dc = {"x": 100, "y": "test", "z": False}
    assert result == {
        "dataclass": expected_dc,
        "list": [1, 2, expected_dc],
        "nested": {"inner_dc": expected_dc, "values": [10, 20]},
        "primitive": 42,
    }


# ============================================================================
# Tests for ErrorMode handling
# ============================================================================


def test_error_mode_except():
    """Test that ErrorMode.EXCEPT raises SerializationException on errors."""

    # Create a handler that always raises an error
    def error_check(self, obj, path):
        return isinstance(obj, str) and obj == "ERROR"

    def error_serialize(self, obj, path):
        raise ValueError("Intentional error")

    error_handler = SerializerHandler(
        check=error_check,
        serialize_func=error_serialize,
        uid="error_handler",
        desc="Handler that raises errors",
    )

    serializer = JsonSerializer(
        error_mode=ErrorMode.EXCEPT, handlers_pre=(error_handler,)
    )

    with pytest.raises(SerializationException) as exc_info:
        serializer.json_serialize("ERROR")

    assert "error serializing" in str(exc_info.value)
    assert "error_handler" in str(exc_info.value)


def test_error_mode_warn():
    """Test that ErrorMode.WARN returns repr on errors and emits warnings."""

    # Create a handler that always raises an error
    def error_check(self, obj, path):
        return isinstance(obj, str) and obj == "ERROR"

    def error_serialize(self, obj, path):
        raise ValueError("Intentional error")

    error_handler = SerializerHandler(
        check=error_check,
        serialize_func=error_serialize,
        uid="error_handler",
        desc="Handler that raises errors",
    )

    serializer = JsonSerializer(
        error_mode=ErrorMode.WARN, handlers_pre=(error_handler,)
    )

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = serializer.json_serialize("ERROR")

        # Should return repr instead of raising
        assert result == "'ERROR'"
        # Should have emitted a warning
        assert len(w) > 0
        assert "error serializing" in str(w[0].message)


def test_error_mode_ignore():
    """Test that ErrorMode.IGNORE returns repr on errors without warnings."""

    # Create a handler that always raises an error
    def error_check(self, obj, path):
        return isinstance(obj, str) and obj == "ERROR"

    def error_serialize(self, obj, path):
        raise ValueError("Intentional error")

    error_handler = SerializerHandler(
        check=error_check,
        serialize_func=error_serialize,
        uid="error_handler",
        desc="Handler that raises errors",
    )

    serializer = JsonSerializer(
        error_mode=ErrorMode.IGNORE, handlers_pre=(error_handler,)
    )

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = serializer.json_serialize("ERROR")

        # Should return repr
        assert result == "'ERROR'"
        # Should not have emitted warnings
        assert len(w) == 0


# ============================================================================
# Tests for write_only_format
# ============================================================================


def test_write_only_format():
    """Test that write_only_format changes _FORMAT_KEY to __write_format__."""

    # Create a handler that outputs _FORMAT_KEY
    def format_check(self, obj, path):
        return isinstance(obj, str) and obj.startswith("FORMAT:")

    def format_serialize(self, obj, path):
        return {_FORMAT_KEY: "custom_format", "data": obj[7:]}

    format_handler = SerializerHandler(
        check=format_check,
        serialize_func=format_serialize,
        uid="format_handler",
        desc="Handler that uses _FORMAT_KEY",
    )

    # Without write_only_format
    serializer1 = JsonSerializer(handlers_pre=(format_handler,))
    result1 = serializer1.json_serialize("FORMAT:test")
    assert isinstance(result1, dict)
    assert _FORMAT_KEY in result1
    assert result1[_FORMAT_KEY] == "custom_format"  # ty: ignore[invalid-argument-type]

    # With write_only_format
    serializer2 = JsonSerializer(handlers_pre=(format_handler,), write_only_format=True)
    result2 = serializer2.json_serialize("FORMAT:test")
    assert isinstance(result2, dict)
    assert _FORMAT_KEY not in result2
    assert "__write_format__" in result2
    assert result2["__write_format__"] == "custom_format"  # ty: ignore[invalid-argument-type, invalid-key]
    assert result2["data"] == "test"  # ty: ignore[invalid-argument-type]


# ============================================================================
# Tests for SerializerHandler.serialize()
# ============================================================================


def test_SerializerHandler_serialize():
    """Test that SerializerHandler can serialize its own metadata."""

    def simple_check(self, obj, path):
        """Check if object is an integer."""
        return isinstance(obj, int)

    def simple_serialize(self, obj, path):
        """Serialize integer."""
        return obj * 2

    handler = SerializerHandler(
        check=simple_check,
        serialize_func=simple_serialize,
        uid="test_handler",
        desc="Test handler description",
    )

    metadata = handler.serialize()

    assert isinstance(metadata, dict)
    assert "check" in metadata
    assert "serialize_func" in metadata
    assert "uid" in metadata
    assert "desc" in metadata

    assert metadata["uid"] == "test_handler"
    assert metadata["desc"] == "Test handler description"

    # Check that code and doc are included
    check_data = metadata["check"]
    assert isinstance(check_data, dict)
    assert "code" in check_data
    assert "doc" in check_data

    serialize_func_data = metadata["serialize_func"]
    assert isinstance(serialize_func_data, dict)
    assert "code" in serialize_func_data
    assert "doc" in serialize_func_data


# ============================================================================
# Tests for hashify
# ============================================================================


def test_hashify():
    """Test JsonSerializer.hashify() method."""
    serializer = JsonSerializer()

    # Test that it converts to hashable types
    result = serializer.hashify({"a": [1, 2, 3]})
    assert isinstance(result, tuple)
    assert result == (("a", (1, 2, 3)),)
    # Should be hashable
    hash(result)

    # Test with list
    result = serializer.hashify([1, 2, 3])
    assert result == (1, 2, 3)
    hash(result)

    # Test with primitive (already hashable)
    result = serializer.hashify(42)
    assert result == 42
    hash(result)


def test_hashify_force():
    """Test hashify with force parameter."""
    serializer = JsonSerializer()

    # With force=True (default), should handle unhashable objects
    obj = UnserializableClass()
    result = serializer.hashify(obj, force=True)
    assert isinstance(result, tuple)  # Converted to hashable form


# ============================================================================
# Tests for path tracking
# ============================================================================


def test_path_tracking():
    """Test that paths are correctly tracked through nested serialization."""
    paths_seen = []

    def tracking_check(self, obj, path):
        paths_seen.append(path)
        return False  # Never actually handle, just track

    tracking_handler = SerializerHandler(
        check=tracking_check,
        serialize_func=lambda self, obj, path: obj,
        uid="tracking",
        desc="Path tracking handler",
    )

    serializer = JsonSerializer(handlers_pre=(tracking_handler,))

    # Serialize nested structure
    nested = {"a": {"b": [1, 2]}}
    serializer.json_serialize(nested)

    # Check that we saw paths for nested elements
    assert tuple() in paths_seen  # Root
    assert ("a",) in paths_seen  # nested dict
    assert ("a", "b") in paths_seen  # nested list
    assert ("a", "b", 0) in paths_seen  # first element
    assert ("a", "b", 1) in paths_seen  # second element


# ============================================================================
# Tests for initialization
# ============================================================================


def test_JsonSerializer_init_no_positional_args():
    """Test that JsonSerializer raises ValueError on positional arguments."""
    with pytest.raises(ValueError, match="no positional arguments"):
        JsonSerializer("invalid", "args")  # type: ignore[arg-type]

    # Should work with keyword args
    serializer = JsonSerializer(error_mode=ErrorMode.WARN)
    assert serializer.error_mode == ErrorMode.WARN


def test_JsonSerializer_init_defaults():
    """Test JsonSerializer default initialization values."""
    serializer = JsonSerializer()

    assert serializer.array_mode == "array_list_meta"
    assert serializer.error_mode == ErrorMode.EXCEPT
    assert serializer.write_only_format is False
    assert serializer.handlers == DEFAULT_HANDLERS


def test_JsonSerializer_init_custom_values():
    """Test JsonSerializer with custom initialization values."""
    custom_handler = SerializerHandler(
        check=lambda self, obj, path: False,
        serialize_func=lambda self, obj, path: obj,
        uid="custom",
        desc="Custom handler",
    )

    serializer = JsonSerializer(
        array_mode="list",
        error_mode=ErrorMode.WARN,
        handlers_pre=(custom_handler,),
        handlers_default=BASE_HANDLERS,
        write_only_format=True,
    )

    assert serializer.array_mode == "list"
    assert serializer.error_mode == ErrorMode.WARN
    assert serializer.write_only_format is True
    assert serializer.handlers[0] == custom_handler
    assert len(serializer.handlers) == len(BASE_HANDLERS) + 1


# ============================================================================
# Edge cases and integration tests
# ============================================================================


def test_empty_handlers():
    """Test serializer with no handlers."""
    serializer = JsonSerializer(handlers_default=tuple())

    # Should fail to serialize anything
    with pytest.raises(SerializationException):
        serializer.json_serialize(42)


# TODO: Implement circular reference protection in the future. see https://github.com/mivanit/muutils/issues/62
@pytest.mark.skip(
    reason="we don't currently have circular reference protection, see https://github.com/mivanit/muutils/issues/62"
)
def test_circular_reference_protection():
    """Test that circular references don't cause infinite loops (will hit recursion limit)."""
    # Note: This test verifies the expected behavior (recursion error) rather than
    # infinite loop, as the module doesn't explicitly handle circular references
    serializer = JsonSerializer()

    # Create circular reference
    circular = {"a": None}
    circular["a"] = circular  # type: ignore

    # Should eventually raise RecursionError
    with pytest.raises(RecursionError):
        serializer.json_serialize(circular)


def test_large_nested_structure():
    """Test serialization of large nested structure."""
    serializer = JsonSerializer()

    # Create large nested list
    large = [[i, i * 2, i * 3] for i in range(100)]
    result = serializer.json_serialize(large)
    assert isinstance(result, list)
    assert len(result) == 100
    assert result[0] == [0, 0, 0]
    assert result[99] == [99, 198, 297]


def test_mixed_container_types():
    """Test serialization of sets, frozensets, and other iterables."""
    serializer = JsonSerializer()

    # Set - serialized with format key
    result = serializer.json_serialize({3, 1, 2})
    assert isinstance(result, dict)
    assert _FORMAT_KEY in result
    assert result[_FORMAT_KEY] == "set"
    assert isinstance(result["data"], list)
    assert set(result["data"]) == {1, 2, 3}

    # Frozenset - serialized with format key
    result = serializer.json_serialize(frozenset([4, 5, 6]))
    assert isinstance(result, dict)
    assert _FORMAT_KEY in result
    assert result[_FORMAT_KEY] == "frozenset"
    assert isinstance(result["data"], list)
    assert set(result["data"]) == {4, 5, 6}

    # Generator (Iterable) - serialized as list
    gen = (x * 2 for x in range(3))
    result = serializer.json_serialize(gen)
    assert result == [0, 2, 4]


def test_string_keys_in_dict():
    """Test that dict keys are converted to strings."""
    serializer = JsonSerializer()

    # Integer keys should be converted to strings
    result = serializer.json_serialize({1: "a", 2: "b", 3: "c"})
    assert isinstance(result, dict)
    assert result == {"1": "a", "2": "b", "3": "c"}
    assert all(isinstance(k, str) for k in result.keys())
