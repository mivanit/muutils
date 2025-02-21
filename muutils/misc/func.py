from __future__ import annotations
import functools
from types import CodeType
import warnings
from typing import (
    Optional,
    cast,
    Callable,
    TypeVar,
    Any,
    TypeVarTuple,
    Unpack,
)

F = TypeVar("F", bound=Callable[..., Any])


def process_kwarg(
    kwarg_name: str,
    processor: Callable[[Any], Any],
) -> Callable[[F], F]:
    """Decorator that applies a processor to a keyword argument.

    This decorator inspects the function call's keyword arguments for `kwarg_name`.
    If present, that argument is transformed by `processor` before being passed on.

    # Parameters:
     - `kwarg_name : str`
        The name of the kwarg to be processed.
     - `processor : Callable[[Any], Any]`
        A callable (e.g. a lambda) that will process the kwarg's value.

    # Returns:
     - `Callable[[F], F]`
        A decorator that transforms the decorated function's kwarg.

    # Modifies:
     - The `kwargs[kwarg_name]` is replaced with the result of `processor(kwargs[kwarg_name])`.

    # Usage:
    ```python
    @process_kwarg("x", lambda x: x * 2)
    def my_func(x: int = 0) -> int:
        return x

    assert my_func(x=3) == 6
    ```
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if kwarg_name in kwargs:
                kwargs[kwarg_name] = processor(kwargs[kwarg_name])
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator


def validate_kwarg(
    kwarg_name: str,
    validator: Callable[[Any], bool],
    description: Optional[str] = None,
    action: str = "raise",
) -> Callable[[F], F]:
    """Decorator that validates a specific keyword argument.

    This decorator inspects the function call's keyword arguments for `kwarg_name`.
    If present, the argument is checked via `validator`. If validation fails,
    either a warning is issued or a `ValueError` is raised (depending on `action`).

    # Parameters:
     - `kwarg_name : str`
        The name of the kwarg to validate.
     - `validator : Callable[[Any], bool]`
        A callable that returns True if the kwarg is valid, otherwise False.
     - `description : Optional[str]`
        An optional message template to use if validation fails.
        May contain placeholders like `{kwarg_name}` and `{value}`.
     - `action : str`
        Either `"raise"` or `"warn"`. If `"raise"`, raises a `ValueError` upon failure.
        If `"warn"`, emits a `UserWarning`.
        (defaults to `"raise"`)

    # Returns:
     - `Callable[[F], F]`
        A decorator that validates the decorated function's kwarg.

    # Modifies:
     - If validation fails and `action == "warn"`, a warning is emitted. Otherwise, an exception is raised.

    # Usage:
    ```python
    @validate_kwarg("x", lambda val: val > 0, "Value for {kwarg_name} must be positive, got {value}")
    def my_func(x: int) -> int:
        return x

    # Raises ValueError if x <= 0
    assert my_func(x=1) == 1
    ```

    # Raises:
     - `ValueError`
        If validation fails and `action == "raise"`.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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

        return cast(F, wrapper)

    return decorator


def replace_kwarg(
    kwarg_name: str,
    default_value: Any,
    replacement_value: Any,
) -> Callable[[F], F]:
    """Decorator that replaces a specific keyword argument value by identity comparison.

    This decorator checks if `kwarg_name` is present in the function call's kwargs, and
    if its value is exactly (by identity) `default_value`. If so, it's replaced by
    `replacement_value`.

    # Parameters:
     - `kwarg_name : str`
        The name of the kwarg to replace.
     - `default_value : Any`
        The value (checked by `is`) that triggers replacement.
     - `replacement_value : Any`
        The value that will replace the kwarg if `default_value` is matched.

    # Returns:
     - `Callable[[F], F]`
        A decorator that replaces kwarg values.

    # Modifies:
     - `kwargs[kwarg_name]` is updated if the original value is `default_value` (by identity).

    # Usage:
    ```python
    @replace_kwarg("x", None, "default_string")
    def my_func(x: str | None = None) -> str:
        return x

    assert my_func(x=None) == "default_string"
    ```
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if kwarg_name in kwargs and kwargs[kwarg_name] is default_value:
                kwargs[kwarg_name] = replacement_value
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator


T_FuncWrap = TypeVar("T_FuncWrap", bound=Callable[..., Any])


def format_docstring(**kwargs) -> Callable[[T_FuncWrap], T_FuncWrap]:
    """Decorator that formats a function's docstring with the provided kwargs"""

    def decorator(func: T_FuncWrap) -> T_FuncWrap:
        func.__doc__ = func.__doc__.format(**kwargs)
        return func

    return decorator


T_Return = TypeVar("T_Return")
T_args = TypeVarTuple("T_args")


def typed_lambda(
    fn: Callable[..., Any],
    in_types: tuple[type[Unpack[T_args]], ...],
    out_type: type[T_Return],
) -> Callable[[Unpack[T_args]], T_Return]:
    """Wraps a lambda function with type hints.

    # Parameters:
     - `fn : Callable[..., Any]`
        The lambda function to wrap
     - `in_types : tuple[type[Unpack[Ts]], ...]`
        Tuple of input types
     - `out_type : type[T]`
        Output type

    # Returns:
     - `Callable[[Unpack[Ts]], T]`
        A new function with the same behavior but with type hints

    # Usage:
    ```python
    >>> add = typed_lambda(lambda x, y: x + y, (int, str), str)
    >>> reveal_type(add)  # type: Callable[[int, str], str]
    >>> add(1, "2")
    "12"
    ```

    # Raises:
     - `ValueError`
        If number of input types doesn't match lambda parameters
    """
    code: CodeType = fn.__code__
    n_params: int = code.co_argcount

    if len(in_types) != n_params:
        raise ValueError(
            f"Number of input types ({len(in_types)}) "
            f"doesn't match number of parameters ({n_params})"
        )

    param_names: tuple[str, ...] = code.co_varnames[:n_params]
    annotations: dict[str, type] = {
        name: type_ for name, type_ in zip(param_names, in_types)
    }
    annotations["return"] = out_type

    @functools.wraps(fn)
    def wrapped(*args: Unpack[T_args], **kwargs: Any) -> T_Return:
        return fn(*args, **kwargs)

    wrapped.__annotations__ = annotations

    return wrapped
