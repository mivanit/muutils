from muutils.json_serialize import SerializableDataclass, serializable_dataclass


@serializable_dataclass
class Person(SerializableDataclass):
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@serializable_dataclass(
    kw_only=True, properties_to_serialize=["full_name", "full_title"]
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

    recovered = Person.load(serialized)

    assert recovered == instance


def test_serialize_titled_person():
    instance = TitledPerson(first_name="Jane", last_name="Smith", title="Dr.")

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
