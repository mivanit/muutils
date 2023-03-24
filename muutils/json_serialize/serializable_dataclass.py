import abc
import dataclasses
import types
import typing
from typing import Any, Callable, Optional, Type, TypeVar

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
            kw_only=field.kw_only,
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


# credit to https://stackoverflow.com/questions/51743827/how-to-compare-equality-of-dataclasses-holding-numpy-ndarray-boola-b-raises
def array_safe_eq(a: Any, b: Any) -> bool:
    """check if two objects are equal, account for if numpy arrays or torch tensors"""
    if a is b:
        return True

    if (
        str(type(a)) == "<class 'numpy.ndarray'>"
        and str(type(b)) == "<class 'numpy.ndarray'>"
    ) or (
        str(type(a)) == "<class 'torch.Tensor'>"
        and str(type(b)) == "<class 'torch.Tensor'>"
    ):
        return (a == b).all()

    if (
        str(type(a)) == "<class 'pandas.core.frame.DataFrame'>"
        and str(type(b)) == "<class 'pandas.core.frame.DataFrame'>"
    ):
        return a.equals(b)

    if isinstance(a, typing.Sequence) and isinstance(b, typing.Sequence):
        return len(a) == len(b) and all(array_safe_eq(a1, b1) for a1, b1 in zip(a, b))

    if isinstance(a, (dict, typing.Mapping)) and isinstance(b, (dict, typing.Mapping)):
        return (
            len(a) == len(b)
            and all(k1 == k2 for k1, k2 in zip(a.keys(), b.keys()))
            and all(array_safe_eq(a[k], b[k]) for k in a.keys())
        )

    try:
        return a == b
    except TypeError:
        return NotImplementedError  # type: ignore[return-value]


def dc_eq(dc1, dc2) -> bool:
    """checks if two dataclasses which hold numpy arrays are equal"""
    if dc1 is dc2:
        return True

    if dc1.__class__ is not dc2.__class__:
        return NotImplementedError  # type: ignore[return-value]

    return all(
        array_safe_eq(getattr(dc1, fld.name), getattr(dc2, fld.name))
        for fld in dataclasses.fields(dc1)
        if fld.compare
    )


T = TypeVar("T")


class SerializableDataclass(abc.ABC):
    """Base class for serializable dataclasses

    only for linting and type checking, still need to call `serializable_dataclass` decorator
    """

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def load(cls: Type[T], data: dict[str, Any] | T) -> T:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        return dc_eq(self, other)


def zanj_register_loader_serializable_dataclass(cls: Type[T]) -> Type[T]:
    """Register a serializable dataclass with the ZANJ backport"""

    from muutils.zanj.loading import create_and_register_loader_handler

    _format: str = f"{cls.__name__}(SerializableDataclass)"
    create_and_register_loader_handler(
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
    return cls


# Step 3: Create a custom serializable_dataclass decorator
def serializable_dataclass(
    # this should be `_cls: Type[T] | None = None,` but mypy doesn't like it
    _cls=None,  # type: ignore
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    properties_to_serialize: Optional[list[str]] = None,
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

            for field in dataclasses.fields(self):
                if not isinstance(field, SerializableField):
                    raise ValueError(
                        f"Field '{field.name}' on class {self.__class__.__module__}.{self.__class__.__name__} is not a SerializableField, "
                        f"but a {type(field)} "
                        "this state should be inaccessible, please report this bug!"
                    )

                if field.serialize:
                    value = getattr(self, field.name)
                    if isinstance(value, SerializableDataclass):
                        value = value.serialize()
                    elif field.serialization_fn:
                        value = field.serialization_fn(value)
                    result[field.name] = value

            for prop in self._properties_to_serialize:
                if hasattr(cls, prop) and isinstance(getattr(cls, prop), property):
                    value = getattr(self, prop)
                    result[prop] = value

            return result

        # mypy thinks this isnt a classmethod
        @classmethod  # type: ignore[misc]
        def load(cls, data: dict[str, Any] | T) -> Type[T]:
            # TODO: this is kind of ugly, but it fixes a lot of issues for when we do recursive loading with ZANJ
            if isinstance(data, cls):
                return data

            assert isinstance(
                data, typing.Mapping
            ), f"Expected {data} to be a Mapping, but it is a {type(data)}"

            ctor_kwargs: dict[str, Any] = dict()
            for field in dataclasses.fields(cls):
                assert isinstance(
                    field, SerializableField
                ), f"Field '{field.name}' on class {cls.__name__} is not a SerializableField, but a {type(field)} this state should be inaccessible, please report this bug!"

                if (field.name in data) and field.init:
                    value = data[field.name]

                    print(f"{field.type = } {type(field.type) = }")
                    if (
                        # mypy thinks typing has no attribute `GenericAlias``
                        not isinstance(field.type, (typing.GenericAlias, typing._SpecialForm))  # type: ignore[attr-defined]
                        and issubclass(field.type, SerializableDataclass)
                    ):
                        if isinstance(value, dict):
                            value = field.type.load(value)
                        else:
                            raise ValueError(
                                f"Cannot load value into {field.type}, espected {type(value) = } to be a dict\n{value = }"
                            )
                    elif field.loading_fn:
                        value = field.loading_fn(data)

                    if field.assert_type:
                        # TODO: make this work
                        # assert isinstance(ctor_kwargs[field.name], field.type)
                        pass

                    ctor_kwargs[field.name] = value
            return cls(**ctor_kwargs)

        # mypy says "Type cannot be declared in assignment to non-self attribute" so thats why I've left the hints in the comments
        # type is `Callable[[T], dict]`
        cls.serialize = serialize  # type: ignore[attr-defined]
        # type is `Callable[[dict], T]`
        cls.load = load  # type: ignore[attr-defined]

        cls.__eq__ = lambda self, other: dc_eq(self, other)  # type: ignore[assignment]

        # Register the class with the ZANJ backport
        zanj_register_loader_serializable_dataclass(cls)

        return cls

    if _cls is None:
        return wrap
    else:
        return wrap(_cls)
