from __future__ import annotations

import random
from math import isclose, isinf, isnan

import pytest

from muutils.misc import shorten_numerical_to_str, str_to_numeric


@pytest.mark.parametrize(
    "quantity, expected",
    [
        ("5", 5),
        ("-5", -5),
        ("0.1", 0.1),
        ("-0.1", -0.1),
        ("1/5", 0.2),
        ("-1/5", -0.2),
        ("1K", 1000.0),
        ("-1K", -1000.0),
        ("1.5M", 1500000.0),
        ("-1.5M", -1500000.0),
        ("2.5B", 2.5 * 1e9),
        ("-2.5B", -2.5 * 1e9),
        ("1/2M", 0.5 * 1e6),
        ("-1/2M", -0.5 * 1e6),
        ("100q", 100 * 1e15),
        ("-100q", -100 * 1e15),
        ("0.001Q", 0.001 * 1e18),
        ("-0.001Q", -0.001 * 1e18),
        ("1.23", 1.23),
        ("-1.23", -1.23),
        ("4.5678e2", 456.78),
        ("-4.5678e2", -456.78),
    ],
)
def test_str_to_numeric(quantity, expected):
    assert str_to_numeric(quantity) == expected


@pytest.mark.parametrize(
    "x, s",
    [
        ("inf", 1),
        ("INF", 1),
        ("infinity", 1),
        ("INFINITY", 1),
        ("-inf", -1),
        ("-INF", -1),
        ("-infinity", -1),
        ("-INFINITY", -1),
    ],
)
def test_str_to_numeric_inf(x: str, s: int):
    x_num: float = str_to_numeric(x)
    assert isinf(x_num)
    if s == 1:
        assert x_num > 0
    else:
        assert x_num < 0


def test_str_to_numeric_nan():
    assert isnan(str_to_numeric("nan"))
    assert isnan(str_to_numeric("NAN"))


@pytest.mark.parametrize(
    "x",
    [
        "1/0",
        "-1/0",
        "5/0",
        "-5/0",
    ],
)
def test_div_by_zero(x: str):
    with pytest.raises(ZeroDivisionError):
        str_to_numeric(x)


@pytest.mark.parametrize(
    "quantity",
    [
        "invalid",
        "5.5.5",
        "1/2/3",
        "1QQ",
        "1K5",
        "1.2.3M",
        "1e1e1",
        "None",
        "null",
        "nil",
        "nanan",
        "infinitesimal",
        "infinity and beyond",
        "True or False",
        "a lot!",
        "12*&**@&#!dkjadhkj",
    ],
)
def test_str_to_numeric_invalid(quantity):
    with pytest.raises(ValueError):
        str_to_numeric(quantity)


@pytest.mark.parametrize(
    "quantity, mapping, expected",
    [
        ("5k", {"k": 1e3}, 5000),
        ("-5k", {"k": 1e3}, -5000),
        ("2.5x", {"x": 1e5}, 2.5 * 1e5),
        ("-2.5x", {"x": 1e5}, -2.5 * 1e5),
        ("1/4y", {"y": 1e2}, 0.25 * 1e2),
        ("-1/4y", {"y": 1e2}, -0.25 * 1e2),
        ("1.2LOL", {"LOL": 1e6}, 1.2 * 1e6),
        ("-1.2LOL", {"LOL": 1e6}, -1.2 * 1e6),
    ],
)
def test_str_to_numeric_custom_mapping(quantity, mapping, expected):
    assert str_to_numeric(quantity, mapping) == expected


@pytest.mark.parametrize(
    "quantity, small_as_decimal, precision, expected",
    [
        (1234, True, 1, "1.2K"),
        (1234, False, 1, "1K"),
        (1234, True, 2, "1.23K"),
        (1234567, True, 1, "1.2M"),
        (1234567890, True, 1, "1.2B"),
        (1234567890123, True, 1, "1.2t"),
        (1234567890123456, True, 1, "1.2q"),
        (1234567890123456789, True, 1, "1.2Q"),
    ],
)
def test_shorten_numerical_to_str(quantity, small_as_decimal, precision, expected):
    assert shorten_numerical_to_str(quantity, small_as_decimal, precision) == expected


@pytest.mark.parametrize(
    "exponent_range, n_tests",
    [
        ((1, 18), 1000),
        ((-2, 2), 1000),
    ],
)
def test_round_trip_fuzzing(exponent_range, n_tests):
    for _ in range(n_tests):
        exponent: int = random.randint(*exponent_range)
        mantissa: float = random.uniform(1, 10)
        num_sign: int = random.choice([-1, 1])
        num: float = num_sign * mantissa * (10**exponent)

        shortened: str = shorten_numerical_to_str(num)
        print(f"num: {num}, shortened: {shortened}")
        restored: float = str_to_numeric(shortened)

        assert isclose(
            num, restored, rel_tol=1e-1
        ), f"Failed for num: {num}, shortened: {shortened}, restored: {restored}"
