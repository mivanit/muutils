"`timeit_fancy` is just a fancier version of timeit with more options"

from __future__ import annotations

import pstats
import timeit
import cProfile
from typing import Callable, Union, TypeVar, NamedTuple, Any
import warnings

from muutils.statcounter import StatCounter

T = TypeVar("T")


class FancyTimeitResult(NamedTuple):
    """return type of `timeit_fancy`"""

    timings: StatCounter
    return_value: T  # type: ignore[valid-type]
    profile: Union[pstats.Stats, None]


def timeit_fancy(
    cmd: Union[Callable[[], T], str],
    setup: Union[str, Callable[[], Any]] = lambda: None,
    repeats: int = 5,
    namespace: Union[dict[str, Any], None] = None,
    get_return: bool = True,
    do_profiling: bool = False,
) -> FancyTimeitResult:
    """
    Wrapper for `timeit` to get the fastest run of a callable with more customization options.

    Approximates the functionality of the %timeit magic or command line interface in a Python callable.

    # Parameters

    - `cmd: Callable[[], T] | str`
        The callable to time. If a string, it will be passed to `timeit.Timer` as the `stmt` argument.
    - `setup: str`
        The setup code to run before `cmd`. If a string, it will be passed to `timeit.Timer` as the `setup` argument.
    - `repeats: int`
        The number of times to run `cmd` to get a reliable measurement.
    - `namespace: dict[str, Any]`
        Passed to `timeit.Timer` constructor.
        If `cmd` or `setup` use local or global variables, they must be passed here. See `timeit` documentation for details.
    - `get_return: bool`
        Whether to pass the value returned from `cmd`. If True, the return value will be appended in a tuple with execution time.
        This is for speed and convenience so that `cmd` doesn't need to be run again in the calling scope if the return values are needed.
        (default: `False`)
    - `do_profiling: bool`
        Whether to return a `pstats.Stats` object in addition to the time and return value.
        (default: `False`)

    # Returns

    `FancyTimeitResult`, which is a NamedTuple with the following fields:

    - `time: float`
        The time in seconds it took to run `cmd` the minimum number of times to get a reliable measurement.
    - `return_value: T|None`
        The return value of `cmd` if `get_return` is `True`, otherwise `None`.
    - `profile: pstats.Stats|None`
        A `pstats.Stats` object if `do_profiling` is `True`, otherwise `None`.
    """
    timer: timeit.Timer = timeit.Timer(cmd, setup, globals=namespace)

    # Perform the timing
    times: list[float] = timer.repeat(repeats, 1)

    # Optionally capture the return value
    profile: pstats.Stats | None = None

    return_value: T | None = None
    if get_return or do_profiling:
        # Optionally perform profiling
        if do_profiling:
            profiler = cProfile.Profile()
            profiler.enable()

        try:
            return_value = cmd()  # type: ignore[operator]
        except TypeError as e:
            warnings.warn(
                f"Failed to get return value from `cmd` due to error (probably passing a string). will return `return_value=None`\n{e}",
            )

        if do_profiling:
            profiler.disable()
            profile = pstats.Stats(profiler).strip_dirs().sort_stats("cumulative")

    # reset the return value if it wasn't requested
    if not get_return:
        return_value = None

    return FancyTimeitResult(
        timings=StatCounter(times),
        return_value=return_value,
        profile=profile,
    )
