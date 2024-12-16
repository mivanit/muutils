import pytest
import multiprocessing
import time
from typing import Any, List, Iterable

# Import the function to test
from muutils.parallel import DEFAULT_PBAR_FN, run_maybe_parallel

# Try to check if multiprocess is installed
multiprocess_installed = True
try:
    import multiprocess  # noqa: F401
except ImportError:
    multiprocess_installed = False


DATA: dict = dict(
    empty=[],
    single=[5],
    small=list(range(4)),
    medium=list(range(10)),
    large=list(range(50)),
)
SQUARE_RESULTS: dict = {k: [x**2 for x in v] for k, v in DATA.items()}
ADD_ONE_RESULTS: dict = {k: [x + 1 for x in v] for k, v in DATA.items()}


# Basic test functions
def square(x: int) -> int:
    return x**2


def add_one(x: int) -> int:
    return x + 1


def raise_value_error(x: int) -> int:
    if x == 5:
        raise ValueError("Test error")
    return x**2


def slow_square(x: int) -> int:
    time.sleep(0.0001)
    return x**2


def raise_on_negative(x: int) -> int:
    if x < 0:
        raise ValueError("Negative number")
    return x


def stateful_fn(x: list) -> list:
    x.append(1)
    return x


class ComplexObject:
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ComplexObject) and self.value == other.value


def dataset_decorator(keys: List[str]):
    def wrapper(test_func):
        return pytest.mark.parametrize(
            "input_range, expected",
            [(DATA[k], SQUARE_RESULTS[k]) for k in keys],
            ids=keys,
        )(test_func)

    return wrapper


@dataset_decorator(["empty", "single", "small"])
@pytest.mark.parametrize("parallel", [False, True, 2, 4])
@pytest.mark.parametrize("keep_ordered", [True, False])
@pytest.mark.parametrize(
    "use_multiprocess",
    [
        False,
        pytest.param(
            True,
            marks=pytest.mark.skipif(
                not multiprocess_installed, reason="multiprocess not installed"
            ),
        ),
    ],
)
def test_general_functionality(
    input_range, expected, parallel, keep_ordered, use_multiprocess
):
    # whether it's possible to use multiprocess
    if use_multiprocess and (
        parallel is False or parallel == 1 or len(input_range) == 1
    ):
        return

    # run the function
    results = run_maybe_parallel(
        func=square,
        iterable=input_range,
        parallel=parallel,
        pbar_kwargs={},
        keep_ordered=keep_ordered,
        use_multiprocess=use_multiprocess,
    )

    # check the results
    assert set(results) == set(expected)
    if keep_ordered:
        assert results == expected


@dataset_decorator(["small"])
@pytest.mark.parametrize(
    "pbar_type",
    ["tqdm", "spinner", "none", None, "invalid"],
)
@pytest.mark.parametrize("disable_flag", [True, False])
def test_progress_bar_types_and_disable(input_range, expected, pbar_type, disable_flag):
    pbar_kwargs = {"disable": disable_flag}
    if pbar_type == "invalid" and not disable_flag:
        with pytest.raises(ValueError):
            run_maybe_parallel(square, input_range, False, pbar_kwargs, pbar=pbar_type)
    else:
        results = run_maybe_parallel(
            square, input_range, False, pbar_kwargs, pbar=pbar_type
        )
        assert results == expected


@dataset_decorator(["small"])
@pytest.mark.parametrize("chunksize", [None, 1, 5])
@pytest.mark.parametrize("parallel", [False, True, 2])
def test_chunksize_and_parallel(input_range, expected, chunksize, parallel):
    results = run_maybe_parallel(square, input_range, parallel, {}, chunksize=chunksize)
    assert results == expected


@dataset_decorator(["small"])
@pytest.mark.parametrize("invalid_parallel", ["invalid", 0, -1, 1.5])
def test_invalid_parallel_values(input_range, expected, invalid_parallel):
    with pytest.raises(ValueError):
        run_maybe_parallel(square, input_range, invalid_parallel)


def test_exception_in_func():
    # one of the inputs is 0..3, no error here
    # Let's inject a known error
    error_input = [5]  # Will raise ValueError
    with pytest.raises(ValueError):
        run_maybe_parallel(raise_value_error, error_input, True, {})


@dataset_decorator(["small"])
@pytest.mark.parametrize(
    "iterable_factory",
    [
        lambda x: list(x),
        lambda x: tuple(x),
        lambda x: set(x),
        lambda x: dict.fromkeys(x, 0),
    ],
)
def test_different_iterables(input_range, expected, iterable_factory):
    test_input = iterable_factory(input_range)
    result = run_maybe_parallel(square, test_input, False)
    if isinstance(test_input, set):
        assert set(result) == set(expected)
    else:
        assert result == expected


@pytest.mark.parametrize("parallel", [False, True])
def test_error_handling(parallel):
    # input_range is all positive small range, let's modify it to include negatives
    input_data = [-1, 0, 1, -2]
    with pytest.raises(ValueError):
        run_maybe_parallel(raise_on_negative, input_data, parallel)


def _process_complex(obj):
    return ComplexObject(obj.value * 2)


COMPLEX_DATA: List[ComplexObject] = [ComplexObject(i) for i in range(5)]
EXPECTED_COMPLEX = [ComplexObject(i * 2) for i in range(5)]


@pytest.mark.parametrize("parallel", [False, True])
@pytest.mark.parametrize("pbar_type", [None, DEFAULT_PBAR_FN])
def test_complex_objects(parallel, pbar_type):
    # override input_range with complex objects just for this test
    result = run_maybe_parallel(
        _process_complex, COMPLEX_DATA, parallel, pbar=pbar_type
    )
    expected_complex = EXPECTED_COMPLEX
    assert all(a == b for a, b in zip(result, expected_complex))


@dataset_decorator(["small"])
def test_resource_cleanup(input_range, expected):
    initial_processes = len(multiprocessing.active_children())
    run_maybe_parallel(square, input_range, True)
    time.sleep(0.05)
    final_processes = len(multiprocessing.active_children())
    assert abs(final_processes - initial_processes) <= 2


@dataset_decorator(["small"])
def test_custom_progress_bar(input_range, expected):
    def custom_progress_bar_fn(iterable: Iterable, **kwargs: Any) -> Iterable:
        return iterable

    result = run_maybe_parallel(square, input_range, False, pbar=custom_progress_bar_fn)
    assert result == expected


@dataset_decorator(["small"])
@pytest.mark.parametrize(
    "kwargs",
    [
        None,
        dict(),
        dict(desc="Processing"),
        dict(disable=True),
        dict(ascii=True),
        dict(config="default"),
        dict(config="bar"),
        dict(ascii=True, config="bar"),
        dict(message="Processing"),
        dict(message="Processing", desc="Processing"),
    ],
)
def test_progress_bar_kwargs(input_range, expected, kwargs):
    result = run_maybe_parallel(square, input_range, False, pbar_kwargs=kwargs)
    assert result == expected


@dataset_decorator(["medium"])
def test_parallel_performance(input_range, expected):
    serial_result = run_maybe_parallel(slow_square, input_range, False)
    parallel_result = run_maybe_parallel(slow_square, input_range, True)
    assert serial_result == parallel_result


@dataset_decorator(["small"])
def test_reject_pbar_str_when_not_str_or_callable(input_range, expected):
    with pytest.raises(TypeError):
        run_maybe_parallel(square, input_range, False, pbar=12345)


def custom_pbar(iterable: Iterable, **kwargs: Any) -> List:
    return list(iterable)


@dataset_decorator(["small"])
def test_manual_callable_pbar(input_range, expected):
    results = run_maybe_parallel(square, input_range, False, pbar=custom_pbar)
    assert results == expected, "Manual callable pbar test failed."


@pytest.mark.parametrize(
    "input_data, parallel",
    [
        (range(multiprocessing.cpu_count() + 1), True),
        (range(multiprocessing.cpu_count() - 1), True),
    ],
)
def test_edge_cases(input_data, parallel):
    result = run_maybe_parallel(square, input_data, parallel)
    assert result == [square(x) for x in input_data]
