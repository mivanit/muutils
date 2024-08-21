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
