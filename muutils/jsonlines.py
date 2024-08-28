"utilities for reading and writing jsonlines files, including gzip support"

from __future__ import annotations

import gzip
import json
from typing import Callable, Sequence

from muutils.json_serialize import JSONitem

_GZIP_EXTENSIONS: tuple = (".gz", ".gzip")


def _file_is_gzip(path: str) -> bool:
    return any(str(path).endswith(ext) for ext in _GZIP_EXTENSIONS)


def _get_opener(
    path: str,
    use_gzip: bool | None = None,
) -> Callable:
    if use_gzip is None:
        use_gzip = _file_is_gzip(path)

    # appears to be another mypy bug
    # https://github.com/python/mypy/issues/10740
    return open if not use_gzip else gzip.open  # type: ignore


def jsonl_load(
    path: str,
    /,
    *,
    use_gzip: bool | None = None,
) -> list[JSONitem]:
    opener: Callable = _get_opener(path, use_gzip)

    data: list[JSONitem] = list()
    with opener(path, "rt", encoding="UTF-8") as f:
        for line in f:
            data.append(json.loads(line))

    return data


def jsonl_load_log(
    path: str,
    /,
    *,
    use_gzip: bool | None = None,
) -> list[dict]:
    data: list[JSONitem] = jsonl_load(path, use_gzip=use_gzip)
    for idx, item in enumerate(data):
        assert isinstance(
            item, dict
        ), f"item {idx = } from file {path} is not a dict: {type(item) = }\t{item = }"

    # mypy complains that we are returning a list[JSONitem] but the function signature says list[dict]
    # it can't figure out that we are asserting that all items are dicts
    return data  # type: ignore


def jsonl_write(
    path: str,
    items: Sequence[JSONitem],
    use_gzip: bool | None = None,
    gzip_compresslevel: int = 2,
) -> None:
    opener: Callable = _get_opener(path, use_gzip)

    opener_kwargs: dict = dict()
    if use_gzip:
        opener_kwargs = dict(compresslevel=gzip_compresslevel)

    with opener(path, "wt", encoding="UTF-8", **opener_kwargs) as f:
        for item in items:
            f.write(json.dumps(item) + "\n")
