"""experimental utility for validating types in python, see `validate_type`"""

from __future__ import annotations

from inspect import signature, unwrap
import types
import typing
import functools

# this is also for python <3.10 compatibility
_GenericAliasTypeNames: typing.List[str] = [
    "GenericAlias",
    "_GenericAlias",
    "_UnionGenericAlias",
    "_BaseGenericAlias",
]

_GenericAliasTypesList: list = [
    getattr(typing, name, None) for name in _GenericAliasTypeNames
]

GenericAliasTypes: tuple = tuple([t for t in _GenericAliasTypesList if t is not None])


class IncorrectTypeException(TypeError):
    pass


class TypeHintNotImplementedError(NotImplementedError):
    pass


class InvalidGenericAliasError(TypeError):
    pass


def _return_validation_except(
    return_val: bool, value: typing.Any, expected_type: typing.Any
) -> bool:
    if return_val:
        return True
    else:
        raise IncorrectTypeException(
            f"Expected {expected_type = } for {value = }",
            f"{type(value) = }",
            f"{type(value).__mro__ = }",
            f"{typing.get_origin(expected_type) = }",
            f"{typing.get_args(expected_type) = }",
            "\ndo --tb=long in pytest to see full trace",
        )
        return False


def _return_validation_bool(return_val: bool) -> bool:
    return return_val


def validate_type(
    value: typing.Any, expected_type: typing.Any, do_except: bool = False
) -> bool:
    """Validate that a `value` is of the `expected_type`

    # Parameters
    - `value`: the value to check the type of
    - `expected_type`: the type to check against. Not all types are supported
    - `do_except`: if `True`, raise an exception if the type is incorrect (instead of returning `False`)
        (default: `False`)

    # Returns
    - `bool`: `True` if the value is of the expected type, `False` otherwise.

    # Raises
    - `IncorrectTypeException(TypeError)`: if the type is incorrect and `do_except` is `True`
    - `TypeHintNotImplementedError(NotImplementedError)`: if the type hint is not implemented
    - `InvalidGenericAliasError(TypeError)`: if the generic alias is invalid

    use `typeguard` for a more robust solution: https://github.com/agronholm/typeguard
    """
    if expected_type is typing.Any:
        return True

    # set up the return function depending on `do_except`
    _return_func: typing.Callable[[bool], bool] = (
        # functools.partial doesn't hint the function signature
        functools.partial(  # type: ignore[assignment]
            _return_validation_except, value=value, expected_type=expected_type
        )
        if do_except
        else _return_validation_bool
    )

    # base type without args
    if isinstance(expected_type, type):
        try:
            # if you use args on a type like `dict[str, int]`, this will fail
            return _return_func(isinstance(value, expected_type))
        except TypeError as e:
            if isinstance(e, IncorrectTypeException):
                raise e

    origin: typing.Any = typing.get_origin(expected_type)
    args: tuple = typing.get_args(expected_type)

    # useful for debugging
    # print(f"{value = },   {expected_type = },   {origin = },   {args = }")
    UnionType = getattr(types, "UnionType", None)

    if (origin is typing.Union) or (  # this works in python <3.10
        False
        if UnionType is None  # return False if UnionType is not available
        else origin is UnionType  # return True if UnionType is available
    ):
        return _return_func(any(validate_type(value, arg) for arg in args))

    # generic alias, more complicated
    item_type: type
    if isinstance(expected_type, GenericAliasTypes):
        if origin is list:
            # no args
            if len(args) == 0:
                return _return_func(isinstance(value, list))
            # incorrect number of args
            if len(args) != 1:
                raise InvalidGenericAliasError(
                    f"Too many arguments for list expected 1, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is list
            if not isinstance(value, list):
                return _return_func(False)
            # check all items in list are of the correct type
            item_type = args[0]
            return all(validate_type(item, item_type) for item in value)

        if origin is dict:
            # no args
            if len(args) == 0:
                return _return_func(isinstance(value, dict))
            # incorrect number of args
            if len(args) != 2:
                raise InvalidGenericAliasError(
                    f"Expected 2 arguments for dict, expected 2, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is dict
            if not isinstance(value, dict):
                return _return_func(False)
            # check all items in dict are of the correct type
            key_type: type = args[0]
            value_type: type = args[1]
            return _return_func(
                all(
                    validate_type(key, key_type) and validate_type(val, value_type)
                    for key, val in value.items()
                )
            )

        if origin is set:
            # no args
            if len(args) == 0:
                return _return_func(isinstance(value, set))
            # incorrect number of args
            if len(args) != 1:
                raise InvalidGenericAliasError(
                    f"Expected 1 argument for Set, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is set
            if not isinstance(value, set):
                return _return_func(False)
            # check all items in set are of the correct type
            item_type = args[0]
            return _return_func(all(validate_type(item, item_type) for item in value))

        if origin is tuple:
            # no args
            if len(args) == 0:
                return _return_func(isinstance(value, tuple))
            # check is tuple
            if not isinstance(value, tuple):
                return _return_func(False)
            # check correct number of items in tuple
            if len(value) != len(args):
                return _return_func(False)
            # check all items in tuple are of the correct type
            return _return_func(
                all(validate_type(item, arg) for item, arg in zip(value, args))
            )

        if origin is type:
            # no args
            if len(args) == 0:
                return _return_func(isinstance(value, type))
            # incorrect number of args
            if len(args) != 1:
                raise InvalidGenericAliasError(
                    f"Expected 1 argument for Type, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is type
            item_type = args[0]
            if item_type in value.__mro__:
                return _return_func(True)
            else:
                return _return_func(False)

        # TODO: Callables, etc.

        raise TypeHintNotImplementedError(
            f"Unsupported generic alias {expected_type = } for {value = },   {origin = },   {args = }",
            f"{origin = }, {args = }",
            f"\n{GenericAliasTypes = }",
        )

    else:
        raise TypeHintNotImplementedError(
            f"Unsupported type hint {expected_type = } for {value = }",
            f"{origin = }, {args = }",
            f"\n{GenericAliasTypes = }",
        )


def get_fn_allowed_kwargs(fn: typing.Callable) -> typing.Set[str]:
    """Get the allowed kwargs for a function, raising an exception if the signature cannot be determined."""
    try:
        fn = unwrap(fn)
        params = signature(fn).parameters
    except ValueError as e:
        raise ValueError(
            f"Cannot retrieve signature for {fn.__name__ = } {fn = }: {str(e)}"
        ) from e

    return {
        param.name
        for param in params.values()
        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
    }
