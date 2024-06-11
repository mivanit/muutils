import abc
import dataclasses
import json
import types
import typing
import warnings
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
        default_factory: (
            Callable[[], Any] | dataclasses._MISSING_TYPE
        ) = dataclasses.MISSING,
        init: bool = True,
        repr: bool = True,
        hash: Optional[bool] = None,
        compare: bool = True,
        # TODO: add field for custom comparator (such as serializing)
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
        return len(a) == len(b) and all(
            array_safe_eq(k1, k2) and array_safe_eq(a[k1], b[k2])
            for k1, k2 in zip(a.keys(), b.keys())
        )

    try:
        return bool(a == b)
    except (TypeError, ValueError) as e:
        warnings.warn(f"Cannot compare {a} and {b} for equality\n{e}")
        return NotImplemented  # type: ignore[return-value]


def dc_eq(
    dc1,
    dc2,
    except_when_class_mismatch: bool = False,
    false_when_class_mismatch: bool = True,
    except_when_field_mismatch: bool = False,
) -> bool:
    """checks if two dataclasses which (might) hold numpy arrays are equal

        # Parameters:
        - `dc1`: the first dataclass
        - `dc2`: the second dataclass
        - `except_when_class_mismatch: bool`
            if `True`, will throw `TypeError` if the classes are different.
            if not, will return false by default or attempt to compare the fields if `false_when_class_mismatch` is `False`
            (default: `False`)
        - `false_when_class_mismatch: bool`
            only relevant if `except_when_class_mismatch` is `False`.
            if `True`, will return `False` if the classes are different.
            if `False`, will attempt to compare the fields.
        - `except_when_field_mismatch: bool`
            only relevant if `except_when_class_mismatch` is `False` and `false_when_class_mismatch` is `False`.
            if `True`, will throw `TypeError` if the fields are different.
            (default: `True`)

        # Returns:
        - `bool`: True if the dataclasses are equal, False otherwise

        # Raises:
        - `TypeError`: if the dataclasses are of different classes
        - `AttributeError`: if the dataclasses have different fields

    ```
              [START]
                 ▼
           ┌───────────┐  ┌─────────┐
           │dc1 is dc2?├─►│ classes │
           └──┬────────┘No│ match?  │
      ────    │           ├─────────┤
     (True)◄──┘Yes        │No       │Yes
      ────                ▼         ▼
          ┌────────────────┐ ┌────────────┐
          │ except when    │ │ fields keys│
          │ class mismatch?│ │ match?     │
          ├───────────┬────┘ ├───────┬────┘
          │Yes        │No    │No     │Yes
          ▼           ▼      ▼       ▼
     ───────────  ┌──────────┐  ┌────────┐
    { raise     } │ except   │  │ field  │
    { TypeError } │ when     │  │ values │
     ───────────  │ field    │  │ match? │
                  │ mismatch?│  ├────┬───┘
                  ├───────┬──┘  │    │Yes
                  │Yes    │No   │No  ▼
                  ▼       ▼     │   ────
     ───────────────     ─────  │  (True)
    { raise         }   (False)◄┘   ────
    { AttributeError}    ─────
     ───────────────
    ```

    """
    if dc1 is dc2:
        return True

    if dc1.__class__ is not dc2.__class__:
        if except_when_class_mismatch:
            # if the classes don't match, raise an error
            raise TypeError(
                f"Cannot compare dataclasses of different classes: `{dc1.__class__}` and `{dc2.__class__}`"
            )
        else:
            dc1_fields: set = set([fld.name for fld in dataclasses.fields(dc1)])
            dc2_fields: set = set([fld.name for fld in dataclasses.fields(dc2)])
            fields_match: bool = set(dc1_fields) == set(dc2_fields)

            if not fields_match:
                # if the fields match, keep going
                if except_when_field_mismatch:
                    raise AttributeError(
                        f"dataclasses {dc1} and {dc2} have different fields: `{dc1_fields}` and `{dc2_fields}`"
                    )
                else:
                    return False

    return all(
        array_safe_eq(getattr(dc1, fld.name), getattr(dc2, fld.name))
        for fld in dataclasses.fields(dc1)
        if fld.compare
    )


T = TypeVar("T")


class ZanjMissingWarning(UserWarning):
    pass


_zanj_loading_needs_import: bool = True


def zanj_register_loader_serializable_dataclass(cls: Type[T]):
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
    register_handler: bool = True,
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
                    try:
                        value = getattr(self, field.name)
                        if isinstance(value, SerializableDataclass):
                            value = value.serialize()
                        if hasattr(value, "serialize") and callable(value.serialize):
                            value = value.serialize()
                        elif field.serialization_fn:
                            value = field.serialization_fn(value)
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

            for prop in self._properties_to_serialize:
                if hasattr(cls, prop):
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
            ), f"When loading {cls.__name__ = } expected a Mapping, but got {type(data) = }:\n{data = }"

            cls_type_hints: dict[str, Any] = typing.get_type_hints(cls)
            ctor_kwargs: dict[str, Any] = dict()
            for field in dataclasses.fields(cls):
                assert isinstance(
                    field, SerializableField
                ), f"Field '{field.name}' on class {cls.__name__} is not a SerializableField, but a {type(field)} this state should be inaccessible, please report this bug!"

                if (field.name in data) and field.init:
                    value = data[field.name]

                    field_type_hint: Any = cls_type_hints.get(field.name, None)
                    if field.loading_fn:
                        value = field.loading_fn(data)
                    elif (
                        field_type_hint is not None
                        and hasattr(field_type_hint, "load")
                        and callable(field_type_hint.load)
                    ):
                        if isinstance(value, dict):
                            value = field_type_hint.load(value)
                        else:
                            raise ValueError(
                                f"Cannot load value into {field_type_hint}, expected {type(value) = } to be a dict\n{value = }"
                            )

                    if field.assert_type:
                        if field.name in ctor_kwargs:
                            assert isinstance(ctor_kwargs[field.name], field_type_hint)

                    ctor_kwargs[field.name] = value
            return cls(**ctor_kwargs)

        # mypy says "Type cannot be declared in assignment to non-self attribute" so thats why I've left the hints in the comments
        # type is `Callable[[T], dict]`
        cls.serialize = serialize  # type: ignore[attr-defined]
        # type is `Callable[[dict], T]`
        cls.load = load  # type: ignore[attr-defined]

        cls.__eq__ = lambda self, other: dc_eq(self, other)  # type: ignore[assignment]

        # Register the class with ZANJ
        if register_handler:
            zanj_register_loader_serializable_dataclass(cls)

        return cls

    if _cls is None:
        return wrap
    else:
        return wrap(_cls)
