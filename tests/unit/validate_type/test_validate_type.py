from __future__ import annotations

import typing
from typing import Any, Optional, Union

import pytest

from muutils.validate_type import validate_type


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
            typing.Tuple[
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
    with pytest.raises(ValueError):
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
    assert validate_type([{"key": 2}], typing.List[typing.Dict[str, str]]) == False
    assert validate_type([[1, 2], [3, 4]], typing.List[typing.List[int]])
    assert validate_type([[1, 2], [3, "4"]], typing.List[typing.List[int]]) == False
    assert validate_type([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]])
    assert (
        validate_type([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]]) == False
    )
    assert validate_type({1: "one", 2: "two"}, typing.Dict[int, str])
    assert validate_type({1: "one", 2: 2}, typing.Dict[int, str]) == False
    assert validate_type([(1, "one"), (2, "two")], typing.List[typing.Tuple[int, str]])
    assert (
        validate_type([(1, "one"), (2, 2)], typing.List[typing.Tuple[int, str]])
        == False
    )
    assert validate_type({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]])
    assert (
        validate_type({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]])
        == False
    )
    assert validate_type([(1, "a"), (2, "b")], typing.List[typing.Tuple[int, str]])
    assert (
        validate_type([(1, "a"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
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
