"""Tests for muutils.json_serialize.serializable_field module.

Tests the SerializableField class and serializable_field function,
which extend dataclasses.Field with serialization capabilities.
"""

from __future__ import annotations

import dataclasses
from dataclasses import field
from typing import Any

import pytest

from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)
from muutils.json_serialize.serializable_field import SerializableField


# ============================================================================
# Test SerializableField creation with various parameters
# ============================================================================


def test_SerializableField_creation():
    """Test creating SerializableField with various parameters."""
    # Basic creation with default parameters
    sf1 = SerializableField()
    assert sf1.serialize is True
    assert sf1.serialization_fn is None
    assert sf1.loading_fn is None
    assert sf1.deserialize_fn is None
    assert sf1.assert_type is True
    assert sf1.custom_typecheck_fn is None
    assert sf1.default is dataclasses.MISSING
    assert sf1.default_factory is dataclasses.MISSING

    # Creation with default value
    sf2 = SerializableField(default=42)
    assert sf2.default == 42
    assert sf2.init is True
    assert sf2.repr is True
    assert sf2.compare is True

    # Creation with default_factory
    sf3 = SerializableField(default_factory=list)
    assert sf3.default_factory == list  # noqa: E721
    assert sf3.default is dataclasses.MISSING

    # Creation with custom parameters
    sf4 = SerializableField(
        default=100,
        init=True,
        repr=False,
        hash=True,
        compare=False,
        serialize=True,
    )
    assert sf4.default == 100
    assert sf4.init is True
    assert sf4.repr is False
    assert sf4.hash is True
    assert sf4.compare is False
    assert sf4.serialize is True

    # Creation with serialization parameters
    def custom_serialize(x):
        return str(x)

    def custom_deserialize(x):
        return int(x)

    sf5 = SerializableField(
        serialization_fn=custom_serialize,
        deserialize_fn=custom_deserialize,
        assert_type=False,
    )
    assert sf5.serialization_fn == custom_serialize
    assert sf5.deserialize_fn == custom_deserialize
    assert sf5.assert_type is False


def test_SerializableField_init_serialize_validation():
    """Test that init=True and serialize=False raises ValueError."""
    with pytest.raises(ValueError, match="Cannot have init=True and serialize=False"):
        SerializableField(init=True, serialize=False)


def test_SerializableField_loading_deserialize_conflict():
    """Test that passing both loading_fn and deserialize_fn raises ValueError."""

    def dummy_fn(x):
        return x

    with pytest.raises(
        ValueError, match="Cannot pass both loading_fn and deserialize_fn"
    ):
        SerializableField(loading_fn=dummy_fn, deserialize_fn=dummy_fn)


def test_SerializableField_doc():
    """Test doc parameter handling across Python versions."""
    sf = SerializableField(doc="Test documentation")
    assert sf.doc == "Test documentation"


# ============================================================================
# Test from_Field() method
# ============================================================================


def test_from_Field():
    """Test converting a dataclasses.Field to SerializableField."""
    # Create a standard dataclasses.Field
    dc_field: dataclasses.Field[int] = field(  # type: ignore[assignment]
        default=42,
        init=True,
        repr=True,
        hash=None,
        compare=True,
    )

    # Convert to SerializableField
    sf = SerializableField.from_Field(dc_field)

    # Verify all standard Field properties were copied
    assert sf.default == 42
    assert sf.init is True
    assert sf.repr is True
    assert sf.hash is None
    assert sf.compare is True

    # Verify SerializableField-specific properties have defaults
    assert sf.serialize == sf.repr  # serialize defaults to repr value
    assert sf.serialization_fn is None
    assert sf.loading_fn is None
    assert sf.deserialize_fn is None

    # Test with default_factory and init=False to avoid init=True, serialize=False error
    dc_field2: dataclasses.Field[list[Any]] = field(
        default_factory=list, repr=True, init=True
    )  # type: ignore[assignment]
    sf2 = SerializableField.from_Field(dc_field2)
    assert sf2.default_factory == list  # noqa: E721
    assert sf2.default is dataclasses.MISSING
    assert sf2.serialize is True  # should match repr=True


# ============================================================================
# Test serialization_fn and deserialize_fn
# ============================================================================


def test_serialization_deserialize_fn():
    """Test custom serialization and deserialization functions."""

    @serializable_dataclass
    class CustomSerialize(SerializableDataclass):
        # Serialize as uppercase, deserialize as lowercase
        value: str = serializable_field(
            serialization_fn=lambda x: x.upper(),
            deserialize_fn=lambda x: x.lower(),
        )

    # Test serialization
    instance = CustomSerialize(value="Hello")
    serialized = instance.serialize()
    assert serialized["value"] == "HELLO"

    # Test deserialization
    loaded = CustomSerialize.load({"value": "WORLD"})
    assert loaded.value == "world"


def test_serialization_fn_with_complex_type():
    """Test serialization_fn with more complex transformations."""

    @serializable_dataclass
    class ComplexSerialize(SerializableDataclass):
        # Store a tuple as a list
        coords: tuple[int, int] = serializable_field(
            default=(0, 0),
            serialization_fn=lambda x: list(x),
            deserialize_fn=lambda x: tuple(x),
        )

    instance = ComplexSerialize(coords=(3, 4))
    serialized = instance.serialize()
    assert serialized["coords"] == [3, 4]  # serialized as list

    loaded = ComplexSerialize.load({"coords": [5, 6]})
    assert loaded.coords == (5, 6)  # loaded as tuple


# ============================================================================
# Test loading_fn (takes full data dict)
# ============================================================================


def test_loading_fn():
    """Test loading_fn which takes the full data dict."""

    @serializable_dataclass
    class WithLoadingFn(SerializableDataclass):
        x: int
        y: int
        # computed field that depends on other fields
        sum_xy: int = serializable_field(
            init=False,
            serialize=False,
            default=0,
        )

    # Create instance
    instance = WithLoadingFn(x=3, y=4)
    instance.sum_xy = instance.x + instance.y
    assert instance.sum_xy == 7


def test_loading_fn_vs_deserialize_fn():
    """Test the difference between loading_fn (dict) and deserialize_fn (value)."""

    @serializable_dataclass
    class WithLoadingFn(SerializableDataclass):
        value: int = serializable_field(
            serialization_fn=lambda x: x * 2,
            loading_fn=lambda data: data["value"] // 2,  # takes full dict
        )

    @serializable_dataclass
    class WithDeserializeFn(SerializableDataclass):
        value: int = serializable_field(
            serialization_fn=lambda x: x * 2,
            deserialize_fn=lambda x: x // 2,  # takes just the value
        )

    # Both should behave the same in this case
    instance1 = WithLoadingFn(value=10)
    serialized1 = instance1.serialize()
    assert serialized1["value"] == 20

    loaded1 = WithLoadingFn.load({"value": 20})
    assert loaded1.value == 10

    instance2 = WithDeserializeFn(value=10)
    serialized2 = instance2.serialize()
    assert serialized2["value"] == 20

    loaded2 = WithDeserializeFn.load({"value": 20})
    assert loaded2.value == 10


# ============================================================================
# Test field validation: assert_type and custom_typecheck_fn
# ============================================================================


def test_field_validation_assert_type():
    """Test assert_type parameter for type validation."""

    @serializable_dataclass
    class StrictType(SerializableDataclass):
        value: int = serializable_field(assert_type=True)

    @serializable_dataclass
    class LooseType(SerializableDataclass):
        value: int = serializable_field(assert_type=False)

    # Strict type checking should warn with wrong type (using WARN mode by default)
    with pytest.warns(UserWarning, match="Type mismatch"):
        instance = StrictType.load({"value": "not an int"})
        assert instance.value == "not an int"

    # Loose type checking should allow wrong type without warning
    instance2 = LooseType.load({"value": "not an int"})
    assert instance2.value == "not an int"


def test_field_validation_custom_typecheck_fn():
    """Test custom_typecheck_fn for custom type validation."""

    def is_positive(value: Any) -> bool:
        """Check if value is a positive number."""
        return isinstance(value, (int, float)) and value > 0

    @serializable_dataclass
    class PositiveNumber(SerializableDataclass):
        value: int = serializable_field(
            custom_typecheck_fn=lambda t: True  # Accept any type
        )

    # This should work because custom_typecheck_fn returns True
    instance = PositiveNumber(value=42)
    assert instance.value == 42


# ============================================================================
# Test serializable_field() function
# ============================================================================


def test_serializable_field_function():
    """Test the serializable_field() function wrapper."""
    # Test basic usage
    f1 = serializable_field()
    assert isinstance(f1, SerializableField)
    assert f1.serialize is True

    # Test with default
    f2: SerializableField = serializable_field(default=100)  # type: ignore[assignment]
    assert f2.default == 100

    # Test with default_factory
    f3: SerializableField = serializable_field(default_factory=list)  # type: ignore[assignment]
    assert f3.default_factory == list  # noqa: E721

    # Test with all parameters
    f4: SerializableField = serializable_field(  # type: ignore[assignment]
        default=42,
        init=True,
        repr=False,
        hash=True,
        compare=False,
        serialize=True,
        serialization_fn=str,
        deserialize_fn=int,
        assert_type=False,
    )
    assert f4.default == 42
    assert f4.repr is False
    assert f4.hash is True
    assert f4.serialization_fn == str  # noqa: E721
    assert f4.deserialize_fn == int  # noqa: E721


def test_serializable_field_no_positional_args():
    """Test that serializable_field doesn't accept positional arguments."""
    with pytest.raises(AssertionError, match="unexpected positional arguments"):
        serializable_field("invalid")  # type: ignore


def test_serializable_field_description_deprecated():
    """Test that 'description' parameter is deprecated in favor of 'doc'."""
    import warnings

    # Using description should raise DeprecationWarning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        f = serializable_field(description="Test description")
        # Check that a deprecation warning was issued
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "`description` is deprecated" in str(w[0].message)
        # Verify doc was set
        assert f.doc == "Test description"

    # Using both doc and description should raise ValueError
    with pytest.raises(ValueError, match="cannot pass both"):
        serializable_field(doc="Doc", description="Description")


# ============================================================================
# Integration tests with SerializableDataclass
# ============================================================================


def test_serializable_field_integration():
    """Test SerializableField integration with SerializableDataclass."""

    @serializable_dataclass
    class IntegrationTest(SerializableDataclass):
        # Regular field
        normal: str

        # Field with custom serialization (no default, so must come before fields with defaults)
        custom: str = serializable_field(
            serialization_fn=lambda x: x.upper(),
            deserialize_fn=lambda x: x.lower(),
        )

        # Field with default
        with_default: int = serializable_field(default=42)

        # Field with default_factory
        with_factory: list = serializable_field(default_factory=list)

        # Non-serialized field
        internal: int = serializable_field(init=False, serialize=False, default=0)

    # Create instance
    instance = IntegrationTest(
        normal="test",
        custom="hello",
        with_default=100,
        with_factory=[1, 2, 3],
    )
    instance.internal = 999

    # Serialize
    serialized = instance.serialize()
    assert serialized["normal"] == "test"
    assert serialized["with_default"] == 100
    assert serialized["with_factory"] == [1, 2, 3]
    assert serialized["custom"] == "HELLO"  # uppercase
    assert "internal" not in serialized  # not serialized

    # Load
    loaded = IntegrationTest.load(
        {
            "normal": "loaded",
            "custom": "WORLD",
            "with_default": 200,
            "with_factory": [4, 5],
        }
    )
    assert loaded.normal == "loaded"
    assert loaded.with_default == 200
    assert loaded.with_factory == [4, 5]
    assert loaded.custom == "world"  # lowercase
    assert loaded.internal == 0  # default value
