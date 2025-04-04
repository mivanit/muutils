import multiprocessing
import functools
from typing import (
    Any,
    Callable,
    Iterable,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Dict,
    List,
    Union,
    Protocol,
)

# for no tqdm fallback
from muutils.spinner import SpinnerContext
from muutils.validate_type import get_fn_allowed_kwargs


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")
# typevars for our iterable and map


class ProgressBarFunction(Protocol):
    "a protocol for a progress bar function"

    def __call__(self, iterable: Iterable, **kwargs: Any) -> Iterable: ...


ProgressBarOption = Literal["tqdm", "spinner", "none", None]
# type for the progress bar option


DEFAULT_PBAR_FN: ProgressBarOption
# default progress bar function

try:
    # use tqdm if it's available
    import tqdm  # type: ignore[import-untyped]

    DEFAULT_PBAR_FN = "tqdm"

except ImportError:
    # use progress bar as fallback
    DEFAULT_PBAR_FN = "spinner"


def spinner_fn_wrap(x: Iterable, **kwargs) -> List:
    "spinner wrapper"
    spinnercontext_allowed_kwargs: set[str] = get_fn_allowed_kwargs(
        SpinnerContext.__init__
    )
    mapped_kwargs: dict = {
        k: v for k, v in kwargs.items() if k in spinnercontext_allowed_kwargs
    }
    if "desc" in kwargs and "message" not in mapped_kwargs:
        mapped_kwargs["message"] = kwargs["desc"]

    if "message" not in mapped_kwargs and "total" in kwargs:
        mapped_kwargs["message"] = f"Processing {kwargs['total']} items"

    with SpinnerContext(**mapped_kwargs):
        output = list(x)

    return output


def map_kwargs_for_tqdm(kwargs: dict) -> dict:
    "map kwargs for tqdm, cant wrap because the pbar dissapears?"
    tqdm_allowed_kwargs: set[str] = get_fn_allowed_kwargs(tqdm.tqdm.__init__)
    mapped_kwargs: dict = {k: v for k, v in kwargs.items() if k in tqdm_allowed_kwargs}

    if "desc" not in kwargs:
        if "message" in kwargs:
            mapped_kwargs["desc"] = kwargs["message"]

        elif "total" in kwargs:
            mapped_kwargs["desc"] = f"Processing {kwargs.get('total')} items"
    return mapped_kwargs


def no_progress_fn_wrap(x: Iterable, **kwargs) -> Iterable:
    "fallback to no progress bar"
    return x


def set_up_progress_bar_fn(
    pbar: Union[ProgressBarFunction, ProgressBarOption],
    pbar_kwargs: Optional[Dict[str, Any]] = None,
    **extra_kwargs,
) -> Tuple[ProgressBarFunction, dict]:
    """set up the progress bar function and its kwargs

    # Parameters:
     - `pbar : Union[ProgressBarFunction, ProgressBarOption]`
       progress bar function or option. if a function, we return as-is. if a string, we figure out which progress bar to use
     - `pbar_kwargs : Optional[Dict[str, Any]]`
       kwargs passed to the progress bar function (default to `None`)
       (defaults to `None`)

    # Returns:
     - `Tuple[ProgressBarFunction, dict]`
         a tuple of the progress bar function and its kwargs

    # Raises:
     - `ValueError` : if `pbar` is not one of the valid options
    """
    pbar_fn: ProgressBarFunction

    if pbar_kwargs is None:
        pbar_kwargs = dict()

    pbar_kwargs = {**extra_kwargs, **pbar_kwargs}

    # dont use a progress bar if `pbar` is None or "none", or if `disable` is set to True in `pbar_kwargs`
    if (pbar is None) or (pbar == "none") or pbar_kwargs.get("disable", False):
        pbar_fn = no_progress_fn_wrap  # type: ignore[assignment]

    # if `pbar` is a different string, figure out which progress bar to use
    elif isinstance(pbar, str):
        if pbar == "tqdm":
            pbar_fn = tqdm.tqdm
            pbar_kwargs = map_kwargs_for_tqdm(pbar_kwargs)
        elif pbar == "spinner":
            pbar_fn = functools.partial(spinner_fn_wrap, **pbar_kwargs)
            pbar_kwargs = dict()
        else:
            raise ValueError(
                f"`pbar` must be either 'tqdm' or 'spinner' if `str`, or a valid callable, got {type(pbar) = } {pbar = }"
            )
    else:
        # the default value is a callable which will resolve to tqdm if available or spinner as a fallback. we pass kwargs to this
        pbar_fn = pbar

    return pbar_fn, pbar_kwargs


# TODO: if `parallel` is a negative int, use `multiprocessing.cpu_count() + parallel` to determine the number of processes
def run_maybe_parallel(
    func: Callable[[InputType], OutputType],
    iterable: Iterable[InputType],
    parallel: Union[bool, int],
    pbar_kwargs: Optional[Dict[str, Any]] = None,
    chunksize: Optional[int] = None,
    keep_ordered: bool = True,
    use_multiprocess: bool = False,
    pbar: Union[ProgressBarFunction, ProgressBarOption] = DEFAULT_PBAR_FN,
) -> List[OutputType]:
    """a function to make it easier to sometimes parallelize an operation

    - if `parallel` is `False`, then the function will run in serial, running `map(func, iterable)`
    - if `parallel` is `True`, then the function will run in parallel, running in parallel with the maximum number of processes
    - if `parallel` is an `int`, it must be greater than 1, and the function will run in parallel with the number of processes specified by `parallel`

    the maximum number of processes is given by the `min(len(iterable), multiprocessing.cpu_count())`

    # Parameters:
     - `func : Callable[[InputType], OutputType]`
       function passed to either `map` or `Pool.imap`
     - `iterable : Iterable[InputType]`
       iterable passed to either `map` or `Pool.imap`
     - `parallel : bool | int`
       whether to run in parallel, and how many processes to use
     - `pbar_kwargs : Dict[str, Any]`
       kwargs passed to the progress bar function

    # Returns:
     - `List[OutputType]`
       a list of the output of `func` for each element in `iterable`

    # Raises:
     - `ValueError` : if `parallel` is not a boolean or an integer greater than 1
     - `ValueError` : if `use_multiprocess=True` and `parallel=False`
     - `ImportError` : if `use_multiprocess=True` and `multiprocess` is not available
    """

    # number of inputs in iterable
    n_inputs: int = len(iterable)  # type: ignore[arg-type]
    if n_inputs == 0:
        # Return immediately if there is no input
        return list()

    # which progress bar to use
    pbar_fn: ProgressBarFunction
    pbar_kwargs_processed: dict
    pbar_fn, pbar_kwargs_processed = set_up_progress_bar_fn(
        pbar=pbar,
        pbar_kwargs=pbar_kwargs,
        # extra kwargs
        total=n_inputs,
    )

    # number of processes
    num_processes: int
    if isinstance(parallel, bool):
        num_processes = multiprocessing.cpu_count() if parallel else 1
    elif isinstance(parallel, int):
        if parallel < 2:
            raise ValueError(
                f"`parallel` must be a boolean, or be an integer greater than 1, got {type(parallel) = } {parallel = }"
            )
        num_processes = parallel
    else:
        raise ValueError(
            f"The 'parallel' parameter must be a boolean or an integer, got {type(parallel) = } {parallel = }"
        )

    # make sure we don't have more processes than iterable, and don't bother with parallel if there's only one process
    num_processes = min(num_processes, n_inputs)
    mp = multiprocessing
    if num_processes == 1:
        parallel = False

    if use_multiprocess:
        if not parallel:
            raise ValueError("`use_multiprocess=True` requires `parallel=True`")

        try:
            import multiprocess  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError(
                "`use_multiprocess=True` requires the `multiprocess` package -- this is mostly useful when you need to pickle a lambda. install muutils with `pip install muutils[multiprocess]` or just do `pip install multiprocess`"
            ) from e

        mp = multiprocess

    # set up the map function -- maybe its parallel, maybe it's just `map`
    do_map: Callable[
        [Callable[[InputType], OutputType], Iterable[InputType]],
        Iterable[OutputType],
    ]
    if parallel:
        # use `mp.Pool` since we might want to use `multiprocess` instead of `multiprocessing`
        pool = mp.Pool(num_processes)

        # use `imap` if we want to keep the order, otherwise use `imap_unordered`
        if keep_ordered:
            do_map = pool.imap
        else:
            do_map = pool.imap_unordered

        # figure out a smart chunksize if one is not given
        chunksize_int: int
        if chunksize is None:
            chunksize_int = max(1, n_inputs // num_processes)
        else:
            chunksize_int = chunksize

        # set the chunksize
        do_map = functools.partial(do_map, chunksize=chunksize_int)  # type: ignore

    else:
        do_map = map

    # run the map function with a progress bar
    output: List[OutputType] = list(
        pbar_fn(
            do_map(
                func,
                iterable,
            ),
            **pbar_kwargs_processed,
        )
    )

    # close the pool if we used one
    if parallel:
        pool.close()
        pool.join()

    # return the output as a list
    return output
