from __future__ import annotations

import sys
import typing
from typing import Any

import pytest

from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)

# pylint: disable=missing-class-docstring, unused-variable


BELOW_PY_3_10: bool = False
# sys.version_info < (3, 10)


def _loading_test_wrapper(cls, data, assert_record_len: int | None = None) -> Any:
    """wrapper for testing the load function, which accounts for version differences"""
    if BELOW_PY_3_10:
        with pytest.warns(UserWarning) as record:
            loaded = cls.load(data)
        print([x.message for x in record])
        if assert_record_len is not None:
            assert len(record) == assert_record_len
        return loaded
    else:
        loaded = cls.load(data)
        return loaded


@serializable_dataclass
class BasicAutofields(SerializableDataclass):
    a: str
    b: int
    c: typing.List[int]


def test_basic_auto_fields():
    data = dict(a="hello", b=42, c=[1, 2, 3])
    instance = BasicAutofields(**data)
    data_with_format = data.copy()
    data_with_format["__format__"] = "BasicAutofields(SerializableDataclass)"
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
        "__format__": "SimpleFields(SerializableDataclass)",
    }


def test_simple_fields_loading(simple_fields_instance):
    serialized = simple_fields_instance.serialize()

    loaded = SimpleFields.load(
        serialized
    )  # _loading_test_wrapper(SimpleFields, serialized)  # , assert_record_len=4)

    assert loaded == simple_fields_instance
    assert loaded.diff(simple_fields_instance) == {}
    assert simple_fields_instance.diff(loaded) == {}


def test_field_options_serialization(field_options_instance):
    serialized = field_options_instance.serialize()
    assert serialized == {
        "a": "hello",
        "b": "world",
        "d": "CASE",
        "__format__": "FieldOptions(SerializableDataclass)",
    }


def test_field_options_loading(field_options_instance):
    serialized = field_options_instance.serialize()
    loaded = _loading_test_wrapper(FieldOptions, serialized)  # , assert_record_len=3)
    assert loaded == field_options_instance


def test_with_property_serialization(with_property_instance):
    serialized = with_property_instance.serialize()
    assert serialized == {
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "__format__": "WithProperty(SerializableDataclass)",
    }


def test_with_property_loading(with_property_instance):
    serialized = with_property_instance.serialize()
    loaded = _loading_test_wrapper(WithProperty, serialized)  # , assert_record_len=2)
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
            "__format__": "Address(SerializableDataclass)",
        },
        "__format__": "Person(SerializableDataclass)",
    }
    assert serialized == expected_ser


def test_nested_loading(person_instance):
    serialized = person_instance.serialize()
    loaded = _loading_test_wrapper(Person, serialized)  # , assert_record_len=6)
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

    loaded_instance = _loading_test_wrapper(
        MyClass, serialized_data  # , assert_record_len=3
    )
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
        "__format__": "SimpleClass(SerializableDataclass)",
    }

    loaded = _loading_test_wrapper(SimpleClass, serialized)  # , assert_record_len=2)
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
        "__format__": "FullPerson(SerializableDataclass)",
    }
    assert serialized == expected_ser, f"Expected {expected_ser}, got {serialized}"

    loaded = _loading_test_wrapper(FullPerson, serialized)  # , assert_record_len=4)

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
        "__format__": "CustomSerialization(SerializableDataclass)",
    }

    loaded = _loading_test_wrapper(
        CustomSerialization, serialized
    )  # , assert_record_len=1)
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
                "__format__": "BasicAutofields(SerializableDataclass)",
            },
            {
                "a": "b",
                "b": 2,
                "c": [4, 5, 6],
                "__format__": "BasicAutofields(SerializableDataclass)",
            },
        ],
        "__format__": "Nested_with_Container(SerializableDataclass)",
    }

    assert serialized == expected_ser

    loaded = _loading_test_wrapper(
        Nested_with_Container, serialized  # , assert_record_len=12
    )

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
        "__format__": "nested_custom(SerializableDataclass)",
    }
    assert serialized == expected_ser
    loaded = _loading_test_wrapper(nested_custom, serialized)
    assert loaded == instance
