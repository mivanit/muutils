"get metadata about a tensor, mostly for `muutils.dbg`"

from __future__ import annotations

import numpy as np
from typing import Union, Any, Literal, List, Dict, overload, Optional

# Global color definitions
COLORS: Dict[str, Dict[str, str]] = {
    "latex": {
        "range": r"\textcolor{purple}",
        "mean": r"\textcolor{teal}",
        "std": r"\textcolor{orange}",
        "median": r"\textcolor{green}",
        "warning": r"\textcolor{red}",
        "shape": r"\textcolor{magenta}",
        "dtype": r"\textcolor{gray}",
        "device": r"\textcolor{gray}",
        "requires_grad": r"\textcolor{gray}",
        "sparkline": r"\textcolor{blue}",
        "torch": r"\textcolor{orange}",
        "dtype_bool": r"\textcolor{gray}",
        "dtype_int": r"\textcolor{blue}",
        "dtype_float": r"\textcolor{red!70}",  # 70% red intensity
        "dtype_str": r"\textcolor{red}",
        "device_cuda": r"\textcolor{green}",
        "reset": "",
    },
    "terminal": {
        "range": "\033[35m",  # purple
        "mean": "\033[36m",  # cyan/teal
        "std": "\033[33m",  # yellow/orange
        "median": "\033[32m",  # green
        "warning": "\033[31m",  # red
        "shape": "\033[95m",  # bright magenta
        "dtype": "\033[90m",  # gray
        "device": "\033[90m",  # gray
        "requires_grad": "\033[90m",  # gray
        "sparkline": "\033[34m",  # blue
        "torch": "\033[38;5;208m",  # bright orange
        "dtype_bool": "\033[38;5;245m",  # medium grey
        "dtype_int": "\033[38;5;39m",  # bright blue
        "dtype_float": "\033[38;5;167m",  # softer red/coral
        "device_cuda": "\033[38;5;76m",  # NVIDIA-style bright green
        "reset": "\033[0m",
    },
    "none": {
        "range": "",
        "mean": "",
        "std": "",
        "median": "",
        "warning": "",
        "shape": "",
        "dtype": "",
        "device": "",
        "requires_grad": "",
        "sparkline": "",
        "torch": "",
        "dtype_bool": "",
        "dtype_int": "",
        "dtype_float": "",
        "dtype_str": "",
        "device_cuda": "",
        "reset": "",
    },
}

OutputFormat = Literal["unicode", "latex", "ascii"]

SYMBOLS: Dict[OutputFormat, Dict[str, str]] = {
    "latex": {
        "range": r"\mathcal{R}",
        "mean": r"\mu",
        "std": r"\sigma",
        "median": r"\tilde{x}",
        "distribution": r"\mathbb{P}",
        "distribution_log": r"\mathbb{P}_L",
        "nan_values": r"\text{NANvals}",
        "warning": "!!!",
        "requires_grad": r"\nabla",
        "true": r"\checkmark",
        "false": r"\times",
    },
    "unicode": {
        "range": "R",
        "mean": "μ",
        "std": "σ",
        "median": "x̃",
        "distribution": "ℙ",
        "distribution_log": "ℙ˪",
        "nan_values": "NANvals",
        "warning": "🚨",
        "requires_grad": "∇",
        "true": "✓",
        "false": "✗",
    },
    "ascii": {
        "range": "range",
        "mean": "mean",
        "std": "std",
        "median": "med",
        "distribution": "dist",
        "distribution_log": "dist_log",
        "nan_values": "NANvals",
        "warning": "!!!",
        "requires_grad": "requires_grad",
        "true": "1",
        "false": "0",
    },
}
"Symbols for different formats"

SPARK_CHARS: Dict[OutputFormat, List[str]] = {
    "unicode": list(" ▁▂▃▄▅▆▇█"),
    "ascii": list(" _.-~=#"),
    "latex": list(" ▁▂▃▄▅▆▇█"),
}
"characters for sparklines in different formats"


def array_info(
    A: Any,
    hist_bins: int = 5,
) -> Dict[str, Any]:
    """Extract statistical information from an array-like object.

    # Parameters:
     - `A : array-like`
            Array to analyze (numpy array or torch tensor)

    # Returns:
     - `Dict[str, Any]`
            Dictionary containing raw statistical information with numeric values
    """
    result: Dict[str, Any] = {
        "is_tensor": None,
        "device": None,
        "requires_grad": None,
        "shape": None,
        "dtype": None,
        "size": None,
        "has_nans": None,
        "nan_count": None,
        "nan_percent": None,
        "min": None,
        "max": None,
        "range": None,
        "mean": None,
        "std": None,
        "median": None,
        "histogram": None,
        "bins": None,
        "status": None,
    }

    # Check if it's a tensor by looking at its class name
    # This avoids importing torch directly
    A_type: str = type(A).__name__
    result["is_tensor"] = A_type == "Tensor"

    # Try to get device information if it's a tensor
    if result["is_tensor"]:
        try:
            result["device"] = str(getattr(A, "device", None))
        except:  # noqa: E722
            pass

    # Convert to numpy array for calculations
    try:
        # For PyTorch tensors
        if result["is_tensor"]:
            # Check if tensor is on GPU
            is_cuda: bool = False
            try:
                is_cuda = bool(getattr(A, "is_cuda", False))
            except:  # noqa: E722
                pass

            if is_cuda:
                try:
                    # Try to get CPU tensor first
                    cpu_tensor = getattr(A, "cpu", lambda: A)()
                except:  # noqa: E722
                    A_np = np.array([])
            else:
                cpu_tensor = A
            try:
                # For CPU tensor, just detach and convert
                detached = getattr(cpu_tensor, "detach", lambda: cpu_tensor)()
                A_np = getattr(detached, "numpy", lambda: np.array([]))()
            except:  # noqa: E722
                A_np = np.array([])
        else:
            # For numpy arrays and other array-like objects
            A_np = np.asarray(A)
    except:  # noqa: E722
        A_np = np.array([])

    # Get basic information
    try:
        result["shape"] = A_np.shape
        result["dtype"] = str(A.dtype if result["is_tensor"] else A_np.dtype)
        result["size"] = A_np.size
        result["requires_grad"] = getattr(A, "requires_grad", None)
    except:  # noqa: E722
        pass

    # If array is empty, return early
    if result["size"] == 0:
        result["status"] = "empty array"
        return result

    # Flatten array for statistics if it's multi-dimensional
    try:
        if len(A_np.shape) > 1:
            A_flat = A_np.flatten()
        else:
            A_flat = A_np
    except:  # noqa: E722
        A_flat = A_np

    # Check for NaN values
    try:
        nan_mask = np.isnan(A_flat)
        result["nan_count"] = np.sum(nan_mask)
        result["has_nans"] = result["nan_count"] > 0
        if result["size"] > 0:
            result["nan_percent"] = (result["nan_count"] / result["size"]) * 100
    except:  # noqa: E722
        pass

    # If all values are NaN, return early
    if result["has_nans"] and result["nan_count"] == result["size"]:
        result["status"] = "all NaN"
        return result

    # Calculate statistics
    try:
        if result["has_nans"]:
            result["min"] = float(np.nanmin(A_flat))
            result["max"] = float(np.nanmax(A_flat))
            result["mean"] = float(np.nanmean(A_flat))
            result["std"] = float(np.nanstd(A_flat))
            result["median"] = float(np.nanmedian(A_flat))
            result["range"] = (result["min"], result["max"])

            # Remove NaNs for histogram
            A_hist = A_flat[~nan_mask]
        else:
            result["min"] = float(np.min(A_flat))
            result["max"] = float(np.max(A_flat))
            result["mean"] = float(np.mean(A_flat))
            result["std"] = float(np.std(A_flat))
            result["median"] = float(np.median(A_flat))
            result["range"] = (result["min"], result["max"])

            A_hist = A_flat

        # Calculate histogram data for sparklines
        if A_hist.size > 0:
            try:
                # TODO: handle bool tensors correctly
                # muutils/tensor_info.py:238: RuntimeWarning: Converting input from bool to <class 'numpy.uint8'> for compatibility.
                hist, bins = np.histogram(A_hist, bins=hist_bins)
                result["histogram"] = hist
                result["bins"] = bins
            except:  # noqa: E722
                pass

        result["status"] = "ok"
    except Exception as e:
        result["status"] = f"error: {str(e)}"

    return result


def generate_sparkline(
    histogram: np.ndarray,
    format: Literal["unicode", "latex", "ascii"] = "unicode",
    log_y: Optional[bool] = None,
) -> tuple[str, bool]:
    """Generate a sparkline visualization of the histogram.

    # Parameters:
    - `histogram : np.ndarray`
        Histogram data
    - `format : Literal["unicode", "latex", "ascii"]`
        Output format (defaults to `"unicode"`)
    - `log_y : bool|None`
        Whether to use logarithmic y-scale. `None` for automatic detection
        (defaults to `None`)

    # Returns:
    - `tuple[str, bool]`
        Sparkline visualization and whether log scale was used
    """
    if histogram is None or len(histogram) == 0:
        return "", False

    # Get the appropriate character set
    chars: List[str]
    if format in SPARK_CHARS:
        chars = SPARK_CHARS[format]
    else:
        chars = SPARK_CHARS["ascii"]

    # automatic detection of log_y
    if log_y is None:
        # we bin the histogram values to the number of levels in our sparkline characters
        hist_hist = np.histogram(histogram, bins=len(chars))[0]
        # if every bin except the smallest (first) and largest (last) is empty,
        # then we should use the log scale. if those bins are nonempty, keep the linear scale
        if hist_hist[1:-1].max() > 0:
            log_y = False
        else:
            log_y = True

    # Handle log scale
    if log_y:
        # Add small value to avoid log(0)
        hist_data = np.log1p(histogram)
    else:
        hist_data = histogram

    # Normalize to character set range
    if hist_data.max() > 0:
        normalized = hist_data / hist_data.max() * (len(chars) - 1)
    else:
        normalized = np.zeros_like(hist_data)

    # Convert to characters
    spark = ""
    for val in normalized:
        idx = round(val)
        spark += chars[idx]

    return spark, log_y


DEFAULT_SETTINGS: Dict[str, Any] = dict(
    fmt="unicode",
    precision=2,
    stats=True,
    shape=True,
    dtype=True,
    device=True,
    requires_grad=True,
    sparkline=False,
    sparkline_bins=5,
    sparkline_logy=None,
    colored=False,
    as_list=False,
    eq_char="=",
)


def apply_color(
    text: str, color_key: str, colors: Dict[str, str], using_tex: bool
) -> str:
    if using_tex:
        return f"{colors[color_key]}{{{text}}}" if colors[color_key] else text
    else:
        return (
            f"{colors[color_key]}{text}{colors['reset']}" if colors[color_key] else text
        )


def colorize_dtype(dtype_str: str, colors: Dict[str, str], using_tex: bool) -> str:
    """Colorize dtype string with specific colors for torch and type names."""

    # Handle torch prefix
    type_part: str = dtype_str
    prefix_part: Optional[str] = None
    if "torch." in dtype_str:
        parts = dtype_str.split("torch.")
        if len(parts) == 2:
            prefix_part = apply_color("torch", "torch", colors, using_tex)
            type_part = parts[1]

    # Handle type coloring
    color_key: str = "dtype"
    if "bool" in dtype_str.lower():
        color_key = "dtype_bool"
    elif "int" in dtype_str.lower():
        color_key = "dtype_int"
    elif "float" in dtype_str.lower():
        color_key = "dtype_float"

    type_colored: str = apply_color(type_part, color_key, colors, using_tex)

    if prefix_part:
        return f"{prefix_part}.{type_colored}"
    else:
        return type_colored


def format_shape_colored(shape_val, colors: Dict[str, str], using_tex: bool) -> str:
    """Format shape with proper coloring for both 1D and multi-D arrays."""

    def apply_color(text: str, color_key: str) -> str:
        if using_tex:
            return f"{colors[color_key]}{{{text}}}" if colors[color_key] else text
        else:
            return (
                f"{colors[color_key]}{text}{colors['reset']}"
                if colors[color_key]
                else text
            )

    if len(shape_val) == 1:
        # For 1D arrays, still color the dimension value
        return apply_color(str(shape_val[0]), "shape")
    else:
        # For multi-D arrays, color each dimension
        return "(" + ",".join(apply_color(str(dim), "shape") for dim in shape_val) + ")"


def format_device_colored(
    device_str: str, colors: Dict[str, str], using_tex: bool
) -> str:
    """Format device string with CUDA highlighting."""

    def apply_color(text: str, color_key: str) -> str:
        if using_tex:
            return f"{colors[color_key]}{{{text}}}" if colors[color_key] else text
        else:
            return (
                f"{colors[color_key]}{text}{colors['reset']}"
                if colors[color_key]
                else text
            )

    if "cuda" in device_str.lower():
        return apply_color(device_str, "device_cuda")
    else:
        return apply_color(device_str, "device")


class _UseDefaultType:
    pass


_USE_DEFAULT = _UseDefaultType()


@overload
def array_summary(
    as_list: Literal[True],
    **kwargs,
) -> List[str]: ...
@overload
def array_summary(
    as_list: Literal[False],
    **kwargs,
) -> str: ...
def array_summary(  # type: ignore[misc]
    array,
    fmt: OutputFormat = _USE_DEFAULT,  # type: ignore[assignment]
    precision: int = _USE_DEFAULT,  # type: ignore[assignment]
    stats: bool = _USE_DEFAULT,  # type: ignore[assignment]
    shape: bool = _USE_DEFAULT,  # type: ignore[assignment]
    dtype: bool = _USE_DEFAULT,  # type: ignore[assignment]
    device: bool = _USE_DEFAULT,  # type: ignore[assignment]
    requires_grad: bool = _USE_DEFAULT,  # type: ignore[assignment]
    sparkline: bool = _USE_DEFAULT,  # type: ignore[assignment]
    sparkline_bins: int = _USE_DEFAULT,  # type: ignore[assignment]
    sparkline_logy: Optional[bool] = _USE_DEFAULT,  # type: ignore[assignment]
    colored: bool = _USE_DEFAULT,  # type: ignore[assignment]
    eq_char: str = _USE_DEFAULT,  # type: ignore[assignment]
    as_list: bool = _USE_DEFAULT,  # type: ignore[assignment]
) -> Union[str, List[str]]:
    """Format array information into a readable summary.

    # Parameters:
     - `array`
            array-like object (numpy array or torch tensor)
     - `precision : int`
            Decimal places (defaults to `2`)
     - `format : Literal["unicode", "latex", "ascii"]`
            Output format (defaults to `{default_fmt}`)
     - `stats : bool`
            Whether to include statistical info (μ, σ, x̃) (defaults to `True`)
     - `shape : bool`
            Whether to include shape info (defaults to `True`)
     - `dtype : bool`
            Whether to include dtype info (defaults to `True`)
     - `device : bool`
            Whether to include device info for torch tensors (defaults to `True`)
     - `requires_grad : bool`
            Whether to include requires_grad info for torch tensors (defaults to `True`)
     - `sparkline : bool`
            Whether to include a sparkline visualization (defaults to `False`)
     - `sparkline_width : int`
            Width of the sparkline (defaults to `20`)
     - `sparkline_logy : bool|None`
            Whether to use logarithmic y-scale for sparkline (defaults to `None`)
     - `colored : bool`
            Whether to add color to output (defaults to `False`)
     - `as_list : bool`
            Whether to return as list of strings instead of joined string (defaults to `False`)

    # Returns:
     - `Union[str, List[str]]`
            Formatted statistical summary, either as string or list of strings
    """
    if fmt is _USE_DEFAULT:
        fmt = DEFAULT_SETTINGS["fmt"]
    if precision is _USE_DEFAULT:
        precision = DEFAULT_SETTINGS["precision"]
    if stats is _USE_DEFAULT:
        stats = DEFAULT_SETTINGS["stats"]
    if shape is _USE_DEFAULT:
        shape = DEFAULT_SETTINGS["shape"]
    if dtype is _USE_DEFAULT:
        dtype = DEFAULT_SETTINGS["dtype"]
    if device is _USE_DEFAULT:
        device = DEFAULT_SETTINGS["device"]
    if requires_grad is _USE_DEFAULT:
        requires_grad = DEFAULT_SETTINGS["requires_grad"]
    if sparkline is _USE_DEFAULT:
        sparkline = DEFAULT_SETTINGS["sparkline"]
    if sparkline_bins is _USE_DEFAULT:
        sparkline_bins = DEFAULT_SETTINGS["sparkline_bins"]
    if sparkline_logy is _USE_DEFAULT:
        sparkline_logy = DEFAULT_SETTINGS["sparkline_logy"]
    if colored is _USE_DEFAULT:
        colored = DEFAULT_SETTINGS["colored"]
    if as_list is _USE_DEFAULT:
        as_list = DEFAULT_SETTINGS["as_list"]
    if eq_char is _USE_DEFAULT:
        eq_char = DEFAULT_SETTINGS["eq_char"]

    array_data: Dict[str, Any] = array_info(array, hist_bins=sparkline_bins)
    result_parts: List[str] = []
    using_tex: bool = fmt == "latex"

    # Set color scheme based on format and colored flag
    colors: Dict[str, str]
    if colored:
        colors = COLORS["latex"] if using_tex else COLORS["terminal"]
    else:
        colors = COLORS["none"]

    # Get symbols for the current format
    symbols: Dict[str, str] = SYMBOLS[fmt]

    # Helper function to colorize text
    def colorize(text: str, color_key: str) -> str:
        if using_tex:
            return f"{colors[color_key]}{{{text}}}" if colors[color_key] else text
        else:
            return (
                f"{colors[color_key]}{text}{colors['reset']}"
                if colors[color_key]
                else text
            )

    # Check if dtype is integer type
    dtype_str: str = array_data.get("dtype", "")
    is_int_dtype: bool = any(
        int_type in dtype_str.lower() for int_type in ["int", "uint", "bool"]
    )

    # Format string for numbers
    float_fmt: str = f".{precision}f"

    # Handle error status or empty array
    if (
        array_data["status"] in ["empty array", "all NaN", "unknown"]
        or array_data["size"] == 0
    ):
        status = array_data["status"]
        result_parts.append(colorize(symbols["warning"] + " " + status, "warning"))
    else:
        # Add NaN warning at the beginning if there are NaNs
        if array_data["has_nans"]:
            _percent: str = "\\%" if using_tex else "%"
            nan_str: str = f"{symbols['warning']} {symbols['nan_values']}{eq_char}{array_data['nan_count']} ({array_data['nan_percent']:.1f}{_percent})"
            result_parts.append(colorize(nan_str, "warning"))

        # Statistics
        if stats:
            for stat_key in ["mean", "std", "median"]:
                if array_data[stat_key] is not None:
                    stat_str: str = f"{array_data[stat_key]:{float_fmt}}"
                    stat_colored: str = colorize(stat_str, stat_key)
                    result_parts.append(f"{symbols[stat_key]}={stat_colored}")

            # Range (min, max)
            if array_data["range"] is not None:
                min_val, max_val = array_data["range"]
                if is_int_dtype:
                    min_str: str = f"{int(min_val):d}"
                    max_str: str = f"{int(max_val):d}"
                else:
                    min_str = f"{min_val:{float_fmt}}"
                    max_str = f"{max_val:{float_fmt}}"
                min_colored: str = colorize(min_str, "range")
                max_colored: str = colorize(max_str, "range")
                range_str: str = f"{symbols['range']}=[{min_colored},{max_colored}]"
                result_parts.append(range_str)

    # Add sparkline if requested
    if sparkline and array_data["histogram"] is not None:
        # this should return whether log_y is used or not and then we set the symbol accordingly
        spark, used_log = generate_sparkline(
            array_data["histogram"],
            format=fmt,
            log_y=sparkline_logy,
        )
        if spark:
            spark_colored = colorize(spark, "sparkline")
            dist_symbol = (
                symbols["distribution_log"] if used_log else symbols["distribution"]
            )
            result_parts.append(f"{dist_symbol}{eq_char}|{spark_colored}|")

    # Add shape if requested
    if shape and array_data["shape"]:
        shape_val = array_data["shape"]
        shape_str = format_shape_colored(shape_val, colors, using_tex)
        result_parts.append(f"shape{eq_char}{shape_str}")

    # Add dtype if requested
    if dtype and array_data["dtype"]:
        dtype_colored = colorize_dtype(array_data["dtype"], colors, using_tex)
        result_parts.append(f"dtype={dtype_colored}")

    # Add device if requested and it's a tensor with device info
    if device and array_data["is_tensor"] and array_data["device"]:
        device_colored = format_device_colored(array_data["device"], colors, using_tex)
        result_parts.append(f"device{eq_char}{device_colored}")

    # Add gradient info
    if requires_grad and array_data["is_tensor"]:
        bool_req_grad_symb: str = (
            symbols["true"] if array_data["requires_grad"] else symbols["false"]
        )
        result_parts.append(
            colorize(symbols["requires_grad"] + bool_req_grad_symb, "requires_grad")
        )

    # Return as list if requested, otherwise join with spaces
    if as_list:
        return result_parts
    else:
        joinchar: str = r" \quad " if using_tex else " "
        return joinchar.join(result_parts)
