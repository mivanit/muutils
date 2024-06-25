from __future__ import annotations

import typing
from typing import Any, Optional, Union

import pytest

from muutils.validate_type import IncorrectTypeException, validate_type


# Tests for basic types and common use cases
@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, int, True),
        (3.14, float, True),
        (5, int, True),
        (5.0, int, False),
        ("hello", str, True),
        (True, bool, True),
        (None, type(None), True),
        (None, int, False),
        ([1, 2, 3], typing.List, True),
        ([1, 2, 3], typing.List, True),
        ({"a": 1, "b": 2}, typing.Dict, True),
        ({"a": 1, "b": 2}, typing.Dict, True),
        ({1, 2, 3}, typing.Set, True),
        ({1, 2, 3}, typing.Set, True),
        ((1, 2, 3), typing.Tuple, True),
        ((1, 2, 3), typing.Tuple, True),
        (b"bytes", bytes, True),
        (b"bytes", str, False),
        ("3.14", float, False),
        ("hello", Any, True),
        (5, Any, True),
        (3.14, Any, True),
        # ints
        (int(0), int, True),
        (int(1), int, True),
        (int(-1), int, True),
        # bools
        (True, bool, True),
        (False, bool, True),
    ],
)
def test_validate_type_basic(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value",
    [
        42,
        "hello",
        3.14,
        True,
        None,
        [1, 2, 3],
        {"a": 1, "b": 2},
        {1, 2, 3},
        (1, 2, 3),
        b"bytes",
        "3.14",
    ],
)
def test_validate_type_any(value):
    try:
        assert validate_type(value, Any)
    except Exception as e:
        raise Exception(f"{value = }, expected `Any`, {e}") from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, Union[int, str], True),
        ("hello", Union[int, str], True),
        (3.14, Union[int, float], True),
        (True, Union[int, str], True),
        (None, Union[int, type(None)], True),
        (None, Union[int, str], False),
        (5, Union[int, str], True),
        (5.0, Union[int, str], False),
        ("hello", Union[int, str], True),
        (5, typing.Union[int, str], True),
        ("hello", typing.Union[int, str], True),
        (5.0, typing.Union[int, str], False),
        (5, Union[int, str], True),
        ("hello", Union[int, str], True),
        (5.0, Union[int, str], False),
    ],
)
def test_validate_type_union(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, Optional[int], True),
        ("hello", Optional[int], False),
        (3.14, Optional[int], False),
        ([1], Optional[typing.List[int]], True),
        (None, Optional[int], True),
        (None, Optional[str], True),
        (None, Optional[int], True),
        (None, Optional[None], True),
        (None, Optional[typing.List[typing.Dict[str, int]]], True),
    ],
)
def test_validate_type_optional(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, typing.List[int], False),
        ([1, 2, 3], typing.List[int], True),
        ([1, 2, 3], typing.List[str], False),
        (["a", "b", "c"], typing.List[str], True),
        ([1, "a", 3], typing.List[int], False),
        (42, typing.List[int], False),
        ([1, 2, 3], typing.List[int], True),
        ([1, "2", 3], typing.List[int], False),
    ],
)
def test_validate_type_list(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, typing.Dict[str, int], False),
        ({"a": 1, "b": 2}, typing.Dict[str, int], True),
        ({"a": 1, "b": 2}, typing.Dict[int, str], False),
        (42, typing.Dict[str, int], False),
        ({"a": 1, "b": 2}, typing.Dict[str, int], True),
        ({"a": 1, "b": 2}, typing.Dict[int, str], False),
        ({1: "a", 2: "b"}, typing.Dict[int, str], True),
        ({1: "a", 2: "b"}, typing.Dict[str, int], False),
        ({"a": 1, "b": "c"}, typing.Dict[str, int], False),
        ([("a", 1), ("b", 2)], typing.Dict[str, int], False),
        ({"key": "value"}, typing.Dict[str, str], True),
        ({"key": 2}, typing.Dict[str, str], False),
        ({"key": 2}, typing.Dict[str, int], True),
        ({"key": 2.0}, typing.Dict[str, int], False),
        ({"a": 1, "b": 2}, typing.Dict[str, int], True),
        ({"a": 1, "b": "2"}, typing.Dict[str, int], False),
    ],
)
def test_validate_type_dict(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, typing.Set[int], False),
        ({1, 2, 3}, typing.Set[int], True),
        (42, typing.Set[int], False),
        ({1, 2, 3}, typing.Set[int], True),
        ({1, 2, 3}, typing.Set[str], False),
        ({"a", "b", "c"}, typing.Set[str], True),
        ({1, "a", 3}, typing.Set[int], False),
        (42, typing.Set[int], False),
        ({1, 2, 3}, typing.Set[int], True),
        ({1, "2", 3}, typing.Set[int], False),
        ([1, 2, 3], typing.Set[int], False),
        ("hello", typing.Set[str], False),
    ],
)
def test_validate_type_set(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, typing.Tuple[int, str], False),
        ((1, "a"), typing.Tuple[int, str], True),
        (42, typing.Tuple[int, str], False),
        ((1, "a"), typing.Tuple[int, str], True),
        ((1, 2), typing.Tuple[int, str], False),
        ((1, 2), typing.Tuple[int, int], True),
        ((1, 2, 3), typing.Tuple[int, int], False),
        ((1, "a", 3.14), typing.Tuple[int, str, float], True),
        (("a", "b", "c"), typing.Tuple[str, str, str], True),
        ((1, "a", 3.14), typing.Tuple[int, str], False),
        ((1, "a", 3.14), typing.Tuple[int, str, float], True),
        ([1, "a", 3.14], typing.Tuple[int, str, float], False),
        (
            (1, "a", 3.14, "b", True, None, (1, 2, 3)),
            # no idea why this throws type error, only locally, and only for the generated modern types
            typing.Tuple[  # type: ignore[misc]
                int, str, float, str, bool, type(None), typing.Tuple[int, int, int]
            ],
            True,
        ),
    ],
)
def test_validate_type_tuple(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (43, typing.Callable),
        (lambda x: x, typing.Callable),
        (42, typing.Callable[[], None]),
        (42, typing.Callable[[int, str], typing.List]),
    ],
)
def test_validate_type_unsupported_type_hint(value, expected_type):
    with pytest.raises(NotImplementedError):
        validate_type(value, expected_type)
        print(f"Failed to except: {value = }, {expected_type = }")


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        ([1, 2, 3], typing.List[int], True),
        (["a", "b", "c"], typing.List[str], True),
        ([1, "a", 3], typing.List[int], False),
        ([1, 2, [3, 4]], typing.List[Union[int, typing.List[int]]], True),
        ([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]], True),
        ([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]], False),
        ({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]], True),
        ({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]], False),
    ],
)
def test_validate_type_collections(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        # empty lists
        ([], typing.List[int], True),
        ([], typing.List[typing.Dict], True),
        (
            [],
            typing.List[typing.Tuple[typing.Dict[typing.Tuple, str], str, None]],
            True,
        ),
        # empty dicts
        ({}, typing.Dict[str, int], True),
        ({}, typing.Dict[str, typing.Dict], True),
        ({}, typing.Dict[str, typing.Dict[str, int]], True),
        ({}, typing.Dict[str, typing.Dict[str, int]], True),
        # empty sets
        (set(), typing.Set[int], True),
        (set(), typing.Set[typing.Dict], True),
        (
            set(),
            typing.Set[typing.Tuple[typing.Dict[typing.Tuple, str], str, None]],
            True,
        ),
        # empty tuple
        (tuple(), typing.Tuple, True),
        # empty string
        ("", str, True),
        # empty bytes
        (b"", bytes, True),
        # None
        (None, type(None), True),
        # bools are ints, ints are not floats
        (True, int, True),
        (False, int, True),
        (True, float, False),
        (False, float, False),
        (1, int, True),
        (0, int, True),
        (1, float, False),
        (0, float, False),
        (0, bool, False),
        (1, bool, False),
        # weird floats
        (float("nan"), float, True),
        (float("inf"), float, True),
        (float("-inf"), float, True),
        (float(0), float, True),
        # list/tuple
        ([1], typing.Tuple[int, int], False),
        ((1, 2), typing.List[int], False),
    ],
)
def test_validate_type_edge_cases(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (42, typing.List[int], False),
        ([1, 2, 3], int, False),
        (3.14, typing.Tuple[float], False),
        (3.14, typing.Tuple[float, float], False),
        (3.14, typing.Tuple[bool, str], False),
        (False, typing.Tuple[bool, str], False),
        (False, typing.Tuple[bool], False),
        ((False,), typing.Tuple[bool], True),
        (("abc",), typing.Tuple[str], True),
        ("test-dict", typing.Dict[str, int], False),
        ("test-dict", typing.Dict, False),
    ],
)
def test_validate_type_wrong_type(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


def test_validate_type_complex():
    assert validate_type([1, 2, [3, 4]], typing.List[Union[int, typing.List[int]]])
    assert validate_type(
        {"a": 1, "b": {"c": 2}}, typing.Dict[str, Union[int, typing.Dict[str, int]]]
    )
    assert validate_type({1, (2, 3)}, typing.Set[Union[int, typing.Tuple[int, int]]])
    assert validate_type((1, ("a", "b")), typing.Tuple[int, typing.Tuple[str, str]])
    assert validate_type([{"key": "value"}], typing.List[typing.Dict[str, str]])
    assert validate_type([{"key": 2}], typing.List[typing.Dict[str, str]]) is False
    assert validate_type([[1, 2], [3, 4]], typing.List[typing.List[int]])
    assert validate_type([[1, 2], [3, "4"]], typing.List[typing.List[int]]) is False
    assert validate_type([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]])
    assert (
        validate_type([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]]) is False
    )
    assert validate_type({1: "one", 2: "two"}, typing.Dict[int, str])
    assert validate_type({1: "one", 2: 2}, typing.Dict[int, str]) is False
    assert validate_type([(1, "one"), (2, "two")], typing.List[typing.Tuple[int, str]])
    assert (
        validate_type([(1, "one"), (2, 2)], typing.List[typing.Tuple[int, str]])
        is False
    )
    assert validate_type({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]])
    assert (
        validate_type({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]])
        is False
    )
    assert validate_type([(1, "a"), (2, "b")], typing.List[typing.Tuple[int, str]])
    assert (
        validate_type([(1, "a"), (2, 2)], typing.List[typing.Tuple[int, str]]) is False
    )


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        ([[[[1]]]], typing.List[typing.List[typing.List[typing.List[int]]]], True),
        ([[[[1]]]], typing.List[typing.List[typing.List[typing.List[str]]]], False),
        (
            {"a": {"b": {"c": 1}}},
            typing.Dict[str, typing.Dict[str, typing.Dict[str, int]]],
            True,
        ),
        (
            {"a": {"b": {"c": 1}}},
            typing.Dict[str, typing.Dict[str, typing.Dict[str, str]]],
            False,
        ),
        ({1, 2, 3}, typing.Set[int], True),
        ({1, 2, 3}, typing.Set[str], False),
        (
            ((1, 2), (3, 4)),
            typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]],
            True,
        ),
        (
            ((1, 2), (3, 4)),
            typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, str]],
            False,
        ),
    ],
)
def test_validate_type_nested(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


def test_validate_type_inheritance():
    class Parent:
        def __init__(self, a: int, b: str):
            self.a: int = a
            self.b: str = b

    class Child(Parent):
        def __init__(self, a: int, b: str):
            self.a: int = 2 * a
            self.b: str = b

    assert validate_type(Parent(1, "a"), Parent)
    validate_type(Child(1, "a"), Parent, do_except=True)
    assert validate_type(Child(1, "a"), Child)
    assert not validate_type(Parent(1, "a"), Child)

    with pytest.raises(IncorrectTypeException):
        validate_type(Parent(1, "a"), Child, do_except=True)


def test_validate_type_class():
    class Parent:
        def __init__(self, a: int, b: str):
            self.a: int = a
            self.b: str = b

    class Child(Parent):
        def __init__(self, a: int, b: str):
            self.a: int = 2 * a
            self.b: str = b

    assert validate_type(Parent, type)
    assert validate_type(Child, type)
    assert validate_type(Parent, typing.Type[Parent], do_except=True)
    assert validate_type(Child, typing.Type[Child])
    assert not validate_type(Parent, typing.Type[Child])

    assert validate_type(Child, typing.Union[typing.Type[Child], typing.Type[Parent]])
    assert validate_type(Child, typing.Union[typing.Type[Child], int])


@pytest.mark.skip(reason="Not implemented")
def test_validate_type_class_union():
    class Parent:
        def __init__(self, a: int, b: str):
            self.a: int = a
            self.b: str = b

    class Child(Parent):
        def __init__(self, a: int, b: str):
            self.a: int = 2 * a
            self.b: str = b

    class Other:
        def __init__(self, x: int, y: str):
            self.x: int = x
            self.y: str = y

    assert validate_type(Child, typing.Type[typing.Union[Child, Parent]])
    assert validate_type(Child, typing.Type[typing.Union[Child, Other]])
    assert validate_type(Parent, typing.Type[typing.Union[Child, Other]])
    assert validate_type(Parent, typing.Type[typing.Union[Parent, Other]])


def test_validate_type_aliases():
    AliasInt = int
    AliasStr = str
    AliasListInt = typing.List[int]
    AliasListStr = typing.List[str]
    AliasDictIntStr = typing.Dict[int, str]
    AliasDictStrInt = typing.Dict[str, int]
    AliasTupleIntStr = typing.Tuple[int, str]
    AliasTupleStrInt = typing.Tuple[str, int]
    AliasSetInt = typing.Set[int]
    AliasSetStr = typing.Set[str]
    AliasUnionIntStr = typing.Union[int, str]
    AliasUnionStrInt = typing.Union[str, int]
    AliasOptionalInt = typing.Optional[int]
    AliasOptionalStr = typing.Optional[str]
    AliasOptionalListInt = typing.Optional[typing.List[int]]
    AliasDictStrListInt = typing.Dict[str, typing.List[int]]

    assert validate_type(42, AliasInt)
    assert not validate_type("42", AliasInt)
    assert validate_type(42, AliasInt)
    assert not validate_type("42", AliasInt)
    assert validate_type("hello", AliasStr)
    assert not validate_type(42, AliasStr)
    assert validate_type([1, 2, 3], AliasListInt)
    assert not validate_type([1, "2", 3], AliasListInt)
    assert validate_type(["hello", "world"], AliasListStr)
    assert not validate_type(["hello", 42], AliasListStr)
    assert validate_type({1: "a", 2: "b"}, AliasDictIntStr)
    assert not validate_type({1: 2, 3: 4}, AliasDictIntStr)
    assert validate_type({"one": 1, "two": 2}, AliasDictStrInt)
    assert not validate_type({1: "one", 2: "two"}, AliasDictStrInt)
    assert validate_type((1, "a"), AliasTupleIntStr)
    assert not validate_type(("a", 1), AliasTupleIntStr)
    assert validate_type(("a", 1), AliasTupleStrInt)
    assert not validate_type((1, "a"), AliasTupleStrInt)
    assert validate_type({1, 2, 3}, AliasSetInt)
    assert not validate_type({1, "two", 3}, AliasSetInt)
    assert validate_type({"one", "two"}, AliasSetStr)
    assert not validate_type({"one", 2}, AliasSetStr)
    assert validate_type(42, AliasUnionIntStr)
    assert validate_type("hello", AliasUnionIntStr)
    assert not validate_type(3.14, AliasUnionIntStr)
    assert validate_type("hello", AliasUnionStrInt)
    assert validate_type(42, AliasUnionStrInt)
    assert not validate_type(3.14, AliasUnionStrInt)
    assert validate_type(42, AliasOptionalInt)
    assert validate_type(None, AliasOptionalInt)
    assert not validate_type("42", AliasOptionalInt)
    assert validate_type("hello", AliasOptionalStr)
    assert validate_type(None, AliasOptionalStr)
    assert not validate_type(42, AliasOptionalStr)
    assert validate_type([1, 2, 3], AliasOptionalListInt)
    assert validate_type(None, AliasOptionalListInt)
    assert not validate_type(["1", "2", "3"], AliasOptionalListInt)
    assert validate_type({"key": [1, 2, 3]}, AliasDictStrListInt)
    assert not validate_type({"key": [1, "2", 3]}, AliasDictStrListInt)
