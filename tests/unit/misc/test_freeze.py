from __future__ import annotations

import pytest

from muutils.misc import freeze

# TODO: there are a bunch of 'type: ignore' comments here which it would be nice to get rid of


def test_freeze_basic_types():
    freeze(True)
    freeze(123)
    freeze(45.67)
    freeze("hello")
    freeze(b"bytes")

    assert True  # No exceptions should be raised


def test_freeze_list():
    lst = [1, 2, 3]
    lst = freeze(lst)

    with pytest.raises(AttributeError):
        lst[0] = 4

    with pytest.raises(AttributeError):
        lst.append(4)

    with pytest.raises(AttributeError):
        lst.extend([4, 5])

    with pytest.raises(AttributeError):
        lst.pop()

    with pytest.raises(AttributeError):
        lst.clear()


def test_freeze_tuple():
    tpl = (1, 2, 3)
    frozen_tpl = freeze(tpl)

    assert frozen_tpl == (1, 2, 3)
    assert isinstance(frozen_tpl, tuple)


def test_freeze_set():
    st = {1, 2, 3}
    frozen_st = freeze(st)

    assert frozen_st == frozenset({1, 2, 3})
    assert isinstance(frozen_st, frozenset)


def test_freeze_dict():
    dct = {"key1": 1, "key2": 2}
    dct = freeze(dct)

    with pytest.raises(AttributeError):
        dct["key1"] = 3

    with pytest.raises(AttributeError):
        del dct["key2"]


def test_freeze_nested_structures():
    nested = {"key1": [1, 2, 3], "key2": {"subkey": 4}}
    freeze(nested)

    with pytest.raises(AttributeError):
        nested["key1"][0] = 4  # type: ignore[index]

    with pytest.raises(AttributeError):
        nested["key2"]["subkey"] = 5  # type: ignore[index]


def test_freeze_custom_class():
    class CustomClass:
        def __init__(self, value):
            self.value = value

    obj = CustomClass(10)
    freeze(obj)

    with pytest.raises(AttributeError):
        obj.value = 20


class CustomClass:
    def __init__(self, value):
        self.value = value


def test_freeze_class_with_nested_structures():
    class NestedClass:
        def __init__(self):
            self.lst = [1, 2, {"key": 3}, (4, 5)]
            self.dct = {"key1": {1, 2, 3}, "key2": [6, 7, 8]}
            self.st = {frozenset((9, 10)), (11, 12)}
            self.tpl = (CustomClass(13), [14, 15], {"key3": 16})

    obj_orig = NestedClass()
    obj = freeze(obj_orig)

    with pytest.raises(AttributeError):
        obj.lst[0] = 10

    with pytest.raises(AttributeError):
        obj.lst[2]["key"] = 30  # type: ignore[index]

    with pytest.raises(AttributeError):
        obj.lst[3] = (40, 50)

    with pytest.raises(AttributeError):
        obj.dct["key1"] = {100, 200}

    with pytest.raises(AttributeError):
        obj.dct["key2"][1] = 70  # type: ignore[index]

    with pytest.raises(AttributeError):
        obj.st.add((13, 14))

    with pytest.raises(AttributeError):
        obj.tpl[1][0] = 140

    with pytest.raises(AttributeError):
        obj.tpl[2]["key3"] = 160


def test_freeze_lists_with_classes_and_nested_structures():
    lst = [CustomClass(1), [2, 3], {"key": (4, 5)}]
    freeze(lst)

    with pytest.raises(AttributeError):
        lst[0].value = 10  # type: ignore[attr-defined]

    with pytest.raises(AttributeError):
        lst[1][1] = 30  # type: ignore[index]

    with pytest.raises(AttributeError):
        lst[2]["key"] = (40, 50)  # type: ignore[index]


def test_freeze_dicts_with_classes_and_nested_structures():
    dct = {"class": CustomClass(6), "lst": [7, 8], "set": {9, (10, 11)}}
    freeze(dct)

    with pytest.raises(AttributeError):
        dct["class"].value = 60  # type: ignore[attr-defined]

    with pytest.raises(AttributeError):
        dct["lst"][0] = 70  # type: ignore[index]

    with pytest.raises(AttributeError):
        dct["set"].add(12)  # type: ignore[attr-defined]


def test_freeze_sets_with_classes_and_nested_structures():
    st = {CustomClass(1), frozenset({2, 3}), (4, 5)}
    freeze(st)

    for item in st:
        if isinstance(item, CustomClass):
            with pytest.raises(AttributeError):
                item.value = 10


def test_freeze_tuples_with_classes_and_nested_structures():
    tpl = (CustomClass(1), [2, 3], {"key": 4})
    frozen_tpl = freeze(tpl)

    for item in frozen_tpl:
        if isinstance(item, CustomClass):
            with pytest.raises(AttributeError):
                item.value = 10
        elif isinstance(item, list):
            with pytest.raises(AttributeError):
                item[0] = 20
        elif isinstance(item, dict):
            with pytest.raises(AttributeError):
                item["key"] = 40
