import warnings
import pytest
from muutils.statcounter import StatCounter
import pstats

# Assuming the timeit_fancy function and FancyTimeitResult are imported from the correct module
from muutils.timeit_fancy import timeit_fancy, FancyTimeitResult


def test_timeit_fancy_basic():
    def simple_function():
        return sum(range(1000))

    result = timeit_fancy(simple_function)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
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
    assert isinstance(result.profile, pstats.Stats)
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_no_return():
    def simple_function_returns_data():
        return "helloworld"

    result = timeit_fancy(simple_function_returns_data, get_return=False)
    assert isinstance(result, FancyTimeitResult)
    assert result.return_value is None
    assert isinstance(result.timings, StatCounter)
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_with_repeats():
    def simple_function():
        return sum(range(100))

    result = timeit_fancy(simple_function, repeats=10)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.timings.total() == 10
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_cmd_lambda():
    result = timeit_fancy(lambda: sum(range(100)))

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_cmd_string_warns():
    # expect a warning
    with pytest.warns(UserWarning):
        result = timeit_fancy("sum(range(100))")

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())


def test_timeit_fancy_cmd_string_nowarn():
    # expect no warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = timeit_fancy("sum(range(100))", get_return=False, do_profiling=False)

    assert isinstance(result, FancyTimeitResult)
    assert isinstance(result.timings, StatCounter)
    assert result.profile is None
    assert all(t > 0 for t in result.timings.values())
