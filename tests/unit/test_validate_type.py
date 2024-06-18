from __future__ import annotations

import pytest

import typing

from muutils.validate_type import validate_type
import types
import typing
from typing import Any, Dict, List, Set, Tuple, Union

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
])
def test_validate_type_basic(value, expected_type, result):
    assert validate_type(value, expected_type) == result


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
    assert validate_type(value, Any)

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
])
def test_validate_type_union(value, expected_type, result):
    assert validate_type(value, expected_type) == result


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
    assert validate_type(value, expected_type) == result


@pytest.mark.parametrize("value, expected_type, result", [
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
    assert validate_type(value, expected_type) == result

@pytest.mark.parametrize("value, expected_type, result", [
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
    assert validate_type(value, expected_type) == result

def test_validate_type_tuple():
    assert validate_type((1, "a"), typing.Tuple[int, str])
    assert validate_type((1, 2), typing.Tuple[int, str]) == False
    assert validate_type((1, 2), typing.Tuple[int, int])
    assert validate_type((1, 2, 3), typing.Tuple[int, int]) == False
    assert validate_type((1, 'a', 3.14), Tuple[int, str, float])
    assert validate_type(('a', 'b', 'c'), Tuple[str, str, str])
    assert not validate_type((1, 'a', 3.14), Tuple[int, str])
    assert not validate_type([1, 'a', 3.14], Tuple[int, str, float])

def test_validate_type_union():
    assert validate_type(5, typing.Union[int, str])
    assert validate_type("hello", typing.Union[int, str])
    assert validate_type(5.0, typing.Union[int, str]) == False
    assert validate_type(None, typing.Union[int, type(None)])
    assert validate_type(None, typing.Union[int, type(None), str])
    assert validate_type(None, typing.Union[int, str]) == False


def test_validate_type_unsupported_type_hint():
    with pytest.raises(ValueError, match="Unsupported type hint"):
        validate_type(42, typing.Callable[[], None])

def test_validate_type_unsupported_generic_alias():
    with pytest.raises(ValueError, match="Unsupported generic alias"):
        validate_type([1, 2, 3], List[int, str])

@pytest.mark.parametrize("value, expected_type, expected_result", [
    ([1, 2, 3], List[int], True),
    (["a", "b", "c"], List[str], True),
    ([1, "a", 3], List[int], False),
    ([1, 2, [3, 4]], List[Union[int, List[int]]], True),
    ([(1, 2), (3, 4)], List[Tuple[int, int]], True),
    ([(1, 2), (3, "4")], List[Tuple[int, int]], False),
    ({1: [1, 2], 2: [3, 4]}, Dict[int, List[int]], True),
    ({1: [1, 2], 2: [3, "4"]}, Dict[int, List[int]], False),
])
def test_validate_type_collections(value, expected_type, expected_result):
    assert validate_type(value, expected_type) == expected_result

def test_validate_type_edge_cases():
    assert validate_type([], List[int])
    assert validate_type({}, Dict[str, int])
    assert validate_type(set(), Set[int])
    # assert validate_type((), Tuple[])
    
    assert not validate_type(42, List[int])
    assert not validate_type("hello", Dict[str, int])
    assert not validate_type([1, 2], Tuple[int, int, int])
    
    assert validate_type([1, 2, [3, 4]], List[Union[int, List[int]]])
    assert validate_type({'a': 1, 'b': {'c': 2}}, Dict[str, Union[int, Dict[str, int]]])
    assert validate_type({1, (2, 3)}, Set[Union[int, Tuple[int, int]]])
    assert validate_type((1, ('a', 'b')), Tuple[int, Tuple[str, str]])

def test_validate_type_complex():
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
    assert validate_type(value, expected_type) == result


                         