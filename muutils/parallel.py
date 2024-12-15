import multiprocessing
import functools
from typing import (
    Any,
    Callable,
    Iterable,
    Literal,
    Optional,
    TypeVar,
    Dict,
    List,
    Union,
    Protocol,
)

# for no tqdm fallback
from muutils.spinner import SpinnerContext
from muutils.validate_type import get_fn_allowed_kwargs


# typevars for our iterable and map
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class ProgressBarFunction(Protocol):
    def __call__(self, iterable: Iterable, **kwargs: Any) -> Iterable: ...


# default progress bar function
progress_bar_fn: Callable


# fallback to spinner option
def spinner_fn_wrap(x: Iterable, **kwargs) -> List:
    mapped_kwargs: dict = {
        k: v
        for k, v in kwargs.items()
        if k in get_fn_allowed_kwargs(SpinnerContext.__init__)
    }
    if "desc" in kwargs:
        mapped_kwargs["message"] = kwargs.get("desc")

    with SpinnerContext(**mapped_kwargs):
        return list(x)


# fallback to "no progress bar" option
def no_progress_fn_wrap(x: Iterable, **kwargs) -> Iterable:
    return x


# set the default progress bar function
try:
    # use tqdm if it's available
    import tqdm

    progress_bar_fn = tqdm.tqdm
except ImportError:
    # use progress bar as fallback
    progress_bar_fn = spinner_fn_wrap


def run_maybe_parallel(
    func: Callable[[InputType], OutputType],
    iterable: Iterable[InputType],
    parallel: Union[bool, int],
    pbar_kwargs: Union[Dict[str, Any], None] = None,
    chunksize: Optional[int] = None,
    keep_ordered: bool = True,
    use_multiprocess: bool = False,
    pbar: Union[Callable, Literal["tqdm", "spinner", "none", None]] = progress_bar_fn,
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
       _description_
     - `pbar_kwargs : Dict[str, Any]`
       _description_

    # Returns:
     - `List[OutputType]`
       _description_

    # Raises:
     - `ValueError` : _description_
    """

    # which progress bar to use
    pbar_fn: ProgressBarFunction

    if pbar_kwargs is None:
        pbar_kwargs = dict()

    # dont use a progress bar if `pbar` is None or "none", or if `disable` is set to True in `pbar_kwargs`
    if (pbar is None) or (pbar == "none") or pbar_kwargs.get("disable", False):
        pbar_fn = no_progress_fn_wrap

    # if `pbar` is a different string, figure out which progress bar to use
    elif isinstance(pbar, str):
        if pbar == "tqdm":
            pbar_fn = functools.partial(tqdm.tqdm, **pbar_kwargs)
        elif pbar == "spinner":
            pbar_fn = functools.partial(spinner_fn_wrap, **pbar_kwargs)
        else:
            raise ValueError(
                f"`pbar` must be either 'tqdm' or 'spinner' if `str`, or a valid callable, got {type(pbar) = } {pbar = }"
            )
    else:
        # the default value is a callable which will resolve to tqdm if available or spinner as a fallback. we pass kwargs to this
        pbar_fn = functools.partial(pbar, **pbar_kwargs)

    # number of inputs in iterable
    n_inputs: int = len(iterable)
    if n_inputs == 0:
        # Return immediately if there is no input
        return list()

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
            import multiprocess
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
        pool: multiprocessing.context._default_context.Pool = mp.Pool(num_processes)

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
        do_map = functools.partial(do_map, chunksize=chunksize_int)

    else:
        do_map = map

    # run the map function with a progress bar
    output: List[OutputType] = list(
        pbar_fn(
            do_map(
                func,
                iterable,
            ),
            total=n_inputs,
            **pbar_kwargs,
        )
    )

    if parallel:
        pool.close()
        pool.join()

    return output
