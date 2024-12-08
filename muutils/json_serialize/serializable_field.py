"""extends `dataclasses.Field` for use with `SerializableDataclass`

In particular, instead of using `dataclasses.field`, use `serializable_field` to define fields in a `SerializableDataclass`.
You provide information on how the field should be serialized and loaded (as well as anything that goes into `dataclasses.field`)
when you define the field, and the `SerializableDataclass` will automatically use those functions.

"""

from __future__ import annotations

import dataclasses
import sys
import types
from typing import Any, Callable, Optional, Union, overload, TypeVar


# pylint: disable=bad-mcs-classmethod-argument, too-many-arguments, protected-access


class SerializableField(dataclasses.Field):
    """extension of `dataclasses.Field` with additional serialization properties"""

    __slots__ = (
        # from dataclasses.Field.__slots__
        "name",
        "type",
        "default",
        "default_factory",
        "repr",
        "hash",
        "init",
        "compare",
        "metadata",
        "kw_only",
        "_field_type",  # Private: not to be used by user code.
        # new ones
        "serialize",
        "serialization_fn",
        "loading_fn",
        "deserialize_fn",  # new alternative to loading_fn
        "assert_type",
        "custom_typecheck_fn",
    )

    def __init__(
        self,
        default: Union[Any, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
        default_factory: Union[
            Callable[[], Any], dataclasses._MISSING_TYPE
        ] = dataclasses.MISSING,
        init: bool = True,
        repr: bool = True,
        hash: Optional[bool] = None,
        compare: bool = True,
        # TODO: add field for custom comparator (such as serializing)
        metadata: Optional[types.MappingProxyType] = None,
        kw_only: Union[bool, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
        serialize: bool = True,
        serialization_fn: Optional[Callable[[Any], Any]] = None,
        loading_fn: Optional[Callable[[Any], Any]] = None,
        deserialize_fn: Optional[Callable[[Any], Any]] = None,
        assert_type: bool = True,
        custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    ):
        # TODO: should we do this check, or assume the user knows what they are doing?
        if init and not serialize:
            raise ValueError("Cannot have init=True and serialize=False")

        # need to assemble kwargs in this hacky way so as not to upset type checking
        super_kwargs: dict[str, Any] = dict(
            default=default,
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            kw_only=kw_only,
        )

        if metadata is not None:
            super_kwargs["metadata"] = metadata
        else:
            super_kwargs["metadata"] = types.MappingProxyType({})

        # special check, kw_only is not supported in python <3.9 and `dataclasses.MISSING` is truthy
        if sys.version_info < (3, 10):
            if super_kwargs["kw_only"] == True:  # noqa: E712
                raise ValueError("kw_only is not supported in python >=3.9")
            else:
                del super_kwargs["kw_only"]

        # actually init the super class
        super().__init__(**super_kwargs)  # type: ignore[call-arg]

        # now init the new fields
        self.serialize: bool = serialize
        self.serialization_fn: Optional[Callable[[Any], Any]] = serialization_fn

        if loading_fn is not None and deserialize_fn is not None:
            raise ValueError(
                "Cannot pass both loading_fn and deserialize_fn, pass only one. ",
                "`loading_fn` is the older interface and takes the dict of the class, ",
                "`deserialize_fn` is the new interface and takes only the field's value.",
            )
        self.loading_fn: Optional[Callable[[Any], Any]] = loading_fn
        self.deserialize_fn: Optional[Callable[[Any], Any]] = deserialize_fn

        self.assert_type: bool = assert_type
        self.custom_typecheck_fn: Optional[Callable[[type], bool]] = custom_typecheck_fn

    @classmethod
    def from_Field(cls, field: dataclasses.Field) -> "SerializableField":
        """copy all values from a `dataclasses.Field` to new `SerializableField`"""
        return cls(
            default=field.default,
            default_factory=field.default_factory,
            init=field.init,
            repr=field.repr,
            hash=field.hash,
            compare=field.compare,
            metadata=field.metadata,
            kw_only=getattr(field, "kw_only", dataclasses.MISSING),  # for python <3.9
            serialize=field.repr,  # serialize if it's going to be repr'd
            serialization_fn=None,
            loading_fn=None,
            deserialize_fn=None,
        )


Sfield_T = TypeVar("Sfield_T")


@overload
def serializable_field(
    *_args,
    default_factory: Callable[[], Sfield_T],
    default: dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[types.MappingProxyType] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    **kwargs: Any,
) -> Sfield_T: ...
@overload
def serializable_field(
    *_args,
    default: Sfield_T,
    default_factory: dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[types.MappingProxyType] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    **kwargs: Any,
) -> Sfield_T: ...
@overload
def serializable_field(
    *_args,
    default: dataclasses._MISSING_TYPE = dataclasses.MISSING,
    default_factory: dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[types.MappingProxyType] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    **kwargs: Any,
) -> Any: ...
def serializable_field(
    *_args,
    default: Union[Any, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
    default_factory: Union[Any, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[types.MappingProxyType] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    **kwargs: Any,
) -> Any:
    """Create a new `SerializableField`

    ```
    default: Sfield_T | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    default_factory: Callable[[], Sfield_T]
    | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: types.MappingProxyType | None = None,
    kw_only: bool | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    # ----------------------------------------------------------------------
    # new in `SerializableField`, not in `dataclasses.Field`
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    loading_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    ```

    # new Parameters:
    - `serialize`: whether to serialize this field when serializing the class'
    - `serialization_fn`: function taking the instance of the field and returning a serializable object. If not provided, will iterate through the `SerializerHandler`s defined in `muutils.json_serialize.json_serialize`
    - `loading_fn`: function taking the serialized object and returning the instance of the field. If not provided, will take object as-is.
    - `deserialize_fn`: new alternative to `loading_fn`. takes only the field's value, not the whole class. if both `loading_fn` and `deserialize_fn` are provided, an error will be raised.
    - `assert_type`: whether to assert the type of the field when loading. if `False`, will not check the type of the field.
    - `custom_typecheck_fn`: function taking the type of the field and returning whether the type itself is valid. if not provided, will use the default type checking.

    # Gotchas:
    - `loading_fn` takes the dict of the **class**, not the field. if you wanted a `loading_fn` that does nothing, you'd write:

    ```python
    class MyClass:
        my_field: int = serializable_field(
            serialization_fn=lambda x: str(x),
            loading_fn=lambda x["my_field"]: int(x)
        )
    ```

    using `deserialize_fn` instead:

    ```python
    class MyClass:
        my_field: int = serializable_field(
            serialization_fn=lambda x: str(x),
            deserialize_fn=lambda x: int(x)
        )
    ```

    In the above code, `my_field` is an int but will be serialized as a string.

    note that if not using ZANJ, and you have a class inside a container, you MUST provide
    `serialization_fn` and `loading_fn` to serialize and load the container.
    ZANJ will automatically do this for you.

    # TODO: `custom_value_check_fn`: function taking the value of the field and returning whether the value itself is valid. if not provided, any value is valid as long as it passes the type test
    """
    assert len(_args) == 0, f"unexpected positional arguments: {_args}"
    return SerializableField(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
        serialize=serialize,
        serialization_fn=serialization_fn,
        deserialize_fn=deserialize_fn,
        assert_type=assert_type,
        custom_typecheck_fn=custom_typecheck_fn,
        **kwargs,
    )
