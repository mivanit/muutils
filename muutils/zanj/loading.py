import json
import typing
import warnings
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal, Iterable

import numpy as np

from muutils.json_serialize.json_serialize import ObjectPath
from muutils.json_serialize.util import JSONdict, JSONitem, MonoTuple, ErrorMode
from muutils.zanj.externals import (
    GET_EXTERNAL_LOAD_FUNC,
    ZANJ_MAIN,
    ZANJ_META,
    _ZANJ_pre,
    ExternalItemType,
    ExternalItemType_vals,
)

# pylint: disable=protected-access, dangerous-default-value

@dataclass
class LoaderHandler:
    """handler for loading an object from a json file or a ZANJ archive"""

    # (zanj_obj, json_data, path) -> whether to use this handler
    check: Callable[[JSONitem, ObjectPath, _ZANJ_pre], bool]
    # function to load the object (zanj_obj, json_data, path) -> loaded_obj
    load: Callable[[JSONitem, ObjectPath, _ZANJ_pre], Any]
    # unique identifier for the handler, saved in __format__ field
    uid: str
    # source package of the handler -- note that this might be overridden by ZANJ
    source_pckg: str
    # priority of the handler, defaults are all 0
    priority: int = 0
    # description of the handler
    desc: str = "(no description)"

    @classmethod
    def from_formattedclass(cls, fc: type, priority: int = 0):
        """create a loader from a class with `serialize`, `load` methods and `__format__` attribute"""
        assert hasattr(fc, "serialize")
        assert callable(fc.serialize)  # type: ignore
        assert hasattr(fc, "load")
        assert callable(fc.load)  # type: ignore
        assert hasattr(fc, "__format__")
        assert isinstance(fc.__format__, str)  # type: ignore

        return cls(
            check=lambda json_item, path, zanj_obj: json_item["__format__"] == fc.__format__,
            load=lambda json_item, path, zanj_obj: fc.load(json_item),
            uid=fc.__format__,
            source_pckg=str(fc.__module__),
            priority=priority,
            desc=f"formatted class loader for {fc.__name__}",
        )


# NOTE: there are type ignores on the loaders, since the type checking should be the responsibility of the check function

LOADER_HANDLERS: list[LoaderHandler] = [
    LoaderHandler(
        check=lambda json_item, path, _=None: (
            isinstance(json_item, typing.Mapping)
            and "__format__" in json_item
            and json_item["__format__"] == "array_list_meta"
        ),
        load=lambda json_item, path, _=None: (
            np.array(json_item["data"], dtype=json_item["dtype"]).reshape(  # type: ignore
                json_item["shape"]  # type: ignore
            )
        ),
        uid="array_list_meta",
        source_pckg="muutils.zanj",
        desc="array_list_meta loader",
    ),
    LoaderHandler(
        check=lambda json_item, path, _=None: (
            isinstance(json_item, typing.Mapping)
            and "__format__" in json_item
            and json_item["__format__"] == "array_hex_meta"
        ),
        load=lambda json_item, path, _: (
            np.frombuffer(
                bytes.fromhex(json_item["data"]), dtype=json_item["dtype"]  # type: ignore
            ).reshape(
                json_item["shape"]  # type: ignore
            )
        ),
        uid="array_hex_meta",
        source_pckg="muutils.zanj",
        desc="array_hex_meta loader",
    ),
]


LOADER_MAP: dict[str, LoaderHandler] = dict()


def _update_loaders():
    """update the loader maps"""
    global LOADER_HANDLERS, LOADER_MAP

    # sort by priority
    LOADER_HANDLERS.sort(key=lambda lh: lh.priority, reverse=True)

    # create map, order should be ensured by the sorting
    LOADER_MAP = {lh.uid: lh for lh in LOADER_HANDLERS}

def register_loader_handler(handler: LoaderHandler):
    """register a custom loader handler"""
    assert not isinstance(
        handler, LoaderHandler
    ), "use register_loader_handler_zanj for LoaderHandlers"
    LOADER_HANDLERS.append(handler)
    _update_loaders()


def get_item_loader(
    json_item: JSONitem,
    path: ObjectPath,
    zanj: _ZANJ_pre | None = None,
    error_mode: ErrorMode = "warn",
    lh_map: dict[str, LoaderHandler] = LOADER_MAP,
) -> LoaderHandler | None:
    """get the loader for a json item"""

    # check if we recognize the format
    if isinstance(json_item, typing.Mapping) and "__format__" in json_item:
        if json_item["__format__"] in lh_map:
            return lh_map[json_item["__format__"]]
        else:
            if error_mode == "warn":
                warnings.warn(f"unknown format {json_item['__format__']} at {path}")
            elif error_mode == "except":
                raise ValueError(f"unknown format {json_item['__format__']} at {path}")
            elif error_mode == "ignore":
                pass
            else:
                raise ValueError(f"invalid error mode {error_mode}")

    # if we dont recognize the format, try to find a loader that can handle it
    for key, lh in lh_map.items():
        if zanj is None:
            if lh.check(json_item, path):
                return lh
        else:
            if lh.check(zanj, json_item, path):
                return lh

    # if we still dont have a loader, return None
    return None




def _external_load(json_item: JSONitem, path: ObjectPath, zanj: _ZANJ_pre) -> Any:
    """load an external object"""
    assert isinstance(json_item, typing.Mapping)
    assert "$ref" in json_item
    assert isinstance(json_item["$ref"], str)
    assert "__format__" in json_item
    assert json_item["__format__"].endswith(":external")
    assert json_item["$ref"] in zanj._externals

    externally_loaded = zanj._externals[json_item["$ref"]]
    
    new_loader: LoaderHandler | None = get_item_loader(externally_loaded, path, zanj)

    if new_loader is None:
        return externally_loaded
    else:
        return new_loader.load(externally_loaded, path, zanj)

# add the special externals loader

LoaderHandler(
    check=lambda json_item, path, zanj: (
        isinstance(json_item, typing.Mapping)
        and "__format__" in json_item
        and json_item["__format__"].endswith(":external")
    ),
    # load function should strip the "external" and load again
    load=_external_load,  # type: ignore
    uid="external",
    source_pckg="muutils.zanj",
    priority=999,
    desc="external object loader",
)




@dataclass
class ZANJLoaderTreeNode(typing.Mapping):
    """acts like a regular dictionary or list, but applies loaders to items
    
    # TODO: this whole class is buggy. Is there a better way to do this?

    does this by passing `_parent` down the stack, whenever you get an item from the container.
    """

    _parent: "LoadedZANJ"
    _data: JSONdict | list[JSONitem]

    def __getitem__(self, key: str | int) -> Any:
        # make sure we have a string key for dict, int key for list
        # --------------------------------------------------
        val: JSONitem
        if (isinstance(self._data, typing.Sequence) and isinstance(key, int)) or (
            isinstance(self._data, typing.Mapping) and isinstance(key, str)
        ):
            # not sure why mypy is complaining, we are performing all checks
            val = self._data[key]  # type: ignore
        else:
            raise KeyError(
                f"invalid key type {type(key) = }, {key = } for {self._data = } with {type(self._data) = }"
            )

        # get value or dereference
        # --------------------------------------------------
        if isinstance(key, str) and (key == "$ref"):
            # dereference
            assert isinstance(
                val, str
            ), f"invalid $ref type: {type(val) = } for {val = }"
            val = self._parent._externals[val]
        else:
            # get value
            val = self._data[key]  # type: ignore

        # nest tree node if necessary
        # --------------------------------------------------
        tree_val: ZANJLoaderTreeNode | JSONitem
        if isinstance(val, (dict, list)):
            tree_val = ZANJLoaderTreeNode(_parent=self._parent, _data=val)
        else:
            tree_val = val

        # apply loaders, if one exists
        # --------------------------------------------------
        item_path: ObjectPath = tuple(self._parent._path) + (key,)
        lh: LoaderHandler | None = get_item_loader(
            zanj=self._parent._zanj,
            json_item=tree_val,
            path=item_path,
            lh_map=self._parent._loader_handlers,
            error_mode=self._parent._format_error_mode,
        )
        if lh is not None:
            return lh.load(self._parent, tree_val, self._parent._path)

        return tree_val

    def __iter__(self):
        yield from self._data

    def __len__(self):
        return len(self._data)




# TODO: this needs to be refactored 
class LoadedZANJ(typing.Mapping):
    """object loaded from ZANJ archive. acts like a dict."""

    def __init__(
        self,
        # config
        path: str | Path,
        zanj: _ZANJ_pre,
        loader_handlers: dict[str, LoaderHandler] | None = None,
    ) -> None:

        # copy handlers
        self._loader_handlers: dict[str, LoaderHandler]
        if loader_handlers is not None:
            self._loader_handlers = loader_handlers
        else:
            self._loader_handlers = LOADER_MAP

        # path and zanj object
        self._path: str = str(path)
        self._zanj: _ZANJ_pre = zanj

        # load zip file
        self._zipf: zipfile.ZipFile = zipfile.ZipFile(file=self._path, mode="r")

        # load data
        self._meta: dict = json.load(self._zipf.open(ZANJ_META, "r"))
        self._json_data: ZANJLoaderTreeNode = ZANJLoaderTreeNode(
            _parent=self,
            _data=json.load(self._zipf.open(ZANJ_MAIN, "r")),
        )

        # externals
        self._externals: dict[str, Any] = dict()

        for fname, val in self._meta["externals_info"].items():
            item_type: str = val["item_type"]
            with self._zipf.open(fname, "r") as fp:
                self._externals[fname] = GET_EXTERNAL_LOAD_FUNC(item_type)(self, fp)

    def __getitem__(self, key: str) -> Any:
        """get the value of the given key"""
        return self._json_data[key]

    def __iter__(self):
        return iter(self._json_data)

    def __len__(self):
        return len(self._json_data)
