from __future__ import annotations

import sys

import pytest

from muutils.json_serialize import SerializableDataclass, serializable_dataclass

SUPPORTS_KW_ONLY: bool = sys.version_info >= (3, 10)

print(f"{SUPPORTS_KW_ONLY = }")


@serializable_dataclass
class Person(SerializableDataclass):
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@serializable_dataclass(
    kw_only=SUPPORTS_KW_ONLY, properties_to_serialize=["full_name", "full_title"]
)
class TitledPerson(Person):
    title: str

    @property
    def full_title(self) -> str:
        return f"{self.title} {self.full_name}"


@serializable_dataclass(
    kw_only=SUPPORTS_KW_ONLY,
    properties_to_serialize=["full_name", "not_a_real_property"],
)
class AgedPerson_not_valid(Person):
    title: str

    @property
    def full_title(self) -> str:
        return f"{self.title} {self.full_name}"


def test_invalid_properties_to_serialize():
    instance = AgedPerson_not_valid(first_name="Jane", last_name="Smith", title="Dr.")

    with pytest.raises(AttributeError):
        instance.serialize()


def test_serialize_person():
    instance = Person(first_name="John", last_name="Doe")

    serialized = instance.serialize()

    assert serialized == {
        "first_name": "John",
        "last_name": "Doe",
        "__format__": "Person(SerializableDataclass)",
    }

    recovered = Person.load(serialized)

    assert recovered == instance


def test_serialize_titled_person():
    instance = TitledPerson(first_name="Jane", last_name="Smith", title="Dr.")

    if SUPPORTS_KW_ONLY:
        with pytest.raises(TypeError):
            TitledPerson("Jane", "Smith", "Dr.")

    serialized = instance.serialize()

    assert serialized == {
        "first_name": "Jane",
        "last_name": "Smith",
        "title": "Dr.",
        "__format__": "TitledPerson(SerializableDataclass)",
        "full_name": "Jane Smith",
        "full_title": "Dr. Jane Smith",
    }

    recovered = TitledPerson.load(serialized)

    assert recovered == instance
