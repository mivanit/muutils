import inspect
import tempfile
from pathlib import Path
import importlib
from typing import Any, Callable, Optional, List, Tuple

import pytest

from muutils.dbg import (
    dbg,
    _NoExpPassed,
    _process_path,
    _CWD,
    # we do use this as a global in `test_dbg_counter_increments`
    _COUNTER,  # noqa: F401
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
