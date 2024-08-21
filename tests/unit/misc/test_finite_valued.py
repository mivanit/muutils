import abc
from dataclasses import dataclass
from typing import Callable, Iterable, Literal

import pytest

from pytest import mark, param

from muutils.misc import IsDataclass, dataclass_set_equals
from muutils.misc.finite_valued import all_instances, FiniteValued


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
    def foo():
        pass


@dataclass(frozen=True)
class DC8(DC7):
    x: bool = False

    def foo():
        pass


@dataclass(frozen=True)
class DC9(DC7):
    y: bool = True

    def foo():
        pass


@mark.parametrize(
    "type_, validation_funcs, result",
    [
        param(
            type_,
            vfs,
            result,
            id=f"{type_}-vfs[{len(vfs) if vfs is not None else 'None'}]",
        )
        for type_, vfs, result in (
            [
                (
                    DC1,
                    None,
                    [
                        DC1(False, False),
                        DC1(False, True),
                        DC1(True, False),
                        DC1(True, True),
                    ],
                ),
                (
                    DC2,
                    None,
                    [
                        DC2(False, False),
                        DC2(False, True),
                        DC2(True, False),
                        DC2(True, True),
                    ],
                ),
                (
                    DC2,
                    {DC2: lambda dc: dc.x ^ dc.y},
                    [
                        DC2(False, True),
                        DC2(True, False),
                    ],
                ),
                (
                    DC1 | DC2,
                    {DC2: lambda dc: dc.x ^ dc.y},
                    [
                        DC2(False, True),
                        DC2(True, False),
                        DC1(False, False),
                        DC1(False, True),
                        DC1(True, False),
                        DC1(True, True),
                    ],
                ),
                (
                    DC1 | DC2,
                    {
                        DC1: lambda dc: dc.x == dc.y,
                        DC2: lambda dc: dc.x ^ dc.y,
                    },
                    [
                        DC2(False, True),
                        DC2(True, False),
                        DC1(False, False),
                        DC1(True, True),
                    ],
                ),
                (
                    DC3,
                    None,
                    [
                        DC3(DC2(False, False)),
                        DC3(DC2(False, True)),
                        DC3(DC2(True, False)),
                        DC3(DC2(True, True)),
                    ],
                ),
                (
                    DC4,
                    None,
                    [
                        DC4(DC2(False, False), True),
                        DC4(DC2(False, True), True),
                        DC4(DC2(True, False), True),
                        DC4(DC2(True, True), True),
                        DC4(DC2(False, False), False),
                        DC4(DC2(False, True), False),
                        DC4(DC2(True, False), False),
                        DC4(DC2(True, True), False),
                    ],
                ),
                (
                    DC4,
                    {DC2: lambda dc: dc.x ^ dc.y},
                    [
                        DC4(DC2(False, True), True),
                        DC4(DC2(True, False), True),
                        DC4(DC2(False, True), False),
                        DC4(DC2(True, False), False),
                    ],
                ),
                (DC5, None, TypeError),
                (DC6, None, TypeError),
                (bool, None, [True, False]),
                (bool, {bool: lambda x: x}, [True]),
                (bool, {bool: lambda x: not x}, [False]),
                (int, None, TypeError),
                (str, None, TypeError),
                (Literal[0, 1, 2], None, [0, 1, 2]),
                (Literal[0, 1, 2], {int: lambda x: x % 2 == 0}, [0, 2]),
                (bool | Literal[0, 1, 2], dict(), [0, 1, 2, True, False]),
                (bool | Literal[0, 1, 2], {bool: lambda x: x}, [0, 1, 2, True]),
                (bool | Literal[0, 1, 2], {int: lambda x: x % 2}, [1, True]),
                (
                    tuple[bool],
                    None,
                    [
                        (True,),
                        (False,),
                    ],
                ),
                (
                    tuple[bool, bool],
                    None,
                    [
                        (True, True),
                        (True, False),
                        (False, True),
                        (False, False),
                    ],
                ),
                (
                    tuple[bool, bool],
                    {bool: lambda x: x},
                    [
                        (True, True),
                    ],
                ),
                (
                    DC8,
                    None,
                    [
                        DC8(False),
                        DC8(True),
                    ],
                ),
                (
                    DC7,
                    None,
                    [
                        DC8(False),
                        DC8(True),
                        DC9(False, False),
                        DC9(False, True),
                        DC9(True, False),
                        DC9(True, True),
                    ],
                ),
                (
                    tuple[DC7],
                    None,
                    [
                        (DC8(False),),
                        (DC8(True),),
                        (DC9(False, False),),
                        (DC9(False, True),),
                        (DC9(True, False),),
                        (DC9(True, True),),
                    ],
                ),
                (
                    tuple[DC7],
                    {DC9: lambda dc: dc.x == dc.y},
                    [
                        (DC8(False),),
                        (DC8(True),),
                        (DC9(False, False),),
                        (DC9(True, True),),
                    ],
                ),
                (
                    tuple[DC8, DC8],
                    None,
                    [
                        (DC8(False), DC8(False)),
                        (DC8(False), DC8(True)),
                        (DC8(True), DC8(False)),
                        (DC8(True), DC8(True)),
                    ],
                ),
                (
                    tuple[DC7, bool],
                    None,
                    [
                        (DC8(False), True),
                        (DC8(True), True),
                        (DC9(False, False), True),
                        (DC9(False, True), True),
                        (DC9(True, False), True),
                        (DC9(True, True), True),
                        (DC8(False), False),
                        (DC8(True), False),
                        (DC9(False, False), False),
                        (DC9(False, True), False),
                        (DC9(True, False), False),
                        (DC9(True, True), False),
                    ],
                ),
            ]
        )
    ],
)
def test_all_instances(
    type_: FiniteValued,
    validation_funcs: dict[FiniteValued, Callable[[FiniteValued], bool]] | None,
    result: type[Exception] | Iterable[FiniteValued],
):
    if isinstance(result, type) and issubclass(result, Exception):
        with pytest.raises(result):
            list(all_instances(type_, validation_funcs))
    elif hasattr(type_, "__dataclass_fields__"):
        assert dataclass_set_equals(all_instances(type_, validation_funcs), result)
    else:  # General case, due to nesting, results might contain some dataclasses and some other types
        out = list(all_instances(type_, validation_funcs))
        assert dataclass_set_equals(
            filter(lambda x: isinstance(x, IsDataclass), out),
            filter(lambda x: isinstance(x, IsDataclass), result),
        )
        assert set(filter(lambda x: not isinstance(x, IsDataclass), out)) == set(
            filter(lambda x: not isinstance(x, IsDataclass), result)
        )
