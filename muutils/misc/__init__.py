"""miscellaneous utilities

- `stable_hash` for hashing that is stable across runs
- `muutils.misc.sequence` for sequence manipulation, applying mappings, and string-like operations on lists
- `muutils.misc.string` for sanitizing things for filenames, adjusting docstrings, and converting dicts to filenames
- `muutils.misc.numerical` for turning numbers into nice strings and back
- `muutils.misc.freezing` for freezing things
- `muutils.misc.classes` for some weird class utilities
"""

from muutils.misc.hashing import stable_hash
from muutils.misc.sequence import (
    WhenMissing,
    empty_sequence_if_attr_false,
    flatten,
    list_split,
    list_join,
    apply_mapping,
    apply_mapping_chain,
)
from muutils.misc.string import (
    sanitize_name,
    sanitize_fname,
    sanitize_identifier,
    dict_to_filename,
    dynamic_docstring,
)
from muutils.misc.numerical import (
    shorten_numerical_to_str,
    str_to_numeric,
    _SHORTEN_MAP,
)
from muutils.misc.freezing import (
    FrozenDict,
    FrozenList,
    freeze,
)
from muutils.misc.classes import (
    is_abstract,
    get_all_subclasses,
    isinstance_by_type_name,
    IsDataclass,
    get_hashable_eq_attrs,
    dataclass_set_equals,
)


__all__ = [
    # submodules
    "classes",
    "freezing",
    "func",
    "hashing",
    "numerical",
    "sequence",
    "string",
    # imports
    "stable_hash",
    "WhenMissing",
    "empty_sequence_if_attr_false",
    "flatten",
    "list_split",
    "list_join",
    "apply_mapping",
    "apply_mapping_chain",
    "sanitize_name",
    "sanitize_fname",
    "sanitize_identifier",
    "dict_to_filename",
    "dynamic_docstring",
    "shorten_numerical_to_str",
    "str_to_numeric",
    "_SHORTEN_MAP",
    "FrozenDict",
    "FrozenList",
    "freeze",
    "is_abstract",
    "get_all_subclasses",
    "isinstance_by_type_name",
    "IsDataclass",
    "get_hashable_eq_attrs",
    "dataclass_set_equals",
]
