import inspect
import tempfile
from pathlib import Path
import importlib
from typing import Any, Callable, Optional, List, Tuple
import re

import pytest

from muutils.dbg import (
    dbg,
    _NoExpPassed,
    _process_path,
    _CWD,
    # we do use this as a global in `test_dbg_counter_increments`
    _COUNTER,  # noqa: F401
    grep_repr,
    _normalize_for_loose,
    _compile_pattern,
)


DBG_MODULE_NAME: str = "muutils.dbg"

# ============================================================================
# Dummy Tensor classes for testing tensor_info* functions
# ============================================================================


class DummyTensor:
    """A dummy tensor whose sum is NaN."""

    shape: Tuple[int, ...] = (2, 3)
    dtype: str = "float32"
    device: str = "cpu"
    requires_grad: bool = False

    def sum(self) -> float:
        return float("nan")


class DummyTensorNormal:
    """A dummy tensor with a normal sum."""

    shape: Tuple[int, ...] = (4, 5)
    dtype: str = "int32"
    device: str = "cuda"
    requires_grad: bool = True

    def sum(self) -> float:
        return 20.0


class DummyTensorPartial:
    """A dummy tensor with only a shape attribute."""

    shape: Tuple[int, ...] = (7,)


# ============================================================================
# Additional Tests for dbg and tensor_info functionality
# ============================================================================


# --- Tests for _process_path (existing ones) ---
def test_process_path_absolute(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        importlib.import_module(DBG_MODULE_NAME), "PATH_MODE", "absolute"
    )
    test_path: Path = Path("somefile.txt")
    expected: str = test_path.absolute().as_posix()
    result: str = _process_path(test_path)
    assert result == expected


def test_process_path_relative_inside_common(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        importlib.import_module(DBG_MODULE_NAME), "PATH_MODE", "relative"
    )
    test_path: Path = _CWD / "file.txt"
    expected: str = "file.txt"
    result: str = _process_path(test_path)
    assert result == expected


def test_process_path_relative_outside_common(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        importlib.import_module(DBG_MODULE_NAME), "PATH_MODE", "relative"
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_path: Path = Path(tmp_dir) / "file.txt"
        expected: str = test_path.absolute().as_posix()
        result: str = _process_path(test_path)
        assert result == expected


def test_process_path_invalid_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        importlib.import_module(DBG_MODULE_NAME), "PATH_MODE", "invalid"
    )
    with pytest.raises(
        ValueError, match="PATH_MODE must be either 'relative' or 'absolute"
    ):
        _process_path(Path("anything.txt"))


# --- Tests for dbg ---
def test_dbg_with_expression(capsys: pytest.CaptureFixture) -> None:
    result: int = dbg(1 + 2)
    captured: str = capsys.readouterr().err
    assert "= 3" in captured
    # check that the printed string includes some form of "1+2"
    assert "1+2" in captured.replace(" ", "") or "1 + 2" in captured
    assert result == 3


def test_dbg_without_expression(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(importlib.import_module(DBG_MODULE_NAME), "_COUNTER", 0)
    result: Any = dbg()
    captured: str = capsys.readouterr().err.strip()
    assert "<dbg 0>" in captured
    no_exp_passed: Any = _NoExpPassed
    assert result is no_exp_passed


def test_dbg_custom_formatter(capsys: pytest.CaptureFixture) -> None:
    custom_formatter: Callable[[Any], str] = lambda x: "custom"  # noqa: E731
    result: str = dbg("anything", formatter=custom_formatter)
    captured: str = capsys.readouterr().err
    assert "custom" in captured
    assert result == "anything"


def test_dbg_complex_expression(capsys: pytest.CaptureFixture) -> None:
    # Test a complex expression (lambda invocation)
    result: int = dbg((lambda x: x * x)(5))
    captured: str = capsys.readouterr().err
    assert (
        "lambda" in captured
    )  # expecting the extracted code snippet to include 'lambda'
    assert "25" in captured  # evaluated result is 25
    assert result == 25


def test_dbg_multiline_code_context(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    # Create a fake stack with two frames; the first frame does not contain "dbg",
    # but the second does.
    class FakeFrame:
        def __init__(
            self, code_context: Optional[List[str]], filename: str, lineno: int
        ) -> None:
            self.code_context = code_context
            self.filename = filename
            self.lineno = lineno

    def fake_inspect_stack() -> List[Any]:
        return [
            FakeFrame(["not line"], "frame1.py", 20),
            FakeFrame(["dbg(2+2)", "ignored line"], "frame2.py", 30),
        ]

    monkeypatch.setattr(inspect, "stack", fake_inspect_stack)
    result: int = dbg(2 + 2)
    captured: str = capsys.readouterr().err
    print(captured)
    assert "2+2" in captured
    assert "4" in captured
    assert result == 4


def test_dbg_counter_increments(capsys: pytest.CaptureFixture) -> None:
    global _COUNTER
    _COUNTER = 0
    dbg()
    out1: str = capsys.readouterr().err
    dbg()
    out2: str = capsys.readouterr().err
    assert "<dbg 0>" in out1
    assert "<dbg 1>" in out2


def test_dbg_formatter_exception() -> None:
    def bad_formatter(x: Any) -> str:
        raise ValueError("formatter error")

    with pytest.raises(ValueError, match="formatter error"):
        dbg(123, formatter=bad_formatter)


def test_dbg_incomplete_expression(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    # Simulate a frame with an incomplete expression (no closing parenthesis)
    class FakeFrame:
        def __init__(
            self, code_context: Optional[List[str]], filename: str, lineno: int
        ) -> None:
            self.code_context = code_context
            self.filename = filename
            self.lineno = lineno

    def fake_inspect_stack() -> List[Any]:
        return [FakeFrame(["dbg(42"], "fake_incomplete.py", 100)]

    monkeypatch.setattr(inspect, "stack", fake_inspect_stack)
    result: int = dbg(42)
    captured: str = capsys.readouterr().err
    # The extracted expression should be "42" (since there's no closing parenthesis)
    assert "42" in captured
    assert result == 42


def test_dbg_non_callable_formatter() -> None:
    with pytest.raises(TypeError):
        dbg(42, formatter="not callable")  # type: ignore


# # --- Tests for tensor_info_dict and tensor_info ---
# def test_tensor_info_dict_with_nan() -> None:
#     tensor: DummyTensor = DummyTensor()
#     info: Dict[str, str] = tensor_info_dict(tensor)
#     expected: Dict[str, str] = {
#         "shape": repr((2, 3)),
#         "sum": repr(float("nan")),
#         "dtype": repr("float32"),
#         "device": repr("cpu"),
#         "requires_grad": repr(False),
#     }
#     assert info == expected


# def test_tensor_info_dict_normal() -> None:
#     tensor: DummyTensorNormal = DummyTensorNormal()
#     info: Dict[str, str] = tensor_info_dict(tensor)
#     expected: Dict[str, str] = {
#         "shape": repr((4, 5)),
#         "dtype": repr("int32"),
#         "device": repr("cuda"),
#         "requires_grad": repr(True),
#     }
#     assert info == expected


# def test_tensor_info_dict_partial() -> None:
#     tensor: DummyTensorPartial = DummyTensorPartial()
#     info: Dict[str, str] = tensor_info_dict(tensor)
#     expected: Dict[str, str] = {"shape": repr((7,))}
#     assert info == expected


# def test_tensor_info() -> None:
#     tensor: DummyTensorNormal = DummyTensorNormal()
#     info_str: str = tensor_info(tensor)
#     expected: str = ", ".join(
#         [
#             f"shape={repr((4, 5))}",
#             f"dtype={repr('int32')}",
#             f"device={repr('cuda')}",
#             f"requires_grad={repr(True)}",
#         ]
#     )
#     assert info_str == expected


# def test_tensor_info_dict_no_attributes() -> None:
#     class DummyEmpty:
#         pass

#     dummy = DummyEmpty()
#     info: Dict[str, str] = tensor_info_dict(dummy)
#     assert info == {}


# def test_tensor_info_no_attributes() -> None:
#     class DummyEmpty:
#         pass

#     dummy = DummyEmpty()
#     info_str: str = tensor_info(dummy)
#     assert info_str == ""


# def test_dbg_tensor(capsys: pytest.CaptureFixture) -> None:
#     tensor: DummyTensorPartial = DummyTensorPartial()
#     result: DummyTensorPartial = dbg_tensor(tensor)  # type: ignore
#     captured: str = capsys.readouterr().err
#     assert "shape=(7,)" in captured
#     assert result is tensor


# ============================================================================
# Tests for grep_repr functionality
# ============================================================================


def test_normalize_for_loose() -> None:
    assert _normalize_for_loose("hello_world") == "hello world"
    assert _normalize_for_loose("doThing") == "doThing"  # camelCase preserved
    assert _normalize_for_loose("DO-THING") == "DO THING"
    assert _normalize_for_loose("a__b__c") == "a b c"
    assert _normalize_for_loose("test.method()") == "test method"
    assert _normalize_for_loose("   spaces   ") == "spaces"


def test_compile_pattern_case_sensitivity() -> None:
    # String patterns default to case-insensitive
    pattern = _compile_pattern("hello")
    assert pattern.match("HELLO") is not None
    assert pattern.match("Hello") is not None

    # With cased=True, string patterns are case-sensitive
    pattern_cased = _compile_pattern("hello", cased=True)
    assert pattern_cased.match("HELLO") is None
    assert pattern_cased.match("hello") is not None


def test_compile_pattern_loose() -> None:
    pattern = _compile_pattern("hello world", loose=True)
    # Pattern should be normalized
    assert pattern.pattern == "hello world"


def test_grep_repr_basic_match(capsys: pytest.CaptureFixture) -> None:
    test_list = [1, 2, 42, 3, 4]
    grep_repr(test_list, "42")
    captured = capsys.readouterr().out
    assert "42" in captured
    assert captured.count("42") >= 1


def test_grep_repr_no_match(capsys: pytest.CaptureFixture) -> None:
    test_list = [1, 2, 3, 4]
    grep_repr(test_list, "999")
    captured = capsys.readouterr().out
    assert captured.strip() == ""


def test_grep_repr_case_insensitive_default(capsys: pytest.CaptureFixture) -> None:
    test_dict = {"Hello": "World"}
    grep_repr(test_dict, "hello")  # Should match "Hello" by default
    captured = capsys.readouterr().out
    assert "Hello" in captured


def test_grep_repr_case_sensitive(capsys: pytest.CaptureFixture) -> None:
    test_dict = {"Hello": "World"}
    grep_repr(test_dict, "hello", cased=True)  # Should NOT match
    captured = capsys.readouterr().out
    assert captured.strip() == ""


def test_grep_repr_loose_matching(capsys: pytest.CaptureFixture) -> None:
    class TestObj:
        def __repr__(self) -> str:
            return "method_name(arg_value)"

    obj = TestObj()
    grep_repr(obj, "method name", loose=True)
    captured = capsys.readouterr().out
    # With loose=True, both pattern and text are normalized, so we should see "method name" highlighted
    assert "method name" in captured


def test_grep_repr_char_context(capsys: pytest.CaptureFixture) -> None:
    test_string = "prefix_42_suffix"
    grep_repr(test_string, "42", char_context=3)
    captured = capsys.readouterr().out
    # Should show 3 chars before and after: "ix_42_su"
    assert "ix_" in captured and "_su" in captured


def test_grep_repr_char_context_zero(capsys: pytest.CaptureFixture) -> None:
    test_string = "prefix_42_suffix"
    grep_repr(test_string, "42", char_context=0)
    captured = capsys.readouterr().out
    # Should only show the match itself
    lines = captured.strip().split("\n")
    assert len(lines) == 1
    assert "42" in lines[0]


def test_grep_repr_line_context(capsys: pytest.CaptureFixture) -> None:
    test_obj = {"line1": 1, "line2": 2, "target": 42, "line4": 4}
    grep_repr(test_obj, "42", line_context=1)
    captured = capsys.readouterr().out
    assert "42" in captured


def test_grep_repr_before_after_context(capsys: pytest.CaptureFixture) -> None:
    class MultilineRepr:
        def __repr__(self) -> str:
            return "line1\nline2\ntarget_line\nline4\nline5"

    multiline_obj = MultilineRepr()
    grep_repr(multiline_obj, "target", before_context=1, after_context=1)
    captured = capsys.readouterr().out
    assert "line2" in captured
    assert "target" in captured
    assert "line4" in captured


def test_grep_repr_context_shortcut(capsys: pytest.CaptureFixture) -> None:
    class MultilineRepr:
        def __repr__(self) -> str:
            return "line1\nline2\ntarget_line\nline4\nline5"

    multiline_obj = MultilineRepr()
    grep_repr(multiline_obj, "target", context=1)
    captured = capsys.readouterr().out
    assert "line2" in captured
    assert "target" in captured
    assert "line4" in captured


def test_grep_repr_max_count(capsys: pytest.CaptureFixture) -> None:
    test_list = [42, 42, 42, 42, 42]  # 5 matches in repr
    grep_repr(
        test_list, "42", max_count=2, char_context=0
    )  # No context to avoid duplicates
    captured = capsys.readouterr().out
    # Should only show 2 match blocks due to max_count=2
    lines = [line for line in captured.strip().split("\n") if line and line != "--"]
    assert len(lines) == 2


def test_grep_repr_line_numbers(capsys: pytest.CaptureFixture) -> None:
    # Create an object whose repr contains actual newlines
    class MultilineRepr:
        def __repr__(self) -> str:
            return "line1\nline2\ntarget_line\nline4"

    multiline_obj = MultilineRepr()
    grep_repr(multiline_obj, "target", line_context=1, line_numbers=True)
    captured = capsys.readouterr().out
    assert "3:" in captured  # Line number for target line
    assert "2:" in captured  # Line number for context
    assert "4:" in captured  # Line number for context


def test_grep_repr_no_highlight(capsys: pytest.CaptureFixture) -> None:
    test_list = [1, 2, 42, 3]
    grep_repr(test_list, "42", highlight=False)
    captured = capsys.readouterr().out
    # Should not contain ANSI escape sequences
    assert "\033[" not in captured
    assert "42" in captured


def test_grep_repr_custom_color(capsys: pytest.CaptureFixture) -> None:
    test_list = [1, 2, 42, 3]
    grep_repr(test_list, "42", color="32")  # Green instead of red
    captured = capsys.readouterr().out
    assert "\033[1;32m" in captured  # Green color code


def test_grep_repr_custom_separator(capsys: pytest.CaptureFixture) -> None:
    test_list = [42, 99, 42]  # Multiple matches
    grep_repr(test_list, r"\d+", separator="---")
    captured = capsys.readouterr().out
    assert "---" in captured


def test_grep_repr_quiet_mode() -> None:
    test_list = [1, 2, 42, 3]
    result = grep_repr(test_list, "42", quiet=True)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) >= 1
    assert any("42" in line for line in result)


def test_grep_repr_multiple_matches(capsys: pytest.CaptureFixture) -> None:
    test_dict = {"key1": 42, "key2": 24, "key3": 42}
    grep_repr(test_dict, "42")
    captured = capsys.readouterr().out
    # Should show multiple matches
    assert captured.count("42") >= 2


def test_grep_repr_regex_pattern(capsys: pytest.CaptureFixture) -> None:
    test_list = [1, 22, 333, 4444]
    grep_repr(test_list, r"\d{3}")  # Exactly 3 digits
    captured = capsys.readouterr().out
    assert "333" in captured
    # Note: "4444" contains "444" which matches \d{3}, so it will be highlighted
    assert "444" in captured
    # The whole list repr is shown, so "22" will be in the output but not highlighted
    # Check that 333 and 444 are highlighted (contain ANSI codes) but 22 is not
    assert "\033[1;31m333\033[0m" in captured
    assert "\033[1;31m444\033[0m" in captured


def test_grep_repr_compiled_regex(capsys: pytest.CaptureFixture) -> None:
    import re

    test_string = "Hello World"
    pattern = re.compile(r"hello", re.IGNORECASE)
    grep_repr(test_string, pattern)
    captured = capsys.readouterr().out
    assert "Hello" in captured


def test_grep_repr_empty_pattern(capsys: pytest.CaptureFixture) -> None:
    test_list = [1, 2, 3]
    # Empty pattern matches everything, should not raise an error but show all content
    grep_repr(test_list, "", char_context=0)
    captured = capsys.readouterr().out
    # Empty pattern should match at every position, but with char_context=0 should show minimal output
    assert len(captured.strip()) > 0


def test_grep_repr_invalid_regex() -> None:
    test_list = [1, 2, 3]
    with pytest.raises(re.error):
        grep_repr(test_list, "[invalid")


def test_grep_repr_large_object() -> None:
    large_dict = {f"key_{i}": i for i in range(1000)}
    large_dict["special_key"] = 42

    # Should handle large objects without issues
    result = grep_repr(large_dict, "special_key", quiet=True)
    assert result is not None
    assert any("special_key" in line for line in result)


def test_grep_repr_nested_objects(capsys: pytest.CaptureFixture) -> None:
    nested = {"outer": {"inner": {"value": 42}}}
    grep_repr(nested, "42")
    captured = capsys.readouterr().out
    assert "42" in captured


def test_grep_repr_custom_objects(capsys: pytest.CaptureFixture) -> None:
    class CustomObject:
        def __repr__(self) -> str:
            return "CustomObject(special_value=123)"

    obj = CustomObject()
    grep_repr(obj, "special_value")
    captured = capsys.readouterr().out
    assert "special_value" in captured
