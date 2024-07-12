from __future__ import annotations
from typing import Iterable

import pytest
from pytest import mark, param

from muutils.misc import (
    dict_to_filename,
    freeze,
    list_join,
    list_split,
    sanitize_fname,
    sanitize_identifier,
    sanitize_name,
    stable_hash,
    flatten,
    get_all_subclasses,
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


def test_sanitize_name():
    assert sanitize_name("Hello World") == "HelloWorld"
    assert sanitize_name("Hello_World", additional_allowed_chars="_") == "Hello_World"
    assert sanitize_name("Hello!World", replace_invalid="-") == "Hello-World"
    assert sanitize_name(None) == "_None_"
    assert sanitize_name(None, when_none="Empty") == "Empty"
    with pytest.raises(ValueError):
        sanitize_name(None, when_none=None)
    assert sanitize_name("123abc") == "123abc"
    assert sanitize_name("123abc", leading_digit_prefix="_") == "_123abc"


def test_sanitize_fname_2():
    assert sanitize_fname("file name.txt") == "filename.txt"
    assert sanitize_fname("file_name.txt") == "file_name.txt"
    assert sanitize_fname("file-name.txt") == "file-name.txt"
    assert sanitize_fname("file!name.txt") == "filename.txt"
    assert sanitize_fname(None) == "_None_"
    assert sanitize_fname(None, when_none="Empty") == "Empty"
    with pytest.raises(ValueError):
        sanitize_fname(None, when_none=None)
    assert sanitize_fname("123file.txt") == "123file.txt"
    assert sanitize_fname("123file.txt", leading_digit_prefix="_") == "_123file.txt"


def test_sanitize_identifier():
    assert sanitize_identifier("variable_name") == "variable_name"
    assert sanitize_identifier("VariableName") == "VariableName"
    assert sanitize_identifier("variable!name") == "variablename"
    assert sanitize_identifier("123variable") == "_123variable"
    assert sanitize_identifier(None) == "_None_"
    assert sanitize_identifier(None, when_none="Empty") == "Empty"
    with pytest.raises(ValueError):
        sanitize_identifier(None, when_none=None)


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


# Testing the flatten function
def test_flatten_full_flattening():
    assert list(flatten([1, [2, [3, 4]], 5])) == [1, 2, 3, 4, 5]
    assert list(flatten([1, [2, [3, [4, [5]]]]])) == [1, 2, 3, 4, 5]
    assert list(flatten([])) == []


def test_flatten_partial_flattening():
    assert list(flatten([1, [2, [3, 4]], 5], levels_to_flatten=1)) == [1, 2, [3, 4], 5]
    assert list(flatten([1, [2, [3, [4, [5]]]]], levels_to_flatten=2)) == [
        1,
        2,
        3,
        [4, [5]],
    ]


def test_flatten_with_non_iterables():
    assert list(flatten([1, 2, 3])) == [1, 2, 3]
    assert list(flatten([1, "abc", 2, [3, 4], 5])) == [1, "abc", 2, 3, 4, 5]


# Testing the get_all_subclasses function
class A:
    pass


class B(A):
    pass


class C(B):
    pass


def test_get_all_subclasses():
    assert get_all_subclasses(A) == {B, C}
    assert get_all_subclasses(B) == {C}
    assert get_all_subclasses(C) == set()


def test_get_all_subclasses_include_self():
    assert get_all_subclasses(A, include_self=True) == {A, B, C}
    assert get_all_subclasses(B, include_self=True) == {B, C}
    assert get_all_subclasses(C, include_self=True) == {C}


@mark.parametrize(
    "deep, flat, depth",
    [
        param(
            iter_tuple[0],
            iter_tuple[1],
            iter_tuple[2],
            id=f"{i}",
        )
        for i, iter_tuple in enumerate(
            [
                ([1, 2, 3, 4], [1, 2, 3, 4], None),
                ((1, 2, 3, 4), [1, 2, 3, 4], None),
                ((j for j in [1, 2, 3, 4]), [1, 2, 3, 4], None),
                (["a", "b", "c", "d"], ["a", "b", "c", "d"], None),
                ("funky duck", [c for c in "funky duck"], None),
                (["funky", "duck"], ["funky", "duck"], None),
                (b"funky duck", [b for b in b"funky duck"], None),
                ([b"funky", b"duck"], [b"funky", b"duck"], None),
                ([[1, 2, 3, 4]], [1, 2, 3, 4], None),
                ([[[[1, 2, 3, 4]]]], [1, 2, 3, 4], None),
                ([[[[1], 2], 3], 4], [1, 2, 3, 4], None),
                ([[1, 2], [[3]], (4,)], [1, 2, 3, 4], None),
                ([[[1, 2, 3, 4]]], [[1, 2, 3, 4]], 1),
                ([[[1, 2, 3, 4]]], [1, 2, 3, 4], 2),
                ([[1, 2], [[3]], (4,)], [1, 2, [3], 4], 1),
                ([[1, 2], [(3,)], (4,)], [1, 2, (3,), 4], 1),
                ([[[[1], 2], 3], 4], [[1], 2, 3, 4], 2),
            ]
        )
    ],
)
def test_flatten(deep: Iterable[any], flat: Iterable[any], depth: int | None):
    assert list(flatten(deep, depth)) == flat


def test_get_all_subclasses2():
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

    class E(B):
        pass

    class F(D):
        pass

    class Z:
        pass

    assert get_all_subclasses(A) == {B, C, D, E, F}
    assert get_all_subclasses(A, include_self=True) == {A, B, C, D, E, F}
    assert get_all_subclasses(B) == {D, E, F}
    assert get_all_subclasses(C) == {D, F}
    assert get_all_subclasses(D) == {F}
    assert get_all_subclasses(D, include_self=True) == {D, F}
    assert get_all_subclasses(Z) == set()
    assert get_all_subclasses(Z, include_self=True) == {Z}
