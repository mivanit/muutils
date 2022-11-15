import functools
import json
from pathlib import Path
from types import GenericAlias, UnionType
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union, Callable, Literal, Iterable
from dataclasses import dataclass, is_dataclass, asdict
from collections import namedtuple
import inspect
import typing
import warnings
from muutils.json_serialize.array import ArrayMode

from muutils.json_serialize.util import JSONitem, Hashableitem, MonoTuple, TypeErrorMode, UniversalContainer, isinstance_namedtuple, try_catch, ErrorMode
from muutils.json_serialize.json_serialize import JsonSerializer


# pylint: disable=pointless-string-statement, unreachable, import-outside-toplevel


def serialize_torch_module(
        obj: "torch.nn.Module", 
        *,
        member_typecasts: dict[str, Callable],
        array_mode: ArrayMode = "array_list_meta",
    ) -> JSONitem:
    """serialize an instance of `torch.nn.Module`
    
    you'll need to specify `member_typecasts`, which is a dict mapping
    member names to functions to call on the member value before serializing it

    the state dict will be saved separately under `state_dict`
    """
    # TODO: add paths to serializer
    raise NotImplementedError()
    return {
        "__format__": "torch_module",
        "name": obj.__class__.__name__,
        "state_dict": {
            k : serialize_array(v.cpu().numpy(), array_mode=array_mode)
            for k, v in obj.state_dict().items()
        },
        "members_dict": {
            k : (
                json_serialize(v)
                if k not in member_typecasts
                else json_serialize(member_typecasts[k](v))
            )
            for k, v in obj.__dict__.items()
            if not k.startswith("_")
        },
    }

def load_torch_module_factory(
        cls, 
        *,
        members_exclude: list[str],
        typecasts: dict[str, Callable],
    ) -> Callable[[Any, JSONitem], "torch.nn.Module"]:
    """create a function which allows for loading a torch module from `JSONitem`

    - everything from the `members_dict` not in `members_exclude` will be passed to the `__init__` method of the module
    - everything from the `state_dict` will be passed to the `load_state_dict` method of the module
    """
    raise NotImplementedError()

    import torch

    @classmethod
    def load(cls, item: JSONitem) -> "torch.nn.Module":
        assert item["__format__"] == "torch_module"
        assert item["name"] == cls.__name__

        module_obj = cls(
            **{
                k: (
                    v 
                    if k not in typecasts 
                    else typecasts[k](v)
                )
                for k, v in item["members_dict"].items()
                if k not in members_exclude
            }
        )
        module_obj.load_state_dict(
            {
                k: torch.from_numpy(load_array(v))
                for k, v in item["state_dict"].items()
            },
        )
        return module_obj

    return load



def dataclass_serializer_factory(
        cls, 
        special_serializers: Optional[dict[str, Callable]] = None,
        fields_exclude: Optional[Iterable[str]] = None,
    ) -> Callable[[Any], JSONitem]:
    """outputs a `.serialize` method for a dataclass,
    where fields present in `special_serializers` are serialized using the corresponding function.

    each function in `special_serializers` should take the class itself as an argument, and return a JSONitem.
    """
    # make it an empty dict if not provided
    if special_serializers is None:
        special_serializers = dict()

    if fields_exclude is None:
        fields_exclude = list()

    sfuncs_simple: dict[str, Callable] = dict() # TODO: deprecate simple serializers? check if they output a nested structure or simple type? idk
    sfuncs_full: dict[str, Callable] = dict()

    # augment special serializers if they are missing `jser` and `path` arguments
    spec_ser: Callable
    for key, spec_ser in special_serializers.items():
        args: list[str] = inspect.getfullargspec(spec_ser).args
        if len(args) == 1:
            sfuncs_simple[key] = spec_ser
        elif len(args) == 3:
            sfuncs_full[key] = spec_ser
        else:
            raise ValueError(f"special serializer function `{spec_ser}` has {len(args)} arguments {args = }, but should have 1 or 3")

    def serialize(self, jser: JsonSerializer, path: tuple[str|int] = tuple()) -> JSONitem:
        # get the base outputs for all keys in the dataclass but which dont have a special serializer
        base_output: dict[str, JSONitem] = {
            k: (
                jser.json_serialize(getattr(self, k), path=path + (k,))
            )
            for k in self.__dataclass_fields__
            if (
                (k not in sfuncs_simple) 
                and (k not in sfuncs_full)
                and (k not in fields_exclude)
            )
        }

        # update with the special serializers
        for k in sfuncs_simple:
            if k not in fields_exclude:
                base_output[k] = sfuncs_simple[k](self)
        for k in sfuncs_full:
            if k not in fields_exclude:
                base_output[k] = sfuncs_full[k](self, jser = jser, path = path)

    return serialize




def loader_typecheck_factory(
        key: str,
        expected_type: type, 
        error_mode: TypeErrorMode = "except",
    ) -> Callable[[JSONitem], Any]:
    """outputs a loader function, which checks the type of the argument
    
    if the argument `data` to the loader is not of the expected type:
    - if `error_mode == "except"`, raises a TypeError 
    - if `error_mode == "try_convert"` return `expected_type(data)`. this might raise further exceptions
    - if `error_mode == "warn"`, print a warning and return `data`
    - if `error_mode == "ignore"`, return `data`

    TODO: perhaps an option to warn, but try to convert?
    """

    origin_type: type = typing.get_origin(expected_type)
    if origin_type is None:
        # set it back if `get_origin()` returns `None`
        origin_type = expected_type

    type_args: tuple[type, ...] = typing.get_args(expected_type)
    return_raw: bool = False

    try:
        if origin_type in (Union, types.UnionType, Optional):
            # TODO: this is incomplete
            pass
        elif isinstance(None, origin_type):
            pass
    except TypeError as e:
        warnings.warn(f"error processing {origin_type = } for {key = }, loader will return raw data\n\t{e}")
        return_raw = True

    def loader(data: JSONitem) -> Any:
        if key not in data:
            raise KeyError(f"while executing `.load(data)`, key {key} not found in data: {data = }")

        if return_raw:
            return data[key]

        # TODO: make unions work correctly
        if (
                (origin_type is Union) 
                or (origin_type is types.UnionType)
                or isinstance(data[key], origin_type)
            ):
                return data[key]
        else:
            if error_mode == "warn":
                warnings.warn(f"error loading, will return raw data")
                return data[key]
            elif error_mode == "except":
                raise TypeError(f"expected {origin_type} for {key = }, got {type(data)}\n\t{data = }")
            elif error_mode == "try_convert":
                return origin_type(data)
            elif error_mode == "ignore":
                return data[key]
            else:
                raise ValueError(f"error mode {error_mode} not recognized")

    return loader


def dataclass_loader_factory(
        cls,
        special_loaders: Optional[dict[str, Callable[[JSONitem], Any]]] = None,
        loader_types_override: Optional[dict[str, type]] = None,
        # key_error_mode: ErrorMode = "except",
        type_error_mode: TypeErrorMode = "except",
    ) -> Callable[[JSONitem], Any]:
    """returns a `.load()` method for a dataclass, recursively calling loader functions if found
    
    where arguments present in `special_loaders` are loaded using the corresponding function
    functions in `special_loaders` should take a JSONitem (the whole dataset) and return an item
    

    `type_error_mode` determines how to handle the JSON item type not matching the type hint of the dataclass field.

    ```
    (not working) 
    `key_error_mode` determines how to handle not being able to find the key in the JSONitem.
    for "warn" or "ignore", a `None` value is given to the key, unless a default exists~
    ```
    """

    # make it an empty dict if not provided
    if special_loaders is None:
        special_loaders = dict()
    
    if loader_types_override is None:
        loader_types_override = dict()

    # check all loaders make sense
    for key in special_loaders:
        if key not in cls.__dataclass_fields__:
            raise ValueError(f"{key} is not a field of {cls}")

    # assemble actual loaders
    type_hints: dict[str, Any] = typing.get_type_hints(cls)

    loader_funcs: dict[str, Callable[[JSONitem], Any]] = dict()

    for k in cls.__dataclass_fields__:
        # first, use the special loader
        if k in special_loaders:
            loader_funcs[k] = special_loaders[k]

        # get the type hint for the field
        elif k in type_hints:
            # if it is a class with a `.load()` method, use that
            if isinstance(type_hints[k], type) and hasattr(type_hints[k], "load"):
                k_loader: Callable = lambda data: type_hints[k].load(data[k])
                # check the `load()` has the correct signature
                k_loader_signature: inspect.Signature = inspect.signature(k_loader)
                if len([
                    True
                    for p_name, p_cls in k_loader_signature.parameters.items()
                    if p_cls.default == inspect._empty
                ]) != 1:
                    raise TypeError(f"`.load()` method for {k} has incorrect signature, expected exactly 1 argument without a default value:\n\t{k = }\n\t{k_loader = }\n\t{k_loader_signature = }\n\t{k_loader_signature.parameters = }")

                # set the load function if everything works
                loader_funcs[k] = k_loader
            else:
                # attempt to create a loader function for the type hint
                typehint_k = type_hints[k]
                if k in loader_types_override:
                    typehint_k = loader_types_override[k]
                loader_funcs[k] = loader_typecheck_factory(
                    key=k,
                    expected_type=typehint_k,
                    error_mode=type_error_mode,
                )

        # otherwise, use the identity function
        else:
            # note here that we cant just use k because it's defined in the loop
            loader_funcs[k] = lambda data, _k=k: data[_k]

    def load(data: JSONitem):
        # get the base outputs for all keys in the dataclass but which dont have a special loader
        output: dict[str, Any] = dict()

        # if an element is missing from data, then dont pass it and the error will be handled by the class
        for k in data:
            if k in loader_funcs:
                output[k] = loader_funcs[k](data)

        loaded = cls(**output)

        if not isinstance(loaded, cls):
            raise TypeError(f"expected {cls}, got {type(loaded)}")

        return loaded

    return load




def augement_dataclass_serializer_loader(
        cls: Any = None,
        /, *,
        special_serializers: Optional[dict[str, Callable]] = None,
        special_loaders: Optional[dict[str, Callable[[JSONitem], Any]]] = None,
        load_type_error_mode: TypeErrorMode = "except",
    ) -> Any:
    """adds a `.serialize()` and `.load()` method to a dataclass,
    using `dataclass_serializer_factory` and `dataclass_loader_factory`

    TODO: dynamically added methods dont show up as attributes during linting, and this makes the decorator suck.
    """

    def wrap(cls):
        cls.serialize = dataclass_serializer_factory(
            cls,
            special_serializers=special_serializers,
        )
        cls.load = dataclass_loader_factory(
            cls,
            special_loaders=special_loaders,
            type_error_mode=load_type_error_mode,
        )

        return cls

    # See if we're being called as `@augement_dataclass_serializer_loader` 
    # or `@augement_dataclass_serializer_loader()`.
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as `@augement_dataclass_serializer_loader` without parens.
    return wrap(cls)
