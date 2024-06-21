"""anonymous getitem class

util for constructing a class which has a getitem method which just calls a function

a `lambda` is an anonymous function: kappa is the letter before lambda in the greek alphabet,
hence the name of this class"""

from __future__ import annotations

from typing import Callable, Mapping, TypeVar

_kappa_K = TypeVar("_kappa_K")
_kappa_V = TypeVar("_kappa_V")

# get the docstring of this file
_BASE_DOC: str = (
    __doc__
    + """

source function docstring:
==============================\n
"""
)


class Kappa(Mapping[_kappa_K, _kappa_V]):
    def __init__(self, func_getitem: Callable[[_kappa_K], _kappa_V]) -> None:
        self.func_getitem = func_getitem
        self.doc = _BASE_DOC + str(
            getattr(
                func_getitem, "__doc__", "<no docstring provided for source function>"
            )
        )

    def __getitem__(self, x) -> _kappa_V:
        return self.func_getitem(x)

    def __iter__(self):
        raise NotImplementedError(
            "This method is not implemented for Kappa, we don't know the valid inputs"
        )

    def __len__(self):
        raise NotImplementedError(
            "This method is not implemented for Kappa, no idea how many valid inputs there are"
        )
