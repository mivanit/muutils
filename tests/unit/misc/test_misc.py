from __future__ import annotations
from typing import Iterable, Any, Type, Union
from dataclasses import dataclass
import abc
import pytest
from pytest import mark, param

from muutils.misc import (
    dict_to_filename,
    freeze,
    sanitize_fname,
    sanitize_identifier,
    sanitize_name,
    stable_hash,
    flatten,
    get_all_subclasses,
    IsDataclass,
    isinstance_by_type_name,
    dataclass_set_equals,
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
def test_flatten(deep: Iterable[Any], flat: Iterable[Any], depth: Union[int, None]):
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


# Test classes
@dataclass
class DC1:
    x: bool
    y: bool = False


@dataclass(frozen=True)
class DC2:
    x: bool
    y: bool = False


@dataclass(frozen=True)
class DC3:
    x: DC2 = DC2(False, False)


@dataclass(frozen=True)
class DC4:
    x: DC2
    y: bool = False


@dataclass(frozen=True)
class DC5:
    x: int


@dataclass(frozen=True)
class DC6:
    x: DC5
    y: bool = False


@dataclass(frozen=True)
class DC7(abc.ABC):
    x: bool

    @abc.abstractmethod
    def foo(self):
        pass


@dataclass(frozen=True)
class DC8(DC7):
    x: bool = False

    def foo(self):
        pass


@dataclass(frozen=True)
class DC9(DC7):
    y: bool = True

    def foo(self):
        pass


@mark.parametrize(
    "coll1, coll2, result",
    [
        param(
            c1,
            c2,
            res,
            id=f"{c1}_{c2}",
        )
        for c1, c2, res in (
            [
                (
                    [
                        DC1(False, False),
                        DC1(False, True),
                    ],
                    [
                        DC1(True, False),
                        DC1(True, True),
                    ],
                    False,
                ),
                (
                    [
                        DC1(False, False),
                        DC1(False, True),
                    ],
                    [
                        DC1(False, False),
                        DC1(False, True),
                    ],
                    True,
                ),
                (
                    [
                        DC1(False, False),
                        DC1(False, True),
                    ],
                    [
                        DC2(False, False),
                        DC2(False, True),
                    ],
                    False,
                ),
                (
                    [
                        DC3(DC2(False)),
                        DC3(DC2(False)),
                    ],
                    [
                        DC3(DC2(False)),
                    ],
                    True,
                ),
                ([], [], True),
                ([DC5], [DC5], AttributeError),
            ]
        )
    ],
)
def test_dataclass_set_equals(
    coll1: Iterable[IsDataclass],
    coll2: Iterable[IsDataclass],
    result: Union[bool, Type[Exception]],
):
    if isinstance(result, type) and issubclass(result, Exception):
        with pytest.raises(result):
            dataclass_set_equals(coll1, coll2)
    else:
        assert dataclass_set_equals(coll1, coll2) == result


@mark.parametrize(
    "o, type_name, result",
    [
        param(
            o,
            name,
            res,
            id=f"{o}_{name}",
        )
        for o, name, res in (
            [
                (True, "bool", True),
                (True, "int", True),
                (1, "int", True),
                (1, "bool", False),
                ([], "list", True),
            ]
        )
    ],
)
def test_isinstance_by_type_name(
    o: object, type_name: str, result: Union[bool, Type[Exception]]
):
    if isinstance(result, type) and issubclass(result, Exception):
        with pytest.raises(result):
            isinstance_by_type_name(o, type_name)
    else:
        assert isinstance_by_type_name(o, type_name) == result
