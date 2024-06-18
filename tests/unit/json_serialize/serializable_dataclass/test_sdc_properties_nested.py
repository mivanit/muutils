from __future__ import annotations

import sys
from typing import Any

import pytest

from muutils.json_serialize import SerializableDataclass, serializable_dataclass

SUPPORS_KW_ONLY: bool = sys.version_info >= (3, 10)

print(f"{SUPPORS_KW_ONLY = }")

BELOW_PY_3_9: bool = sys.version_info < (3, 9)


def _loading_test_wrapper(cls, data, assert_record_len: int | None = None) -> Any:
    """wrapper for testing the load function, which accounts for version differences"""
    if BELOW_PY_3_9:
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
class Person(SerializableDataclass):
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@serializable_dataclass(
    kw_only=SUPPORS_KW_ONLY, properties_to_serialize=["full_name", "full_title"]
)
class TitledPerson(Person):
    title: str

    @property
    def full_title(self) -> str:
        return f"{self.title} {self.full_name}"


def test_serialize_person():
    instance = Person("John", "Doe")

    serialized = instance.serialize()

    assert serialized == {
        "first_name": "John",
        "last_name": "Doe",
        "__format__": "Person(SerializableDataclass)",
    }

    recovered = _loading_test_wrapper(Person, serialized)

    assert recovered == instance


def test_serialize_titled_person():
    instance = TitledPerson(first_name="Jane", last_name="Smith", title="Dr.")

    if SUPPORS_KW_ONLY:
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

    recovered = _loading_test_wrapper(TitledPerson, serialized)

    assert recovered == instance
