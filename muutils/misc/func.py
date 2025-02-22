from __future__ import annotations
import functools
import sys
from types import CodeType
import warnings
from typing import Any, Callable, Tuple, cast, TypeVar

try:
    if sys.version_info >= (3, 11):
        # 3.11+
        from typing import Unpack, TypeVarTuple, ParamSpec
    else:
        # 3.9+
        from typing_extensions import Unpack, TypeVarTuple, ParamSpec  # type: ignore[assignment]
except ImportError:
    warnings.warn(
        "muutils.misc.func could not import Unpack and TypeVarTuple from typing or typing_extensions, typed_lambda may not work"
    )
    ParamSpec = TypeVar  # type: ignore
    Unpack = Any  # type: ignore
    TypeVarTuple = TypeVar  # type: ignore


from muutils.errormode import ErrorMode

warnings.warn("muutils.misc.func is experimental, use with caution")

ReturnType = TypeVar("ReturnType")
T_kwarg = TypeVar("T_kwarg")
T_process_in = TypeVar("T_process_in")
T_process_out = TypeVar("T_process_out")

FuncParams = ParamSpec("FuncParams")
FuncParamsPreWrap = ParamSpec("FuncParamsPreWrap")


def process_kwarg(
    kwarg_name: str,
    processor: Callable[[T_process_in], T_process_out],
) -> Callable[
    [Callable[FuncParamsPreWrap, ReturnType]], Callable[FuncParams, ReturnType]
]:
    """Decorator that applies a processor to a keyword argument.

    The underlying function is expected to have a keyword argument
    (with name `kwarg_name`) of type `T_out`, but the caller provides
    a value of type `T_in` that is converted via `processor`.

    # Parameters:
     - `kwarg_name : str`
        The name of the keyword argument to process.
     - `processor : Callable[[T_in], T_out]`
        A callable that converts the input value (`T_in`) into the
        type expected by the function (`T_out`).

    # Returns:
     - A decorator that converts a function of type
       `Callable[OutputParams, ReturnType]` (expecting `kwarg_name` of type `T_out`)
       into one of type `Callable[InputParams, ReturnType]` (accepting `kwarg_name` of type `T_in`).
    """

    def decorator(
        func: Callable[FuncParamsPreWrap, ReturnType],
    ) -> Callable[FuncParams, ReturnType]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> ReturnType:
            if kwarg_name in kwargs:
                # Convert the caller’s value (of type T_in) to T_out
                kwargs[kwarg_name] = processor(kwargs[kwarg_name])
            return func(*args, **kwargs)  # type: ignore[arg-type]

        return cast(Callable[FuncParams, ReturnType], wrapper)

    return decorator


@process_kwarg("action", ErrorMode.from_any)
def validate_kwarg(
    kwarg_name: str,
    validator: Callable[[T_kwarg], bool],
    description: str | None = None,
    action: ErrorMode = ErrorMode.EXCEPT,
) -> Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]:
    """Decorator that validates a specific keyword argument.

    # Parameters:
     - `kwarg_name : str`
        The name of the keyword argument to validate.
     - `validator : Callable[[Any], bool]`
        A callable that returns True if the keyword argument is valid.
     - `description : str | None`
        A message template if validation fails.
     - `action : str`
        Either `"raise"` (default) or `"warn"`.

    # Returns:
     - `Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]`
        A decorator that validates the keyword argument.

    # Modifies:
     - If validation fails and `action=="warn"`, emits a warning.
       Otherwise, raises a ValueError.

    # Usage:

    ```python
    @validate_kwarg("x", lambda val: val > 0, "Invalid {kwarg_name}: {value}")
    def my_func(x: int) -> int:
        return x

    assert my_func(x=1) == 1
    ```

    # Raises:
     - `ValueError` if validation fails and `action == "raise"`.
    """

    def decorator(
        func: Callable[FuncParams, ReturnType],
    ) -> Callable[FuncParams, ReturnType]:
        @functools.wraps(func)
        def wrapper(*args: FuncParams.args, **kwargs: FuncParams.kwargs) -> ReturnType:
            if kwarg_name in kwargs:
                value: Any = kwargs[kwarg_name]
                if not validator(value):
                    msg: str = (
                        description.format(kwarg_name=kwarg_name, value=value)
                        if description
                        else f"Validation failed for keyword '{kwarg_name}' with value {value}"
                    )
                    if action == "warn":
                        warnings.warn(msg, UserWarning)
                    else:
                        raise ValueError(msg)
            return func(*args, **kwargs)

        return cast(Callable[FuncParams, ReturnType], wrapper)

    return decorator


def replace_kwarg(
    kwarg_name: str,
    check: Callable[[T_kwarg], bool],
    replacement_value: T_kwarg,
    replace_if_missing: bool = False,
) -> Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]:
    """Decorator that replaces a specific keyword argument value by identity comparison.

    # Parameters:
     - `kwarg_name : str`
        The name of the keyword argument to replace.
     - `check : Callable[[T_kwarg], bool]`
        A callable that returns True if the keyword argument should be replaced.
     - `replacement_value : T_kwarg`
        The value to replace with.
     - `replace_if_missing : bool`
        If True, replaces the keyword argument even if it's missing.

    # Returns:
     - `Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]`
        A decorator that replaces the keyword argument value.

    # Modifies:
     - Updates `kwargs[kwarg_name]` if its value is `default_value`.

    # Usage:

    ```python
    @replace_kwarg("x", None, "default_string")
    def my_func(*, x: str | None = None) -> str:
        return x

    assert my_func(x=None) == "default_string"
    ```
    """

    def decorator(
        func: Callable[FuncParams, ReturnType],
    ) -> Callable[FuncParams, ReturnType]:
        @functools.wraps(func)
        def wrapper(*args: FuncParams.args, **kwargs: FuncParams.kwargs) -> ReturnType:
            if kwarg_name in kwargs:
                # TODO: no way to type hint this, I think
                if check(kwargs[kwarg_name]):  # type: ignore[arg-type]
                    kwargs[kwarg_name] = replacement_value
            elif replace_if_missing and kwarg_name not in kwargs:
                kwargs[kwarg_name] = replacement_value
            return func(*args, **kwargs)

        return cast(Callable[FuncParams, ReturnType], wrapper)

    return decorator


def is_none(value: Any) -> bool:
    return value is None


def always_true(value: Any) -> bool:
    return True


def always_false(value: Any) -> bool:
    return False


def format_docstring(
    **fmt_kwargs: Any,
) -> Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]:
    """Decorator that formats a function's docstring with the provided keyword arguments."""

    def decorator(
        func: Callable[FuncParams, ReturnType],
    ) -> Callable[FuncParams, ReturnType]:
        if func.__doc__ is not None:
            func.__doc__ = func.__doc__.format(**fmt_kwargs)
        return func

    return decorator


# TODO: no way to make the type system understand this afaik
LambdaArgs = TypeVarTuple("LambdaArgs")
LambdaArgsTypes = TypeVar("LambdaArgsTypes", bound=Tuple[type, ...])


def typed_lambda(
    fn: Callable[[Unpack[LambdaArgs]], ReturnType],
    in_types: LambdaArgsTypes,
    out_type: type[ReturnType],
) -> Callable[[Unpack[LambdaArgs]], ReturnType]:
    """Wraps a lambda function with type hints.

    # Parameters:
     - `fn : Callable[[Unpack[LambdaArgs]], ReturnType]`
        The lambda function to wrap.
     - `in_types : tuple[type, ...]`
        Tuple of input types.
     - `out_type : type[ReturnType]`
        The output type.

    # Returns:
     - `Callable[..., ReturnType]`
        A new function with annotations matching the given signature.

    # Usage:

    ```python
    add = typed_lambda(lambda x, y: x + y, (int, int), int)
    assert add(1, 2) == 3
    ```

    # Raises:
     - `ValueError` if the number of input types doesn't match the lambda's parameters.
    """
    code: CodeType = fn.__code__
    n_params: int = code.co_argcount

    if len(in_types) != n_params:
        raise ValueError(
            f"Number of input types ({len(in_types)}) doesn't match number of parameters ({n_params})"
        )

    param_names: tuple[str, ...] = code.co_varnames[:n_params]
    annotations: dict[str, type] = {  # type: ignore[var-annotated]
        name: typ
        for name, typ in zip(param_names, in_types)  # type: ignore[arg-type]
    }
    annotations["return"] = out_type

    @functools.wraps(fn)
    def wrapped(*args: Unpack[LambdaArgs]) -> ReturnType:
        return fn(*args)

    wrapped.__annotations__ = annotations
    return wrapped
