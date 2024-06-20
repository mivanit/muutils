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
        "assert_type",
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
        assert_type: bool = True,
        # TODO: add field for custom type assertion
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
        self.loading_fn: Optional[Callable[[Any], Any]] = loading_fn
        self.assert_type: bool = assert_type

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
            serialize=field.repr,
            serialization_fn=None,
            loading_fn=None,
        )


# Step 2: Create a serializable_field function
# no type hint to avoid confusing mypy
def serializable_field(*args, **kwargs):  # -> SerializableField:
    """Create a new SerializableField

    note that if not using ZANJ, and you have a class inside a container, you MUST provide
    `serialization_fn` and `loading_fn` to serialize and load the container.
    ZANJ will automatically do this for you.

    ```
    default: Any | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    default_factory: Callable[[], Any]
    | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: types.MappingProxyType | None = None,
    kw_only: bool | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    loading_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    ```
    """
    return SerializableField(*args, **kwargs)