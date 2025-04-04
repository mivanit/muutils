from __future__ import annotations

from pathlib import Path
from typing import Any, List, Tuple

import numpy as np
import pytest
import torch

import muutils.tensor_info as tensor_info
from muutils.tensor_info import array_summary, generate_sparkline

TEMP_PATH: Path = Path("tests/_temp")

# Check if torch supports the "meta" device.
meta_supported: bool = False
if torch is not None:
    try:
        torch.empty(1, device="meta")
        meta_supported = True
    except Exception:
        meta_supported = False


# Helper function to generate an input based on type and a flag for tensor's requires_grad.
def generate_input(input_type: str, tensor_requires_grad: bool) -> Any:
    """
    Generate an input array or tensor according to input_type.

    Parameters:
     - `input_type : str`
             Must be one of:
             "numpy_normal", "numpy_with_nan", "numpy_empty",
             "torch_cpu", "torch_cpu_nan", "torch_meta", "torch_meta_nan"
     - `tensor_requires_grad : bool`
             For torch arrays, set requires_grad accordingly (ignored for numpy).

    Returns:
     - Array-like input.
    """
    if input_type.startswith("numpy"):
        if input_type == "numpy_normal":
            return np.array([1, 2, 3, 4, 5])
        elif input_type == "numpy_with_nan":
            return np.array([np.nan, 1, 2, np.nan, 3])
        elif input_type == "numpy_empty":
            return np.array([])
        else:
            raise ValueError("Unknown numpy input type")
    elif torch is not None and input_type.startswith("torch"):
        if "cpu" in input_type:
            device_str: str = "cpu"
        elif "meta" in input_type:
            device_str = "meta"
        else:
            device_str = "cpu"
        if "with_nan" in input_type:
            data = [float("nan"), 1.0, 2.0, float("nan"), 3.0]
        else:
            data = [1.0, 2.0, 3.0, 4.0, 5.0]
        return torch.tensor(data, device=device_str, requires_grad=tensor_requires_grad)
    else:
        raise ValueError("Unknown input type or torch not available")


# Define option dictionaries covering a variety of settings.
option_dicts: List[dict] = [
    # All defaults (most verbose, no sparkline)
    {
        "fmt": "unicode",
        "sparkline": False,
        "colored": False,
        "as_list": False,
        "stats": True,
        "shape": True,
        "dtype": True,
        "device": True,
        "call_requires_grad": True,
        "eq_char": "=",
        "sparkline_bins": 5,
        "sparkline_logy": False,
    },
    # Turn off most extra info; sparkline on with different bin count and log scale
    {
        "fmt": "latex",
        "sparkline": True,
        "colored": True,
        "as_list": True,
        "stats": False,
        "shape": False,
        "dtype": False,
        "device": False,
        "call_requires_grad": False,
        "eq_char": ":",
        "sparkline_bins": 10,
        "sparkline_logy": True,
    },
    # Mixed options with ascii format and some extras off
    {
        "fmt": "ascii",
        "sparkline": True,
        "colored": False,
        "as_list": False,
        "stats": True,
        "shape": False,
        "dtype": True,
        "device": False,
        "call_requires_grad": True,
        "eq_char": "=",
        "sparkline_bins": 5,
        "sparkline_logy": True,
    },
    # All features on, but no gradient info requested in the summary call.
    {
        "fmt": "unicode",
        "sparkline": True,
        "colored": True,
        "as_list": True,
        "stats": True,
        "shape": True,
        "dtype": True,
        "device": True,
        "call_requires_grad": False,
        "eq_char": ":",
        "sparkline_bins": 10,
        "sparkline_logy": False,
    },
]

# Build a list of (input_type, tensor_requires_grad) tuples.
# For numpy inputs, the tensor_requires_grad flag is irrelevant.
input_params: List[Tuple[str, bool]] = [
    ("numpy_normal", False),
    ("numpy_with_nan", False),
    ("numpy_empty", False),
]

if torch is not None:
    # Torch CPU inputs: test both with and without grad.
    input_params.extend(
        [
            ("torch_cpu", True),
            ("torch_cpu", False),
            ("torch_cpu_nan", True),
            ("torch_cpu_nan", False),
        ]
    )
    if meta_supported:
        input_params.extend(
            [
                ("torch_meta", True),
                ("torch_meta", False),
                ("torch_meta_nan", True),
                ("torch_meta_nan", False),
            ]
        )


@pytest.mark.parametrize(
    "options", option_dicts
)  # , ids=lambda opt: f'opts_{opt["fmt"]}_spark{opt["sparkline"]}_col{opt["colored"]}')
@pytest.mark.parametrize(
    "input_type,tensor_requires_grad", input_params
)  # , ids=lambda p: f'{p[0]}_grad{p[1]}')
def test_array_summary_comprehensive(
    input_type: str, tensor_requires_grad: bool, options: dict
) -> None:
    """
    Comprehensive test for array_summary.

    This test uses a wide range of parameter combinations for both numpy and torch
    inputs (including with/without NaNs and empty arrays) and a set of option dictionaries.
    The resulting summary string (or list of strings) is written to two output files along with an explanation.
    The file content is then checked for expected substrings based on the input type and option settings.
    """
    # Generate the input.
    arr: Any = generate_input(input_type, tensor_requires_grad)

    # Call array_summary with the options.
    summary: Any = array_summary(  # type: ignore[call-overload]
        arr,
        fmt=options["fmt"],
        sparkline=options["sparkline"],
        colored=options["colored"],
        as_list=options["as_list"],
        stats=options["stats"],
        shape=options["shape"],
        dtype=options["dtype"],
        device=options["device"],
        requires_grad=options["call_requires_grad"],
        eq_char=options["eq_char"],
        sparkline_bins=options["sparkline_bins"],
        sparkline_logy=options["sparkline_logy"],
    )

    print(f"{arr = }")
    print(f"{options = }")
    print(f"{summary = }")

    # If as_list is True, join to a string for checking.
    summary_str: str = summary if isinstance(summary, str) else " ".join(summary)

    # Write explanation and summary to output files.
    output_dir = TEMP_PATH / "tensor_info"
    output_dir.mkdir(parents=True, exist_ok=True)
    tex_file = output_dir / "tensor_info_outputs.tex"
    txt_file = output_dir / "tensor_info_outputs.txt"
    explanation: str = f"Test: {input_type} with tensor_requires_grad={tensor_requires_grad} and options={options}\n"
    with open(tex_file, "a") as f_tex, open(txt_file, "a") as f_txt:
        f_tex.write(explanation + summary_str + "\n")
        f_txt.write(explanation + summary_str + "\n")

    # --- Now perform our assertions ---
    # If the input is empty, the summary should mention "empty array".
    if (hasattr(arr, "size") and arr.size == 0) or (
        torch is not None and isinstance(arr, torch.Tensor) and arr.numel() == 0
    ):
        assert (
            "empty" in summary_str.lower()
        ), f"Expected 'empty' in summary for {input_type}"
    else:
        # For non-empty arrays, if the options ask for dtype and shape info, they should appear.
        if options["dtype"]:
            assert (
                "dtype" in summary_str.lower()
            ), f"Expected 'dtype' info in summary for {input_type}"
        if options["shape"]:
            assert (
                "shape" in summary_str.lower()
            ), f"Expected 'shape' info in summary for {input_type}"
        # For torch inputs with device info requested.
        if torch is not None and isinstance(arr, torch.Tensor) and options["device"]:
            assert (
                "device" in summary_str.lower()
            ), f"Expected 'device' info in summary for {input_type}"
        # For arrays with NaNs, if not empty, a warning should be present.
        if input_type.endswith("with_nan"):
            assert (
                "nan" in summary_str.lower() or "nAN" in summary_str
            ), f"Expected NaN warning in summary for {input_type}"
        # Check that the equality character appears in the summary (or its an error)
        assert (
            options["eq_char"] in summary_str
            or tensor_info.SYMBOLS[options["fmt"]]["warning"] in summary_str
        ), f"Expected eq_char '{options['eq_char']}' in summary for {input_type}"
        # If stats are enabled, at least one statistic (e.g. mean) should appear.
        if options["stats"] and not (
            ("empty" in summary_str.lower()) or ("all nan" in summary_str.lower())
        ):
            # The symbol for mean depends on format.
            if options["fmt"] == "unicode":
                assert (
                    "μ" in summary_str
                ), f"Expected unicode mean symbol in summary for {input_type}"
            elif options["fmt"] == "latex":
                assert (
                    r"\mu" in summary_str
                ), f"Expected latex mean symbol in summary for {input_type}"
            elif options["fmt"] == "ascii":
                assert (
                    "mean" in summary_str
                ), f"Expected ascii 'mean' in summary for {input_type}"
        # If sparkline is enabled and the input is non-empty (and not all NaN) then a sparkline should appear.
        if (
            options["sparkline"]
            and summary_str
            and not (
                ("empty" in summary_str.lower()) or ("all nan" in summary_str.lower())
            )
        ):
            # We expect at least one vertical bar or sparkline characters.
            assert "|" in summary_str or any(
                c in summary_str for c in "▁▂▃▄▅▆▇█_-~=#"
            ), f"Expected sparkline in summary for {input_type}"


@pytest.mark.parametrize(
    "bad_input",
    [
        42,
        "not an array",
        {"a": 1},
        None,
    ],
)
def test_array_summary_failure(bad_input: Any) -> None:
    """
    Test that array_summary returns a summary indicating failure or empty array
    when given non–array inputs.
    """
    summary = array_summary(bad_input)
    summary_str: str = summary if isinstance(summary, str) else " ".join(summary)
    assert summary_str


def test_generate_sparkline_basic() -> None:
    """
    Test the sparkline generator with a fixed histogram.
    """
    histogram: np.ndarray = np.array([1, 3, 5, 2, 0])
    spark: str = generate_sparkline(histogram, format="unicode", log_y=False)
    assert isinstance(spark, str)
    assert len(spark) == len(histogram)
    # Test with log_y=True
    spark_log: str = generate_sparkline(histogram, format="ascii", log_y=True)
    assert isinstance(spark_log, str)
    assert len(spark_log) == len(histogram)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(["--maxfail=1", "--disable-warnings", "-q"]))
