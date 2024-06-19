from __future__ import annotations

from typing import Any


from muutils.json_serialize import (
    JsonSerializer,
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)

# pylint: disable=missing-class-docstring


# TODO: get rid of all _loading_test_wrapper functions across all files
def _loading_test_wrapper(cls, data) -> Any:
    """wrapper for testing the load function, which accounts for version differences"""
    loaded = cls.load(data)
    return loaded


@serializable_dataclass
class Config(SerializableDataclass):
    name: str = serializable_field(default="default_name")
    save_model: bool = serializable_field(default=True)
    batch_size: int = serializable_field(default=64)


def test_sdc_empty():
    instance = Config()
    serialized = instance.serialize()
    assert serialized == {
        "name": "default_name",
        "save_model": True,
        "batch_size": 64,
        "__format__": "Config(SerializableDataclass)",
    }
    recovered = _loading_test_wrapper(Config, serialized)
    assert recovered == instance


def test_sdc_strip_format_jser():
    instance = Config()
    jser: JsonSerializer = JsonSerializer(write_only_format=True)
    serialized = jser.json_serialize(instance)
    assert serialized == {
        "name": "default_name",
        "save_model": True,
        "batch_size": 64,
        "__write_format__": "Config(SerializableDataclass)",
    }
    recovered = _loading_test_wrapper(Config, serialized)
    assert recovered == instance


TYPE_MAP: dict[str, type] = {x.__name__: x for x in [int, float, str, bool]}


@serializable_dataclass
class ComplicatedConfig(SerializableDataclass):
    name: str = serializable_field(default="default_name")
    save_model: bool = serializable_field(default=True)
    batch_size: int = serializable_field(default=64)

    some_type: type = serializable_field(
        default=float,
        serialization_fn=lambda x: x.__name__,
        loading_fn=lambda data: TYPE_MAP[data["some_type"]],
    )


def test_sdc_empty_complicated():
    instance = ComplicatedConfig()
    serialized = instance.serialize()
    recovered = _loading_test_wrapper(ComplicatedConfig, serialized)
    assert recovered == instance
