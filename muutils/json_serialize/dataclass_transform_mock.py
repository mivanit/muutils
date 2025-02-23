from __future__ import annotations

import typing
from typing import Any, Union


def dataclass_transform(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    frozen_default: bool = False,
    field_specifiers: tuple[Union[type[Any], typing.Callable[..., Any]], ...] = (),
    **kwargs: Any,
) -> typing.Callable:
    "mock `typing.dataclass_transform` for python <3.11"

    def decorator(cls_or_fn):
        cls_or_fn.__dataclass_transform__ = {
            "eq_default": eq_default,
            "order_default": order_default,
            "kw_only_default": kw_only_default,
            "frozen_default": frozen_default,
            "field_specifiers": field_specifiers,
            "kwargs": kwargs,
        }
        return cls_or_fn

    return decorator
