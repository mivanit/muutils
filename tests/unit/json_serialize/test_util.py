from collections import namedtuple
from typing import NamedTuple

import pytest

# Module code assumed to be imported from my_module
from muutils.json_serialize.util import (
    UniversalContainer,
    _recursive_hashify,
    isinstance_namedtuple,
    safe_getsource,
    string_as_lines,
    try_catch,
)


def test_universal_container():
    uc = UniversalContainer()
    assert "anything" in uc
    assert 123 in uc
    assert None in uc


def test_isinstance_namedtuple():
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    assert isinstance_namedtuple(p)
    assert not isinstance_namedtuple((1, 2))

    class Point2(NamedTuple):
        x: int
        y: int

    p2 = Point2(1, 2)
    assert isinstance_namedtuple(p2)


def test_try_catch():
    @try_catch
    def raises_value_error():
        raise ValueError("test error")

    @try_catch
    def normal_func(x):
        return x

    assert raises_value_error() == "ValueError: test error"
    assert normal_func(10) == 10


def test_recursive_hashify():
    assert _recursive_hashify({"a": [1, 2, 3]}) == (("a", (1, 2, 3)),)
    assert _recursive_hashify([1, 2, 3]) == (1, 2, 3)
    assert _recursive_hashify(123) == 123
    with pytest.raises(ValueError):
        _recursive_hashify(object(), force=False)


def test_string_as_lines():
    assert string_as_lines("line1\nline2\nline3") == ["line1", "line2", "line3"]
    assert string_as_lines(None) == []


def test_safe_getsource():
    def sample_func():
        pass

    source = safe_getsource(sample_func)
    print(f"Source of sample_func: {source}")
    assert "def sample_func():" in source[0]

    def raises_error():
        raise Exception("test error")

    wrapped_func = try_catch(raises_error)
    error_source = safe_getsource(wrapped_func)
    print(f"Source of wrapped_func: {error_source}")
    # Check for the original function's source since the decorator doesn't change this
    assert any("def raises_error():" in line for line in error_source)
