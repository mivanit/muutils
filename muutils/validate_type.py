from __future__ import annotations

import types
import typing

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


def validate_type(value: typing.Any, expected_type: typing.Any) -> bool:
    """Validate that a value is of the expected type. use `typeguard` for a more robust solution.

    https://github.com/agronholm/typeguard
    """
    if expected_type is typing.Any:
        return True

    # base type without args
    if isinstance(expected_type, type):
        try:
            # if you use args on a type like `dict[str, int]`, this will fail
            return isinstance(value, expected_type)
        except TypeError:
            pass

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
        return any(validate_type(value, arg) for arg in args)

    # generic alias, more complicated
    item_type: type
    if isinstance(expected_type, GenericAliasTypes):
        if origin is list:
            # no args
            if len(args) == 0:
                return isinstance(value, list)
            # incorrect number of args
            if len(args) != 1:
                raise TypeError(
                    f"Too many arguments for list expected 1, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is list
            if not isinstance(value, list):
                return False
            # check all items in list are of the correct type
            item_type = args[0]
            return all(validate_type(item, item_type) for item in value)

        if origin is dict:
            # no args
            if len(args) == 0:
                return isinstance(value, dict)
            # incorrect number of args
            if len(args) != 2:
                raise TypeError(
                    f"Expected 2 arguments for dict, expected 2, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is dict
            if not isinstance(value, dict):
                return False
            # check all items in dict are of the correct type
            key_type: type = args[0]
            value_type: type = args[1]
            return all(
                validate_type(key, key_type) and validate_type(val, value_type)
                for key, val in value.items()
            )

        if origin is set:
            # no args
            if len(args) == 0:
                return isinstance(value, set)
            # incorrect number of args
            if len(args) != 1:
                raise TypeError(
                    f"Expected 1 argument for Set, got {args = },   {expected_type = },   {value = },   {origin = }",
                    f"{GenericAliasTypes = }",
                )
            # check is set
            if not isinstance(value, set):
                return False
            # check all items in set are of the correct type
            item_type = args[0]
            return all(validate_type(item, item_type) for item in value)

        if origin is tuple:
            # no args
            if len(args) == 0:
                return isinstance(value, tuple)
            # check is tuple
            if not isinstance(value, tuple):
                return False
            # check correct number of items in tuple
            if len(value) != len(args):
                return False
            # check all items in tuple are of the correct type
            return all(validate_type(item, arg) for item, arg in zip(value, args))

        # TODO: Callables, etc.

        raise ValueError(
            f"Unsupported generic alias {expected_type = } for {value = },   {origin = },   {args = }",
            f"{GenericAliasTypes = }",
        )

    else:
        raise ValueError(
            f"Unsupported type hint {expected_type = } for {value = }",
            f"{GenericAliasTypes = }",
        )
