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
    EXTERNAL_ITEMS_EXTENSIONS,
    GET_EXTERNAL_ITEM_EXTENSION,
    EXTERNAL_LOAD_FUNCS,
    GET_EXTERNAL_LOAD_FUNC,
    ZANJ_MAIN,
    ZANJ_META,
    _ZANJ_pre,
    ExternalItemType,
    ExternalItemType_vals,
)

# pylint: disable=protected-access, dangerous-default-value

ExternalsLoadingMode = Literal["lazy", "full"]


def _assert_mappings_equal(m1, m2) -> bool:
    shared_keys = set(m1.keys()) & set(m2.keys())

    for k in shared_keys:
        assert k in m1
        assert k in m2

        v1 = m1[k]
        v2 = m2[k]

        if isinstance(v1, typing.Mapping):
            assert isinstance(v2, typing.Mapping)
            _assert_mappings_equal(v1, v2)
        else:
            if isinstance(v1, Iterable):
                assert isinstance(v2, Iterable)
                assert len(v1) == len(v2), f"{len(v1)} != {len(v2)}"

                tval = v1 == v2

                if hasattr(tval, "all") and callable(tval.all):
                    assert v1.shape == v2.shape, f"{v1.shape} != {v2.shape}"
                    assert tval.all()
                else:
                    if isinstance(tval, Iterable):
                        assert all(tval)
                    else:
                        assert isinstance(tval, bool)
                        assert tval
            else:
                assert tval

    return True


@dataclass(kw_only=True)
class LoaderHandler:
    """handler for loading an object from a json file"""

    # (json_data, path) -> whether to use this handler
    check: Callable[[JSONitem, ObjectPath], bool]
    # function to load the object
    load: Callable[[JSONitem, ObjectPath], Any]
    # unique identifier for the handler
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
            check=lambda json_item, path: json_item["__format__"] == fc.__format__,
            load=lambda json_item, path: fc.load(json_item),
            uid=fc.__format__,
            source_pckg=str(fc.__module__),
            priority=priority,
            desc=f"formatted class loader for {fc.__name__}",
        )


@dataclass
class ZANJLoaderHandler(LoaderHandler):
    """handler for loading an object from a ZANJ archive (takes ZANJ object as first arg)"""

    # (zanj_obi, json_data, path) -> whether to use this handler
    check: Callable[[_ZANJ_pre, JSONitem, ObjectPath], bool]  # type: ignore[assignment]
    # function to load the object (zanj_obj, json_data, path) -> loaded_obj
    load: Callable[[_ZANJ_pre, JSONitem, ObjectPath], Any]  # type: ignore[assignment]
    # priority is higher for ZANJ loaders
    priority: int = 100

    @classmethod
    def from_LoaderHandler(cls, lh: LoaderHandler):
        """wrap a standard LoaderHandler to make it compatible with ZANJ"""
        return cls(
            check=lambda zanj, json_item, path: lh.check(json_item, path),
            load=lambda zanj, json_item, path: lh.load(json_item, path),
            uid=lh.uid,
            source_pckg=lh.source_pckg,
            priority=lh.priority,
            desc=lh.desc,
        )

    @classmethod
    def from_formattedclass(cls, fc: type):
        return cls.from_LoaderHandler(LoaderHandler.from_formattedclass(fc))


# NOTE: there are type ignores on the loaders, since the type checking should be the responsibility of the check function

LOADER_HANDLERS: list[LoaderHandler] = [
    LoaderHandler(
        check=lambda json_item, path: (
            isinstance(json_item, typing.Mapping)
            and "__format__" in json_item
            and json_item["__format__"] == "array_list_meta"
        ),
        load=lambda json_item, path: (
            np.array(json_item["data"], dtype=json_item["dtype"]).reshape(  # type: ignore
                json_item["shape"]  # type: ignore
            )
        ),
        uid="array_list_meta",
        source_pckg="muutils.zanj",
        desc="array_list_meta loader",
    ),
    LoaderHandler(
        check=lambda json_item, path: (
            isinstance(json_item, typing.Mapping)
            and "__format__" in json_item
            and json_item["__format__"] == "array_hex_meta"
        ),
        load=lambda json_item, path: (
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


LOADER_HANDLERS_ZANJ: list[ZANJLoaderHandler] = [
    ZANJLoaderHandler(
        check=lambda zanj, json_item, path: (
            isinstance(json_item, typing.Mapping)
            and "__format__" in json_item
            and json_item["__format__"].startswith("external:")
        ),
        load=lambda zanj, json_item, path: (zanj._externals[json_item["$ref"]]),  # type: ignore
        uid="external",
        source_pckg="muutils.zanj",
        desc="external object loader",
    ),
]

# these are populated in _update_loaders to avoid code duplication
LOADER_HANDLERS_JOINED: list[ZANJLoaderHandler] = list()
LOADER_MAP: dict[str, LoaderHandler] = dict()
LOADER_MAP_ZANJ: dict[str, ZANJLoaderHandler] = dict()
LOADER_MAP_JOINED: dict[str, ZANJLoaderHandler] = dict()


def _update_loaders():
    """update the loader maps"""
    global LOADER_HANDLERS, LOADER_HANDLERS_ZANJ, LOADER_HANDLERS_JOINED, LOADER_MAP, LOADER_MAP_ZANJ, LOADER_MAP_JOINED

    # join zanj and non-zanj loaders
    LOADER_HANDLERS_JOINED = LOADER_HANDLERS_ZANJ + [
        ZANJLoaderHandler.from_LoaderHandler(lh) for lh in LOADER_HANDLERS
    ]

    # sort by priority
    LOADER_HANDLERS.sort(key=lambda lh: lh.priority, reverse=True)
    LOADER_HANDLERS_ZANJ.sort(key=lambda lh: lh.priority, reverse=True)
    LOADER_HANDLERS_JOINED.sort(key=lambda lh: lh.priority, reverse=True)

    # create maps, order should be ensured by the sorting
    LOADER_MAP = {lh.uid: lh for lh in LOADER_HANDLERS}
    LOADER_MAP_ZANJ = {lh.uid: lh for lh in LOADER_HANDLERS_ZANJ}
    LOADER_MAP_JOINED = {lh.uid: lh for lh in LOADER_HANDLERS_JOINED}


def register_loader_handler(handler: LoaderHandler):
    """register a custom loader handler"""
    assert not isinstance(
        handler, ZANJLoaderHandler
    ), "use register_loader_handler_zanj for ZANJLoaderHandlers"
    LOADER_HANDLERS.append(handler)
    _update_loaders()


def register_loader_handler_zanj(handler: ZANJLoaderHandler):
    """register a custom loader handler for ZANJ"""
    LOADER_HANDLERS_ZANJ.append(handler)
    _update_loaders()


def get_item_loader(
    json_item: JSONitem,
    path: ObjectPath,
    zanj: _ZANJ_pre | None = None,
    error_mode: ErrorMode = "warn",
    lh_map: dict[str, LoaderHandler] = LOADER_MAP_JOINED,
) -> LoaderHandler | None:
    # check loaders map is correct
    if zanj is None:
        assert not any(
            isinstance(lh, ZANJLoaderHandler) for lh in lh_map.values()
        ), "invalid lh_map"
    else:
        assert all(
            isinstance(lh, ZANJLoaderHandler) for lh in lh_map.values()
        ), "invalid lh_map"

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


@dataclass
class ZANJLoaderTreeNode(typing.Mapping):
    """acts like a regular dictionary or list, but applies loaders to items

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
        lh: ZANJLoaderHandler | None = get_item_loader(
            zanj=self._parent.zanj,
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


class LazyExternalLoader:
    """lazy load np arrays or jsonl files, similar tp NpzFile from np.lib

    initialize with zipfile object and zanj metadata (for list of externals)
    """

    def __init__(
        self,
        zipf: zipfile.ZipFile,
        zanj_meta: dict,
        loaded_zanj: "LoadedZANJ",
    ):
        self._zipf: zipfile.ZipFile = zipf
        self._zanj_meta: JSONitem = zanj_meta
        # (path, item_type) pairs
        self._externals_types: dict[str, str] = {
            key: val["item_type"] for key, val in zanj_meta["externals_info"].items()
        }

        self._loaded_zanj: LoadedZANJ = loaded_zanj

        # validate by checking each external file exists
        for key, item_type in self._externals_types.items():
            if key not in zipf.namelist():
                raise ValueError(f"external file {key} not found in archive")

    def __getitem__(self, key: str) -> Any:
        if key in self._externals_types:
            item_type: str = self._externals_types[key]
            with self._zipf.open(key, "r") as fp:
                return GET_EXTERNAL_LOAD_FUNC(item_type)(self._loaded_zanj, fp)


class LoadedZANJ(typing.Mapping):
    """object loaded from ZANJ archive. acts like a dict."""

    def __init__(
        self,
        # config
        path: str | Path,
        zanj: _ZANJ_pre,
        loader_handlers: dict[str, ZANJLoaderHandler] | None = None,
        externals_mode: ExternalsLoadingMode = "lazy",
        format_error_mode: ErrorMode = "warn",
    ) -> None:

        # copy handlers
        self._loader_handlers: dict[str, ZANJLoaderHandler]
        if loader_handlers is not None:
            self._loader_handlers = loader_handlers
        else:
            loader_handlers = LOADER_MAP_JOINED

        # path and zanj object
        self._path: str = str(path)
        self._zanj: _ZANJ_pre = zanj

        # config
        self._externals_mode: ExternalsLoadingMode = externals_mode
        self._format_error_mode: ErrorMode = format_error_mode

        # load zip file
        self._zipf: zipfile.ZipFile = zipfile.ZipFile(file=self._path, mode="r")

        # load data
        self._meta: dict = json.load(self._zipf.open(ZANJ_META, "r"))
        self._json_data: ZANJLoaderTreeNode = ZANJLoaderTreeNode(
            _parent=self,
            _data=json.load(self._zipf.open(ZANJ_MAIN, "r")),
        )

        # externals
        self._externals: LazyExternalLoader | dict
        if externals_mode == "lazy":
            self._externals = LazyExternalLoader(
                zipf=self._zipf,
                zanj_meta=self._meta,
                loaded_zanj=self,
            )
        elif externals_mode == "full":
            self._externals = dict()

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
