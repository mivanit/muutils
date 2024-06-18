import types
import typing


def validate_type(value: typing.Any, expected_type: typing.Any) -> bool:
    if expected_type is typing.Any:
        return True

    # base type without args
    if isinstance(expected_type, type):
        return isinstance(value, expected_type)

    origin: type = typing.get_origin(expected_type)
    args: list = typing.get_args(expected_type)

    # useful for debugging
    # print(f"{value = },   {expected_type = },   {origin = },   {args = }")

    if origin is types.UnionType or origin is typing.Union:
        return any(validate_type(value, arg) for arg in args)

    # generic alias, more complicated
    if isinstance(
        expected_type,
        (
            typing.GenericAlias,
            typing._GenericAlias,
            typing._UnionGenericAlias,
            typing._BaseGenericAlias,
        ),
    ):

        if origin is list:
            # no args
            if len(args) == 0:
                return isinstance(value, list)
            # incorrect number of args
            if len(args) != 1:
                raise TypeError(
                    f"Too many arguments for list expected 1, got {args = },   {expected_type = },   {value = },   {origin = }"
                )
            # check is list
            if not isinstance(value, list):
                return False
            # check all items in list are of the correct type
            item_type: type = args[0]
            return all(validate_type(item, item_type) for item in value)

        if origin is dict:
            # no args
            if len(args) == 0:
                return isinstance(value, dict)
            # incorrect number of args
            if len(args) != 2:
                raise TypeError(
                    f"Expected 2 arguments for dict, expected 2, got {args = },   {expected_type = },   {value = },   {origin = }"
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
                    f"Expected 1 argument for Set, got {args = },   {expected_type = },   {value = },   {origin = }"
                )
            # check is set
            if not isinstance(value, set):
                return False
            # check all items in set are of the correct type
            item_type: type = args[0]
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
            f"Unsupported generic alias {expected_type = } for {value = },   {origin = },   {args = }"
        )

    else:
        raise ValueError(f"Unsupported type hint {expected_type = } for {value = }")
