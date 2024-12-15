import pytest
import multiprocessing
import time
from typing import Any, List, Iterable

# Import the function to test
from muutils.parallel import run_maybe_parallel

# Try to check if multiprocess is installed
multiprocess_installed = True
try:
    import multiprocess
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
    if use_multiprocess and (
        parallel is False or parallel == 1 or len(input_range) == 1
    ):
        pytest.skip(
            "`use_multiprocess=True` requires `parallel=True` with parallel > 1 and more than one input"
        )
    results = run_maybe_parallel(
        func=square,
        iterable=input_range,
        parallel=parallel,
        pbar_kwargs={},
        keep_ordered=keep_ordered,
        use_multiprocess=use_multiprocess,
    )
    assert set(results) == set(expected)
    if keep_ordered:
        assert results == expected


@dataset_decorator(["small"])
@pytest.mark.parametrize(
    "pbar_type",
    ["tqdm", "spinner", "none", None, pytest.param("invalid", marks=pytest.mark.xfail)],
)
@pytest.mark.parametrize("disable_flag", [True, False])
def test_progress_bar_types_and_disable(input_range, expected, pbar_type, disable_flag):
    pbar_kwargs = {"disable": disable_flag}
    if pbar_type == "invalid":
        with pytest.raises(ValueError):
            run_maybe_parallel(square, input_range, True, pbar_kwargs, pbar=pbar_type)
    else:
        results = run_maybe_parallel(
            square, input_range, False, pbar_kwargs, pbar=pbar_type
        )
        assert results == expected


@dataset_decorator(["small"])
@pytest.mark.parametrize("chunksize", [None, 1, 2, 5, 10, 20])
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


@pytest.mark.parametrize(
    "input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small"]]
)
@pytest.mark.parametrize(
    "iterable_factory",
    [
        lambda x: list(x),
        lambda x: tuple(x),
        lambda x: set(x),
    ],
)
def test_different_iterables(input_range, expected, iterable_factory):
    test_input = iterable_factory(input_range)
    result = run_maybe_parallel(square, test_input, True)
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


def test_complex_objects():
    # override input_range with complex objects just for this test
    complex_data = [ComplexObject(i) for i in range(len(5))]
    result = run_maybe_parallel(_process_complex, complex_data, True)
    expected_complex = [ComplexObject(x.value * 2) for x in complex_data]
    assert all(a == b for a, b in zip(result, expected_complex))


@dataset_decorator(["small"])
def test_resource_cleanup(input_range, expected):
    initial_processes = len(multiprocessing.active_children())
    run_maybe_parallel(square, input_range, True)
    time.sleep(0.01)
    final_processes = len(multiprocessing.active_children())
    assert abs(final_processes - initial_processes) <= 2


@dataset_decorator(["medium", "large"])
@pytest.mark.parametrize("chunk_size", [None, 1, 5])
def test_large_input_handling(input_range, expected, chunk_size):
    result = run_maybe_parallel(square, input_range, True, chunksize=chunk_size)
    assert result == expected


@dataset_decorator(["small"])
def test_custom_progress_bar(input_range, expected):
    def custom_progress_bar_fn(iterable: Iterable, **kwargs: Any) -> Iterable:
        return iterable

    result = run_maybe_parallel(square, input_range, False, pbar=custom_progress_bar_fn)
    assert result == expected


@dataset_decorator(["medium"])
def test_parallel_performance(input_range, expected):
    serial_result = run_maybe_parallel(slow_square, input_range, False)
    parallel_result = run_maybe_parallel(slow_square, input_range, True)
    assert serial_result == parallel_result


# @pytest.mark.parametrize("input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small", "medium",]])
# def test_single_process_basic(input_range, expected):
#     results = list(run_maybe_parallel(square, input_range, False, {}))
#     assert results == expected, "Single processing test failed."

# @pytest.mark.parametrize("input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small", "medium"]])
# def test_multi_process_basic(input_range, expected):
#     results = list(run_maybe_parallel(square, input_range, True, {}))
#     assert results == expected, "Multi processing test failed."

# @pytest.mark.parametrize("input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small"]])
# @pytest.mark.parametrize("parallel", [2, 3, 4])
# def test_explicit_process_count_basic(input_range, expected, parallel):
#     results = list(run_maybe_parallel(square, input_range, parallel, {}))
#     assert results == expected, "Explicit process count test failed."

# @pytest.mark.parametrize("parallel", [False, True, 2, 3, 4])
# def test_zero_inputs_basic(parallel):
#     results = list(run_maybe_parallel(square, [], parallel, {}))
#     assert results == [], "Zero inputs test failed."


@pytest.mark.parametrize("invalid_parallel", ["invalid", -1, 1.5, None])
def test_invalid_parallel_value_basic(invalid_parallel):
    with pytest.raises(ValueError):
        list(run_maybe_parallel(square, DATA["small"], invalid_parallel, {}))


@pytest.mark.parametrize(
    "input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small"]]
)
@pytest.mark.parametrize("parallel", [4])
@pytest.mark.parametrize("chunksize", [1, 2, 3, 10, None])
def test_chunksize_effectiveness_basic(input_range, expected, parallel, chunksize):
    results = list(
        run_maybe_parallel(square, input_range, parallel=parallel, chunksize=chunksize)
    )
    assert results == expected, f"Chunksize test failed with chunksize={chunksize}"


# @pytest.mark.parametrize("input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small"]])
# @pytest.mark.parametrize("parallel", [4])
# @pytest.mark.parametrize("keep_ordered", [True, False])
# def test_order_preservation_basic(input_range, expected, parallel, keep_ordered):
#     results = list(run_maybe_parallel(square, input_range, parallel=parallel, keep_ordered=keep_ordered))
#     if keep_ordered:
#         assert results == expected, "Order preservation (ordered) test failed."
#     else:
#         assert set(results) == set(expected), "Order preservation (unordered) test failed."

# @pytest.mark.parametrize("input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small"]])
# def test_use_multiprocess_basic(input_range, expected):
#     if not multiprocess_installed:
#         pytest.skip("Multiprocess package not installed; test skipped.")
#     results = list(run_maybe_parallel(square, input_range, True, use_multiprocess=True))
#     assert results == expected, "Multiprocess usage test failed."


@pytest.mark.parametrize(
    "input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["small"]]
)
@pytest.mark.parametrize("pbar_type", ["tqdm", "spinner", "none", None])
def test_progress_bar_types_basic(input_range, expected, pbar_type):
    try:
        results = list(run_maybe_parallel(square, input_range, False, pbar=pbar_type))
        assert results == expected, f"Progress bar type {pbar_type} test failed."
    except ValueError:
        # If we hit ValueError, it means the pbar_type wasn't valid when it should have been
        assert pbar_type not in [
            "tqdm",
            "spinner",
            "none",
            None,
        ], f"Invalid pbar value {pbar_type} accepted."


@pytest.mark.parametrize(
    "input_range, expected", [(DATA[k], SQUARE_RESULTS[k]) for k in ["empty", "small"]]
)
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
def test_basic_functionality(
    input_range, expected, parallel, keep_ordered, use_multiprocess
):
    if use_multiprocess and (parallel is False or parallel == 1):
        pytest.skip(
            "`use_multiprocess=True` requires `parallel=True` with parallel > 1"
        )
    results = run_maybe_parallel(
        func=square,
        iterable=input_range,
        parallel=parallel,
        pbar_kwargs={},
        keep_ordered=keep_ordered,
        use_multiprocess=use_multiprocess,
    )
    assert set(results) == set(expected), "Basic functionality set check failed."
    if keep_ordered:
        assert results == expected, "Ordering was lost when keep_ordered=True."


# def test_empty_input():
#     results = run_maybe_parallel(square, [], True, {})
#     assert results == [], "Empty input test failed."


def test_single_input():
    results = run_maybe_parallel(square, [5], True, {})
    assert results == [25], "Single input test failed."


# def test_serial_mode():
#     data = list(range(20))
#     results = run_maybe_parallel(square, data, False, {})
#     assert results == [x**2 for x in data], "Serial mode test failed."


@pytest.mark.parametrize("parallel_value", ["invalid", -1, 0, 1])
def test_invalid_parallel_value(parallel_value):
    with pytest.raises(ValueError):
        run_maybe_parallel(square, DATA["small"], parallel_value, {})


@pytest.mark.parametrize("pbar_value", ["invalid_string", 123, []])
def test_invalid_pbar_value(pbar_value):
    data = list(range(5))
    with pytest.raises((ValueError, TypeError)):
        run_maybe_parallel(square, data, True, {}, pbar=pbar_value)


def test_no_progress_fn_wrap():
    data = list(range(5))
    results = run_maybe_parallel(square, data, True, {}, pbar="none")
    assert results == [x**2 for x in data], "No progress function test failed."


def test_spinner_fn_wrap():
    data = list(range(5))
    results = run_maybe_parallel(square, data, True, {}, pbar="spinner")
    assert results == [x**2 for x in data], "Spinner mode test failed."


@pytest.mark.parametrize("disable_flag", [True, False])
def test_progress_bar_disable(disable_flag):
    data = list(range(5))
    pbar_kwargs = {"disable": disable_flag}
    results = run_maybe_parallel(square, data, True, pbar_kwargs, pbar="tqdm")
    assert results == [
        x**2 for x in data
    ], f"Progress bar disable={disable_flag} test failed."


@pytest.mark.parametrize("chunksize", [1, 2, 5, 10, None])
def test_chunksize(chunksize):
    data = list(range(10))
    results = run_maybe_parallel(square, data, True, {}, chunksize=chunksize)
    assert results == [x**2 for x in data], f"Chunksize {chunksize} test failed."


def test_no_pbar_kwargs():
    data = list(range(5))
    results = run_maybe_parallel(square, data, True, pbar_kwargs=None)
    assert results == [x**2 for x in data], "No pbar_kwargs test failed."


@pytest.mark.parametrize("use_multiprocess_flag", [True, False])
def test_use_multiprocess_without_parallel(use_multiprocess_flag):
    data = [1, 2, 3]
    if use_multiprocess_flag and not multiprocess_installed:
        pytest.skip("multiprocess not installed.")
    if use_multiprocess_flag:
        with pytest.raises(ValueError):
            run_maybe_parallel(square, data, False, {}, use_multiprocess=True)
    else:
        results = run_maybe_parallel(square, data, False, {}, use_multiprocess=False)
        assert results == [1, 4, 9], "use_multiprocess=False test failed."


@pytest.mark.skipif(not multiprocess_installed, reason="multiprocess not installed")
def test_use_multiprocess_true():
    data = list(range(5))
    results = run_maybe_parallel(square, data, True, {}, use_multiprocess=True)
    assert set(results) == set(x**2 for x in data), "use_multiprocess=True test failed."


@pytest.mark.parametrize("pbar_value", [None, "none", "tqdm", "spinner"])
def test_various_pbar_options(pbar_value):
    data = list(range(5))
    results = run_maybe_parallel(square, data, True, pbar_kwargs={}, pbar=pbar_value)
    assert set(results) == set(
        x**2 for x in data
    ), f"Various pbar options test with pbar={pbar_value} failed."


def test_exception_in_func():
    data = list(range(5))
    with pytest.raises(ValueError):
        run_maybe_parallel(raise_value_error, data, True, {})


@pytest.mark.parametrize("parallel", [False, True, 2])
def test_order_preservation_enhanced(parallel):
    data = list(range(5))
    results = run_maybe_parallel(
        add_one, data, parallel=parallel, pbar_kwargs={}, keep_ordered=True
    )
    assert results == [
        x + 1 for x in data
    ], f"Order preservation test failed with parallel={parallel}"


@pytest.mark.parametrize("keep_ordered", [True, False])
def test_order_disabling(keep_ordered):
    data = list(range(5))
    results = run_maybe_parallel(
        add_one, data, parallel=True, pbar_kwargs={}, keep_ordered=keep_ordered
    )
    assert set(results) == set(x + 1 for x in data), "Order disabling set check failed."
    if keep_ordered:
        assert results == [
            x + 1 for x in data
        ], "Order was not preserved when keep_ordered=True."


def test_invalid_pbar_string():
    data = list(range(5))
    with pytest.raises(ValueError):
        run_maybe_parallel(square, data, True, pbar_kwargs={}, pbar="unknown_bar")


def test_zero_length_parallel():
    data = []
    results = run_maybe_parallel(square, data, True, {})
    assert results == [], "Zero length parallel test failed."


@pytest.mark.parametrize(
    "parallel_count", [multiprocessing.cpu_count(), multiprocessing.cpu_count() * 2]
)
def test_process_limit(parallel_count):
    data = list(range(5))
    results = run_maybe_parallel(square, data, parallel_count, {})
    assert results == [x**2 for x in data], "Process limit test failed."


def test_disable_pbar_flag():
    data = list(range(10))
    results = run_maybe_parallel(square, data, True, pbar_kwargs={"disable": True})
    assert results == [x**2 for x in data], "Disable pbar flag test failed."


def test_desc_in_pbar_kwargs():
    data = list(range(5))
    results = run_maybe_parallel(
        square, data, True, pbar_kwargs={"desc": "Testing Desc"}
    )
    assert results == [x**2 for x in data], "desc in pbar_kwargs test failed."


def test_reject_pbar_str_when_not_str_or_callable():
    data = list(range(5))
    with pytest.raises(TypeError):
        run_maybe_parallel(square, data, True, pbar=12345)


def test_very_large_input():
    data = list(range(100))
    results_true = [x**2 for x in data]
    results_parallel = run_maybe_parallel(square, data, parallel=True, pbar_kwargs={})
    results_serial = run_maybe_parallel(square, data, parallel=False, pbar_kwargs={})
    assert (
        results_parallel == results_true
    ), "Very large input test failed for parallel=True."
    assert (
        results_serial == results_true
    ), "Very large input test failed for parallel=False."


def custom_pbar(iterable: Iterable, **kwargs: Any) -> List:
    return list(iterable)


def test_manual_callable_pbar():
    data = list(range(10))
    results = run_maybe_parallel(square, data, True, pbar=custom_pbar)
    assert results == [x**2 for x in data], "Manual callable pbar test failed."


###############################################
# ADDITIONAL TESTS FROM THE SECOND CODE BLOCK
###############################################


# Basic functionality tests (again, but more parametric)
@pytest.mark.parametrize("parallel", [False, True, 2, multiprocessing.cpu_count()])
def test_basic_functionality_again(parallel):
    input_data = list(range(10))
    expected = [square(x) for x in input_data]
    result = run_maybe_parallel(square, input_data, parallel)
    assert result == expected


@pytest.mark.parametrize("size", [0, 1, 10, 100])
@pytest.mark.parametrize("parallel", [False, True])
def test_different_sizes(size, parallel):
    input_data = list(range(size))
    expected = [square(x) for x in input_data]
    result = run_maybe_parallel(square, input_data, parallel)
    assert result == expected


@pytest.mark.parametrize("pbar", ["tqdm", "spinner", "none", None])
def test_progress_bar_types_again(pbar):
    input_data = list(range(5))
    result = run_maybe_parallel(square, input_data, False, pbar=pbar)
    assert result == [square(x) for x in input_data]


@pytest.mark.parametrize(
    "pbar_kwargs", [{"desc": "Processing"}, {"disable": True}, {"leave": False}, {}]
)
def test_progress_bar_kwargs_again(pbar_kwargs):
    input_data = list(range(5))
    result = run_maybe_parallel(square, input_data, False, pbar_kwargs=pbar_kwargs)
    assert result == [square(x) for x in input_data]


@pytest.mark.parametrize("parallel", [False, True])
def test_error_handling(parallel):
    input_data = [-1, 0, 1, -2]
    with pytest.raises(ValueError):
        run_maybe_parallel(raise_on_negative, input_data, parallel)


@pytest.mark.parametrize("invalid_parallel", ["invalid", 0, -1, 1.5])
def test_invalid_parallel_values_again(invalid_parallel):
    with pytest.raises(ValueError):
        run_maybe_parallel(square, range(10), invalid_parallel)


@pytest.mark.parametrize("chunksize", [1, 2, 5])
def test_chunking_again(chunksize):
    input_data = list(range(10))
    result = run_maybe_parallel(square, input_data, True, chunksize=chunksize)
    assert result == [square(x) for x in input_data]


@pytest.mark.parametrize("keep_ordered", [True, False])
def test_ordering_again(keep_ordered):
    input_data = list(range(100))
    result = run_maybe_parallel(
        slow_square, input_data, True, keep_ordered=keep_ordered
    )
    expected = [x**2 for x in input_data]
    if keep_ordered:
        assert result == expected
    else:
        assert sorted(result) == sorted(expected)


@pytest.mark.parametrize(
    "iterable_factory",
    [
        lambda x: list(x),
        lambda x: tuple(x),
        lambda x: set(x),
    ],
)
def test_different_iterables(iterable_factory):
    input_data = iterable_factory(range(10))
    result = run_maybe_parallel(square, input_data, True)
    expected = [x**2 for x in input_data]
    if isinstance(input_data, set):
        assert set(result) == set(expected)
    else:
        assert result == expected


def _process_complex(obj):
    return ComplexObject(obj.value * 2)


def test_complex_objects():
    input_data = [ComplexObject(i) for i in range(5)]
    result = run_maybe_parallel(_process_complex, input_data, True)
    expected = [ComplexObject(x.value * 2) for x in input_data]
    assert all(a == b for a, b in zip(result, expected))


@pytest.mark.skipif(not multiprocess_installed, reason="multiprocess not installed")
def test_multiprocess():
    input_data = list(range(10))
    result = run_maybe_parallel(square, input_data, True, use_multiprocess=True)
    assert result == [square(x) for x in input_data]


def test_resource_cleanup():
    initial_processes = len(multiprocessing.active_children())
    run_maybe_parallel(square, range(10), True)
    time.sleep(0.01)
    final_processes = len(multiprocessing.active_children())
    # We can't strictly guarantee exact equality due to test environment,
    # but we expect them to be close. We'll just assert no huge leaks.
    # For a strict environment:
    assert (
        abs(final_processes - initial_processes) <= 2
    ), "Resource cleanup test failed. Processes did not close properly."


def test_parallel_performance():
    input_size = 20
    input_data = list(range(input_size))

    start_time = time.time()
    serial_result = run_maybe_parallel(slow_square, input_data, False)
    serial_time = time.time() - start_time

    start_time = time.time()
    parallel_result = run_maybe_parallel(slow_square, input_data, True)
    parallel_time = time.time() - start_time

    # Just ensure parallel time isn't drastically worse
    # Actual speedup depends on environment, let's just ensure correctness:
    assert serial_result == parallel_result
    # It's possible that parallel might not always be faster in a test environment,
    # but we'll allow this as is. If we want to enforce speedup:
    # assert parallel_time < serial_time, "Parallel did not speed up as expected."


@pytest.mark.parametrize("chunk_size", [None, 1, 10, 20])
def test_large_input_handling(chunk_size):
    large_input = list(range(100))
    result = run_maybe_parallel(square, large_input, True, chunksize=chunk_size)
    assert result == [square(x) for x in large_input]


@pytest.mark.parametrize(
    "test_case",
    [
        ([], True),
        ([0], True),
        (range(multiprocessing.cpu_count() + 1), True),
        (range(multiprocessing.cpu_count() - 1), True),
    ],
)
def test_edge_cases(test_case):
    input_data, parallel = test_case
    result = run_maybe_parallel(square, input_data, parallel)
    assert result == [square(x) for x in input_data]


def test_custom_progress_bar():
    input_data = list(range(5))

    def custom_progress_bar_fn(iterable: Iterable, **kwargs: Any) -> Iterable:
        return iterable

    result = run_maybe_parallel(square, input_data, False, pbar=custom_progress_bar_fn)
    assert result == [square(x) for x in input_data]
