import sys
import math
from typing import Optional, Union, Tuple

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
    assert str(zero_open) == str(Interval())
    assert str(zero_closed) == r"{1}"
    assert 1 not in zero_open
    assert 1 in zero_closed
    with pytest.raises(ValueError):
        assert zero_open.clamp(1) == 1 + _EPSILON
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

    with pytest.raises(ValueError):
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
        Interval("a", "b")  # type: ignore[arg-type]
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
    assert Interval(1, 2) != (1, 2)
    assert Interval(1, 2) != [1, 2]
    assert Interval(1, 2) != "Interval(1, 2)"


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
    assert i == Interval.get_empty()
    assert i == Interval()
    assert str(i) == str(Interval.get_empty())
    assert 1 not in i

    ci = ClosedInterval(1, 1)
    assert str(ci) == r"{1}"
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


@pytest.mark.parametrize(
    "container,contained,expected",
    [
        (Interval(0, 6), Interval(1, 5), True),
        (Interval(2, 6), Interval(1, 5), False),
        (OpenInterval(0, 6), ClosedInterval(1, 5), True),
        (ClosedInterval(1, 5), OpenInterval(1, 5), True),
        (OpenInterval(1, 5), ClosedInterval(1, 5), False),
        (Interval(1, 5), Interval(1, 5), True),
        (Interval(1, 5), ClosedInterval(1, 5), False),
        (ClosedInterval(1, 5), Interval(1, 5), True),
        (Interval(1, 5), OpenInterval(1, 5), True),
        (Interval(1, 5), Interval(1, 5, closed_L=True), False),
        (Interval(1, 5), Interval(1, 5, closed_R=True), False),
        (ClosedInterval(1, 5), Interval(1, 5, closed_L=True), True),
        (ClosedInterval(1, 5), Interval(1, 5, closed_R=True), True),
        (Interval(1, 5, closed_R=True), ClosedInterval(1, 5), False),
        (Interval(1, 5, closed_L=True), ClosedInterval(1, 5), False),
        (Interval(1, 5, closed_L=True, closed_R=True), ClosedInterval(1, 5), True),
        (Interval(1, 5, is_closed=True), ClosedInterval(1, 5), True),
        (ClosedInterval(1, 5), Interval(1, 5, closed_L=True), True),
        (ClosedInterval(1, 5), Interval(1, 5, closed_R=True), True),
        (Interval(1, 5, closed_L=True, closed_R=True), Interval(1, 5), True),
        (Interval(-math.inf, math.inf), Interval(-math.inf, math.inf), True),
        (Interval(0, 1, closed_L=True), Interval(0, 1), True),
        (
            Interval(1, 5),
            Interval(0, 6),
            False,
        ),  # Contained interval extends beyond container
        (Interval(1, 5), Interval(2, 4), True),  # Strictly contained interval
        (OpenInterval(1, 5), OpenInterval(1, 5), True),  # Equal open intervals
        (ClosedInterval(1, 5), ClosedInterval(1, 5), True),  # Equal closed intervals
        (
            OpenInterval(1, 5),
            ClosedInterval(1, 5),
            False,
        ),  # Open doesn't contain closed with same bounds
        (
            ClosedInterval(1, 5),
            OpenInterval(1, 5),
            True,
        ),  # Closed contains open with same bounds
        (Interval(1, 5, closed_L=True), Interval(1, 5), True),
        (
            Interval(1, 5),
            Interval(1, 5, closed_L=True),
            False,
        ),  # Open doesn't contain half-open
        (Interval(1, 5, closed_R=True), Interval(1, 5), True),
        (
            Interval(1, 5),
            Interval(1, 5, closed_R=True),
            False,
        ),  # Open doesn't contain half-open
        (Interval(1, 1), Interval(1, 1), True),  # Point intervals
        (OpenInterval(1, 1), OpenInterval(1, 1), True),  # Empty open intervals
        (ClosedInterval(1, 1), ClosedInterval(1, 1), True),  # Point closed intervals
        (
            OpenInterval(1, 1),
            ClosedInterval(1, 1),
            False,
        ),  # Empty open doesn't contain point closed
        (
            ClosedInterval(1, 1),
            OpenInterval(1, 1),
            True,
        ),  # Point closed contains empty open
        (Interval(0, math.inf), Interval(1, math.inf), True),  # Infinite upper bound
        (Interval(-math.inf, 0), Interval(-math.inf, -1), True),  # Infinite lower bound
        (
            Interval(-math.inf, math.inf),
            Interval(0, 0),
            True,
        ),  # Real line contains any point
        (
            Interval(0, 1),
            Interval(-math.inf, math.inf),
            False,
        ),  # Finite doesn't contain infinite
        (Interval(1, 5), Interval(5, 10), False),  # Adjacent intervals
        (
            ClosedInterval(1, 5),
            ClosedInterval(5, 10),
            False,
        ),  # Adjacent closed intervals
        (OpenInterval(1, 5), OpenInterval(5, 10), False),  # Adjacent open intervals
        (
            Interval(1, 5, closed_R=True),
            Interval(5, 10, closed_L=True),
            False,
        ),  # Adjacent half-open intervals
    ],
)
def test_interval_containment(container, contained, expected):
    print(f"{container = }, {contained = }, {expected = }")
    assert (contained in container) == expected


@pytest.mark.parametrize(
    "interval_a,interval_b,expected",
    [
        (ClosedInterval(1, 5), Interval(1, 5, is_closed=True), True),
        (Interval(1, 5), Interval(1, 5, closed_L=True), False),
        (Interval(1, 5), Interval(1, 5, closed_R=True), False),
        (Interval(1, 5), Interval(1, 5, closed_L=True, closed_R=True), False),
        (
            Interval(1, 5, is_closed=True),
            Interval(1, 5, closed_L=True, closed_R=True),
            True,
        ),
        (ClosedInterval(1, 5), Interval(1, 5, closed_L=True, closed_R=True), True),
        (OpenInterval(1, 5), ClosedInterval(1, 5), False),
        (Interval(1, 5, closed_L=True), ClosedInterval(0, 6), False),
        (OpenInterval(1, 5), ClosedInterval(1, 5), False),
    ],
)
def test_mixed_interval_types(interval_a, interval_b, expected):
    assert (interval_a == interval_b) == expected


@pytest.mark.parametrize(
    "interval",
    [
        Interval(),
        Interval(5),
        Interval.get_singleton(5),
        Interval(1, 5),
        ClosedInterval(1, 5),
        OpenInterval(1, 5),
        Interval(1, 5, closed_L=True),
        Interval(1, 5, closed_R=True),
        Interval(1, 5, is_closed=True),
        Interval(0, math.inf, closed_L=True),
        Interval(-math.inf, 0, closed_R=True),
        Interval(5.0),
        Interval.get_singleton(5.0),
        Interval(1.0, 5.0),
        ClosedInterval(1.0, 5.0),
        OpenInterval(1.0, 5.0),
        Interval(1.0, 5.0, closed_L=True),
        Interval(1.0, 5.0, closed_R=True),
        Interval(1.0, 5.0, is_closed=True),
        Interval(0.0, math.inf, closed_L=True),
        Interval(-math.inf, 0.0, closed_R=True),
        Interval(-math.inf, math.inf),
        ClosedInterval(-math.inf, math.inf),
        OpenInterval(-math.inf, math.inf),
    ],
)
def test_string_representation_round_trip(interval):
    assert Interval.from_str(str(interval)) == interval


@pytest.mark.parametrize(
    "string,expected",
    [
        ("[1, 5]", ClosedInterval(1, 5)),
        ("(1, 5)", OpenInterval(1, 5)),
        ("[1, 5)", Interval(1, 5, closed_L=True)),
        ("(1, 5]", Interval(1, 5, closed_R=True)),
        ("[-inf, inf]", ClosedInterval(-math.inf, math.inf)),
        ("(0, inf)", OpenInterval(0, math.inf)),
        (" [ 1.5, 5.5 ) ", Interval(1.5, 5.5, closed_L=True)),
        ("(-1e3, 1e3]", Interval(-1000, 1000, closed_R=True)),
        ("[1K, 1M)", Interval(1000, 1000000, closed_L=True)),
        ("[-1K, 1M)", Interval(-1000, 1000000, closed_L=True)),
        ("(1/2, 3/2]", Interval(0.5, 1.5, closed_R=True)),
    ],
)
def test_parsing_from_strings(string, expected):
    assert Interval.from_str(string) == expected


@pytest.mark.parametrize(
    "interval,expected_size",
    [
        (Interval(1, 5), 4),
        (ClosedInterval(1, 5), 4),
        (OpenInterval(1, 5), 4),
        (Interval(0, math.inf), math.inf),
        (Interval(-math.inf, math.inf), math.inf),
        (Interval(1, 1), 0),
        (ClosedInterval(1, 1), 0),
        (Interval(0.1, 0.2), 0.1),
    ],
)
def test_interval_size(interval, expected_size):
    assert interval.size() == expected_size


@pytest.mark.parametrize(
    "interval,value,expected",
    [
        (ClosedInterval(1, 5), 0, 1),
        (OpenInterval(1, 5), 5, 5 - _EPSILON),
    ],
)
def test_clamp_mixed_types(interval, value, expected):
    assert math.isclose(interval.clamp(value), expected, rel_tol=1e-9, abs_tol=1e-15)


def test_interval_edge_cases():
    # Test with very small intervals
    small = Interval(1, 1 + 1e-4)
    assert math.isclose(small.size(), 1e-4)
    assert 1 + 0.5e-4 in small
    assert math.isclose(small.clamp(1), 1 + _EPSILON, rel_tol=1e-9, abs_tol=1e-15)
    assert math.isclose(
        small.clamp(2), 1 + 1e-4 - _EPSILON, rel_tol=1e-9, abs_tol=1e-15
    )

    # Test with intervals smaller than epsilon
    tiny = Interval(1, 1 + _EPSILON / 2)
    assert math.isclose(
        tiny.size(), _EPSILON / 2, rel_tol=1e-9, abs_tol=1e-12
    ), f"Size: {tiny.size()}, Epsilon: {_EPSILON}, {tiny = }"
    with pytest.raises(ValueError):
        assert math.isclose(
            tiny.clamp(0), 1 + _EPSILON / 4, rel_tol=1e-9, abs_tol=1e-15
        )

    # Test with large intervals
    large = Interval(-1e100, 1e100)
    assert large.size() == 2e100
    assert 1e99 in large
    assert math.isclose(
        large.clamp(-2e100), -1e100 + _EPSILON, rel_tol=1e-9, abs_tol=1e-15
    )


@pytest.mark.parametrize(
    "a,b,expected_intersection,expected_union",
    [
        (
            Interval(1, 3),
            Interval(2, 4),
            Interval(2, 3),
            Interval(1, 4),
        ),
        (
            ClosedInterval(0, 2),
            OpenInterval(1, 3),
            Interval(1, 2, closed_R=True),
            Interval(0, 3, closed_L=True),
        ),
        (
            OpenInterval(1, 5),
            ClosedInterval(2, 4),
            ClosedInterval(2, 4),
            OpenInterval(1, 5),
        ),
        # Non-overlapping intervals
        (Interval(1, 3), Interval(4, 6), Interval(), Interval()),
        # Touching intervals
        (
            Interval(1, 3, closed_R=True),
            Interval(3, 5),
            Interval.get_singleton(3),
            Interval(1, 5),
        ),
        (
            ClosedInterval(1, 3),
            ClosedInterval(3, 5),
            Interval.get_singleton(3),
            ClosedInterval(1, 5),
        ),
        # Fully contained interval
        (
            Interval(1, 5),
            Interval(2, 3),
            Interval(2, 3),
            Interval(1, 5),
        ),
        # Infinite intervals
        (
            Interval(-float("inf"), 1),
            Interval(0, float("inf")),
            Interval(0, 1),
            Interval(-float("inf"), float("inf")),
        ),
    ],
)
def test_interval_arithmetic(
    a: Interval,
    b: Interval,
    expected_intersection: Optional[Interval],
    expected_union: Optional[Interval],
):
    # Test intersection
    if expected_intersection == Interval():
        assert a.intersection(b) == Interval()
        assert b.intersection(a) == Interval()
    else:
        assert a.intersection(b) == expected_intersection
        assert b.intersection(a) == expected_intersection  # Commutativity

    # Test union
    if expected_union == Interval():
        with pytest.raises(Exception):
            a.union(b)
        with pytest.raises(Exception):
            b.union(a)
    else:
        assert a.union(b) == expected_union
        assert b.union(a) == expected_union  # Commutativity


# Additional tests for edge cases
def test_interval_arithmetic_edge_cases():
    # Self-intersection and self-union
    a = Interval(1, 3)
    assert a.intersection(a) == a
    assert a.union(a) == a

    # Empty interval intersection
    empty = Interval(1, 1)
    assert empty.intersection(Interval(2, 3)) == Interval()
    assert Interval(2, 3).intersection(empty) == Interval()

    # Intersection with universal set
    universal = Interval(-float("inf"), float("inf"))
    assert Interval(1, 2).intersection(universal) == Interval(1, 2)
    assert universal.intersection(Interval(1, 2)) == Interval(1, 2)

    # Union with universal set
    assert Interval(1, 2).union(universal) == universal
    assert universal.union(Interval(1, 2)) == universal


# Test for invalid operations
def test_interval_arithmetic_invalid():
    with pytest.raises(TypeError):
        # Invalid type for intersection
        Interval(1, 2).intersection(5)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        # Invalid type for union
        Interval(1, 2).union("invalid")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "invalid_string",
    [
        "1, 5",  # Missing brackets
        "[1, 5, 7]",  # Too many values
        "[5, 1]",  # Lower > Upper
        "[a, b]",  # Non-numeric values
    ],
)
def test_from_str_errors(invalid_string):
    with pytest.raises(ValueError):
        Interval.from_str(invalid_string)


def test_interval_repr():
    assert repr(Interval(1, 5)) == "(1, 5)"
    assert repr(ClosedInterval(1, 5)) == "[1, 5]"
    assert repr(OpenInterval(1, 5)) == "(1, 5)"
    assert repr(Interval(1, 5, closed_L=True)) == "[1, 5)"
    assert repr(Interval(1, 5, closed_R=True)) == "(1, 5]"


def test_interval_from_str_with_whitespace():
    assert Interval.from_str(" ( 1 , 5 ) ") == Interval(1, 5)
    assert Interval.from_str("[1.5 , 3.5]") == ClosedInterval(1.5, 3.5)


def test_interval_from_str_with_scientific_notation():
    assert Interval.from_str("(1e-3, 1e3)") == Interval(0.001, 1000)


def test_interval_clamp_with_custom_epsilon():
    i = Interval(0, 1)
    assert math.isclose(i.clamp(-0.5, epsilon=0.25), 0.25, rel_tol=1e-9)
    assert math.isclose(i.clamp(1.5, epsilon=0.25), 0.75, rel_tol=1e-9)


def test_interval_size_with_small_values():
    i = Interval(1e-10, 2e-10)
    assert math.isclose(i.size(), 1e-10, rel_tol=1e-9)


def test_interval_intersection_edge_cases():
    i1 = Interval(1, 2)
    i2 = Interval(2, 3)
    i3 = ClosedInterval(2, 3)

    assert i1.intersection(i2) == Interval.get_empty()
    assert i1.intersection(i3) == Interval(2, 2, closed_L=True)


def test_interval_union_edge_cases():
    i1 = Interval(1, 2, closed_R=True)
    i2 = Interval(2, 3, closed_L=True)
    i3 = Interval(3, 4)

    assert i1.union(i2) == Interval(1, 3)
    with pytest.raises(NotImplementedError):
        i1.union(i3)


def test_interval_contains_with_epsilon():
    i = OpenInterval(0, 1)
    assert 0 + _EPSILON in i
    assert 1 - _EPSILON in i
    assert 0 not in i
    assert 1 not in i


def test_singleton_creation():
    s = Interval.get_singleton(5)
    assert s.is_singleton
    assert s.singleton == 5
    assert len(s) == 1
    assert s.lower == s.upper == 5
    assert s.closed_L and s.closed_R


def test_empty_creation():
    e = Interval.get_empty()
    assert e.is_empty
    assert len(e) == 0
    with pytest.raises(ValueError):
        _ = e.singleton


def test_singleton_properties():
    s = Interval.get_singleton(3.14)
    assert s.is_singleton
    assert not s.is_empty
    assert s.is_finite
    assert s.is_closed
    assert not s.is_open
    assert not s.is_half_open


def test_empty_properties():
    e = Interval.get_empty()
    assert e.is_empty
    assert not e.is_singleton
    assert e.is_finite
    assert e.is_closed
    assert e.is_open
    assert not e.is_half_open


def test_singleton_containment():
    s = Interval.get_singleton(5)
    assert 5 in s
    assert 5.0 in s
    assert 4.999999999999999 not in s
    assert 5.000000000000001 not in s
    assert Interval.get_singleton(5) in s
    assert Interval(4, 6) not in s
    assert s in Interval(4, 6)


def test_empty_containment():
    e = Interval.get_empty()
    assert 0 not in e
    assert e in Interval(0, 1)  # Empty set is a subset of all sets
    assert Interval.get_empty() in e


@pytest.mark.parametrize("value", [0, 1, -1, math.pi, math.e, math.inf, -math.inf])
def test_singleton_various_values(value):
    s = Interval.get_singleton(value)
    assert s.is_singleton
    assert s.singleton == value
    assert value in s


def test_singleton_nan():
    assert Interval.get_singleton(math.nan).is_empty


def test_singleton_operations():
    s = Interval.get_singleton(5)
    assert s.size() == 0
    assert s.clamp(3) == 5
    assert s.clamp(7) == 5


def test_empty_operations():
    e = Interval.get_empty()
    assert e.size() == 0
    with pytest.raises(ValueError):
        e.clamp(3)


def test_singleton_intersection():
    s = Interval.get_singleton(5)
    assert s.intersection(Interval(0, 10)) == s
    assert s.intersection(Interval(5, 10)) == Interval.get_empty()
    assert s.intersection(ClosedInterval(5, 10)) == s
    assert s.intersection(Interval(5, 10, closed_R=True)) == Interval.get_empty()
    assert s.intersection(Interval(5, 10, closed_L=True)) == s
    assert s.intersection(Interval(5, 10, is_closed=True)) == s
    assert s.intersection(Interval(0, 6)) == s
    assert s.intersection(Interval(0, 5)) == Interval.get_empty()
    assert s.intersection(Interval(6, 10)) == Interval.get_empty()
    assert s.intersection(Interval(6, 10)) == Interval.get_empty()
    assert s.intersection(Interval.get_singleton(5)) == s
    assert s.intersection(Interval.get_singleton(6)) == Interval.get_empty()


def test_empty_intersection():
    e = Interval.get_empty()
    assert e.intersection(Interval(0, 1)) == e
    assert e.intersection(Interval.get_singleton(0)) == e
    assert e.intersection(Interval.get_empty()) == e


def test_singleton_union():
    s = Interval.get_singleton(5)
    assert s.union(Interval(0, 10)) == Interval(0, 10)
    assert s.union(Interval(5, 10)) == Interval(5, 10, closed_L=True)
    assert s.union(Interval(0, 5)) == Interval(0, 5, closed_R=True)
    with pytest.raises(NotImplementedError):
        s.union(Interval(6, 10))
    assert s.union(Interval.get_singleton(5)) == s
    with pytest.raises(NotImplementedError):
        s.union(Interval.get_singleton(6))


def test_empty_union():
    e = Interval.get_empty()
    assert e.union(Interval(0, 1)) == Interval(0, 1)
    assert e.union(Interval.get_singleton(0)) == Interval.get_singleton(0)
    assert e.union(Interval.get_empty()) == Interval.get_empty()


def test_singleton_equality():
    assert Interval.get_singleton(5) == Interval.get_singleton(5)
    assert Interval.get_singleton(5) != Interval.get_singleton(6)
    assert Interval.get_singleton(5) == ClosedInterval(5, 5)
    assert Interval.get_singleton(5) != OpenInterval(5, 5)


def test_empty_equality():
    assert Interval.get_empty() == Interval.get_empty()
    assert Interval.get_empty() == OpenInterval(5, 5)
    assert Interval.get_empty() != ClosedInterval(5, 5)


def test_singleton_representation():
    assert repr(Interval.get_singleton(5)) == "{5}"
    assert str(Interval.get_singleton(5)) == "{5}"


def test_empty_representation():
    assert repr(Interval.get_empty()) == "∅"
    assert str(Interval.get_empty()) == "∅"


def test_singleton_from_str():
    assert Interval.from_str("{5}") == Interval.get_singleton(5)
    assert Interval.from_str("{3.14}") == Interval.get_singleton(3.14)


def test_empty_from_str():
    assert Interval.from_str("∅") == Interval.get_empty()
    assert Interval.from_str("{}") == Interval.get_empty()


def test_singleton_iteration():
    s = Interval.get_singleton(5)
    assert list(s) == [5]
    assert [x for x in s] == [5]


def test_empty_iteration():
    e = Interval.get_empty()
    assert list(e) == []
    assert [x for x in e] == []


def test_singleton_indexing():
    s = Interval.get_singleton(5)
    assert s[0] == 5
    with pytest.raises(IndexError):
        _ = s[1]


def test_empty_indexing():
    e = Interval.get_empty()
    with pytest.raises(IndexError):
        _ = e[0]


def test_singleton_bool():
    assert bool(Interval.get_singleton(5))
    assert bool(Interval.get_singleton(0))


def test_empty_bool():
    assert not bool(Interval.get_empty())


def test_singleton_infinity():
    inf_singleton = Interval.get_singleton(math.inf)
    assert inf_singleton.is_singleton
    assert not inf_singleton.is_finite
    assert math.inf in inf_singleton
    assert math.inf - 1 in inf_singleton


def test_mixed_operations():
    s = Interval.get_singleton(5)
    e = Interval.get_empty()
    i = Interval(0, 10)

    assert s.intersection(e) == e
    assert e.intersection(s) == e
    assert i.intersection(s) == s
    assert i.intersection(e) == e

    assert s.union(e) == s
    assert e.union(s) == s
    assert i.union(s) == i
    assert i.union(e) == i


def test_edge_case_conversions():
    assert Interval(5, 5, closed_L=True, closed_R=True).is_singleton
    assert Interval(5, 5, closed_L=False, closed_R=False).is_empty
    assert not Interval(5, 5, closed_L=True, closed_R=False).is_empty
    assert not Interval(5, 5, closed_L=False, closed_R=True).is_empty


def test_nan_handling_is_empty():
    assert Interval(math.nan, math.nan).is_empty
    assert Interval(None, None).is_empty  # type: ignore[arg-type]
    assert Interval().is_empty
    assert Interval.get_empty().is_empty
    with pytest.raises(ValueError):
        Interval(math.nan, 5)
    with pytest.raises(ValueError):
        assert Interval(5, math.nan)


def test_infinity_edge_cases():
    assert not Interval(-math.inf, math.inf).is_empty
    assert not Interval(-math.inf, math.inf).is_singleton
    assert Interval(math.inf, math.inf, closed_L=True, closed_R=True).is_singleton
    assert Interval(-math.inf, -math.inf, closed_L=True, closed_R=True).is_singleton


# Potential bug: What should happen in this case?
def test_potential_bug_infinity_singleton():
    inf_singleton = Interval.get_singleton(math.inf)
    assert math.isinf(inf_singleton.singleton)
    assert inf_singleton == Interval(math.inf, math.inf, closed_L=True, closed_R=True)


# Potential bug: Epsilon handling with singletons
def test_potential_bug_singleton_epsilon():
    s = Interval.get_singleton(5)
    assert 5 + 1e-15 not in s  # This might fail if epsilon is not handled correctly


# Potential bug: Empty set comparison
def test_potential_bug_empty_comparison():
    e1 = Interval.get_empty()
    e2 = OpenInterval(5, 5)
    assert e1 == e2  # This might fail if empty sets are not compared correctly


# Potential bug: Singleton at zero
def test_potential_bug_zero_singleton():
    zero_singleton = Interval.get_singleton(0)
    assert 0 in zero_singleton
    assert -0.0 in zero_singleton  # This might fail due to float representation


# Potential bug: Empty set size
def test_potential_bug_empty_set_size():
    e = Interval.get_empty()
    assert (
        e.size() == 0
    )  # This might fail if size is not correctly implemented for empty sets


@pytest.mark.parametrize(
    "interval",
    [
        # Empty set
        Interval.get_empty(),
        # Singletons
        Interval.get_singleton(0),
        Interval.get_singleton(5),
        Interval.get_singleton(-3),
        Interval.get_singleton(3.14),
        Interval.get_singleton(-2.718),
        # Regular intervals
        Interval(0, 1),
        Interval(0, 1, closed_L=True),
        Interval(0, 1, closed_R=True),
        Interval(0, 1, closed_L=True, closed_R=True),
        OpenInterval(-5, 5),
        ClosedInterval(-5, 5),
        # Intervals with infinities
        Interval(-math.inf, math.inf),
        Interval(-math.inf, 0),
        Interval(0, math.inf),
        Interval(-math.inf, 0, closed_R=True),
        Interval(0, math.inf, closed_L=True),
        ClosedInterval(-math.inf, math.inf),
        # Mixed finite and infinite bounds
        Interval(-math.inf, 5),
        Interval(-5, math.inf),
        Interval(-math.inf, 5, closed_R=True),
        Interval(-5, math.inf, closed_L=True),
        # Very large and very small numbers
        Interval(1e-100, 1e100),
        ClosedInterval(-1e50, 1e50),
        # Intervals with non-integer bounds
        Interval(math.e, math.pi),
        ClosedInterval(math.sqrt(2), math.sqrt(3)),
    ],
)
def test_interval_string_round_trip(interval):
    # Convert interval to string
    interval_str = str(interval)

    # Parse string back to interval
    parsed_interval = Interval.from_str(interval_str)

    # Check if the parsed interval is equal to the original
    assert (
        parsed_interval == interval
    ), f"Round trip failed for {interval}. Got {parsed_interval}"

    # Additional check for string representation consistency
    assert (
        str(parsed_interval) == interval_str
    ), f"String representation mismatch for {interval}. Expected {interval_str}, got {str(parsed_interval)}"


def test_empty_set_string_representations():
    empty = Interval.get_empty()
    assert str(empty) == "∅"
    assert Interval.from_str("∅") == empty
    assert Interval.from_str("{}") == empty


@pytest.mark.parametrize("value", [0, 1, -1, 3.14, -2.718, math.pi, math.e])
def test_singleton_string_representations(value):
    singleton = Interval.get_singleton(value)
    assert str(singleton) == f"{{{value}}}"
    assert Interval.from_str(f"{{{value}}}") == singleton


def test_infinity_string_representations():
    assert str(Interval(-math.inf, math.inf)) == "(-inf, inf)"
    assert str(ClosedInterval(-math.inf, math.inf)) == "[-inf, inf]"
    assert str(Interval(-math.inf, 0)) == "(-inf, 0)"
    assert str(Interval(0, math.inf)) == "(0, inf)"


def test_mixed_closure_string_representations():
    assert str(Interval(0, 1, closed_L=True)) == "[0, 1)"
    assert str(Interval(0, 1, closed_R=True)) == "(0, 1]"
    assert str(Interval(-math.inf, 0, closed_R=True)) == "(-inf, 0]"
    assert str(Interval(0, math.inf, closed_L=True)) == "[0, inf)"


@pytest.mark.parametrize(
    "string_repr",
    [
        "(0, 1)",
        "[0, 1]",
        "(0, 1]",
        "[0, 1)",
        "(-inf, inf)",
        "[0, inf)",
        "(-inf, 0]",
        "{2.5}",
        "∅",
    ],
)
def test_string_parsing_consistency(string_repr):
    parsed_interval = Interval.from_str(string_repr)
    assert (
        str(parsed_interval) == string_repr
    ), f"Parsing inconsistency for {string_repr}. Got {str(parsed_interval)}"


def test_string_parsing_edge_cases():
    with pytest.raises(ValueError):
        Interval.from_str("(1, 0)")  # Lower bound greater than upper bound

    with pytest.raises(ValueError):
        Interval.from_str("[1, 2, 3]")  # Too many values

    with pytest.raises(ValueError):
        Interval.from_str("(a, b)")  # Non-numeric values


def test_string_representation_precision():
    # Test that string representation maintains sufficient precision
    small_interval = Interval(1e-10, 2e-10)
    parsed_small_interval = Interval.from_str(str(small_interval))
    assert small_interval == parsed_small_interval
    assert small_interval.lower == parsed_small_interval.lower
    assert small_interval.upper == parsed_small_interval.upper


def test_string_representation_with_scientific_notation():
    large_interval = Interval(1e100, 2e100)
    large_interval_str = str(large_interval)
    assert "e+" in large_interval_str  # Ensure scientific notation is used
    parsed_large_interval = Interval.from_str(large_interval_str)
    assert large_interval == parsed_large_interval


# Potential bug: Handling of -0.0 in string representation
def test_potential_bug_negative_zero():
    zero_singleton = Interval.get_singleton(-0.0)
    zero_singleton_str = str(zero_singleton)
    assert Interval.from_str(zero_singleton_str) == zero_singleton
    assert (
        Interval.from_str(zero_singleton_str).singleton == 0.0
    )  # Should this be -0.0 or 0.0?

    i = Interval(-1, 1)
    assert 0.0 in i
    assert -0.0 in i  # This might fail if -0.0 is not handled correctly


# Potential bug: Precision loss in string representation
def test_potential_bug_precision_loss():
    precise_interval = Interval(1 / 3, 2 / 3)
    precise_interval_str = str(precise_interval)
    parsed_precise_interval = Interval.from_str(precise_interval_str)
    assert precise_interval == parsed_precise_interval
    assert precise_interval.lower == parsed_precise_interval.lower
    assert precise_interval.upper == parsed_precise_interval.upper


def test_interval_with_very_close_bounds():
    i = Interval(1, 1 + 2 * _EPSILON)
    assert i.size() > 0
    assert 1 + _EPSILON in i
    assert i.clamp(1) == 1 + _EPSILON
    assert i.clamp(2) == 1 + _EPSILON


def test_interval_with_bounds_closer_than_epsilon():
    i = Interval(1, 1 + _EPSILON / 2)
    assert i.size() > 0
    with pytest.raises(ValueError):
        assert math.isclose(i.clamp(0), 1 + _EPSILON / 4)


def test_interval_with_extremely_large_bounds():
    i = Interval(1e300, 1e301)
    assert 5e300 in i
    assert i.clamp(0) == 1e300 + _EPSILON
    assert i.clamp(2e301) == 1e301 - _EPSILON


def test_interval_with_mixed_infinities():
    i = Interval(-math.inf, math.inf)
    assert i.size() == math.inf
    assert 0 in i
    assert math.inf not in i
    assert -math.inf not in i
    assert i.clamp(math.inf) == math.inf - _EPSILON
    assert i.clamp(-math.inf) == -math.inf + _EPSILON


def test_interval_with_one_infinity():
    i1 = Interval(-math.inf, 0)
    assert i1.size() == math.inf
    assert -1e300 in i1
    assert 0 not in i1
    assert i1.clamp(1) == 0 - _EPSILON

    i2 = Interval(0, math.inf)
    assert i2.size() == math.inf
    assert 1e300 in i2
    assert 0 not in i2
    assert i2.clamp(-1) == 0 + _EPSILON


def test_interval_singleton_edge_cases():
    s = Interval.get_singleton(0)
    assert 0 in s
    assert -0.0 in s
    assert 1e-16 not in s
    assert -1e-16 not in s


def test_interval_empty_edge_cases():
    e = Interval.get_empty()
    assert e.size() == 0
    assert e.is_open and e.is_closed
    assert Interval.get_empty() in e
    assert e in Interval(0, 1)


def test_interval_from_str_edge_cases():
    assert Interval.from_str("(0, 0)") == Interval.get_empty()
    assert Interval.from_str("[0, 0]") == Interval.get_singleton(0)
    assert Interval.from_str("(0, 0]") == Interval.get_singleton(0)
    assert Interval.from_str("[0, 0)") == Interval.get_singleton(0)


def test_interval_arithmetic_with_empty_intervals():
    e = Interval.get_empty()
    i = Interval(0, 1)
    assert e.intersection(i) == e
    assert i.intersection(e) == e
    assert e.union(i) == i
    assert i.union(e) == i


def test_interval_arithmetic_with_singletons():
    s = Interval.get_singleton(1)
    i = Interval(0, 2)
    assert s.intersection(i) == s
    assert i.intersection(s) == s
    assert s.union(i) == i
    assert i.union(s) == i


def test_interval_precision_near_bounds():
    i = Interval(1, 2)
    assert 1 + _EPSILON / 2 in i
    assert 2 - _EPSILON / 2 in i
    assert 1 - _EPSILON / 2 not in i
    assert 2 + _EPSILON / 2 not in i


def test_interval_serialization_precision():
    i = Interval(1 / 3, 2 / 3)
    serialized = str(i)
    deserialized = Interval.from_str(serialized)
    assert math.isclose(i.lower, deserialized.lower, rel_tol=1e-15)
    assert math.isclose(i.upper, deserialized.upper, rel_tol=1e-15)


def test_interval_with_repeated_float_operations():
    i = Interval(0, 1)
    for _ in range(1000):
        i = Interval(i.lower + _EPSILON, i.upper - _EPSILON)
    assert i.lower < i.upper
    assert 0.5 in i


def test_interval_near_float_precision_limit():
    small_interval = Interval(1, 1 + 1e-15)
    assert small_interval.size() > 0
    assert 1 + 5e-16 in small_interval


def test_interval_with_irrational_bounds():
    i = Interval(math.e, math.pi)
    print(f"{i.size() = }, {math.e - math.pi = }")
    assert math.isclose(i.size(), math.pi - math.e)
    assert (math.pi + math.e) / 2 in i
    assert 3 in i


def test_interval_commutativity_of_operations():
    i1 = Interval(1, 3)
    i2 = Interval(2, 4)
    assert i1.intersection(i2) == i2.intersection(i1)
    assert i1.union(i2) == i2.union(i1)


def test_interval_associativity_of_operations():
    i1 = Interval(1, 4)
    i2 = Interval(2, 5)
    i3 = Interval(3, 6)
    assert (i1.intersection(i2)).intersection(i3) == i1.intersection(
        i2.intersection(i3)
    )
    assert (i1.union(i2)).union(i3) == i1.union(i2.union(i3))


def test_interval_distributivity_of_operations():
    i1 = Interval(1, 3)
    i2 = Interval(2, 4)
    i3 = Interval(3, 5)
    assert i1.intersection(i2.union(i3)) == (i1.intersection(i2)).union(
        i1.intersection(i3)
    )


def test_interval_comparison():
    i1 = Interval(1, 3)
    i2 = Interval(2, 4)
    i3 = Interval(1, 3)
    assert i1 != i2
    assert i1 == i3
    with pytest.raises(TypeError):
        i1 < i2  # type: ignore[operator]


def test_interval_copy():
    i = Interval(1, 2, closed_L=True)
    i_copy = i.copy()
    assert i == i_copy
    assert i is not i_copy


def test_interval_pickling():
    import pickle

    i = Interval(1, 2, closed_L=True)
    pickled = pickle.dumps(i)
    unpickled = pickle.loads(pickled)
    assert i == unpickled


def test_interval_with_numpy_types():
    import numpy as np

    i = Interval(np.float64(1), np.float64(2))  # type: ignore[arg-type]
    assert np.float64(1.5) in i
    assert isinstance(i.clamp(np.float64(0)), np.float64)  # type: ignore[arg-type]


def test_interval_with_decimal_types():
    from decimal import Decimal

    i = Interval(Decimal("1"), Decimal("2"))  # type: ignore[arg-type]
    assert Decimal("1.5") in i
    assert min(i) == Decimal("1")
    assert max(i) == Decimal("2")
    assert isinstance(i.clamp(Decimal("0")), Decimal)  # type: ignore[arg-type]


def test_interval_with_fractions():
    from fractions import Fraction

    i = Interval(Fraction(1, 3), Fraction(2, 3))  # type: ignore[arg-type]
    assert Fraction(1, 2) in i
    assert isinstance(i.clamp(Fraction(0, 1)), Fraction)  # type: ignore[arg-type]


# Potential bug: Infinity comparisons
def test_potential_bug_infinity_comparisons():
    i = Interval(-math.inf, math.inf)
    assert (
        math.inf not in i
    )  # This might fail if infinity comparisons are not handled correctly


# Potential bug: NaN handling
def test_potential_bug_nan_handling():
    with pytest.raises(ValueError):
        Interval(0, float("nan"))

    i = Interval(0, 1)
    with pytest.raises(ValueError):
        float("nan") in i


# Potential bug: Intersection of adjacent intervals
def test_potential_bug_adjacent_interval_intersection():
    i1 = Interval(0, 1, closed_R=True)
    i2 = Interval(1, 2, closed_L=True)
    intersection = i1.intersection(i2)
    assert intersection == Interval.get_singleton(
        1
    )  # This might fail if adjacent intervals are not handled correctly


# Potential bug: Union of overlapping intervals
def test_potential_bug_overlapping_interval_union():
    i1 = Interval(0, 2)
    i2 = Interval(1, 3)
    union = i1.union(i2)
    assert union == Interval(
        0, 3
    )  # This might fail if overlapping intervals are not handled correctly


# Potential bug: Interval containing only infinity
def test_potential_bug_infinity_only_interval():
    i = Interval(math.inf, math.inf)
    assert (
        i.is_empty
    )  # This might fail if infinity-only intervals are not handled correctly
    assert (
        i.size() == 0
    )  # This might fail if the size calculation doesn't account for this case


# Potential bug: Interval containing only negative infinity
def test_potential_bug_negative_infinity_only_interval():
    i = Interval(-math.inf, -math.inf)
    assert (
        i.is_empty
    )  # This might fail if negative infinity-only intervals are not handled correctly
    assert (
        i.size() == 0
    )  # This might fail if the size calculation doesn't account for this case


# Potential bug: Clamp with infinity
def test_potential_bug_clamp_with_infinity():
    i = Interval(0, 1)
    assert math.isclose(i.clamp(math.inf), 1)
    assert i.clamp(math.inf) < 1
    print(i.clamp(-math.inf))
    assert math.isclose(i.clamp(-math.inf), 0, rel_tol=1e-6, abs_tol=1e-6)
    assert i.clamp(-math.inf) > 0


# Potential bug: Intersection of intervals with different types
def test_potential_bug_intersection_different_types():
    i1 = Interval(0, 1)
    i2 = ClosedInterval(0.5, 1.5)
    intersection = i1.intersection(i2)
    assert intersection == Interval(
        0.5, 1, closed_L=True
    )  # This might fail if mixing interval types is not handled correctly


# Potential bug: Union of intervals with different types
def test_potential_bug_union_different_types():
    i1 = Interval(0, 1)
    i2 = ClosedInterval(0.5, 1.5)
    union = i1.union(i2)
    assert union == Interval(
        0, 1.5, closed_R=True
    )  # This might fail if mixing interval types is not handled correctly


# Potential bug: Interval bounds very close to each other
def test_potential_bug_very_close_bounds():
    i = Interval(1, 1 + sys.float_info.epsilon)
    assert (
        not i.is_empty
    )  # This might fail if very close bounds are not handled correctly
    assert (
        i.size() > 0
    )  # This might fail if size calculation doesn't account for very close bounds


# Potential bug: Interval from string with excessive precision
def test_potential_bug_excessive_precision_from_string():
    s = "(0.1234567890123456, 0.1234567890123457)"
    i = Interval.from_str(s)
    assert (
        str(i) == s
    )  # This might fail if string conversion doesn't preserve precision


# Potential bug: Interval with bounds that are not exactly representable in binary
def test_potential_bug_non_binary_representable_bounds():
    i = Interval(0.1, 0.3)
    assert 0.2 in i  # This might fail due to binary representation issues


# Potential bug: Clamp with value very close to bound
def test_potential_bug_clamp_near_bound():
    i = Interval(0, 1)
    result = i.clamp(1 - sys.float_info.epsilon)
    assert (
        result < 1
    )  # This might fail if clamping near bounds is not handled carefully


# Potential bug: Empty interval intersection with itself
def test_potential_bug_empty_self_intersection():
    e = Interval.get_empty()
    assert e.intersection(e) == e  # This should pass, but worth checking


# Potential bug: Empty interval union with itself
def test_potential_bug_empty_self_union():
    e = Interval.get_empty()
    assert e.union(e) == e  # This should pass, but worth checking


# Potential bug: Interval containing only NaN
def test_potential_bug_nan_interval():
    i = Interval(float("nan"), float("nan"))
    assert i.is_empty
    assert 0 not in i


# Potential bug: Interval with reversed bounds after float operation
def test_potential_bug_reversed_bounds_after_operation():
    i = Interval(1, 1 + 1e-15)
    new_lower = i.lower + 1e-16
    new_upper = i.upper - 1e-16
    assert new_lower <= new_upper  # This might fail due to float imprecision


# Potential bug: Interval size calculation with small numbers
def test_potential_bug_small_number_size():
    i = Interval(1e-300, 1e-300 + 1e-310)
    assert math.isclose(
        i.size(), 1e-310, rel_tol=1e-6
    )  # This might fail due to float imprecision with small numbers


# Potential bug: Clamp with large epsilon
def test_potential_bug_clamp_large_epsilon():
    i = Interval(0, 1)
    with pytest.raises(ValueError):
        i.clamp(2, epsilon=10)


# Potential bug: Intersection of intervals with shared bound
def test_potential_bug_intersection_shared_bound():
    i1 = Interval(0, 1, closed_R=True)
    i2 = Interval(1, 2, closed_L=True)
    intersection = i1.intersection(i2)
    assert intersection == Interval.get_singleton(
        1
    )  # This might fail if shared bounds are not handled correctly


# Potential bug: Union of intervals with shared bound
def test_potential_bug_union_shared_bound():
    i1 = Interval(0, 1, closed_R=True)
    i2 = Interval(1, 2, closed_L=True)
    union = i1.union(i2)
    assert union == Interval(
        0, 2
    )  # This might fail if shared bounds are not handled correctly


# Potential bug: Interval containing only zero
def test_potential_bug_zero_only_interval():
    i = Interval(0, 0)
    assert (
        i.is_empty
    )  # This might fail if zero-only intervals are not handled correctly
    assert (
        i.size() == 0
    )  # This might fail if the size calculation doesn't account for this case


# Potential bug: Interval with custom numeric types
def test_potential_bug_custom_numeric_types():
    from decimal import Decimal

    i = Interval(Decimal("0.1"), Decimal("0.3"))  # type: ignore[arg-type]
    assert (
        Decimal("0.2") in i
    )  # This might fail if custom numeric types are not handled correctly


# Potential bug: Clamp with value equal to bound
def test_potential_bug_clamp_equal_to_bound():
    i = Interval(0, 1)
    assert i.clamp(0) > 0
    assert i.clamp(1) < 1


# Potential bug: Interval containing only infinity with closed bounds
def test_potential_bug_closed_infinity_interval():
    i = ClosedInterval(math.inf, math.inf)
    assert (
        i.is_singleton
    )  # This might fail if closed infinity-only intervals are not handled correctly
    assert (
        math.inf in i
    )  # This might fail if membership of infinity in closed intervals is not handled correctly


# Potential bug: Interval spanning entire float range
def test_potential_bug_full_float_range():
    i = Interval(float("-inf"), float("inf"))
    assert sys.float_info.max in i
    assert sys.float_info.min in i
    assert 0.0 in i
    assert -0.0 in i


# Potential bug: Interval comparison with different types
def test_potential_bug_comparison_different_types():
    i1 = Interval(0, 1)
    i2 = ClosedInterval(0, 1)
    assert (
        i1 != i2
    )  # This might fail if comparison between different interval types is not handled correctly


# Potential bug: Interval with bounds differing only in sign (0.0 vs -0.0)
def test_potential_bug_zero_sign_difference():
    i1 = Interval(0.0, 1.0)
    i2 = Interval(-0.0, 1.0)
    assert i1 == i2  # This might fail if signed zero is not handled correctly


# Potential bug: Clamp with NaN epsilon
def test_potential_bug_clamp_nan_epsilon():
    i = Interval(0, 1)
    with pytest.raises(ValueError):
        i.clamp(0.5, epsilon=float("nan"))


# Potential bug: Interval containing only NaN with closed bounds
def test_potential_bug_closed_inf():
    i1 = ClosedInterval.get_singleton(float("inf"))
    i2 = Interval.get_singleton(float("inf"))
    i3 = ClosedInterval(-float("inf"), float("inf"))
    i4 = Interval(-float("inf"), float("inf"))
    i5 = ClosedInterval(float("inf"), float("inf"))
    i6 = Interval(float("inf"), float("inf"))

    assert i1.is_singleton
    assert i2.is_singleton
    assert not i3.is_singleton
    assert not i4.is_singleton
    assert not i3.is_empty
    assert not i4.is_empty
    assert i5.is_singleton
    assert i6.is_empty

    assert i1.clamp(1) == float("inf")
    assert i2.clamp(1) == float("inf")
    assert i3.clamp(1) == 1
    assert i4.clamp(1) == 1


# Potential bug: Intersection of universal set with itself
def test_potential_bug_universal_set_self_intersection():
    u = Interval(float("-inf"), float("inf"))
    assert u.intersection(u) == u


# Potential bug: Union of universal set with any other set
def test_potential_bug_universal_set_union():
    u = Interval(float("-inf"), float("inf"))
    i = Interval(0, 1)
    assert u.union(i) == u


# Potential bug: Clamp with integer bounds and float value
def test_potential_bug_clamp_integer_bounds_float_value():
    i = Interval(0, 1)
    result = i.clamp(0.5)
    assert isinstance(
        result, float
    )  # This might fail if type consistency is not maintained


# Potential bug: Interval from string with scientific notation
def test_potential_bug_interval_from_scientific_notation():
    i = Interval.from_str("[1e-10, 1e10]")
    assert i.lower == 1e-10
    assert i.upper == 1e10


# Potential bug: Interval with repeated float operations leading to unexpected results
def test_potential_bug_repeated_float_operations():
    i = Interval(0, 1)
    for _ in range(1000):
        i = Interval(i.lower + sys.float_info.epsilon, i.upper - sys.float_info.epsilon)
    assert 0.5 in i  # This might fail due to accumulated float imprecision


# Potential bug: Interval size with subnormal numbers
def test_potential_bug_subnormal_size():
    tiny = sys.float_info.min * sys.float_info.epsilon
    i = Interval(tiny, tiny * 2)
    assert (
        0 < i.size() < sys.float_info.min
    )  # This might fail if subnormal numbers are not handled correctly in size calculation


# Potential bug: Clamp with subnormal epsilon
def test_potential_bug_clamp_subnormal_epsilon():
    i = Interval(0, 1)
    tiny_epsilon = sys.float_info.min * sys.float_info.epsilon
    result = i.clamp(-1, epsilon=tiny_epsilon)
    assert result > 0  # This might fail if subnormal epsilons are not handled correctly


# Potential bug: Interval containing maximum and minimum floats
def test_potential_bug_max_min_float_interval():
    i = Interval(sys.float_info.min, sys.float_info.max)
    assert 1.0 in i
    assert -1.0 not in i
    assert i.size() == sys.float_info.max - sys.float_info.min


# Potential bug: Interval with bounds very close to zero
def test_potential_bug_near_zero_bounds():
    epsilon = sys.float_info.epsilon
    i = Interval(-epsilon, epsilon)
    assert 0 in i
    assert i.size() == 2 * epsilon


# Potential bug: Clamp with value very close to infinity
def test_potential_bug_clamp_near_infinity():
    i = ClosedInterval(0, 1)
    very_large = sys.float_info.max * 0.99
    result = i.clamp(very_large)
    assert (
        result == 1
    )  # This might fail if values near infinity are not handled correctly in clamp
