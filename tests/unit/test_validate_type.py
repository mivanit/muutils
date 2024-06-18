import pytest

import typing

from muutils.validate_type import validate_type
import types
import typing
from typing import Any, Dict, List, Set, Tuple, Union


def testvalidate_type_basic_types():
    assert validate_type(42, int)
    assert validate_type(3.14, float)
    assert validate_type("hello", str)
    assert validate_type(True, bool)
    assert validate_type([1, 2, 3], list)
    assert validate_type({'a': 1, 'b': 2}, dict)
    assert validate_type({1, 2, 3}, set)
    assert validate_type((1, 2, 3), tuple)

def testvalidate_type_any():
    assert validate_type(42, Any)
    assert validate_type("hello", Any)
    assert validate_type([1, 2, 3], Any)

def testvalidate_type_union():
    assert validate_type(42, Union[int, str])
    assert validate_type("hello", Union[int, str])
    assert validate_type(3.14, Union[int, float])
    assert not validate_type(True, Union[int, str])

def testvalidate_type_list():
    assert validate_type([1, 2, 3], List[int])
    assert validate_type(["a", "b", "c"], List[str])
    assert not validate_type([1, "a", 3], List[int])
    assert not validate_type(42, List[int])

def testvalidate_type_dict():
    assert validate_type({'a': 1, 'b': 2}, Dict[str, int])
    assert validate_type({1: 'a', 2: 'b'}, Dict[int, str])
    assert not validate_type({'a': 1, 'b': 'c'}, Dict[str, int])
    assert not validate_type([('a', 1), ('b', 2)], Dict[str, int])

def testvalidate_type_set():
    assert validate_type({1, 2, 3}, Set[int])
    assert validate_type({"a", "b", "c"}, Set[str])
    assert not validate_type({1, "a", 3}, Set[int])
    assert not validate_type([1, 2, 3], Set[int])

def testvalidate_type_tuple():
    assert validate_type((1, 'a', 3.14), Tuple[int, str, float])
    assert validate_type(('a', 'b', 'c'), Tuple[str, str, str])
    assert not validate_type((1, 'a', 3.14), Tuple[int, str])
    assert not validate_type([1, 'a', 3.14], Tuple[int, str, float])

def testvalidate_type_unsupported_type_hint():
    with pytest.raises(ValueError, match="Unsupported type hint"):
        validate_type(42, typing.Callable[[], None])

def testvalidate_type_unsupported_generic_alias():
    with pytest.raises(ValueError, match="Unsupported generic alias"):
        validate_type([1, 2, 3], List[int, str])

def testvalidate_type_edge_cases():
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

def testvalidate_type():
    assert validate_type(5, int) == True
    assert validate_type(5.0, int) == False
    assert validate_type("hello", str) == True
    assert validate_type("hello", typing.Any) == True
    assert validate_type([1, 2, 3], typing.List[int]) == True
    assert validate_type([1, "2", 3], typing.List[int]) == False
    assert validate_type({"key": "value"}, typing.Dict[str, str]) == True
    assert validate_type({"key": 2}, typing.Dict[str, str]) == False
    assert validate_type((1, "a"), typing.Tuple[int, str]) == True
    assert validate_type((1, 2), typing.Tuple[int, str]) == False
    assert validate_type((1, 2), typing.Tuple[int, int]) == True
    assert validate_type((1, 2, 3), typing.Tuple[int, int]) == False
    assert validate_type(5, typing.Union[int, str]) == True
    assert validate_type("hello", typing.Union[int, str]) == True
    assert validate_type(5.0, typing.Union[int, str]) == False
    assert validate_type(None, typing.Union[int, type(None)]) == True
    assert validate_type(None, typing.Union[int, type(None), str]) == True
    assert validate_type(None, typing.Union[int, str]) == False
    assert validate_type({"key": 2}, typing.Dict[str, int]) == True
    assert validate_type({"key": 2.0}, typing.Dict[str, int]) == False
    assert validate_type([{"key": "value"}], typing.List[typing.Dict[str, str]]) == True
    assert validate_type([{"key": 2}], typing.List[typing.Dict[str, str]]) == False
    assert validate_type([[1, 2], [3, 4]], typing.List[typing.List[int]]) == True
    assert validate_type([[1, 2], [3, "4"]], typing.List[typing.List[int]]) == False
    assert validate_type([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]]) == True
    assert validate_type([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]]) == False
    assert validate_type({1: "one", 2: "two"}, typing.Dict[int, str]) == True
    assert validate_type({1: "one", 2: 2}, typing.Dict[int, str]) == False
    assert validate_type([(1, "one"), (2, "two")], typing.List[typing.Tuple[int, str]]) == True
    assert validate_type([(1, "one"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
    assert validate_type({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]]) == True
    assert validate_type({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]]) == False
    assert validate_type(3.14, float) == True
    assert validate_type(3.14, int) == False
    assert validate_type("3.14", float) == False
    assert validate_type(b"bytes", bytes) == True
    assert validate_type(b"bytes", str) == False
    assert validate_type({"a": 1, "b": 2}, typing.Dict[str, int]) == True
    assert validate_type({"a": 1, "b": "2"}, typing.Dict[str, int]) == False
    assert validate_type([(1, "a"), (2, "b")], typing.List[typing.Tuple[int, str]]) == True
    assert validate_type([(1, "a"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
    assert validate_type([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]]) == True
    assert validate_type([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]]) == False
    assert validate_type({1: "one", 2: "two"}, typing.Dict[int, str]) == True
    assert validate_type({1: "one", 2: 2}, typing.Dict[int, str]) == False
    assert validate_type([(1, "one"), (2, "two")], typing.List[typing.Tuple[int, str]]) == True
    assert validate_type([(1, "one"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
    assert validate_type({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]]) == True
    assert validate_type({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]]) == False
    assert validate_type(3.14, float) == True
    assert validate_type(3.14, int) == False
    assert validate_type("3.14", float) == False
    assert validate_type(b"bytes", bytes) == True
    assert validate_type(b"bytes", str) == False
    assert validate_type({"a": 1, "b": 2}, typing.Dict[str, int]) == True
    assert validate_type({"a": 1, "b": "2"}, typing.Dict[str, int]) == False
    assert validate_type([(1, "a"), (2, "b")], typing.List[typing.Tuple[int, str]]) == True
    assert validate_type([(1, "a"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
    assert validate_type([(1, 2), (3, 4)], typing.List[typing.Tuple[int, int]]) == True
    assert validate_type([(1, 2), (3, "4")], typing.List[typing.Tuple[int, int]]) == False
    assert validate_type({1: "one", 2: "two"}, typing.Dict[int, str]) == True
    assert validate_type({1: "one", 2: 2}, typing.Dict[int, str]) == False
    assert validate_type([(1, "one"), (2, "two")], typing.List[typing.Tuple[int, str]]) == True
    assert validate_type([(1, "one"), (2, 2)], typing.List[typing.Tuple[int, str]]) == False
    assert validate_type({1: [1, 2], 2: [3, 4]}, typing.Dict[int, typing.List[int]]) == True
    assert validate_type({1: [1, 2], 2: [3, "4"]}, typing.Dict[int, typing.List[int]]) == False
    assert validate_type(3.14, float) == True
    assert validate_type(3.14, int) == False
    assert validate_type("3.14", float) == False
    assert validate_type(b"bytes", bytes) == True
    assert validate_type(b"bytes", str) == False
    assert validate_type({"a": 1, "b": 2}, typing.Dict[str, int]) == True
    assert validate_type({"a": 1, "b": "2"}, typing.Dict[str, int]) == False
    assert validate_type([(1, "a"), (2, "b")], typing.List[typing.Tuple[int, str]]) == True
