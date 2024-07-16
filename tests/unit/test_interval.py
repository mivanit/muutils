import math
from typing import Union, Tuple

import pytest

from muutils.interval import Interval, ClosedInterval, OpenInterval, _EPSILON


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


def test_interval_tuple_behavior():
    i = Interval(1, 5)
    assert len(i) == 2
    assert i[0] == 1
    assert i[1] == 5
    with pytest.raises(IndexError):
        _ = i[2]

    lower, upper = i
    assert lower == 1
    assert upper == 5

    assert tuple(i) == (1, 5)
    assert list(i) == [1, 5]


def test_min_max_intervals():
    i1 = Interval(1, 5)
    i2 = Interval([1, 5])
    i3 = Interval(1, 5, closed_L=True)
    i4 = Interval(2, 6)

    assert min(i1) == 1
    assert max(i1) == 5
    assert min(i2) == 1
    assert max(i2) == 5
    assert min(i3) == 1
    assert max(i3) == 5
    assert min(i4) == 2
    assert max(i4) == 6


def test_min_max_with_numbers():
    i1 = Interval(1, 5)
    i2 = ClosedInterval(2, 6)

    assert min(i1) == 1
    assert max(i1) == 5
    assert min(i2) == 2
    assert max(i2) == 6


@pytest.mark.parametrize(
    "interval,value,expected",
    [
        (Interval(1, 5), 3, 3),
        (Interval(1, 5), 0, 1 + _EPSILON),
        (Interval(1, 5), 6, 5 - _EPSILON),
        (Interval([1, 5]), 0, 1),
        (Interval([1, 5]), 6, 5),
        (Interval(1, 5, closed_L=True), 0, 1),
        (Interval(1, 5, closed_R=True), 6, 5),
        (ClosedInterval(1, 5), 0, 1),
        (ClosedInterval(1, 5), 6, 5),
        (OpenInterval(1, 5), 1, 1 + _EPSILON),
        (OpenInterval(1, 5), 5, 5 - _EPSILON),
        (Interval(-math.inf, math.inf), 0, 0),
        (Interval(-math.inf, 0), -1000000, -1000000),
        (Interval(0, math.inf), 1000000, 1000000),
    ],
)
def test_clamp(interval: Interval, value: Union[int, float], expected: float):
    assert math.isclose(interval.clamp(value), expected, rel_tol=1e-9, abs_tol=1e-15)


def test_clamp_nan():
    interval = Interval(0, 1)
    with pytest.raises(ValueError):
        interval.clamp(math.nan)


def test_zero_width_interval():
    # Test initialization and behavior of zero-width intervals
    zero_open = Interval(1, 1)
    zero_closed = ClosedInterval(1, 1)
    assert str(zero_open) == "(1, 1)"
    assert str(zero_closed) == "[1, 1]"
    assert 1 not in zero_open
    assert 1 in zero_closed
    with pytest.warns(Warning):
        assert zero_open.clamp(1) == 1 + _EPSILON
    with pytest.warns(Warning):
        assert zero_closed.clamp(1) == 1


def test_interval_containing_zero():
    # Test intervals that contain zero, especially for multiplication operations
    i = Interval(-1, 1)
    assert 0 in i
    assert i.clamp(0) == 0


def test_very_large_intervals():
    # Test intervals with very large bounds
    large = Interval(1e300, 1e301)
    assert 1e300 not in large
    assert 5e300 in large
    assert large.clamp(0) == 1e300 + _EPSILON
    assert large.clamp(2e301) == 1e301 - _EPSILON


def test_very_small_intervals():
    # Test intervals with very small bounds
    small = Interval(1e-20, 1e-19)
    assert 1e-20 not in small
    assert 2e-20 in small

    with pytest.warns(Warning):
        small.clamp(-1)

    assert small.clamp(2e-19, epsilon=1e-20) == 1e-19 - 1e-20


def test_intervals_with_epsilon_width():
    # Test intervals with width close to or less than epsilon
    i = Interval(1, 1.5)
    assert 1 not in i
    assert 1.2 in i
    assert i.clamp(1) == 1 + _EPSILON
    assert i.clamp(2) == 1.5 - _EPSILON


def test_extreme_epsilon_values():
    # Test clamp method with extreme epsilon values
    i = Interval(0, 1)
    assert i.clamp(2, epsilon=1e-100) == 1 - 1e-100
    assert i.clamp(-1, epsilon=0.1) == 0.1
    with pytest.raises(ValueError):
        i.clamp(0.5, epsilon=-1e-10)  # Negative epsilon should raise an error


def test_interval_intersection():
    # Test intersection of intervals
    assert Interval(1, 3) in Interval(0, 4)
    assert Interval(1, 3) not in Interval(2, 4)
    assert ClosedInterval(1, 2) in OpenInterval(0, 3)


def test_interval_with_non_numeric_types():
    # Test behavior with non-numeric types
    with pytest.raises(TypeError):
        Interval("a", "b")
    with pytest.raises(TypeError):
        "a" in Interval(1, 2)


def test_interval_initialization_with_iterables():
    # Test initialization with different iterable types
    assert str(Interval(range(1, 3))) == "(1, 2)"
    assert str(Interval((1, 2))) == "(1, 2)"


def test_clamp_with_infinite_values():
    # Test clamping with infinite values
    inf_interval = Interval(-math.inf, math.inf)
    assert inf_interval.clamp(1e1000) == 1e1000
    assert inf_interval.clamp(-1e1000) == -1e1000

    right_inf = Interval(0, math.inf)
    assert right_inf.clamp(1e1000) == 1e1000
    assert right_inf.clamp(-1) == 0 + _EPSILON

    left_inf = Interval(-math.inf, 0)
    assert left_inf.clamp(-1e1000) == -1e1000
    assert left_inf.clamp(1) == 0 - _EPSILON


def test_interval_equality_with_different_types():
    assert Interval(1, 2) == OpenInterval(1, 2)
    assert Interval(1, 2, is_closed=True) == ClosedInterval(1, 2)
    assert Interval(1, 2) != ClosedInterval(1, 2)
    assert Interval(1, 2, closed_L=True) != Interval(1, 2, closed_R=True)


def test_interval_containment_edge_cases():
    i = Interval(0, 1)
    assert 0 + _EPSILON / 2 in i
    assert 1 - _EPSILON / 2 in i
    assert 0 not in i
    assert 1 not in i

    ci = ClosedInterval(0, 1)
    assert 0 in ci
    assert 1 in ci
    assert 0 - _EPSILON / 2 not in ci
    assert 1 + _EPSILON / 2 not in ci


def test_clamp_with_custom_epsilon():
    i = Interval(0, 1)
    assert i.clamp(-1, epsilon=0.1) == 0.1
    assert i.clamp(2, epsilon=0.1) == 0.9
    assert i.clamp(0.5, epsilon=0.4) == 0.5  # epsilon doesn't affect internal points


def test_interval_with_float_imprecision():
    # Test handling of float imprecision
    i = Interval(0.1, 0.2)
    assert 0.15 in i
    assert 0.1 + 1e-15 in i
    assert 0.2 - 1e-15 in i


def test_interval_initialization_with_reversed_bounds():
    with pytest.raises(ValueError):
        Interval(2, 1)
    with pytest.raises(ValueError):
        ClosedInterval([5, 3])


def test_interval_initialization_with_equal_bounds():
    i = Interval(1, 1)
    assert str(i) == "(1, 1)"
    assert 1 not in i

    ci = ClosedInterval(1, 1)
    assert str(ci) == "[1, 1]"
    assert 1 in ci


def test_interval_with_only_one_infinite_bound():
    left_inf = Interval(-math.inf, 5, closed_L=True)
    assert -1e1000 in left_inf
    assert 5 not in left_inf
    assert left_inf.clamp(6) == 5 - _EPSILON

    right_inf = Interval(5, math.inf, closed_R=True)
    assert 1e1000 in right_inf
    assert 5 not in right_inf
    assert right_inf.clamp(4) == 5 + _EPSILON
