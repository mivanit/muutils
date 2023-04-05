from typing import Any

import pytest

from muutils.json_serialize import (
    SerializableDataclass,
    serializable_dataclass,
    serializable_field,
)

@serializable_dataclass
class ChildData(SerializableDataclass):
    x: int
    y: int

@serializable_dataclass
class ParentData(SerializableDataclass):
    a: int
    b: ChildData


def test_update_from_nested_dict():
    parent = ParentData(a=1, b=ChildData(x=2, y=3))
    update_data = {"a": 5, "b": {"x": 6}}
    parent.update_from_nested_dict(update_data)

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 3

    update_data2 = {"b": {"y": 7}}
    parent.update_from_nested_dict(update_data2)

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 7