from __future__ import annotations

import abc
import dataclasses
import functools
import json
import sys
import types
import typing
import warnings
from typing import Any, Callable, Optional, Type, TypeVar, Union

from muutils.validate_type import validate_type
from muutils.json_serialize.serializable_field import SerializableField, serializable_field
from muutils.json_serialize.util import array_safe_eq, dc_eq

# pylint: disable=bad-mcs-classmethod-argument, too-many-arguments, protected-access

T = TypeVar("T")


class ZanjMissingWarning(UserWarning):
    pass


_zanj_loading_needs_import: bool = True


def zanj_register_loader_serializable_dataclass(cls: typing.Type[T]):
    """Register a serializable dataclass with the ZANJ backport


    # TODO: there is some duplication here with register_loader_handler
    """
    global _zanj_loading_needs_import

    if _zanj_loading_needs_import:
        try:
            from zanj.loading import (  # type: ignore[import]
                LoaderHandler,
                register_loader_handler,
            )
        except ImportError:
            warnings.warn(
                "ZANJ not installed, cannot register serializable dataclass loader. ZANJ can be found at https://github.com/mivanit/ZANJ or installed via `pip install zanj`",
                ZanjMissingWarning,
            )
            return

    _format: str = f"{cls.__name__}(SerializableDataclass)"
    lh: LoaderHandler = LoaderHandler(
        check=lambda json_item, path=None, z=None: (  # type: ignore
            isinstance(json_item, dict)
            and "__format__" in json_item
            and json_item["__format__"].startswith(_format)
        ),
        load=lambda json_item, path=None, z=None: cls.load(json_item),  # type: ignore
        uid=_format,
        source_pckg=cls.__module__,
        desc=f"{_format} loader via muutils.json_serialize.serializable_dataclass",
    )

    register_loader_handler(lh)

    return lh

OnTypeAssertDo = typing.Literal["raise", "warn", "ignore"]

DEFAULT_ON_TYPE_ASSERT: OnTypeAssertDo = "warn"

def SerializableDataclass__validate_field_type(
    self: SerializableDataclass,
    field: SerializableField|str,
    on_type_assert: OnTypeAssertDo = DEFAULT_ON_TYPE_ASSERT,
) -> bool:
    # do nothing
    if not field.assert_type:
        return True
    
    if on_type_assert == "ignore":
        return True
    
    # get field
    if isinstance(field, str):
        field = self.__dataclass_fields__[field]

    assert isinstance(
        field, SerializableField
    ), f"Field '{field.name = }' on class {self.__class__ = } is not a SerializableField, but a {type(field) = }"

    # get field type hints
    field_type_hint: Any = get_cls_type_hints(self.__class__).get(field.name, None)

    # get the value
    value: Any = getattr(self, field.name)
    
    # validate the type    
    if field_type_hint is not None:
        try:
            # validate the type
            type_is_valid: bool = validate_type(
                value, field_type_hint
            )

            # if not valid, raise or warn depending on the setting in the SerializableDataclass
            if not type_is_valid:
                msg: str = f"Field '{field.name}' on class {self.__class__.__name__} has type {type(value)}, but expected {field_type_hint}"
                if on_type_assert == "raise":
                    raise ValueError(msg)
                else:
                    warnings.warn(msg)

        except Exception as e:
            raise ValueError(
                "exception while validating type: "
                + f"{field.name = }, {field_type_hint = }, {type(field_type_hint) = }, {value = }"
            ) from e
    else:
        raise ValueError(
            f"Cannot get type hints for {self.__class__.__name__}, field {field.name = } and so cannot validate."
            + f"Python version is {sys.version_info = }. You can:\n"
            + f"  - disable `assert_type`. Currently: {field.assert_type = }\n"
            + f"  - use hints like `typing.Dict` instead of `dict` in type hints (this is required on python 3.8.x). You had {field.type = }\n"
            + "  - use python 3.9.x or higher\n"
            + "  - coming in a future release, specify custom type validation functions\n"
        )



def SerializableDataclass__validate_fields_types(self: SerializableDataclass, on_type_assert: OnTypeAssertDo = DEFAULT_ON_TYPE_ASSERT) -> bool:
    """validate the types of the fields on a SerializableDataclass"""

    # arg validation
    if on_type_assert not in ("raise", "warn", "ignore"):
        raise ValueError(
            f"Invalid value for {on_type_assert = }, expected 'raise', 'warn', or 'ignore'"
        )
    
    # do nothing if ignore
    if on_type_assert == "ignore":
        return
    
    # if except, bundle the exceptions
    results: dict[str, bool] = dict()
    exceptions: dict[str, Exception] = dict()
    
    # for each field in the class
    cls_fields: typing.Sequence[SerializableField] = dataclasses.fields(self)
    for field in cls_fields:
        try:
            assert self.validate_field_type(field, on_type_assert)
        except Exception as e:
            exceptions[field.name] = e

    # figure out what to do with the exceptions
    if len(exceptions) > 0:
        if on_type_assert in ("warn", "ignore"):
            msg: str = (
                f"Exceptions while validating types of fields on {self.__class__.__name__}: {[x.name for x in cls_fields]}"
                + f"\n\t" + "\n\t".join([f"{k}:\t{v}" for k, v in exceptions.items()])
            )
            if on_type_assert == "warn":
                warnings.warn(msg)
            else:
                raise ValueError(msg) from exceptions[0]
        else:
            assert on_type_assert == "ignore"
    
    return True

    


class SerializableDataclass(abc.ABC):
    """Base class for serializable dataclasses

    only for linting and type checking, still need to call `serializable_dataclass` decorator
    """

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError(f"decorate {self.__class__ = } with `@serializable_dataclass`")

    @classmethod
    def load(cls: Type[T], data: dict[str, Any] | T) -> T:
        raise NotImplementedError(f"decorate {cls = } with `@serializable_dataclass`")
    
    def validate_fields_types(self, on_type_assert: OnTypeAssertDo = DEFAULT_ON_TYPE_ASSERT) -> bool:
        return SerializableDataclass__validate_fields_types(self, on_type_assert)
    
    def validate_field_type(self, field: SerializableField|str, on_type_assert: OnTypeAssertDo = DEFAULT_ON_TYPE_ASSERT) -> bool:
        return SerializableDataclass__validate_field_type(self, field, on_type_assert)

    def __eq__(self, other: Any) -> bool:
        return dc_eq(self, other)

    def __hash__(self) -> int:
        return hash(json.dumps(self.serialize()))

    def diff(
        self, other: "SerializableDataclass", of_serialized: bool = False
    ) -> dict[str, Any]:
        if type(self) != type(other):
            raise ValueError(
                f"Instances must be of the same type, but got {type(self)} and {type(other)}"
            )

        diff_result: dict = {}

        if self == other:
            return diff_result

        if of_serialized:
            ser_self: dict = self.serialize()
            ser_other: dict = other.serialize()

        for field in dataclasses.fields(self):  # type: ignore[arg-type]
            if not field.compare:
                continue

            field_name: str = field.name
            self_value = getattr(self, field_name)
            other_value = getattr(other, field_name)

            if isinstance(self_value, SerializableDataclass) and isinstance(
                other_value, SerializableDataclass
            ):
                nested_diff: dict = self_value.diff(
                    other_value, of_serialized=of_serialized
                )
                if nested_diff:
                    diff_result[field_name] = nested_diff
            elif dataclasses.is_dataclass(self_value) and dataclasses.is_dataclass(
                other_value
            ):
                raise ValueError("Non-serializable dataclass is not supported")
            else:
                self_value_s = ser_self[field_name] if of_serialized else self_value
                other_value_s = ser_other[field_name] if of_serialized else other_value
                if not array_safe_eq(self_value_s, other_value_s):
                    diff_result[field_name] = {"self": self_value, "other": other_value}

        return diff_result

    def update_from_nested_dict(self, nested_dict: dict[str, Any]):
        for field in dataclasses.fields(self):  # type: ignore[arg-type]
            field_name: str = field.name
            self_value = getattr(self, field_name)

            if field_name in nested_dict:
                if isinstance(self_value, SerializableDataclass):
                    self_value.update_from_nested_dict(nested_dict[field_name])
                else:
                    setattr(self, field_name, nested_dict[field_name])

    def __copy__(self) -> "SerializableDataclass":
        return self.__class__.load(self.serialize())

    def __deepcopy__(self, memo: dict) -> "SerializableDataclass":
        return self.__class__.load(self.serialize())


class CantGetTypeHintsWarning(UserWarning):
    pass


# cache this so we don't have to keep getting it
@functools.lru_cache(typed=True)
def get_cls_type_hints(cls: Type[T]) -> dict[str, Any]:
    "cached typing.get_type_hints for a class"
    # get the type hints for the class
    cls_type_hints: dict[str, Any]
    try:
        cls_type_hints = typing.get_type_hints(cls)
    except TypeError as e:
        if sys.version_info < (3, 9):
            warnings.warn(
                f"Cannot get type hints for {cls.__name__}. Python version is {sys.version_info = }. You can:\n"
                + "  - use hints like `typing.Dict` instead of `dict` in type hints (this is required on python 3.8.x)\n"
                + "  - use python 3.9.x or higher\n"
                + "  - add explicit loading functions to the fields\n"
                + f"  {dataclasses.fields(cls) = }",
                CantGetTypeHintsWarning,
            )
            cls_type_hints = dict()
        else:
            raise TypeError(
                f"Cannot get type hints for {cls.__name__}. Python version is {sys.version_info = }\n"
                + f"  {dataclasses.fields(cls) = }\n"
                + f"   {e = }"
            ) from e
    
    return cls_type_hints


# Step 3: Create a custom serializable_dataclass decorator
def serializable_dataclass(
    # this should be `_cls: Type[T] | None = None,` but mypy doesn't like it
    _cls=None,  # type: ignore
    *,
    init: bool = True,
    repr: bool = True,  # this overrides the actual `repr` builtin, but we have to match the interface of `dataclasses.dataclass`
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    properties_to_serialize: Optional[list[str]] = None,
    register_handler: bool = True,
    on_type_assert: typing.Literal[
        "raise", "warn", "ignore"
    ] = "warn",  # TODO: change default to "raise" once more stable
    **kwargs,
):
    # -> Union[Callable[[Type[T]], Type[T]], Type[T]]:

    if properties_to_serialize is None:
        _properties_to_serialize: list = list()
    else:
        _properties_to_serialize = properties_to_serialize

    def wrap(cls: Type[T]) -> Type[T]:
        # Modify the __annotations__ dictionary to replace regular fields with SerializableField
        for field_name, field_type in cls.__annotations__.items():
            field_value = getattr(cls, field_name, None)
            if not isinstance(field_value, SerializableField):
                if isinstance(field_value, dataclasses.Field):
                    # Convert the field to a SerializableField while preserving properties
                    field_value = SerializableField.from_Field(field_value)
                else:
                    # Create a new SerializableField
                    field_value = serializable_field()
                setattr(cls, field_name, field_value)

        # special check, kw_only is not supported in python <3.9 and `dataclasses.MISSING` is truthy
        if sys.version_info < (3, 10):
            if "kw_only" in kwargs:
                if kwargs["kw_only"] == True:  # noqa: E712
                    raise ValueError("kw_only is not supported in python >=3.9")
                else:
                    del kwargs["kw_only"]

        cls = dataclasses.dataclass(  # type: ignore[call-overload]
            cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            **kwargs,
        )

        cls._properties_to_serialize = _properties_to_serialize.copy()  # type: ignore[attr-defined]

        def serialize(self) -> dict[str, Any]:
            result: dict[str, Any] = {
                "__format__": f"{self.__class__.__name__}(SerializableDataclass)"
            }
            # for each field in the class
            for field in dataclasses.fields(self):
                # need it to be our special SerializableField
                if not isinstance(field, SerializableField):
                    raise ValueError(
                        f"Field '{field.name}' on class {self.__class__.__module__}.{self.__class__.__name__} is not a SerializableField, "
                        f"but a {type(field)} "
                        "this state should be inaccessible, please report this bug!"
                    )

                # try to save it
                if field.serialize:
                    try:
                        # get the val
                        value = getattr(self, field.name)
                        # if it is a serializable dataclass, serialize it
                        if isinstance(value, SerializableDataclass):
                            value = value.serialize()
                        # if the value has a serialization function, use that
                        if hasattr(value, "serialize") and callable(value.serialize):
                            value = value.serialize()
                        # if the field has a serialization function, use that
                        # it would be nice to be able to override a class's `.serialize()`, but that could lead to some inconsistencies!
                        elif field.serialization_fn:
                            value = field.serialization_fn(value)

                        # store the value in the result
                        result[field.name] = value
                    except Exception as e:
                        raise ValueError(
                            "\n".join(
                                [
                                    f"Error serializing field '{field.name}' on class {self.__class__.__module__}.{self.__class__.__name__}",
                                    f"{field = }",
                                    f"{value = }",
                                    f"{self = }",
                                ]
                            )
                        ) from e

            # store each property if we can get it
            for prop in self._properties_to_serialize:
                if hasattr(cls, prop):
                    value = getattr(self, prop)
                    result[prop] = value
                else:
                    raise AttributeError(
                        f"Cannot serialize property '{prop}' on class {self.__class__.__module__}.{self.__class__.__name__}"
                        + f"but it is in {self._properties_to_serialize = }"
                        + f"\n{self = }"
                    )

            return result

        # mypy thinks this isnt a classmethod
        @classmethod  # type: ignore[misc]
        def load(cls, data: dict[str, Any] | T) -> Type[T]:
            # HACK: this is kind of ugly, but it fixes a lot of issues for when we do recursive loading with ZANJ
            if isinstance(data, cls):
                return data

            assert isinstance(
                data, typing.Mapping
            ), f"When loading {cls.__name__ = } expected a Mapping, but got {type(data) = }:\n{data = }"

            cls_type_hints: dict[str, Any] = get_cls_type_hints(cls)

            # initialize dict for keeping what we will pass to the constructor
            ctor_kwargs: dict[str, Any] = dict()

            # iterate over the fields of the class
            for field in dataclasses.fields(cls):
                # check if the field is a SerializableField
                assert isinstance(
                    field, SerializableField
                ), f"Field '{field.name}' on class {cls.__name__} is not a SerializableField, but a {type(field)}. this state should be inaccessible, please report this bug!\nhttps://github.com/mivanit/muutils/issues/new"

                # check if the field is in the data and if it should be initialized
                if (field.name in data) and field.init:
                    # get the value, we will be processing it
                    value: Any = data[field.name]

                    # get the type hint for the field
                    field_type_hint: Any = cls_type_hints.get(field.name, None)

                    if field.loading_fn:
                        # if it has a loading function, use that
                        value = field.loading_fn(data)
                    elif (
                        field_type_hint is not None
                        and hasattr(field_type_hint, "load")
                        and callable(field_type_hint.load)
                    ):
                        # if no loading function but has a type hint with a load method, use that
                        if isinstance(value, dict):
                            value = field_type_hint.load(value)
                        else:
                            raise ValueError(
                                f"Cannot load value into {field_type_hint}, expected {type(value) = } to be a dict\n{value = }"
                            )
                    else:
                        # assume no loading needs to happen, keep `value` as-is
                        pass

                    # store the value in the constructor kwargs
                    ctor_kwargs[field.name] = value

            # create a new instance of the class with the constructor kwargs
            output: cls = cls(**ctor_kwargs)

            # validate the types of the fields if needed
            if on_type_assert in ("raise", "warn"):
                output.validate_fields_types()

            # return the new instance
            return output

        # mypy says "Type cannot be declared in assignment to non-self attribute" so thats why I've left the hints in the comments
        # type is `Callable[[T], dict]`
        cls.serialize = serialize  # type: ignore[attr-defined]
        # type is `Callable[[dict], T]`
        cls.load = load  # type: ignore[attr-defined]
        # type is `Callable[[T, OnTypeAssertDo], bool]`
        cls.validate_fields_types = SerializableDataclass__validate_fields_types  # type: ignore[attr-defined]

        # type is `Callable[[T, T], bool]`
        cls.__eq__ = lambda self, other: dc_eq(self, other)  # type: ignore[assignment]

        # Register the class with ZANJ
        if register_handler:
            zanj_register_loader_serializable_dataclass(cls)

        return cls

    if _cls is None:
        return wrap
    else:
        return wrap(_cls)
