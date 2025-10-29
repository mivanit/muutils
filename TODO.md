# Mypy Type Error Fixes

## Source Files (Priority 1)

### muutils/jsonlines.py
- Line 63-68: Change `items: Sequence[JSONitem]` to `items: Sequence[Any]`
- Current signature is too restrictive for actual usage patterns

### muutils/logger/log_util.py
- Line 47: Change `keys: tuple[str]` to `keys: tuple[str, ...]` in `gather_val()`
- Line 5: Change return type from `None` to `Any` in `get_any_from_stream()`

### muutils/json_serialize/array.py
- Line 167: Change `load_array()` return type from `Any` to `np.ndarray`

## Test Files (Priority 2)

### tests/unit/json_serialize/test_json_serialize.py
Lines 129-130, 151-152, 496-497, 502-505, 709-711, 745:
- Add `assert isinstance(result, dict)` before dict operations
- Or use `cast(dict[str, Any], result)`

Lines 266, 723, 730:
- Add `assert isinstance(result["key"], list)` before calling `set()`

Line 656:
- Pass `error_mode=ErrorMode.EXCEPT` instead of string

### tests/unit/json_serialize/test_serializable_field.py
Line 127:
- Remove incorrect indexing of Field object

Line 143:
- Add type annotation: `dc_field2: Field[list] = field(default_factory=list)`

Lines 312-334:
- Fix variable assignments - `serializable_field()` returns SerializableField, not primitive values
- Don't access `.default`, `.repr`, `.hash`, etc. on non-Field objects

### tests/unit/json_serialize/test_array.py
Lines 122, 125, 128, 138, 195-197:
- Add `assert isinstance(loaded, np.ndarray)` after `load_array()` calls

Lines 154-156, 166-167:
- Add dict type assertions before indexing serialized results

### tests/unit/json_serialize/test_array_torch.py
Lines 23, 30, 37:
- Add `assert isinstance(shape, list)` before `in` checks

Lines 126, 146:
- Add type ignore or change signature to accept torch.Tensor

Lines 191-193, 195-196, 198, 201-202, 221-224, 227-228:
- Add dict type assertions before indexing

### tests/unit/test_jsonlines.py
Lines 40-41:
- Add dict type assertions before indexing

Lines 59, 94, 106, 112, 136, 150, 167, 188, 192:
- Will be fixed by jsonl_write signature change

### tests/unit/logger/test_log_util.py
Lines 35, 77, 116:
- Will be fixed by jsonl_write signature change

Lines 119, 129, 137, 140, 145:
- Will be fixed by gather_val signature change

Lines 159, 163, 167:
- Will be fixed by get_any_from_stream return type change

### tests/unit/benchmark_parallel/benchmark_parallel.py
Lines 197, 208, 219, 234, 251 (task_type, save_path), 283, 308:
- Add `| None` to type hints: `param: Type = None` → `param: Type | None = None`

Line 399:
- Change parameter type from `list[int]` to `Sequence[int]` or cast argument

Lines 416, 419, 422:
- Change parameter types to accept `str | Path` or cast Path to str

### tests/unit/benchmark_parallel/test_benchmark_demo.py
Line 10:
- Change `main()` signature to accept `base_path: str | Path`
- Or wrap string in `Path()` call

## Total Errors
157 errors across 8 files
