import math
from typing import Union, Tuple

import pytest

from muutils.interval import Interval, ClosedInterval, OpenInterval


@pytest.fixture
def sample_intervals():
    return [
        Interval(1, 5),
        Interval([1, 5]),
        Interval(1, 5, closed_L=True),
        ClosedInterval(1, 5),
        OpenInterval(1, 5),
    ]


def test_interval_initialization():
    assert str(Interval(1, 5)) == "(1, 5)"
    assert str(Interval([1, 5])) == "[1, 5]"
    assert str(Interval(1, 5, closed_L=True)) == "[1, 5)"
    assert str(Interval(1, 5, closed_R=True)) == "(1, 5]"
    assert str(Interval(1, 5, is_closed=True)) == "[1, 5]"


def test_closed_interval_initialization():
    assert str(ClosedInterval(1, 5)) == "[1, 5]"
    assert str(ClosedInterval([1, 5])) == "[1, 5]"


def test_open_interval_initialization():
    assert str(OpenInterval(1, 5)) == "(1, 5)"
    assert str(OpenInterval([1, 5])) == "(1, 5)"


@pytest.mark.parametrize(
    "interval,point,expected",
    [
        (Interval(1, 5), 3, True),
        (Interval(1, 5), 1, False),
        (Interval(1, 5), 5, False),
        (Interval([1, 5]), 1, True),
        (Interval([1, 5]), 5, True),
        (Interval(1, 5, closed_L=True), 1, True),
        (Interval(1, 5, closed_R=True), 5, True),
        (ClosedInterval(1, 5), 1, True),
        (ClosedInterval(1, 5), 5, True),
        (OpenInterval(1, 5), 1, False),
        (OpenInterval(1, 5), 5, False),
    ],
)
def test_containment_minimal(
    interval: Interval, point: Union[int, float], expected: bool
):
    assert (point in interval) == expected


def test_equality():
    assert Interval(1, 5) == Interval(1, 5)
    assert Interval([1, 5]) == Interval(1, 5, is_closed=True)
    assert Interval(1, 5) != Interval(1, 5, closed_L=True)
    assert ClosedInterval(1, 5) == Interval([1, 5])
    assert OpenInterval(1, 5) == Interval(1, 5)
    assert Interval(1, 5) != "not an interval"


@pytest.mark.parametrize(
    "args,kwargs",
    [
        ((5, 1), {}),  # Lower bound greater than upper bound
        ((1, 2, 3), {}),  # Too many arguments
        (([1, 2, 3],), {}),  # List with wrong number of elements
        (
            (1, 5),
            {"is_closed": True, "closed_L": True},
        ),  # Conflicting closure specifications
    ],
)
def test_invalid_initialization(args: Tuple, kwargs: dict):
    with pytest.raises(ValueError):
        Interval(*args, **kwargs)


def test_closed_interval_invalid_initialization():
    with pytest.raises(ValueError):
        ClosedInterval(1, 5, closed_L=True)


def test_open_interval_invalid_initialization():
    with pytest.raises(ValueError):
        OpenInterval(1, 5, is_closed=True)


@pytest.mark.parametrize(
    "interval,point,expected",
    [
        # Integer tests
        (Interval(1, 5), 3, True),
        (Interval(1, 5), 1, False),
        (Interval(1, 5), 5, False),
        (Interval([1, 5]), 1, True),
        (Interval([1, 5]), 5, True),
        (Interval(1, 5, closed_L=True), 1, True),
        (Interval(1, 5, closed_R=True), 5, True),
        (ClosedInterval(1, 5), 1, True),
        (ClosedInterval(1, 5), 5, True),
        (OpenInterval(1, 5), 1, False),
        (OpenInterval(1, 5), 5, False),
        # Float tests
        (Interval(1.5, 5.5), 3.14, True),
        (Interval(1.5, 5.5), 1.5, False),
        (Interval(1.5, 5.5), 5.5, False),
        (Interval([1.5, 5.5]), 1.5, True),
        (Interval([1.5, 5.5]), 5.5, True),
        # Mixed integer and float tests
        (Interval(1, 5.5), 5, True),
        (Interval(1.5, 5), 2, True),
        # Infinity tests
        (Interval(-math.inf, 0), -1000000, True),
        (Interval(-math.inf, 0), 0, False),
        (Interval(-math.inf, 0, closed_R=True), 0, True),
        (Interval(0, math.inf), 1000000, True),
        (Interval(0, math.inf), 0, False),
        (Interval(0, math.inf, closed_L=True), 0, True),
        (Interval(-math.inf, math.inf), 0, True),
        (Interval(-math.inf, math.inf), math.inf, False),
        (Interval(-math.inf, math.inf), -math.inf, False),
        (ClosedInterval(-math.inf, math.inf), math.inf, True),
        (ClosedInterval(-math.inf, math.inf), -math.inf, True),
        # Very large and very small number tests
        (Interval(1e-10, 1e10), 1, True),
        (Interval(1e-10, 1e10), 1e-11, False),
        (Interval(1e-10, 1e10), 1e11, False),
    ],
)
def test_containment(interval: Interval, point: Union[int, float], expected: bool):
    assert (point in interval) == expected


def test_nan_handling():
    interval = Interval(0, 1)
    with pytest.raises(ValueError):
        _ = math.nan in interval

    with pytest.raises(ValueError):
        Interval(0, math.nan)

    with pytest.raises(ValueError):
        Interval(math.nan, 1)
