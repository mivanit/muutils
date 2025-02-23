from __future__ import annotations

from copy import deepcopy
import typing
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import pytest

from muutils.errormode import ErrorMode
from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)

from muutils.json_serialize.serializable_dataclass import (
    FieldIsNotInitOrSerializeWarning,
    FieldTypeMismatchError,
)
from muutils.json_serialize.util import _FORMAT_KEY

# pylint: disable=missing-class-docstring, unused-variable


@serializable_dataclass
class BasicAutofields(SerializableDataclass):
    a: str
    b: int
    c: typing.List[int]


def test_basic_auto_fields():
    data = dict(a="hello", b=42, c=[1, 2, 3])
    instance = BasicAutofields(**data)  # type: ignore[arg-type]
    data_with_format = data.copy()
    data_with_format[_FORMAT_KEY] = "BasicAutofields(SerializableDataclass)"
    assert instance.serialize() == data_with_format
    assert instance == instance
    assert instance.diff(instance) == {}


def test_basic_diff():
    instance_1 = BasicAutofields(a="hello", b=42, c=[1, 2, 3])
    instance_2 = BasicAutofields(a="goodbye", b=42, c=[1, 2, 3])
    instance_3 = BasicAutofields(a="hello", b=-1, c=[1, 2, 3])
    instance_4 = BasicAutofields(a="hello", b=-1, c=[42])

    assert instance_1.diff(instance_2) == {"a": {"self": "hello", "other": "goodbye"}}
    assert instance_1.diff(instance_3) == {"b": {"self": 42, "other": -1}}
    assert instance_1.diff(instance_4) == {
        "b": {"self": 42, "other": -1},
        "c": {"self": [1, 2, 3], "other": [42]},
    }
    assert instance_1.diff(instance_1) == {}
    assert instance_2.diff(instance_3) == {
        "a": {"self": "goodbye", "other": "hello"},
        "b": {"self": 42, "other": -1},
    }


@serializable_dataclass
class SimpleFields(SerializableDataclass):
    d: str
    e: int = 42
    f: typing.List[int] = serializable_field(default_factory=list)  # noqa: F821


@serializable_dataclass
class FieldOptions(SerializableDataclass):
    a: str = serializable_field()
    b: str = serializable_field()
    c: str = serializable_field(init=False, serialize=False, repr=False, compare=False)
    d: str = serializable_field(
        serialization_fn=lambda x: x.upper(), loading_fn=lambda x: x["d"].lower()
    )


@serializable_dataclass(properties_to_serialize=["full_name"])
class WithProperty(SerializableDataclass):
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Child(FieldOptions, WithProperty):
    pass


@pytest.fixture
def simple_fields_instance():
    return SimpleFields(d="hello", e=42, f=[1, 2, 3])


@pytest.fixture
def field_options_instance():
    return FieldOptions(a="hello", b="world", d="case")


@pytest.fixture
def with_property_instance():
    return WithProperty(first_name="John", last_name="Doe")


def test_simple_fields_serialization(simple_fields_instance):
    serialized = simple_fields_instance.serialize()
    assert serialized == {
        "d": "hello",
        "e": 42,
        "f": [1, 2, 3],
        _FORMAT_KEY: "SimpleFields(SerializableDataclass)",
    }


def test_simple_fields_loading(simple_fields_instance):
    serialized = simple_fields_instance.serialize()

    loaded = SimpleFields.load(serialized)

    assert loaded == simple_fields_instance
    assert loaded.diff(simple_fields_instance) == {}
    assert simple_fields_instance.diff(loaded) == {}


def test_field_options_serialization(field_options_instance):
    serialized = field_options_instance.serialize()
    assert serialized == {
        "a": "hello",
        "b": "world",
        "d": "CASE",
        _FORMAT_KEY: "FieldOptions(SerializableDataclass)",
    }


def test_field_options_loading(field_options_instance):
    # ignore a `FieldIsNotInitOrSerializeWarning`
    serialized = field_options_instance.serialize()
    with pytest.warns(FieldIsNotInitOrSerializeWarning):
        loaded = FieldOptions.load(serialized)
    assert loaded == field_options_instance


def test_with_property_serialization(with_property_instance):
    serialized = with_property_instance.serialize()
    assert serialized == {
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        _FORMAT_KEY: "WithProperty(SerializableDataclass)",
    }


def test_with_property_loading(with_property_instance):
    serialized = with_property_instance.serialize()
    loaded = WithProperty.load(serialized)
    assert loaded == with_property_instance


@serializable_dataclass
class Address(SerializableDataclass):
    street: str
    city: str
    zip_code: str


@serializable_dataclass
class Person(SerializableDataclass):
    name: str
    age: int
    address: Address


@pytest.fixture
def address_instance():
    return Address(street="123 Main St", city="New York", zip_code="10001")


@pytest.fixture
def person_instance(address_instance):
    return Person(name="John Doe", age=30, address=address_instance)


def test_nested_serialization(person_instance):
    serialized = person_instance.serialize()
    expected_ser = {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zip_code": "10001",
            _FORMAT_KEY: "Address(SerializableDataclass)",
        },
        _FORMAT_KEY: "Person(SerializableDataclass)",
    }
    assert serialized == expected_ser


def test_nested_loading(person_instance):
    serialized = person_instance.serialize()
    loaded = Person.load(serialized)
    assert loaded == person_instance
    assert loaded.address == person_instance.address


def test_with_printing():
    @serializable_dataclass(properties_to_serialize=["full_name"])
    class MyClass(SerializableDataclass):
        name: str
        age: int = serializable_field(
            serialization_fn=lambda x: x + 1, loading_fn=lambda x: x["age"] - 1
        )
        items: list = serializable_field(default_factory=list)

        @property
        def full_name(self) -> str:
            return f"{self.name} Doe"

    # Usage
    my_instance = MyClass(name="John", age=30, items=["apple", "banana"])
    serialized_data = my_instance.serialize()
    print(serialized_data)

    loaded_instance = MyClass.load(serialized_data)
    print(loaded_instance)


def test_simple_class_serialization():
    @serializable_dataclass
    class SimpleClass(SerializableDataclass):
        a: int
        b: str

    simple = SimpleClass(a=42, b="hello")
    serialized = simple.serialize()
    assert serialized == {
        "a": 42,
        "b": "hello",
        _FORMAT_KEY: "SimpleClass(SerializableDataclass)",
    }

    loaded = SimpleClass.load(serialized)
    assert loaded == simple


def test_error_when_init_and_not_serialize():
    with pytest.raises(ValueError):

        @serializable_dataclass
        class SimpleClass(SerializableDataclass):
            a: int = serializable_field(init=True, serialize=False)


def test_person_serialization():
    @serializable_dataclass(properties_to_serialize=["full_name"])
    class FullPerson(SerializableDataclass):
        name: str = serializable_field()
        age: int = serializable_field(default=-1)
        items: typing.List[str] = serializable_field(default_factory=list)

        @property
        def full_name(self) -> str:
            return f"{self.name} Doe"

    person = FullPerson(name="John", items=["apple", "banana"])
    serialized = person.serialize()
    expected_ser = {
        "name": "John",
        "age": -1,
        "items": ["apple", "banana"],
        "full_name": "John Doe",
        _FORMAT_KEY: "FullPerson(SerializableDataclass)",
    }
    assert serialized == expected_ser, f"Expected {expected_ser}, got {serialized}"

    loaded = FullPerson.load(serialized)

    assert loaded == person


def test_custom_serialization():
    @serializable_dataclass
    class CustomSerialization(SerializableDataclass):
        data: Any = serializable_field(
            serialization_fn=lambda x: x * 2, loading_fn=lambda x: x["data"] // 2
        )

    custom = CustomSerialization(data=5)
    serialized = custom.serialize()
    assert serialized == {
        "data": 10,
        _FORMAT_KEY: "CustomSerialization(SerializableDataclass)",
    }

    loaded = CustomSerialization.load(serialized)
    assert loaded == custom


@serializable_dataclass
class Nested_with_Container(SerializableDataclass):
    val_int: int
    val_str: str
    val_list: typing.List[BasicAutofields] = serializable_field(
        default_factory=list,
        serialization_fn=lambda x: [y.serialize() for y in x],
        loading_fn=lambda x: [BasicAutofields.load(y) for y in x["val_list"]],
    )


def test_nested_with_container():
    instance = Nested_with_Container(
        val_int=42,
        val_str="hello",
        val_list=[
            BasicAutofields(a="a", b=1, c=[1, 2, 3]),
            BasicAutofields(a="b", b=2, c=[4, 5, 6]),
        ],
    )

    serialized = instance.serialize()
    expected_ser = {
        "val_int": 42,
        "val_str": "hello",
        "val_list": [
            {
                "a": "a",
                "b": 1,
                "c": [1, 2, 3],
                _FORMAT_KEY: "BasicAutofields(SerializableDataclass)",
            },
            {
                "a": "b",
                "b": 2,
                "c": [4, 5, 6],
                _FORMAT_KEY: "BasicAutofields(SerializableDataclass)",
            },
        ],
        _FORMAT_KEY: "Nested_with_Container(SerializableDataclass)",
    }

    assert serialized == expected_ser

    loaded = Nested_with_Container.load(serialized)

    assert loaded == instance


class Custom_class_with_serialization:
    """custom class which doesnt inherit but does serialize"""

    def __init__(self, a: int, b: str):
        self.a: int = a
        self.b: str = b

    def serialize(self):
        return {"a": self.a, "b": self.b}

    @classmethod
    def load(cls, data):
        return cls(data["a"], data["b"])

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)


@serializable_dataclass
class nested_custom(SerializableDataclass):
    value: float
    data1: Custom_class_with_serialization


def test_nested_custom(recwarn):  # this will send some warnings but whatever
    instance = nested_custom(
        value=42.0, data1=Custom_class_with_serialization(1, "hello")
    )
    serialized = instance.serialize()
    expected_ser = {
        "value": 42.0,
        "data1": {"a": 1, "b": "hello"},
        _FORMAT_KEY: "nested_custom(SerializableDataclass)",
    }
    assert serialized == expected_ser
    loaded = nested_custom.load(serialized)
    assert loaded == instance


def test_deserialize_fn():
    @serializable_dataclass
    class DeserializeFn(SerializableDataclass):
        data: int = serializable_field(
            serialization_fn=lambda x: str(x),
            deserialize_fn=lambda x: int(x),
        )

    instance = DeserializeFn(data=5)
    serialized = instance.serialize()
    assert serialized == {
        "data": "5",
        _FORMAT_KEY: "DeserializeFn(SerializableDataclass)",
    }

    loaded = DeserializeFn.load(serialized)
    assert loaded == instance
    assert loaded.data == 5


@serializable_dataclass
class DictContainer(SerializableDataclass):
    """Test class containing a dictionary field"""

    simple_dict: Dict[str, int]
    nested_dict: Dict[str, Dict[str, int]] = serializable_field(default_factory=dict)
    optional_dict: Dict[str, str] = serializable_field(default_factory=dict)


def test_dict_serialization():
    """Test serialization of dictionaries within SerializableDataclass"""
    data = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "world"},
    )

    serialized = data.serialize()
    expected = {
        _FORMAT_KEY: "DictContainer(SerializableDataclass)",
        "simple_dict": {"a": 1, "b": 2},
        "nested_dict": {"x": {"y": 3, "z": 4}},
        "optional_dict": {"hello": "world"},
    }

    assert serialized == expected


def test_dict_loading():
    """Test loading dictionaries into SerializableDataclass"""
    original_data = {
        _FORMAT_KEY: "DictContainer(SerializableDataclass)",
        "simple_dict": {"a": 1, "b": 2},
        "nested_dict": {"x": {"y": 3, "z": 4}},
        "optional_dict": {"hello": "world"},
    }

    loaded = DictContainer.load(original_data)
    assert loaded.simple_dict == {"a": 1, "b": 2}
    assert loaded.nested_dict == {"x": {"y": 3, "z": 4}}
    assert loaded.optional_dict == {"hello": "world"}


def test_dict_equality():
    """Test equality comparison of dictionaries within SerializableDataclass"""
    instance1 = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "world"},
    )

    instance2 = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "world"},
    )

    instance3 = DictContainer(
        simple_dict={"a": 1, "b": 3},  # Different value
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "world"},
    )

    assert instance1 == instance2
    assert instance1 != instance3
    assert instance2 != instance3


def test_dict_diff():
    """Test diff functionality with dictionaries"""
    instance1 = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "world"},
    )

    # Different simple_dict value
    instance2 = DictContainer(
        simple_dict={"a": 1, "b": 3},
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "world"},
    )

    # Different nested_dict value
    instance3 = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3, "z": 5}},
        optional_dict={"hello": "world"},
    )

    # Different optional_dict value
    instance4 = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3, "z": 4}},
        optional_dict={"hello": "python"},
    )

    # Test diff with simple_dict changes
    diff1 = instance1.diff(instance2)
    assert diff1 == {
        "simple_dict": {"self": {"a": 1, "b": 2}, "other": {"a": 1, "b": 3}}
    }

    # Test diff with nested_dict changes
    diff2 = instance1.diff(instance3)
    assert diff2 == {
        "nested_dict": {
            "self": {"x": {"y": 3, "z": 4}},
            "other": {"x": {"y": 3, "z": 5}},
        }
    }

    # Test diff with optional_dict changes
    diff3 = instance1.diff(instance4)
    assert diff3 == {
        "optional_dict": {"self": {"hello": "world"}, "other": {"hello": "python"}}
    }

    # Test no diff when comparing identical instances
    assert instance1.diff(instance1) == {}


@serializable_dataclass
class ComplexDictContainer(SerializableDataclass):
    """Test class with more complex dictionary structures"""

    mixed_dict: Dict[str, Any]
    list_dict: Dict[str, typing.List[int]]
    multi_nested: Dict[str, Dict[str, Dict[str, int]]]


def test_complex_dict_serialization():
    """Test serialization of more complex dictionary structures"""
    data = ComplexDictContainer(
        mixed_dict={"str": "hello", "int": 42, "list": [1, 2, 3]},
        list_dict={"a": [1, 2, 3], "b": [4, 5, 6]},
        multi_nested={"x": {"y": {"z": 1, "w": 2}, "v": {"u": 3, "t": 4}}},
    )

    serialized = data.serialize()
    loaded = ComplexDictContainer.load(serialized)
    assert loaded == data
    assert loaded.diff(data) == {}


def test_empty_dicts():
    """Test handling of empty dictionaries"""
    data = DictContainer(simple_dict={}, nested_dict={}, optional_dict={})

    serialized = data.serialize()
    loaded = DictContainer.load(serialized)
    assert loaded == data
    assert loaded.diff(data) == {}

    # Test equality with another empty instance
    another_empty = DictContainer(simple_dict={}, nested_dict={}, optional_dict={})
    assert data == another_empty


# Test invalid dictionary type validation
@serializable_dataclass(on_typecheck_mismatch=ErrorMode.EXCEPT)
class StrictDictContainer(SerializableDataclass):
    """Test class with strict dictionary typing"""

    int_dict: Dict[str, int]
    str_dict: Dict[str, str]
    float_dict: Dict[str, float]


# TODO: figure this out
@pytest.mark.skip(reason="dict type validation doesnt seem to work")
def test_dict_type_validation():
    """Test type validation for dictionary values"""
    # Valid case
    valid = StrictDictContainer(
        int_dict={"a": 1, "b": 2},
        str_dict={"x": "hello", "y": "world"},
        float_dict={"m": 1.0, "n": 2.5},
    )
    assert valid.validate_fields_types()

    # Invalid int_dict
    with pytest.raises(FieldTypeMismatchError):
        StrictDictContainer(
            int_dict={"a": "not an int"},  # type: ignore[dict-item]
            str_dict={"x": "hello"},
            float_dict={"m": 1.0},
        )

    # Invalid str_dict
    with pytest.raises(FieldTypeMismatchError):
        StrictDictContainer(
            int_dict={"a": 1},
            str_dict={"x": 123},  # type: ignore[dict-item]
            float_dict={"m": 1.0},
        )


# Test dictionary with optional values
@serializable_dataclass
class OptionalDictContainer(SerializableDataclass):
    """Test class with optional dictionary values"""

    optional_values: Dict[str, Optional[int]]
    union_values: Dict[str, Union[int, str]]
    nullable_dict: Optional[Dict[str, int]] = None


def test_optional_dict_values():
    """Test dictionaries with optional/union values"""
    instance = OptionalDictContainer(
        optional_values={"a": 1, "b": None, "c": 3},
        union_values={"x": 1, "y": "string", "z": 42},
        nullable_dict={"m": 1, "n": 2},
    )

    serialized = instance.serialize()
    loaded = OptionalDictContainer.load(serialized)
    assert loaded == instance

    # Test with None dict
    instance2 = OptionalDictContainer(
        optional_values={"a": None, "b": None},
        union_values={"x": "all strings", "y": "here"},
        nullable_dict=None,
    )

    serialized2 = instance2.serialize()
    loaded2 = OptionalDictContainer.load(serialized2)
    assert loaded2 == instance2


# Test dictionary mutation
def test_dict_mutation():
    """Test behavior when mutating dictionary contents"""
    instance1 = DictContainer(
        simple_dict={"a": 1, "b": 2},
        nested_dict={"x": {"y": 3}},
        optional_dict={"hello": "world"},
    )

    instance2 = deepcopy(instance1)

    # Mutate dictionary in instance1
    instance1.simple_dict["c"] = 3
    instance1.nested_dict["x"]["z"] = 4
    instance1.optional_dict["new"] = "value"

    # Verify instance2 was not affected
    assert instance2.simple_dict == {"a": 1, "b": 2}
    assert instance2.nested_dict == {"x": {"y": 3}}
    assert instance2.optional_dict == {"hello": "world"}

    # Verify diff shows the changes
    diff = instance2.diff(instance1)
    assert "simple_dict" in diff
    assert "nested_dict" in diff
    assert "optional_dict" in diff


# Test dictionary key types
@serializable_dataclass
class IntKeyDictContainer(SerializableDataclass):
    """Test class with non-string dictionary keys"""

    int_keys: Dict[int, str] = serializable_field(
        serialization_fn=lambda x: {str(k): v for k, v in x.items()},
        loading_fn=lambda x: {int(k): v for k, v in x["int_keys"].items()},
    )


def test_non_string_dict_keys():
    """Test handling of dictionaries with non-string keys"""
    instance = IntKeyDictContainer(int_keys={1: "one", 2: "two", 3: "three"})

    serialized = instance.serialize()
    # Keys should be converted to strings in serialized form
    assert all(isinstance(k, str) for k in serialized["int_keys"].keys())

    loaded = IntKeyDictContainer.load(serialized)
    # Keys should be integers again after loading
    assert all(isinstance(k, int) for k in loaded.int_keys.keys())
    assert loaded == instance


@serializable_dataclass
class RecursiveDictContainer(SerializableDataclass):
    """Test class with recursively defined dictionary type"""

    data: Dict[str, Any]


def test_recursive_dict_structure():
    """Test handling of recursively nested dictionaries"""
    deep_dict = {
        "level1": {
            "level2": {"level3": {"value": 42, "list": [1, 2, {"nested": "value"}]}}
        }
    }

    instance = RecursiveDictContainer(data=deep_dict)
    serialized = instance.serialize()
    loaded = RecursiveDictContainer.load(serialized)

    assert loaded == instance
    assert loaded.data == deep_dict


# need to define this outside, otherwise the validator cant see it?
class CustomSerializable:
    def __init__(self, value):
        self.value: Union[str, int] = value

    def serialize(self):
        return {"value": self.value}

    @classmethod
    def load(cls, data):
        return cls(data["value"])

    def __eq__(self, other):
        return isinstance(other, CustomSerializable) and self.value == other.value


def test_dict_with_custom_objects():
    """Test dictionaries containing custom objects that implement serialize/load"""

    @serializable_dataclass
    class CustomObjectDict(SerializableDataclass):
        data: Dict[str, CustomSerializable] = serializable_field()

    instance: CustomObjectDict = CustomObjectDict(
        data={"a": CustomSerializable(42), "b": CustomSerializable("hello")}
    )

    assert isinstance(instance, CustomObjectDict)
    assert isinstance(instance.data, dict)
    assert isinstance(instance.data["a"], CustomSerializable)
    assert isinstance(instance.data["a"].value, int)
    assert isinstance(instance.data["b"], CustomSerializable)
    assert isinstance(instance.data["b"].value, str)

    serialized = instance.serialize()
    loaded = CustomObjectDict.load(serialized)
    assert loaded == instance


def test_empty_optional_dicts():
    """Test handling of None vs empty dict in optional dictionary fields"""

    @serializable_dataclass
    class OptionalDictFields(SerializableDataclass):
        required_dict: Dict[str, int]
        optional_dict: Optional[Dict[str, int]] = None
        default_empty: Dict[str, int] = serializable_field(default_factory=dict)

    # Test with None
    instance1 = OptionalDictFields(required_dict={"a": 1}, optional_dict=None)

    # Test with empty dict
    instance2 = OptionalDictFields(required_dict={"a": 1}, optional_dict={})

    serialized1 = instance1.serialize()
    serialized2 = instance2.serialize()

    loaded1 = OptionalDictFields.load(serialized1)
    loaded2 = OptionalDictFields.load(serialized2)

    assert loaded1.optional_dict is None
    assert loaded2.optional_dict == {}
    assert loaded1.default_empty == {}
    assert loaded2.default_empty == {}


# Test inheritance hierarchies
@serializable_dataclass(
    on_typecheck_error=ErrorMode.EXCEPT, on_typecheck_mismatch=ErrorMode.EXCEPT
)
class BaseClass(SerializableDataclass):
    """Base class for testing inheritance"""

    base_field: str
    shared_field: int = serializable_field(default=0)


@serializable_dataclass
class ChildClass(BaseClass):
    """Child class inheriting from BaseClass"""

    child_field: float = serializable_field(default=0.1)
    shared_field: int = serializable_field(default=1)  # Override base class field


@serializable_dataclass
class GrandchildClass(ChildClass):
    """Grandchild class for deep inheritance testing"""

    grandchild_field: bool = serializable_field(default=True)


def test_inheritance():
    """Test inheritance behavior of serializable dataclasses"""
    instance = GrandchildClass(
        base_field="base", shared_field=42, child_field=3.14, grandchild_field=True
    )

    serialized = instance.serialize()
    assert serialized["base_field"] == "base"
    assert serialized["shared_field"] == 42
    assert serialized["child_field"] == 3.14
    assert serialized["grandchild_field"] is True

    loaded = GrandchildClass.load(serialized)
    assert loaded == instance

    # Test that we can load as parent class
    base_loaded = BaseClass.load({"base_field": "test", "shared_field": 1})
    assert isinstance(base_loaded, BaseClass)
    assert not isinstance(base_loaded, ChildClass)


@pytest.mark.skip(
    reason="Not implemented yet, generic types not supported and throw a `TypeHintNotImplementedError`"
)
def test_generic_types():
    """Test handling of generic type parameters"""

    T = TypeVar("T")

    @serializable_dataclass(on_typecheck_mismatch=ErrorMode.EXCEPT)
    class GenericContainer(SerializableDataclass, Generic[T]):
        """Test generic type parameters"""

        value: T
        values: List[T]

    # Test with int
    int_container = GenericContainer[int](value=42, values=[1, 2, 3])
    serialized = int_container.serialize()
    loaded = GenericContainer[int].load(serialized)
    assert loaded == int_container

    # Test with str
    str_container = GenericContainer[str](value="hello", values=["a", "b", "c"])
    serialized2 = str_container.serialize()
    loaded2 = GenericContainer[str].load(serialized2)
    assert loaded2 == str_container


# Test custom serialization/deserialization
class CustomObject:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, CustomObject) and self.value == other.value


@serializable_dataclass
class CustomSerializationContainer(SerializableDataclass):
    """Test custom serialization functions"""

    custom_obj: CustomObject = serializable_field(
        serialization_fn=lambda x: x.value,
        loading_fn=lambda x: CustomObject(x["custom_obj"]),
    )
    transform_field: int = serializable_field(
        serialization_fn=lambda x: x * 2, loading_fn=lambda x: x["transform_field"] // 2
    )


def test_custom_serialization_2():
    """Test custom serialization and loading functions"""
    instance = CustomSerializationContainer(
        custom_obj=CustomObject(42), transform_field=10
    )

    serialized = instance.serialize()
    assert serialized["custom_obj"] == 42
    assert serialized["transform_field"] == 20

    loaded = CustomSerializationContainer.load(serialized)
    assert loaded == instance
    assert loaded.transform_field == 10


# @pytest.mark.skip(reason="Not implemented yet, waiting on `custom_value_check_fn`")
# def test_value_validation():
#     """Test field validation"""
#     @serializable_dataclass
#     class ValidationContainer(SerializableDataclass):
#         """Test validation and error handling"""
#         positive_int: int = serializable_field(
#             custom_value_check_fn=lambda x: x > 0
#         )
#         email: str = serializable_field(
#             custom_value_check_fn=lambda x: '@' in x
#         )

#     # Valid case
#     valid = ValidationContainer(positive_int=42, email="test@example.com")
#     assert valid.validate_fields_types()

#     # what will this do?
#     maybe_valid = ValidationContainer(positive_int=4.2, email="test@example.com")
#     assert maybe_valid.validate_fields_types()

#     maybe_valid_2 = ValidationContainer(positive_int=42, email=["test", "@", "example", ".com"])
#     assert maybe_valid_2.validate_fields_types()

#     # Invalid positive_int
#     with pytest.raises(ValueError):
#         ValidationContainer(positive_int=-1, email="test@example.com")

#     # Invalid email
#     with pytest.raises(ValueError):
#         ValidationContainer(positive_int=42, email="invalid")


def test_init_true_serialize_false():
    with pytest.raises(ValueError):

        @serializable_dataclass
        class MetadataContainer(SerializableDataclass):
            """Test field metadata and options"""

            hidden: str = serializable_field(serialize=False, init=True)
            readonly: int = serializable_field(init=True, frozen=True)
            computed: float = serializable_field(init=False, serialize=True)

            def __post_init__(self):
                object.__setattr__(self, "computed", self.readonly * 2.0)


# Test property serialization
@serializable_dataclass(properties_to_serialize=["full_name", "age_in_months"])
class PropertyContainer(SerializableDataclass):
    """Test property serialization"""

    first_name: str
    last_name: str
    age_years: int

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age_in_months(self) -> int:
        return self.age_years * 12


def test_property_serialization():
    """Test serialization of properties"""
    instance = PropertyContainer(first_name="John", last_name="Doe", age_years=30)

    serialized = instance.serialize()
    assert serialized["full_name"] == "John Doe"
    assert serialized["age_in_months"] == 360

    loaded = PropertyContainer.load(serialized)
    assert loaded == instance


# TODO: this would be nice to fix, but not a massive issue
@pytest.mark.skip(reason="Not implemented yet")
def test_edge_cases():
    """Test a sdc containing instances of itself"""

    @serializable_dataclass
    class EdgeCaseContainer(SerializableDataclass):
        """Test edge cases and corner cases"""

        empty_list: List[Any] = serializable_field(default_factory=list)
        optional_value: Optional[int] = serializable_field(default=None)
        union_field: Union[str, int, None] = serializable_field(default=None)
        recursive_ref: Optional["EdgeCaseContainer"] = serializable_field(default=None)

    # Test recursive structure
    nested = EdgeCaseContainer()
    instance = EdgeCaseContainer(recursive_ref=nested)

    serialized = instance.serialize()
    loaded = EdgeCaseContainer.load(serialized)
    assert loaded == instance

    # Test empty/None handling
    empty = EdgeCaseContainer()
    assert empty.empty_list == []
    assert empty.optional_value is None
    assert empty.union_field is None

    # Test union field with different types
    instance.union_field = "string"
    serialized = instance.serialize()
    loaded = EdgeCaseContainer.load(serialized)
    assert loaded.union_field == "string"

    instance.union_field = 42
    serialized = instance.serialize()
    loaded = EdgeCaseContainer.load(serialized)
    assert loaded.union_field == 42


# Test error handling for malformed data
def test_error_handling():
    """Test error handling for malformed data"""
    # Missing required field
    with pytest.raises(TypeError):
        BaseClass.load({})

    x = BaseClass(base_field=42, shared_field="invalid")  # type: ignore[arg-type]
    assert not x.validate_fields_types()

    with pytest.raises(FieldTypeMismatchError):
        BaseClass.load(
            {
                "base_field": 42,  # Should be str
                "shared_field": "invalid",  # Should be int
            }
        )

    # Invalid format string
    # with pytest.raises(ValueError):
    #     BaseClass.load({
    #         _FORMAT_KEY: "InvalidClass(SerializableDataclass)",
    #         "base_field": "test",
    #         "shared_field": 0
    #     })


# Test for memory leaks and cyclic references
# TODO: make .serialize() fail on cyclic references! see https://github.com/mivanit/muutils/issues/62
@pytest.mark.skip(reason="Not implemented yet")
def test_cyclic_references():
    """Test handling of cyclic references"""

    @serializable_dataclass
    class Node(SerializableDataclass):
        value: str
        next: Optional["Node"] = serializable_field(default=None)

    # Create a cycle
    node1 = Node("one")
    node2 = Node("two")
    node1.next = node2
    node2.next = node1

    # Ensure we can serialize without infinite recursion
    serialized = node1.serialize()
    loaded = Node.load(serialized)
    assert loaded.value == "one"
    # TODO: idk why we type ignore here
    assert loaded.next.value == "two"  # type: ignore[union-attr]
