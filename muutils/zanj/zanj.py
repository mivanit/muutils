"""
an HDF5/exdir file alternative, which uses json for attributes, allows serialization of arbitrary data

for large arrays, the output is a .tar.gz file with most data in a json file, but with sufficiently large arrays stored in binary .npy files


"ZANJ" is an acronym that the AI tool [Elicit](https://elicit.org) came up with for me. not to be confused with:

- https://en.wikipedia.org/wiki/Zanj
- https://www.plutojournals.com/zanj/

"""

import json
import os
import time
import zipfile
from pathlib import Path
from typing import Any, Union

import numpy as np
import pandas as pd

from muutils.json_serialize.array import ArrayMode, arr_metadata
from muutils.json_serialize.json_serialize import (
    JsonSerializer,
    SerializerHandler,
    json_serialize,
)
from muutils.json_serialize.util import ErrorMode, JSONitem, MonoTuple
from muutils.sysinfo import SysInfo
from muutils.zanj.externals import ZANJ_MAIN, ZANJ_META, ExternalItem, _ZANJ_pre
from muutils.zanj.loading import LOADER_MAP, LoadedZANJ, load_item_recursive
from muutils.zanj.serializing import (
    DEFAULT_SERIALIZER_HANDLERS_ZANJ,
    EXTERNAL_STORE_FUNCS,
)

# pylint: disable=protected-access, unused-import, dangerous-default-value, line-too-long

ZANJitem = Union[
    JSONitem,
    np.ndarray,
    pd.DataFrame,
]


class ZANJ(JsonSerializer):
    """Zip up: Arrays in Numpy, JSON for everything else

    given an arbitrary object, throw into a zip file, with arrays stored in .npy files, and everything else stored in a json file

    (basically npz file with json)

    - numpy (or pytorch) arrays are stored in paths according to their name and structure in the object
    - everything else about the object is stored in a json file `zanj.json` in the root of the archive, via `muutils.json_serialize.JsonSerializer`
    - metadata about ZANJ configuration, and optionally packages and versions, is stored in a `__zanj_meta__.json` file in the root of the archive

    create a ZANJ-class via `z_cls = ZANJ().create(obj)`, and save/read instances of the object via `z_cls.save(obj, path)`, `z_cls.load(path)`. be sure to pass an **instance** of the object, to make sure that the attributes of the class can be correctly recognized

    """

    def __init__(
        self,
        error_mode: ErrorMode = "except",
        internal_array_mode: ArrayMode = "array_list_meta",
        external_array_threshold: int = 64,
        external_table_threshold: int = 64,
        compress: bool | int = True,
        handlers_pre: MonoTuple[SerializerHandler] = tuple(),
        handlers_default: MonoTuple[
            SerializerHandler
        ] = DEFAULT_SERIALIZER_HANDLERS_ZANJ,
    ) -> None:
        super().__init__(
            array_mode=internal_array_mode,
            error_mode=error_mode,
            handlers_pre=handlers_pre,
            handlers_default=handlers_default,
        )

        self.external_array_threshold: int = external_array_threshold
        self.external_table_threshold: int = external_table_threshold

        # process compression to int if bool given
        self.compress = compress
        if isinstance(compress, bool):
            if compress:
                self.compress = zipfile.ZIP_DEFLATED
            else:
                self.compress = zipfile.ZIP_STORED

        # create the externals, leave it empty
        self._externals: dict[str, ExternalItem] = dict()

    def externals_info(self) -> dict[str, dict]:
        """return information about the current externals"""
        output: dict[str, dict] = dict()

        key: str
        item: ExternalItem
        for key, item in self._externals.items():
            data = item.data
            output[key] = {
                "item_type": item.item_type,
                "path": item.path,
                "type(data)": str(type(data)),
                "len(data)": len(data),
            }

            if item.item_type == "ndarray":
                output[key].update(arr_metadata(data))
            elif item.item_type.startswith("jsonl"):
                output[key]["data[0]"] = data[0]

        return output

    def meta(self) -> JSONitem:
        """return the metadata of the ZANJ archive"""
        global LOADER_MAP

        serialization_handlers = {h.uid: h.serialize() for h in self.handlers}
        load_handlers = {h.uid: h.serialize() for h in LOADER_MAP.values()}

        return json_serialize(
            dict(
                # configuration of this ZANJ instance
                zanj_cfg=dict(
                    error_mode=str(self.error_mode),
                    array_mode=str(self.array_mode),
                    external_array_threshold=self.external_array_threshold,
                    external_table_threshold=self.external_table_threshold,
                    compress=self.compress,
                    serialization_handlers=serialization_handlers,
                    load_handlers=load_handlers,
                ),
                # system info (python, pip packages, torch & cuda, platform info, git info)
                sysinfo=SysInfo.get_all(include=("python", "pytorch")),
                externals_info=self.externals_info(),
                timestamp=time.time(),
            )
        )

    def save(self, obj: Any, file_path: str | Path) -> str:
        """save the object to a ZANJ archive. returns the path to the archive"""

        # adjust extension
        file_path = str(file_path)
        if not file_path.endswith(".zanj"):
            file_path += ".zanj"

        # make directory
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # clear the externals!
        self._externals = dict()

        # serialize the object -- this will populate self._externals
        # TODO: calling self.json_serialize again here might be slow
        json_data: JSONitem = self.json_serialize(self.json_serialize(obj))

        # open the zip file
        zipf: zipfile.ZipFile = zipfile.ZipFile(
            file=file_path, mode="w", compression=self.compress
        )

        # store base json data and metadata
        zipf.writestr(
            ZANJ_META,
            json.dumps(
                self.json_serialize(self.meta()),
                indent="\t",
            ),
        )
        zipf.writestr(
            ZANJ_MAIN,
            json.dumps(
                json_data,
                indent="\t",
            ),
        )

        # store externals
        for key, (ext_type, ext_data, ext_path) in self._externals.items():
            # why force zip64? numpy.savez does it
            with zipf.open(key, "w", force_zip64=True) as fp:
                EXTERNAL_STORE_FUNCS[ext_type](self, fp, ext_data)

        zipf.close()

        # clear the externals, again
        self._externals = dict()

        return file_path

    def read(
        self,
        path: Union[str, Path],
    ) -> JSONitem:
        """load the object from a ZANJ archive"""
        loaded_zanj: LoadedZANJ = LoadedZANJ(
            path=path,
            zanj=self,
        )

        loaded_zanj.populate_externals()

        return load_item_recursive(
            loaded_zanj._json_data,
            path=tuple(),
            zanj=loaded_zanj,
            error_mode=self.error_mode,
            # lh_map=loader_handlers,
        )


_ZANJ_pre = ZANJ  # type: ignore
