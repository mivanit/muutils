import random
from math import isclose

import pytest

from muutils.misc import str_to_numeric, shorten_numerical_to_str

@pytest.mark.parametrize("quantity, expected", [
    ("5", 5),
    ("0.1", 0.1),
    ("1/5", 0.2),
    ("1K", 1000.0),
    ("1.5M", 1500000.0),
    ("2.5B", 2.5 * 1e9),
    ("1/2M", 0.5 * 1e6),
    ("100q", 100 * 1e15),
    ("0.001Q", 0.001 * 1e18),
])
def test_str_to_numeric(quantity, expected):
    assert str_to_numeric(quantity) == expected

@pytest.mark.parametrize("quantity", [
    "invalid",
    "5.5.5",
    "1/2/3",
    "1QQ",
])
def test_str_to_numeric_invalid(quantity):
    with pytest.raises(ValueError):
        str_to_numeric(quantity)

@pytest.mark.parametrize("quantity, mapping, expected", [
    ("5k", {"k": 1e3}, 5000),
    ("2.5x", {"x": 1e5}, 2.5 * 1e5),
    ("1/4y", {"y": 1e2}, 0.25 * 1e2),
    ("1.2LOL", {"LOL": 1e6}, 1.2 * 1e6),
])
def test_str_to_numeric_custom_mapping(quantity, mapping, expected):
    assert str_to_numeric(quantity, mapping) == expected
    

@pytest.mark.parametrize("exponent_range, n_tests", [
    ((1, 18), 1000),
    ((-2, 2), 1000),
])
def test_round_trip_fuzzing(exponent_range, n_tests):
    for _ in range(n_tests):
        exponent: int = random.randint(*exponent_range)
        mantissa: float = random.uniform(1, 10)
        sign: int = random.choice([-1, 1])
        num: float = sign * mantissa * (10 ** exponent)
        
        shortened: str = shorten_numerical_to_str(num)
        print(f"num: {num}, shortened: {shortened}")
        restored: float = str_to_numeric(shortened)
        
        assert isclose(num, restored, rel_tol=1e-1), f"Failed for num: {num}, shortened: {shortened}, restored: {restored}"
