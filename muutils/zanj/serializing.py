import json
from dataclasses import dataclass
from typing import IO, Any, Callable, Iterable, Sequence

import numpy as np
import pandas as pd

from muutils.json_serialize.array import arr_metadata
from muutils.json_serialize.json_serialize import (  # JsonSerializer,
    DEFAULT_HANDLERS,
    ObjectPath,
    SerializerHandler,
)
from muutils.json_serialize.util import JSONdict, JSONitem, MonoTuple
from muutils.tensor_utils import NDArray
from muutils.zanj.externals import ExternalItem, ExternalItemType, _ZANJ_pre

# pylint: disable=unused-argument, protected-access, unexpected-keyword-arg
# for some reason pylint complains about kwargs to ZANJSerializerHandler


def jsonl_metadata(data: list[JSONdict]) -> dict:
    """metadata about a jsonl object"""
    all_cols: set[str] = set([col for item in data for col in item.keys()])
    return {
        "data[0]": data[0],
        "len(data)": len(data),
        "columns": {
            col: {
                "types": list(
                    set([type(item[col]).__name__ for item in data if col in item])
                ),
                "len": len([item[col] for item in data if col in item]),
            }
            for col in all_cols
        },
    }


def store_npy(self: _ZANJ_pre, fp: IO[bytes], data: NDArray) -> None:
    """store numpy array to given file as .npy"""
    np.lib.format.write_array(
        fp=fp,
        array=np.asanyarray(data),
        allow_pickle=False,
    )


def store_jsonl(self: _ZANJ_pre, fp: IO[bytes], data: Sequence[JSONitem]) -> None:
    """store sequence to given file as .jsonl"""

    for item in data:
        fp.write(json.dumps(item).encode("utf-8"))
        fp.write("\n".encode("utf-8"))


EXTERNAL_STORE_FUNCS: dict[
    ExternalItemType, Callable[[_ZANJ_pre, IO[bytes], Any], None]
] = {
    "npy": store_npy,
    "jsonl": store_jsonl,
}


@dataclass(kw_only=True)
class ZANJSerializerHandler(SerializerHandler):
    """a handler for ZANJ serialization"""

    # (self_config, object) -> whether to use this handler
    check: Callable[[_ZANJ_pre, Any, ObjectPath], bool]
    # (self_config, object, path) -> serialized object
    serialize_func: Callable[[_ZANJ_pre, Any, ObjectPath], JSONitem]
    # unique identifier for the handler, saved in __format__ field
    uid: str
    # source package of the handler -- note that this might be overridden by ZANJ
    source_pckg: str
    # optional description of how this serializer works
    desc: str = "(no description)"


def zanj_external_serialize(
    jser: _ZANJ_pre,
    data: Any,
    path: ObjectPath,
    item_type: ExternalItemType,
    _format: str,
) -> JSONitem:
    """stores a numpy array or jsonl externally in a ZANJ object

    # Parameters:
     - `jser: ZANJ`
     - `data: Any`
     - `path: ObjectPath`
     - `item_type: ExternalItemType`

    # Returns:
     - `JSONitem`
       json data with reference

    # Modifies:
     - modifies `jser._externals`
    """
    # get the path, make sure its unique
    assert isinstance(
        path, tuple
    ), f"path must be a tuple, got {type(path) = } {path = }"
    joined_path: str = "/".join([str(p) for p in path])
    archive_path: str = f"{joined_path}.{item_type}"

    if archive_path in jser._externals:
        raise ValueError(f"external path {archive_path} already exists!")
    if any([p.startswith(joined_path) for p in jser._externals.keys()]):
        raise ValueError(f"external path {joined_path} is a prefix of another path!")

    # process the data if needed, assemble metadata
    data_new: Any = data
    output: dict = {
        "__format__": _format,
        "$ref": archive_path,
    }
    if item_type == "npy":
        # check type
        data_type_str: str = str(type(data))
        if data_type_str == "<class 'torch.Tensor'>":
            # detach and convert
            data_new = data.detach().cpu().numpy()
        elif data_type_str == "<class 'numpy.ndarray'>":
            pass
        else:
            # if not a numpy array, except
            raise TypeError(f"expected numpy.ndarray, got {data_type_str}")
        # get metadata
        output.update(arr_metadata(data))
    elif item_type.startswith("jsonl"):
        if isinstance(data, pd.DataFrame):
            output["columns"] = data.columns.tolist()
            data_new = data.to_dict(orient="records")
        elif isinstance(data, (list, tuple, Iterable)):
            data_new = [
                jser.json_serialize(item, tuple(path) + (i,))
                for i, item in enumerate(data)
            ]
        else:
            raise TypeError(f"expected list or pd.DataFrame, got {type(data)}")

        output.update(jsonl_metadata(data_new))

    # store the item for external serialization
    jser._externals[archive_path] = ExternalItem(
        item_type=item_type,
        data=data_new,
        path=path,
    )

    return output


DEFAULT_SERIALIZER_HANDLERS_ZANJ: MonoTuple[ZANJSerializerHandler] = tuple(
    [
        ZANJSerializerHandler(
            check=lambda self, obj, path: (
                isinstance(obj, np.ndarray)
                and obj.size >= self.external_array_threshold
            ),
            serialize_func=lambda self, obj, path: zanj_external_serialize(
                self, obj, path, item_type="npy", _format="numpy.ndarray:external"
            ),
            uid="numpy.ndarray:external",
            source_pckg="muutils.zanj",
            desc="external numpy array",
        ),
        ZANJSerializerHandler(
            check=lambda self, obj, path: (
                str(type(obj)) == "<class 'torch.Tensor'>"
                and int(obj.nelement()) >= self.external_array_threshold
            ),
            serialize_func=lambda self, obj, path: zanj_external_serialize(
                self, obj, path, item_type="npy", _format="torch.Tensor:external"
            ),
            uid="torch.Tensor:external",
            source_pckg="muutils.zanj",
            desc="external torch tensor",
        ),
        ZANJSerializerHandler(
            check=lambda self, obj, path: isinstance(obj, list)
            and len(obj) >= self.external_table_threshold,
            serialize_func=lambda self, obj, path: zanj_external_serialize(
                self, obj, path, item_type="jsonl", _format="list:external"
            ),
            uid="list:external",
            source_pckg="muutils.zanj",
            desc="external list",
        ),
        ZANJSerializerHandler(
            check=lambda self, obj, path: isinstance(obj, tuple)
            and len(obj) >= self.external_table_threshold,
            serialize_func=lambda self, obj, path: zanj_external_serialize(
                self, obj, path, item_type="jsonl", _format="tuple:external"
            ),
            uid="tuple:external",
            source_pckg="muutils.zanj",
            desc="external tuple",
        ),
        ZANJSerializerHandler(
            check=lambda self, obj, path: isinstance(obj, pd.DataFrame)
            and len(obj) >= self.external_table_threshold,
            serialize_func=lambda self, obj, path: zanj_external_serialize(
                self, obj, path, item_type="jsonl", _format="pandas.DataFrame:external"
            ),
            uid="pandas.DataFrame:external",
            source_pckg="muutils.zanj",
            desc="external pandas DataFrame",
        ),
        # ZANJSerializerHandler(
        #     check=lambda self, obj, path: "<class 'torch.nn.modules.module.Module'>"
        #     in [str(t) for t in obj.__class__.__mro__],
        #     serialize_func=lambda self, obj, path: zanj_serialize_torchmodule(
        #         self, obj, path,
        #     ),
        #     uid="torch.nn.Module",
        #     source_pckg="muutils.zanj",
        #     desc="fallback torch serialization",
        # ),
    ]
) + tuple(
    DEFAULT_HANDLERS  # type: ignore[arg-type]
)

# the complaint above is:
# error: Argument 1 to "tuple" has incompatible type "Sequence[SerializerHandler]"; expected "Iterable[ZANJSerializerHandler]"  [arg-type]
