from __future__ import annotations
import pytest

from muutils.misc import (
    dict_to_filename,
    freeze,
    list_join,
    list_split,
    sanitize_fname,
    stable_hash,
)


def test_stable_hash():
    # no real way to test this without running multiple interpreters, but I'm pretty sure it works lol
    assert stable_hash("test") == stable_hash(
        "test"
    ), "Hash should be stable for the same input"
    assert stable_hash("test") != stable_hash(
        "Test"
    ), "Hash should be different for different inputs"


def test_sanitize_fname():
    assert (
        sanitize_fname("filename.txt") == "filename.txt"
    ), "Alphanumeric characters and '.' should remain"
    assert (
        sanitize_fname("file-name.txt") == "file-name.txt"
    ), "Alphanumeric characters, '-' and '.' should remain"
    assert (
        sanitize_fname("file@name!?.txt") == "filename.txt"
    ), "Special characters should be removed"
    assert sanitize_fname(None) == "_None_", "None input should return '_None_'"


def test_dict_to_filename():
    data = {"key1": "value1", "key2": "value2"}
    assert (
        dict_to_filename(data) == "key1_value1.key2_value2"
    ), "Filename should be formatted correctly"

    long_data = {f"key{i}": f"value{i}" for i in range(100)}
    assert dict_to_filename(long_data).startswith(
        "h_"
    ), "Filename should be hashed if too long"


def test_freeze():
    class TestClass:
        def __init__(self):
            self.attr = "value"

    instance = TestClass()
    freeze(instance)
    with pytest.raises(AttributeError):
        instance.attr = "new_value"


def test_list_split():
    # with integers
    assert list_split([1, 2, 3, 2, 4], 2) == [
        [1],
        [3],
        [4],
    ], "List should be split correctly"
    assert list_split([1, 2, 2, 2, 4], 2) == [
        [1],
        [],
        [],
        [4],
    ], "Empty sublists should be created for consecutive delimiters"
    assert list_split([], 2) == [
        []
    ], "Empty list should return a list with one empty sublist"

    # with strings
    assert list_split(["a", "b", "c", "b", "d"], "b") == [
        ["a"],
        ["c"],
        ["d"],
    ], "List should be split correctly"
    assert list_split(["a", "b", "b", "b", "d"], "b") == [
        ["a"],
        [],
        [],
        ["d"],
    ], "Empty sublists should be created for consecutive delimiters"
    assert list_split([], "b") == [
        []
    ], "Empty list should return a list with one empty sublist"

    # mixed types
    assert list_split([1, "b", 3, "b", 4], "b") == [
        [1],
        [3],
        [4],
    ], "List should be split correctly"
    assert list_split([1, "b", "b", "b", 4], "b") == [
        [1],
        [],
        [],
        [4],
    ], "Empty sublists should be created for consecutive delimiters"
    assert list_split([], "b") == [
        []
    ], "Empty list should return a list with one empty sublist"


def test_list_join():
    # with integers
    assert list_join([1, 2, 3], lambda: 0) == [
        1,
        0,
        2,
        0,
        3,
    ], "Items should be joined correctly with factory-produced values"
    assert list_join([1], lambda: 0) == [1], "Single item list should remain unchanged"
    assert list_join([], lambda: 0) == [], "Empty list should remain unchanged"

    # with strings
    assert list_join(["a", "b", "c"], lambda: "x") == [
        "a",
        "x",
        "b",
        "x",
        "c",
    ], "Items should be joined correctly with factory-produced values"
    assert list_join(["a"], lambda: "x") == [
        "a"
    ], "Single item list should remain unchanged"
    assert list_join([], lambda: "x") == [], "Empty list should remain unchanged"

    # mixed types
    assert list_join([1, "b", 3], lambda: "x") == [
        1,
        "x",
        "b",
        "x",
        3,
    ], "Items should be joined correctly with factory-produced values"
    assert list_join([1], lambda: "x") == [
        1
    ], "Single item list should remain unchanged"
    assert list_join([], lambda: "x") == [], "Empty list should remain unchanged"
