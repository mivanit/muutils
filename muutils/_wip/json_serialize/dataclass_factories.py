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

from muutils._wip.json_serialize.util import JSONitem, Hashableitem, MonoTuple, UniversalContainer, isinstance_namedtuple, try_catch, ErrorMode
from muutils._wip.json_serialize.json_serialize import JsonSerializer


# pylint: disable=pointless-string-statement, unreachable, import-outside-toplevel


def serialize_torch_module(
        obj: "torch.nn.Module", 
        *,
        member_typecasts: Dict[str, Callable],
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
        members_exclude: List[str],
        typecasts: Dict[str, Callable],
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

    special_serializers_1arg: dict[str, Callable] = dict()
    special_serializers_3arg: dict[str, Callable] = dict()
    # TODO: deprecate this??

    # augment special serializers if they are missing `jser` and `path` arguments
    spec_ser: Callable
    for key, spec_ser in special_serializers.items():
        args: list[str] = inspect.getfullargspec(spec_ser).args
        if len(args) == 1:
            # if there is only one argument, it is the class itself
            # so we can just add the `jser` and `path` arguments
            # special_serializers_processed[key] = lambda cls, jser=None, path=None: spec_ser(cls)
            # this doesnt work since spec_ser is defined in the loop, so access via key
            # special_serializers_processed[key] = lambda self, jser=None, path=None: special_serializers[key](self)
            raise NotImplementedError()

        else:
            # here, we assume the args are (self, jser, path)
            assert len(args) == 3, f"special serializer for field {key} should have 1 or 3 arguments"
            special_serializers_processed[key] = 

    def serialize(self, jser: JsonSerializer, path: tuple[str|int] = tuple()) -> JSONitem:
        # get the base outputs for all keys in the dataclass but which dont have a special serializer
        base_output: dict[str, JSONitem] = {
            k: (
                jser.json_serialize(getattr(self, k), path=path + (k,))
            )
            for k in self.__dataclass_fields__
            if (
                (k not in special_serializers_processed)
                and (k not in fields_exclude)
            )
        }

        # update with the special serializers
        for k in special_serializers_processed:
            if k not in fields_exclude:
                base_output[k] = special_serializers_processed[k](self, jser, path=path + (k,))

    return serialize

TypeErrorMode = Union[ErrorMode, Literal["try_convert"]]


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

    type_args: Tuple[type, ...] = typing.get_args(expected_type)
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

def _test():

    # @augement_dataclass_serializer_loader(
    #     special_serializers=dict(rand_data=lambda self: str(self.rand_data)),
    # )
    @dataclass
    class TestClass:
        a: int
        b: str
        c: float
        rand_data: Any = None
    
    TestClass.serialize = dataclass_serializer_factory(
        TestClass,
        special_serializers=dict(rand_data=lambda self: str(self.rand_data)),
    )
    TestClass.load = dataclass_loader_factory(TestClass)
    
    # @augement_dataclass_serializer_loader
    @dataclass
    class OuterTestClass:
        a2: int
        b2: str
        c2: float
        d2: TestClass

    OuterTestClass.serialize = dataclass_serializer_factory(OuterTestClass)
    OuterTestClass.load = dataclass_loader_factory(OuterTestClass)

    item_a: TestClass = TestClass(a=1, b="x", c=3.0)
    item_b: OuterTestClass = OuterTestClass(a2=2, b2="y", c2=4.0, d2=item_a)

    print(f"{item_a = }")
    print(f"{item_a.serialize() = }")
    print(f"{item_b = }")
    print(f"{item_b.serialize() = }")
    
    item_b_ser: JSONitem = item_b.serialize()

    item_b_loaded: OuterTestClass = OuterTestClass.load(item_b_ser)

    # assert item_b_loaded == item_b
    # assert item_b_loaded.d2 == item_a

    print(f"{item_b_loaded = }")
    print(f"{item_b_loaded.serialize() = }")
