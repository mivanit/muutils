from typing import Callable, Generic, TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class DefaulterDict(dict[_KT, _VT], Generic[_KT, _VT]):
    """like a defaultdict, but default_factory is passed the key as an argument"""

    def __init__(self, default_factory: Callable[[_KT], _VT], *args, **kwargs):
        if args:
            raise TypeError(
                f"DefaulterDict does not support positional arguments: *args = {args}"
            )
        super().__init__(**kwargs)
        self.default_factory: Callable[[_KT], _VT] = default_factory

    def __getitem__(self, k: _KT) -> _VT:
        if k in self:
            return dict.__getitem__(self, k)
        else:
            return self.default_factory(k)
