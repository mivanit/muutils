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
    print(f"{value = },   {expected_type = },   {origin = },   {args = }")

    if origin is types.UnionType or origin is typing.Union:
        return any(validate_type(value, arg) for arg in args)

    # generic alias, more complicated
    if isinstance(expected_type, (typing.GenericAlias, typing._GenericAlias, typing._UnionGenericAlias)):

        
        if origin is list:
            if len(args) != 1:
                raise TypeError(f"Too many arguments for list expected 1, got {args = },   {expected_type = },   {value = },   {origin = }")
            if not isinstance(value, list):
                return False
            return all(validate_type(item, args[0]) for item in value)
        
        if origin is dict:
            if len(args) != 2:
                raise TypeError(f"Expected 2 arguments for dict, expected 2, got {args = },   {expected_type = },   {value = },   {origin = }")
            if not isinstance(value, dict):
                return False
            return all(
                validate_type(key, args[0]) and validate_type(val, args[1])
                for key, val in value.items()
            )
        
        if origin is set:
            if len(args) != 1:
                raise TypeError(f"Expected 1 argument for Set, got {args = },   {expected_type = },   {value = },   {origin = }")
            if not isinstance(value, set):
                return False
            return all(validate_type(item, args[0]) for item in value)
        
        if origin is tuple:
            if not isinstance(value, tuple):
                return False
            if len(value) != len(args):
                return False
            return all(validate_type(item, arg) for item, arg in zip(value, args))
        
        # TODO: Callables, etc.
        
        raise ValueError(f"Unsupported generic alias {expected_type = } for {value = },   {origin = },   {args = }")

    else:
        raise ValueError(f"Unsupported type hint {expected_type = } for {value = }")