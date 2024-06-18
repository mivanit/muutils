from __future__ import annotations

import pytest

import typing

from muutils.validate_type import validate_type
import types
import typing
from typing import Any, Dict, List, Set, Tuple, Union, Optional

# Tests for basic types and common use cases
@pytest.mark.parametrize("value, expected_type, result", [
    (42, int, True),
    (3.14, float, True),
    (5, int, True),
    (5.0, int, False),
    ("hello", str, True),
    (True, bool, True),
    (None, type(None), True),
    (None, int, False),
    ([1, 2, 3], list, True),
    ([1, 2, 3], List, True),
    ({'a': 1, 'b': 2}, dict, True),
    ({'a': 1, 'b': 2}, Dict, True),
    ({1, 2, 3}, set, True),
    ({1, 2, 3}, Set, True),
    ((1, 2, 3), tuple, True),
    ((1, 2, 3), Tuple, True),
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

])
def test_validate_type_basic(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e

@pytest.mark.parametrize("value", [
    42,
    "hello",
    3.14,
    True,
    None,
    [1, 2, 3],
    {'a': 1, 'b': 2},
    {1, 2, 3},
    (1, 2, 3),
    b"bytes",
    "3.14",
])
def test_validate_type_any(value):
    try:
        assert validate_type(value, Any)
    except Exception as e:
        raise Exception(f"{value = }, expected `Any`, {e}") from e

@pytest.mark.parametrize("value, expected_type, result", [
    (42, Union[int, str], True),
    ("hello", Union[int, str], True),
    (3.14, Union[int, float], True),
    (True, Union[int, str], False),
    (None, Union[int, type(None)], True),
    (None, Union[int, str], False),
    (5, Union[int, str], True),
    (5.0, Union[int, str], True),
    ("hello", Union[int, str], True),
    (5, typing.Union[int, str], True),
    ("hello", typing.Union[int, str], True),
    (5.0, typing.Union[int, str], False),
    (5, Union[int, str], True),
    ("hello", Union[int, str], True),
    (5.0, Union[int, str], False),
    (5, int|str, True),
    ("hello", int|str, True),
    (5.0, int|str, False),
    (None, typing.Union[int, type(None)], True),
    (None, typing.Union[int, str], False),
    (None, int|str, False),
])
def test_validate_type_union(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e

@pytest.mark.parametrize("value, expected_type, result", [
    (42, Optional[int], True),
    ("hello", Optional[int], False),
    (3.14, Optional[int], False),
    ([1], Optional[List[int]], True),
    (None, Optional[int], True),
    (None, Optional[str], False),
    (None, Optional[int], True),
    (None, Optional[None], True),
    (None, Optional[list[dict[str, int]]], True),
    (42, int|None, True),
    ("hello", int|None, False),
    (3.14, int|None, False),
    ([1], List[int]|None, True),
    (None, int|None, True),
    (None, str|None, False),
    (None, None|str, False),
    (None, None|int, True),
    (None, None|List[Dict[str, int]], True),
])
def test_validate_type_optional(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e

@pytest.mark.parametrize("value, expected_type, result", [
    (42, List[int], False),
    ([1, 2, 3], List[int], True),
    ([1, 2, 3], List[str], False),
    (["a", "b", "c"], List[str], True),
    ([1, "a", 3], List[int], False),
    (42, List[int], False),
    ([1, 2, 3], List[int], True),
    ([1, "2", 3], List[int], False),
])
def test_validate_type_list(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e



@pytest.mark.parametrize("value, expected_type, result", [
    (42, dict[str, int], False),
    ({'a': 1, 'b': 2}, dict[str, int], True),
    ({'a': 1, 'b': 2}, dict[int, str], False),
    (42, Dict[str, int], False),
    ({'a': 1, 'b': 2}, Dict[str, int], True),
    ({'a': 1, 'b': 2}, Dict[int, str], False),
    ({1: 'a', 2: 'b'}, Dict[int, str], True),
    ({1: 'a', 2: 'b'}, Dict[str, int], False),
    ({'a': 1, 'b': 'c'}, Dict[str, int], False),
    ([('a', 1), ('b', 2)], Dict[str, int], False),
    ({"key": "value"}, Dict[str, str], True),
    ({"key": 2}, Dict[str, str], False),
    ({"key": 2}, Dict[str, int], True),
    ({"key": 2.0}, Dict[str, int], False),
    ({"a": 1, "b": 2}, Dict[str, int], True),
    ({"a": 1, "b": "2"}, Dict[str, int], False),
])
def test_validate_type_dict(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e

@pytest.mark.parametrize("value, expected_type, result", [
    (42, set[int], False),
    ({1, 2, 3}, set[int], True),
    (42, Set[int], False),
    ({1, 2, 3}, Set[int], True),
    ({1, 2, 3}, Set[str], False),
    ({"a", "b", "c"}, Set[str], True),
    ({1, "a", 3}, Set[int], False),
    (42, Set[int], False),
    ({1, 2, 3}, Set[int], True),
    ({1, "2", 3}, Set[int], False),
    ([1, 2, 3], Set[int], False),
    ("hello", Set[str], False),
])
def test_validate_type_set(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e

@pytest.mark.parametrize("value, expected_type, result", [
    (42, tuple[int, str], False),
    ((1, "a"), tuple[int, str], True),
    (42, Tuple[int, str], False),
    ((1, "a"), Tuple[int, str], True),
    ((1, 2), Tuple[int, str], False),
    ((1, 2), Tuple[int, int], True),
    ((1, 2, 3), Tuple[int, int], False),
    ((1, 'a', 3.14), Tuple[int, str, float], True),
    (('a', 'b', 'c'), Tuple[str, str, str], True),
    ((1, 'a', 3.14), Tuple[int, str], False),
    ([1, 'a', 3.14], Tuple[int, str, float], True),
])
def test_validate_type_tuple(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e

@pytest.mark.parametrize("value, expected_type", [
    (43, typing.Callable),
    (lambda x: x, typing.Callable),
    (42, typing.Callable[[], None]),
    (42, typing.Callable[[int, str], list]),
])
def test_validate_type_unsupported_type_hint(value, expected_type):
    with pytest.raises(ValueError):
        validate_type(value, expected_type)
        print(f"Failed to except: {value = }, {expected_type = }")

@pytest.mark.parametrize("value, expected_type", [
    (42, list[int, str]),
    ([1, 2, 3], list[int, str]),
    ({"a": 1, "b": 2}, set[str, int]),
    ({1: "a", 2: "b"}, set[int, str]),
    ({"a": 1, "b": 2}, set[str, int, str]),
    ({1: "a", 2: "b"}, set[int, str, int]),
    ({1, 2, 3}, set[int, str]),
    ({"a"}, set[int, str]),
])
def test_validate_type_unsupported_generic_alias(value, expected_type):
    with pytest.raises(TypeError):
        validate_type(value, expected_type)
        print(f"Failed to except: {value = }, {expected_type = }")

@pytest.mark.parametrize("value, expected_type, result", [
    ([1, 2, 3], List[int], True),
    (["a", "b", "c"], List[str], True),
    ([1, "a", 3], List[int], False),
    ([1, 2, [3, 4]], List[Union[int, List[int]]], True),
    ([(1, 2), (3, 4)], List[Tuple[int, int]], True),
    ([(1, 2), (3, "4")], List[Tuple[int, int]], False),
    ({1: [1, 2], 2: [3, 4]}, Dict[int, List[int]], True),
    ({1: [1, 2], 2: [3, "4"]}, Dict[int, List[int]], False),
])
def test_validate_type_collections(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e


@pytest.mark.parametrize("value, expected_type, result", [
    # empty lists
    ([], List[int], True),
    ([], list[dict], True),
    ([], list[tuple[dict[tuple, str], str, None]], True),
    # empty dicts
    ({}, Dict[str, int], True),
    ({}, dict[str, dict], True),
    ({}, dict[str, dict[str, int]], True),
    ({}, dict[str, dict[str, int]], True),
    # empty sets
    (set(), Set[int], True),
    (set(), set[dict], True),
    (set(), set[tuple[dict[tuple, str], str, None]], True),
    # empty tuple
    (tuple(), tuple, True),
    # empty string
    ("", str, True),
    # empty bytes
    (b"", bytes, True),
    # None
    (None, type(None), True),
    # weird floats
    (float("nan"), float, True),
    (float("inf"), float, True),
    (float("-inf"), float, True),
    (float(0), float, True),
    # list/tuple
    ([1], tuple[int, int], False),
    ((1,2), list[int], False),
])
def test_validate_type_edge_cases(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e


@pytest.mark.parametrize("value, expected_type, result", [
    (42, list[int], False),
    ([1, 2, 3], int, False),
    (3.14, tuple[float], False),
    (3.14, tuple[float, float], False),
    (3.14, tuple[bool, str], False),
    (False, tuple[bool, str], False),
    (False, tuple[bool], False),
    ((False,), tuple[bool], True),
    (("abc",), tuple[str], True),
    ("test-dict", dict[str, int], False),
    ("test-dict", dict, False),
])
def test_validate_type_wrong_type(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e



def test_validate_type_complex():
    assert validate_type([1, 2, [3, 4]], List[Union[int, List[int]]])
    assert validate_type({'a': 1, 'b': {'c': 2}}, Dict[str, Union[int, Dict[str, int]]])
    assert validate_type({1, (2, 3)}, Set[Union[int, Tuple[int, int]]])
    assert validate_type((1, ('a', 'b')), Tuple[int, Tuple[str, str]])
    assert validate_type([{"key": "value"}], typing.List[typing.Dict[str, str]])
    assert validate_type([{"key": 2}], typing.List[typing.Dict[str, str]]) == False
    assert validate_type([[1, 2], [3, 4]], typing.List[typing.List[int]])
    assert validate_type([[1, 2], [3, "4"]], typing.List[typing.List[int]]) == False
    assert validate_type([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]])
    assert validate_type([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]]) == False
    assert validate_type({1: "one", 2: "two"}, typing.Dict[int, str])
    assert validate_type({1: "one", 2: 2}, typing.Dict[int, str]) == False
    assert validate_type([(1, "one"), (2, "two")], typing.List[typing.Tuple[int, str]])
    assert validate_type([(1, "one"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
    assert validate_type({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]])
    assert validate_type({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]]) == False
    assert validate_type([(1, "a"), (2, "b")], typing.List[typing.Tuple[int, str]])
    assert validate_type([(1, "a"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False

    
@pytest.mark.parametrize("value, expected_type, result", [
    ([[[[1]]]], List[List[List[List[int]]]], True),
    ([[[[1]]]], List[List[List[List[str]]]], False),
    ({"a": {"b": {"c": 1}}}, Dict[str, Dict[str, Dict[str, int]]], True),
    ({"a": {"b": {"c": 1}}}, Dict[str, Dict[str, Dict[str, str]]], False),
    ({1, 2, 3}, Set[int], True),
    ({1, 2, 3}, Set[str], False),
    (((1, 2), (3, 4)), Tuple[Tuple[int, int], Tuple[int, int]], True),
    (((1, 2), (3, 4)), Tuple[Tuple[int, int], Tuple[int, str]], False),
])
def test_validate_type_nested(value, expected_type, result):
    try:
        assert validate_type(value, expected_type) == result
    except Exception as e:
        raise Exception(f"{value = }, {expected_type = }, {result = }, {e}") from e


                         