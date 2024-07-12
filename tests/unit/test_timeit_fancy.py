import pytest
from muutils.statcounter import StatCounter
from typing import Callable, Any
import pstats

# Assuming the timeit_fancy function and FancyTimeitResult are imported from the correct module
from muutils.timeit_fancy import timeit_fancy, FancyTimeitResult


def test_timeit_fancy_basic():
    def simple_function():
        return sum(range(1000))

    result = timeit_fancy(simple_function)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.return_value is None
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_with_return():
    def simple_function():
        return sum(range(1000))

    result = timeit_fancy(simple_function, get_return=True)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.return_value == 499500
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_with_profiling():
    def simple_function():
        return sum(range(1000))

    result = timeit_fancy(simple_function, do_profiling=True)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.return_value is None
    assert isinstance(result.profile, pstats.Stats)
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_with_setup():
    setup = "x = 10"

    def simple_function():
        # x is defined in the setup
        return x * 2  # noqa: F821

    result = timeit_fancy(simple_function, setup=setup, namespace={"x": 10})

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.return_value is None
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_with_repeats():
    def simple_function():
        return sum(range(100))

    result = timeit_fancy(simple_function, repeats=10)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert len(result.timings) == 10
    assert result.return_value is None
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


@pytest.mark.parametrize("cmd", [lambda: sum(range(100)), "sum(range(100))"])
def test_timeit_fancy_with_different_cmd_types(cmd: Callable[[], Any] | str):
    result = timeit_fancy(cmd)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.return_value is None
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())
