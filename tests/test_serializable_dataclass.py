import pytest
from typing import Any

from muutils.json_serialize import (
    serializable_dataclass,
    serializable_field,
    SerializableDataclass,
)

# pylint: disable=missing-class-docstring, unused-variable


@serializable_dataclass
class SimpleFields(SerializableDataclass):
    a: str
    b: int = 42
    c: list[int] = serializable_field(default_factory=list)


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
    return SimpleFields(a="hello", b=42, c=[1, 2, 3])


@pytest.fixture
def field_options_instance():
    return FieldOptions(a="hello", b="world", d="case")


@pytest.fixture
def with_property_instance():
    return WithProperty(first_name="John", last_name="Doe")


def test_simple_fields_serialization(simple_fields_instance):
    serialized = simple_fields_instance.serialize()
    assert serialized == {"a": "hello", "b": 42, "c": [1, 2, 3]}


def test_simple_fields_loading(simple_fields_instance):
    serialized = simple_fields_instance.serialize()
    loaded = SimpleFields.load(serialized)
    assert loaded == simple_fields_instance


def test_field_options_serialization(field_options_instance):
    serialized = field_options_instance.serialize()
    assert serialized == {"a": "hello", "b": "world", "d": "CASE"}


def test_field_options_loading(field_options_instance):
    serialized = field_options_instance.serialize()
    loaded = FieldOptions.load(serialized)
    assert loaded == field_options_instance


def test_with_property_serialization(with_property_instance):
    serialized = with_property_instance.serialize()
    assert serialized == {
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
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
    assert serialized == {
        "name": "John Doe",
        "age": 30,
        "address": {"street": "123 Main St", "city": "New York", "zip_code": "10001"},
    }


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
    assert serialized == {"a": 42, "b": "hello"}

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
        items: list[str] = serializable_field(default_factory=list)

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
    assert serialized == {"data": 10}

    loaded = CustomSerialization.load(serialized)
    assert loaded == custom
