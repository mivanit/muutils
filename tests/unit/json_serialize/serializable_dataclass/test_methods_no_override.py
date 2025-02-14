from typing import Any
import typing

import pytest

# Import the decorator and base class.
# (Adjust the import below to match your project structure.)
from muutils.json_serialize import (
    serializable_dataclass,
    SerializableDataclass,
)
from muutils.json_serialize.util import _FORMAT_KEY


@serializable_dataclass
class SimpleClass(SerializableDataclass):
    a: int
    b: str


def test_simple_class_serialization():
    simple = SimpleClass(a=42, b="hello")
    serialized = simple.serialize()
    assert serialized == {
        "a": 42,
        "b": "hello",
        _FORMAT_KEY: "SimpleClass(SerializableDataclass)",
    }

    loaded = SimpleClass.load(serialized)
    assert loaded == simple


def test_default_overrides():
    """Test that by default the decorator overrides __eq__, serialize, load, and validate_fields_types."""

    @serializable_dataclass
    class DefaultClass(SerializableDataclass):
        a: int
        b: str

    # Instantiate and serialize.
    obj: DefaultClass = DefaultClass(a=1, b="test")
    ser: typing.Dict[str, Any] = obj.serialize()
    # Check that the _FORMAT_KEY is present with the correct value.
    assert ser.get(_FORMAT_KEY) == "DefaultClass(SerializableDataclass)"
    assert ser.get("a") == 1
    assert ser.get("b") == "test"

    # Test load method: re-create the object from its serialization.
    loaded: DefaultClass = DefaultClass.load(ser)
    # Equality is provided by the decorator (via dc_eq).
    assert loaded == obj

    # Check that validate_fields_types works (should be True with correct types).
    assert obj.validate_fields_types() is True

    # Test __eq__ by comparing two instances with same values.
    obj2: DefaultClass = DefaultClass(a=1, b="test")
    assert obj == obj2
    obj3: DefaultClass = DefaultClass(a=2, b="test")
    assert obj != obj3


def test_no_override_serialize():
    """Test that specifying 'serialize' in methods_no_override preserves the user-defined serialize method."""

    @serializable_dataclass(methods_no_override=["serialize"], register_handler=False)
    class NoSerializeClass(SerializableDataclass):
        a: int

        def serialize(self) -> typing.Dict[str, Any]:
            # Custom serialization (ignoring the _FORMAT_KEY mechanism)
            return {"custom": self.a}

    obj: NoSerializeClass = NoSerializeClass(a=42)
    ser: typing.Dict[str, Any] = obj.serialize()
    # The custom serialize should be preserved.
    assert ser == {"custom": 42}

    # The load method is still provided by the decorator.
    loaded: NoSerializeClass = NoSerializeClass.load({"a": 42})
    # Since load uses the type hints to call the constructor, it will create an instance with a==42.
    assert loaded.a == 42

    # __eq__ should be the decorator's version (via dc_eq).
    obj2: NoSerializeClass = NoSerializeClass(a=42)
    assert obj == obj2


def test_no_override_eq_and_serialize():
    """Test that specifying both '__eq__' and 'serialize' in methods_no_override preserves the user-defined methods,
    while load and validate_fields_types are still overridden."""

    @serializable_dataclass(
        methods_no_override=["__eq__", "serialize"], register_handler=False
    )
    class NoEqSerializeClass(SerializableDataclass):
        a: int

        def __eq__(self, other: Any) -> bool:
            if not isinstance(other, NoEqSerializeClass):
                return False
            # Custom equality: only compare the 'a' attribute.
            return self.a == other.a

        def serialize(self) -> typing.Dict[str, Any]:
            return {"custom_serialize": self.a}

    obj1: NoEqSerializeClass = NoEqSerializeClass(a=100)
    obj2: NoEqSerializeClass = NoEqSerializeClass(a=100)
    obj3: NoEqSerializeClass = NoEqSerializeClass(a=200)

    # Check that the custom serialize is used.
    assert obj1.serialize() == {"custom_serialize": 100}

    # Check that the custom __eq__ is used.
    assert obj1 == obj2
    assert obj1 != obj3

    # The load method should be the decorator's version.
    loaded: NoEqSerializeClass = NoEqSerializeClass.load({"a": 100})
    assert loaded.a == 100

    # validate_fields_types should be provided by the decorator.
    assert obj1.validate_fields_types() is True


def test_inheritance_override():
    """Test behavior when inheritance is involved:
    - A base class with a custom serialize (preserved via methods_no_override)
      and a subclass that does not preserve it gets the decorator's version.
    - A subclass that preserves 'serialize' keeps the custom method from the base.
    """

    @serializable_dataclass(methods_no_override=["serialize"], register_handler=False)
    class BaseClass(SerializableDataclass):
        a: int

        def serialize(self) -> typing.Dict[str, Any]:
            return {"base": self.a}

    # SubClass without preserving 'serialize': decorator will override.
    @serializable_dataclass(register_handler=False)
    class SubClass(BaseClass):
        b: int

    # SubClassPreserve preserves serialize (and hence inherits BaseClass.serialize).
    @serializable_dataclass(methods_no_override=["serialize"], register_handler=False)
    class SubClassPreserve(BaseClass):
        b: int

    base_obj: BaseClass = BaseClass(a=10)
    # Custom serialize from BaseClass is preserved.
    assert base_obj.serialize() == {"base": 10}

    sub_obj: SubClass = SubClass(a=1, b=2)
    ser_sub: typing.Dict[str, Any] = sub_obj.serialize()
    # Since SubClass does not preserve serialize, it gets the decorator version.
    # It will include the _FORMAT_KEY and the field values.
    assert _FORMAT_KEY in ser_sub
    assert ser_sub.get("a") == 1
    assert ser_sub.get("b") == 2

    sub_preserve: SubClassPreserve = SubClassPreserve(a=20, b=30)
    # This subclass preserves its custom (inherited) serialize from BaseClass.
    assert sub_preserve.serialize() == {"base": 20}


def test_polymorphic_behavior():
    """Test that polymorphic classes can use different serialize implementations based on methods_no_override."""

    @serializable_dataclass(methods_no_override=["serialize"], register_handler=False)
    class PolyA(SerializableDataclass):
        a: int

        def serialize(self) -> typing.Dict[str, Any]:
            return {"poly_a": self.a}

    @serializable_dataclass(register_handler=False)
    class PolyB(SerializableDataclass):
        b: int

    a_obj: PolyA = PolyA(a=5)
    b_obj: PolyB = PolyB(b=15)

    # PolyA uses its custom serialize.
    assert a_obj.serialize() == {"poly_a": 5}

    # PolyB uses the default decorator-provided serialize.
    ser_b: typing.Dict[str, Any] = b_obj.serialize()
    assert ser_b.get(_FORMAT_KEY) == "PolyB(SerializableDataclass)"
    assert ser_b.get("b") == 15

    # Equality and load should work polymorphically.
    a_loaded: PolyA = PolyA.load({"a": 5})
    b_loaded: PolyB = PolyB.load({"b": 15})
    assert a_loaded.a == 5
    assert b_loaded.b == 15


def test_unknown_methods_warning():
    """Test that if unknown method names are passed to methods_no_override, a warning is issued."""
    with pytest.warns(UserWarning, match="Unknown methods in `methods_no_override`"):

        @serializable_dataclass(
            methods_no_override=["non_existing_method"], register_handler=False
        )
        class UnknownMethodClass(SerializableDataclass):
            a: int

    # Even though the warning is raised, the class should still work normally.
    obj: UnknownMethodClass = UnknownMethodClass(a=999)
    ser: typing.Dict[str, Any] = obj.serialize()
    # Since "serialize" was not preserved, decorator provides it.
    assert _FORMAT_KEY in ser
    assert ser.get("a") == 999
