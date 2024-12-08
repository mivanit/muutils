from typing import Callable, Literal, Optional, Union


def dataclass_validator_factory(
    cls,
    checks: Optional[
        list[
            tuple[
                Callable[
                    [object], bool
                ],  # method taking self as argument and returning True if valid
                Optional[str],  # error message
            ]
        ]
    ] = None,
    default_throw_except: bool = False,
    field_check_types: Union[bool, list[str]] = True,
    type_strictness: Literal["except", "check", "ignore"] = "except",
) -> Callable:
    """validate dataclass through type checking and a list of checks

    # Args
    - cls: dataclass to validate (so, define MyClass.validate outside of the class defn. see example)
    - `checks`: a list of tuples of the form (method, error_message). the method should take self as argument and return True if valid
    - `default_throw_except: bool` : if True, will throw an exception if any check in `checks` fails. does not apply to type checking
    - `field_check_types: Union[bool, list[str]]`: if True, will check the type of each field. if a list, will check the type of only the fields in the list. if False, will not check the type of any field.
    - `type_strictness: Literal['except', 'check', 'ignore']` : if 'except', will throw an exception if any type is incorrect. if 'check', will return false if a type check fails, but will not raise an exception. if 'ignore', will not check type at all.

    # Returns
    - `validator: Callable` : a function that takes a dataclass instance and a boolean indicating whether to throw an exception or not, and returns `True` if the dataclass is valid, `False` otherwise.

    # Usage:
    ```python
    # define our class
    @dataclass
    class MyClass:
        a: int
        x: str

    # now construct the validator *outside* the class
    MyClass.validate = dataclass_validator_factory(
        MyClass,
        checks = [
            (lambda x: x.a > 0, "a must be greater than 0"),
        ],
        field_check_types = ['a'],
        default_throw_except = True,
        type_strictness = 'except',
    )
    ```

    """

    # check type strictness value
    if type_strictness not in ("except", "check", "ignore"):
        raise ValueError(
            f"type_strictness must be one of 'except', 'check', 'ignore'. got {type_strictness = }"
        )

    # if set to True and no list given, set to all the keys
    if field_check_types and isinstance(field_check_types, bool):
        field_check_types = list(cls.__dataclass_fields__.keys())

    # filter and convert the fields and their types
    fields_types: dict[str, type] = {
        key: (
            # if complex type, list `list[int]`, get `list`
            field.type.__origin__ if hasattr(field.type, "__origin__") else field.type
        )
        for key, field in cls.__dataclass_fields__.items()
        if key in field_check_types  # filter by
    }

    def validate(self, throw_except: bool = default_throw_except) -> bool:
        f"""automagically created validator function for {cls.__name__}"""
        valid: bool = True

        # type checking
        for field_name, field_type in fields_types.items():
            if not isinstance(getattr(self, field_name), field_type):
                # if incorrect type
                valid = False
                if type_strictness == "except":
                    raise TypeError(
                        f"`{cls.__name__}.{field_name}` must be of type `{field_type}`, is of type `{type(getattr(self, field_name))}`"
                    )

        # custom checks
        if checks is not None:
            for check_func, error_msg in checks:
                # call the function and check output
                if not check_func(self):
                    valid = False
                    if throw_except:
                        raise ValueError(error_msg.format(self) + f"\n\t{self = }")

        return valid

    return validate
