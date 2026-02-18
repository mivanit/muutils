
Type system overhaul achieving full compliance with ty, basedpyright, and mypy (thanks to updated makefile). Python 3.14 support added, 3.8 compatibility maintained. New `Command` class. Serialization fixes for sets, frozensets, and namedtuples. Test suite expanded.

165 commits since `c812aaf`

## Added

- **Python 3.14 support** - Added to test matrix (`f140cb5`)
- **`Command` class** - Typed subprocess wrapper with env, shell, and inheritance support (`8446d8e`)
- **`doc` parameter for dataclass fields** - Replaces deprecated `description` parameter, with Python 3.14 compatibility (`b47a772`, `19aff29`, `e4e4cf0`)
- **`json_serialize.types` module** - Centralized type definitions to avoid import cycles (`54d8e10`)
- **`typing_breakdown` module** - CLI tool for analyzing mypy/basedpyright/ty outputs and generating error breakdowns
- **`@overload` signatures** - Added to `serialize_array()`, `load_array()`, `infer_array_mode()`, `json_serialize()` for better type narrowing (`494cd9d`)
- **TypedDict definitions** - `ArrayMetadata`, `SerializedArrayWithMeta`, `NumericList`, `_SerializedSet`, `_SerializedFrozenset`, `DBGDictDefaultsType`, `DBGListDefaultsType`, `DBGTensorArraySummaryDefaultsType`
- **New tests** - `test_collect_warnings.py`, `test_jsonlines.py`, `test_tensor_info_torch.py`, `test_configure_notebook_torch.py`, `test_json_serialize.py`, `test_serializable_field.py`, `test_arg_bool.py`, `test_command.py` (`573ef83`)

## Changed

- **Type system overhaul** - Full compliance with ty, basedpyright, and mypy type checkers
- **`JSONitem` type is now recursive** - Simplified from flattened union to proper recursive `Sequence["JSONitem"]` (`d004e54`)
- **Literal types for format key and ref key** - `_FORMAT_KEY` and `_REF_KEY` now use `Literal` types (`b78c960`)
- **Set/frozenset serialization** - Now uses format-key metadata: `{__muutils_format__: "set", data: [...]}` (`49ee854`)
- **Namedtuple serialization** - Uses `_asdict()` method, preserves field names (`49ee854`)
- **Handler ordering** - Namedtuple handler moved from DEFAULT_HANDLERS to BASE_HANDLERS (`49ee854`)
- **Split torch and non-torch tests** - Tests ending in `_torch.py` skipped when torch unavailable (`f432bd1`, `42f626d`)
- **README rewrite** - All 26 modules documented in table format, added 16 previously undocumented modules (`5203836`)
- **Makefile restructuring** - Merged and updated makefile template (`a3ca613`, `50d14a6`, `cd00b94`)
- **Warn on deprecated `description` parameter usage** (`60f9103`)
- **`muutils.logger`**: `Logger.log()` and `SimpleLogger.log()` now require keyword arguments for all parameters after `msg`. This change was made to fix type checker compatibility between the two classes.

  **Before:**
  ```python
  logger.log("message", -10)  # lvl as positional arg
  ```

  **After:**
  ```python
  logger.log("message", lvl=-10)  # lvl as keyword arg
  ```


## Fixed

- **`Distribution.name` in `SysInfo.pip()`** - Use `.metadata["Name"]` for Python <3.10 compatibility (`f0bb63b`)
- **`SerializableField` not passing `doc` to init** (`30d0cb0`)
- **Array serialization** - Removed 0-dim list mode, added TypedDict definitions for type safety (`e90cfa0`)
- **`_recursive_hashify()`** - Check scalar types before Iterables, prevents infinite recursion (`49ee854`)
- **ErrorMode comparison** - Compare against enum values instead of strings (`49ee854`)
- **Iterable handler** - Restricted to not match lists, tuples, or strings (`49ee854`)
- **Matrix powers benchmark** - Warn instead of expect when slower, fixes stochastic test failures (`178f2f8`)
- **PyTorch `_remote_module_non_scriptable` coverage error** (`ba29619`)
- **Weasyprint compatibility** (`e85fa01`)
- **`@override` import** (`eb5fda6`)
- **pytest 9 deprecation warning** - Renamed `path` to `collection_path` in hook (`08edae0`)
- **Pillow deprecation warning on Python 3.9** (`2fc1cf8`)
- **`muutils.json_serialize.util.dc_eq`**: Fixed docstring that incorrectly stated `except_when_field_mismatch` defaults to `True` (actual default is `False`), and that it raises `TypeError` (it actually raises `AttributeError`)
- **`muutils.json_serialize.util.dc_eq`**: Updated flowchart in docstring to accurately reflect the control flow, including the missing `false_when_class_mismatch` decision branch

## Python Compatibility

- **Python 3.8** - Type hint fixes, legacy package pins (pandas 2.0.3, pillow 10.4.0) (`4e085ff`, `08fe412`)
- **Python 3.9** - Added `from __future__ import annotations` for union syntax (`88942df`)
- **Python 3.10** - Fixed torch.backends.mps import warnings (`3516df8`)
- **Python <3.11** - Restored `COMPATIBILITY_MODE` for type checking (`e09eecc`)
- **Python 3.14** - torch exists for this now, so removed compatibility casing

## Dependencies

- Updated `uv.lock`
- Bumped ty dev dependency (`a9fc10d`)
- Added stubs (dev) (`e31eea0`)
