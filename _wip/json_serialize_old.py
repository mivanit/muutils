import functools
import inspect
import types
import typing
import warnings
from dataclasses import dataclass, is_dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Optional, Union

from muutils.json_serialize.util import JSONdict

_NUMPY_WORKING: bool
try:
    import numpy as np

    _NUMPY_WORKING = True
except ImportError:
    warnings.warn("numpy not found, cannot serialize numpy arrays!")
    _NUMPY_WORKING = False

JSONitem = Union[bool, int, float, str, list, dict, None]
Hashableitem = Union[bool, int, float, str, tuple]


class UniversalContainer:
    """contains everything -- `x in UniversalContainer()` is always True"""

    def __contains__(self, x: Any) -> bool:
        return True


def isinstance_namedtuple(x):
    """checks if `x` is a `namedtuple`

    credit to https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
    """
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, "_fields", None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def try_catch(func: Callable):
    """wraps the function to catch exceptions, returns serialized error message on exception

    returned func will return normal result on success, or error message on exception
    """

    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"{e.__class__.__name__}: {e}"

    return newfunc


SERIALIZER_SPECIAL_KEYS: list[str] = [
    "__name__",
    "__doc__",
    "__module__",
    "__class__",
    "__dict__",
    "__annotations__",
]

SERIALIZER_SPECIAL_FUNCS: dict[str, Callable] = {
    "str": str,
    "dir": dir,
    "type": try_catch(lambda x: str(type(x).__name__)),
    "repr": try_catch(lambda x: repr(x)),
    "code": try_catch(lambda x: inspect.getsource(x)),
    "sourcefile": try_catch(lambda x: inspect.getsourcefile(x)),
}

ErrorMode = Literal["ignore", "warn", "except"]

ArrayMode = Literal["list", "array_list_meta", "array_hex_meta"]


def serialize_array(arr: Any, array_mode: ArrayMode = "array_list_meta") -> JSONitem:
    """serialize a numpy or pytorch array in one of several modes

    if the object is zero-dimensional, simply get the unique item

    `array_mode: ArrayMode` can be one of:
    - `list`: serialize as a list of values, no metadata (equivalent to `arr.tolist()`)
    - `array_list_meta`: serialize dict with metadata, actual list under the key `data`
    - `array_hex_meta`: serialize dict with metadata, actual hex string under the key `data`

    for the latter two, the output will look like
    ```
    {
        "__format__": <array_list_meta|array_hex_meta>,
        "shape": arr.shape,
        "dtype": str(arr.dtype),
        "data": <arr.tolist()|arr.tobytes().hex()>,
    }
    ```

    # Parameters:
     - `arr : Any` array to serialize
     - `array_mode : ArrayMode` mode in which to serialize the array
       (defaults to `"array_list_meta"`)

    # Returns:
     - `JSONitem`
       json serialized array

    # Raises:
     - `KeyError` : if the array mode is not valid

    # TODO: allow external-file storage of large arrays?
    """

    if len(arr.shape) == 0:
        return arr.item()

    if array_mode == "array_list_meta":
        return {
            "__format__": "array_list_meta",
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "data": arr.tolist(),
        }
    elif array_mode == "list":
        return arr.tolist()
    elif array_mode == "array_hex_meta":
        return {
            "__format__": "array_hex_meta",
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "data": arr.tobytes().hex(),
        }
    else:
        raise KeyError(f"invalid array_mode: {array_mode}")


def infer_array_mode(arr: JSONitem) -> ArrayMode:
    """given a serialized array, infer the mode

    assumes the array was serialized via `serialize_array()`
    """
    if isinstance(arr, typing.Mapping):
        fmt: Optional[str] = arr.get("__format__", None)
        if fmt == "array_list_meta":
            if type(arr["data"]) != list:
                raise ValueError(f"invalid list format: {arr}")
            return fmt
        elif fmt == "array_hex_meta":
            if type(arr["data"]) != str:
                raise ValueError(f"invalid hex format: {arr}")
            return fmt
        else:
            raise ValueError(f"invalid format: {arr}")

    elif isinstance(arr, list):
        return "list"
    else:
        raise ValueError(f"cannot infer array_mode from {arr}")


def load_array(arr: JSONitem, array_mode: Optional[ArrayMode] = None) -> Any:
    """load a json-serialized array, infer the mode if not specified"""
    # try to infer the array_mode
    array_mode_inferred: ArrayMode = infer_array_mode(arr)
    if array_mode is None:
        array_mode = array_mode_inferred
    elif array_mode != array_mode_inferred:
        warnings.warn(
            f"array_mode {array_mode} does not match inferred array_mode {array_mode_inferred}"
        )

    # actually load the array
    if array_mode == "array_list_meta":
        data = np.array(arr["data"], dtype=arr["dtype"])
        if tuple(arr["shape"]) != tuple(data.shape):
            raise ValueError(f"invalid shape: {arr}")
        return data
    elif array_mode == "array_hex_meta":
        data = np.frombuffer(bytes.fromhex(arr["data"]), dtype=arr["dtype"])
        return data.reshape(arr["shape"])
    elif array_mode == "list":
        return np.array(arr)
    else:
        raise ValueError(f"invalid array_mode: {array_mode}")


SERIALIZE_DIRECT_AS_STR: set[str] = (
    "<class 'torch.device'>",
    "<class 'torch.dtype'>",
)


def json_serialize(
    obj: Any,
    depth: int = -1,
    array_mode: ArrayMode = "array_list_meta",
    error_mode: ErrorMode = "except",
    direct_as_str: tuple[str] = SERIALIZE_DIRECT_AS_STR,
    **kwargs,
) -> JSONitem:
    """serialize __any__ python object to json, not guaranteed to be recoverable

    in general, tries the following (recursive) serialization:
    - try to call a `.serialize()` method on the object (if present)
    - serialize as a base type (bool, int, float, str)
    - recursively serialize dicts
    - if a namedtuple, serialize as a dict with the namedtuple fields as keys
    - if a dataclass, serialize as a dict with the dataclass fields as keys ( but call this function recursively, not just `asdict(obj)` )
    - if an iterable, call this function recursively on each element and return a list
    - if numpy or torch array, call `serialize_array()`
    - if none of the above, serialize as a dict with
      - the items at `SERIALIZER_SPECIAL_KEYS` as keys
      - the results of calling `SERIALIZER_SPECIAL_FUNCS` as values
    - if there is an exception in the above
      - if `error_mode == "ignore"`, ignore the exception and return `repr(obj)`
      - if `error_mode == "warn"`, warn and return `repr(obj)`
      - if `error_mode == "except"`, raise the exception
    """

    if len(kwargs) > 0:
        warnings.warn(f"unused kwargs: {kwargs}")

    newdepth: int = depth - 1
    try:
        str_type_obj: str = str(type(obj))
        # special
        # ==================================================
        # check for special `serialize` method
        if hasattr(obj, "serialize"):
            # print(f'\n### using custom serialize: {str(obj) = }\n')
            return json_serialize(obj.serialize())

        # basics
        # ==================================================
        # if `None`, return `None`
        if obj is None:
            return None

        # if primitive type, just add it
        if isinstance(obj, (bool, int, float, str)):
            return obj

        # if max depth is reached, return the object as a string and dont recurse
        if depth == 0:
            return str(obj)

        if isinstance(obj, typing.Mapping):
            # print(f'\n### reading obj as dict: {str(obj)}')
            # if dict, recurse
            out_dict: JSONdict = dict()
            for k, v in obj.items():
                out_dict[str(k)] = json_serialize(v, newdepth)
            return out_dict

        # common structures
        # ==================================================
        elif isinstance_namedtuple(obj):
            # if namedtuple, treat as dict
            return json_serialize(dict(obj._asdict()), newdepth)

        elif is_dataclass(obj):
            # if dataclass, treat as dict
            # print(f'\n### reading obj as dataclass: {str(obj)}')
            return {
                k: json_serialize(getattr(obj, k)) for k in obj.__dataclass_fields__
            }
        elif isinstance(obj, Path):
            return obj.as_posix()

        elif str_type_obj in direct_as_str:
            return str(obj)

        # iterables
        # ==================================================
        elif str_type_obj == "<class 'numpy.ndarray'>":
            # try serializing numpy arrays
            return serialize_array(obj, array_mode)
        elif str_type_obj == "<class 'torch.Tensor'>":
            # same for torch tensors
            return serialize_array(obj.detach().cpu().numpy())
        elif isinstance(obj, (set, list, tuple)) or isinstance(obj, Iterable):
            # if iterable, recurse
            # print(f'\n### reading obj as iterable: {str(obj)}')
            return [json_serialize(x, newdepth) for x in obj]
        else:
            # if not basic type, serialize it however we can
            return {
                **{k: str(getattr(obj, k, None)) for k in SERIALIZER_SPECIAL_KEYS},
                **{k: f(obj) for k, f in SERIALIZER_SPECIAL_FUNCS.items()},
            }
    except Exception as e:
        if error_mode == "except":
            raise e
        elif error_mode == "warn":
            warnings.warn(
                f"error serializing, will return as string\n{obj = }\nexception = {e}"
            )

        return repr(obj)


def _recursive_hashify(obj: Any, force: bool = True) -> Hashableitem:
    if isinstance(obj, typing.Mapping):
        return tuple((k, _recursive_hashify(v)) for k, v in obj.items())
    elif isinstance(obj, (tuple, list, Iterable)):
        return tuple(_recursive_hashify(v) for v in obj)
    elif isinstance(obj, (bool, int, float, str)):
        return obj
    else:
        if force:
            return str(obj)
        else:
            raise ValueError(f"cannot hashify:\n{obj}")


def hashify(obj: Any, force: bool = True) -> Hashableitem:
    """try to turn any object into something hashable"""
    data = json_serialize(obj, depth=-1)

    # recursive hashify, turning dicts and lists into tuples
    return _recursive_hashify(data, force=force)


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
    return {
        "__format__": "torch_module",
        "name": obj.__class__.__name__,
        "state_dict": {
            k: serialize_array(v.cpu().numpy(), array_mode=array_mode)
            for k, v in obj.state_dict().items()
        },
        "members_dict": {
            k: (
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
    import torch

    @classmethod
    def load(cls, item: JSONitem) -> "torch.nn.Module":
        assert item["__format__"] == "torch_module"
        assert item["name"] == cls.__name__

        module_obj = cls(
            **{
                k: (v if k not in typecasts else typecasts[k](v))
                for k, v in item["members_dict"].items()
                if k not in members_exclude
            }
        )
        module_obj.load_state_dict(
            {k: torch.from_numpy(load_array(v)) for k, v in item["state_dict"].items()},
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

    def serialize(self):
        # get the base outputs for all keys in the dataclass but which dont have a special serializer
        base_output: JSONdict = {
            k: (json_serialize(getattr(self, k)))
            for k in self.__dataclass_fields__
            if ((k not in special_serializers) and (k not in fields_exclude))
        }

        # update with the special serializers
        return {
            **base_output,
            **{
                k: special_serializers[k](self)
                for k in special_serializers
                if k not in fields_exclude
            },
        }

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

    type_args: tuple[type, ...] = typing.get_args(expected_type)
    return_raw: bool = False

    try:
        if origin_type in (Union, types.UnionType, Optional):
            # TODO: this is incomplete
            pass
        elif isinstance(None, origin_type):
            pass
    except TypeError as e:
        warnings.warn(
            f"error processing {origin_type = } for {key = }, loader will return raw data\n\t{e}"
        )
        return_raw = True

    def loader(data: JSONitem) -> Any:
        if key not in data:
            raise KeyError(
                f"while executing `.load(data)`, key {key} not found in data: {data = }"
            )

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
                warnings.warn("error loading, will return raw data")
                return data[key]
            elif error_mode == "except":
                raise TypeError(
                    f"expected {origin_type} for {key = }, got {type(data)}\n\t{data = }"
                )
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
                if (
                    len(
                        [
                            True
                            for p_name, p_cls in k_loader_signature.parameters.items()
                            if p_cls.default == inspect._empty
                        ]
                    )
                    != 1
                ):
                    raise TypeError(
                        f"`.load()` method for {k} has incorrect signature, expected exactly 1 argument without a default value:\n\t{k = }\n\t{k_loader = }\n\t{k_loader_signature = }\n\t{k_loader_signature.parameters = }"
                    )

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
    /,
    *,
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


if __name__ == "__main__":
    print("# running tests")
    _test()
