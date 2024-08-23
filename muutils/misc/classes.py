from __future__ import annotations

from typing import (
    Iterable,
    Any,
    Protocol,
    ClassVar,
    runtime_checkable,
)

from muutils.misc.sequence import flatten


def is_abstract(cls: type) -> bool:
    """
    Returns if a class is abstract.
    """
    if not hasattr(cls, "__abstractmethods__"):
        return False  # an ordinary class
    elif len(cls.__abstractmethods__) == 0:
        return False  # a concrete implementation of an abstract class
    else:
        return True  # an abstract class


def get_all_subclasses(class_: type, include_self=False) -> set[type]:
    """
    Returns a set containing all child classes in the subclass graph of `class_`.
    I.e., includes subclasses of subclasses, etc.

    # Parameters
    - `include_self`: Whether to include `class_` itself in the returned set
    - `class_`: Superclass

    # Development
    Since most class hierarchies are small, the inefficiencies of the existing recursive implementation aren't problematic.
    It might be valuable to refactor with memoization if the need arises to use this function on a very large class hierarchy.
    """
    subs: set[type] = set(
        flatten(
            get_all_subclasses(sub, include_self=True)
            for sub in class_.__subclasses__()
            if sub is not None
        )
    )
    if include_self:
        subs.add(class_)
    return subs


def isinstance_by_type_name(o: object, type_name: str):
    """Behaves like stdlib `isinstance` except it accepts a string representation of the type rather than the type itself.
    This is a hacky function intended to circumvent the need to import a type into a module.
    It is susceptible to type name collisions.

    # Parameters
    `o`: Object (not the type itself) whose type to interrogate
    `type_name`: The string returned by `type_.__name__`.
    Generic types are not supported, only types that would appear in `type_.__mro__`.
    """
    return type_name in {s.__name__ for s in type(o).__mro__}


# dataclass magic
# --------------------------------------------------------------------------------


@runtime_checkable
class IsDataclass(Protocol):
    # Generic type for any dataclass instance
    # https://stackoverflow.com/questions/54668000/type-hint-for-an-instance-of-a-non-specific-dataclass
    __dataclass_fields__: ClassVar[dict[str, Any]]


def get_hashable_eq_attrs(dc: IsDataclass) -> tuple[Any]:
    """Returns a tuple of all fields used for equality comparison, including the type of the dataclass itself.
    The type is included to preserve the unequal equality behavior of instances of different dataclasses whose fields are identical.
    Essentially used to generate a hashable dataclass representation for equality comparison even if it's not frozen.
    """
    return *(
        getattr(dc, fld.name)
        for fld in filter(lambda x: x.compare, dc.__dataclass_fields__.values())
    ), type(dc)


def dataclass_set_equals(
    coll1: Iterable[IsDataclass], coll2: Iterable[IsDataclass]
) -> bool:
    """Compares 2 collections of dataclass instances as if they were sets.
    Duplicates are ignored in the same manner as a set.
    Unfrozen dataclasses can't be placed in sets since they're not hashable.
    Collections of them may be compared using this function.
    """

    return {get_hashable_eq_attrs(x) for x in coll1} == {
        get_hashable_eq_attrs(y) for y in coll2
    }
