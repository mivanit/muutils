import numpy as np
from typing import Union, Any, Literal, List, Dict, overload

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
    log_y: bool = False,
) -> str:
    """Generate a sparkline visualization of the histogram.

    # Parameters:
     - `histogram : np.ndarray`
            Histogram data
     - `format : Literal["unicode", "latex", "ascii"]`
            Output format (defaults to `"unicode"`)
     - `log_y : bool`
            Whether to use logarithmic y-scale (defaults to `False`)

    # Returns:
     - `str`
            Sparkline visualization
    """
    if histogram is None or len(histogram) == 0:
        return ""

    # Get the appropriate character set
    if format in SPARK_CHARS:
        chars = SPARK_CHARS[format]
    else:
        chars = SPARK_CHARS["ascii"]

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
        idx = int(val)
        spark += chars[idx]

    return spark


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
    sparkline_logy=False,
    colored=False,
    as_list=False,
    eq_char="=",
)


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
    sparkline_logy: bool = _USE_DEFAULT,  # type: ignore[assignment]
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
     - `sparkline_logy : bool`
            Whether to use logarithmic y-scale for sparkline (defaults to `False`)
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
                min_str: str = f"{min_val:{float_fmt}}"
                max_str: str = f"{max_val:{float_fmt}}"
                min_colored: str = colorize(min_str, "range")
                max_colored: str = colorize(max_str, "range")
                range_str: str = f"{symbols['range']}=[{min_colored},{max_colored}]"
                result_parts.append(range_str)

    # Add sparkline if requested
    if sparkline and array_data["histogram"] is not None:
        print(array_data["histogram"])
        print(array_data["bins"])
        spark = generate_sparkline(
            array_data["histogram"], format=fmt, log_y=sparkline_logy
        )
        if spark:
            spark_colored = colorize(spark, "sparkline")
            result_parts.append(f"{symbols['distribution']}{eq_char}|{spark_colored}|")

    # Add shape if requested
    if shape and array_data["shape"]:
        shape_val = array_data["shape"]
        if len(shape_val) == 1:
            shape_str = str(shape_val[0])
        else:
            shape_str = (
                "(" + ",".join(colorize(str(dim), "shape") for dim in shape_val) + ")"
            )
        result_parts.append(f"shape{eq_char}{shape_str}")

    # Add dtype if requested
    if dtype and array_data["dtype"]:
        result_parts.append(colorize(f"dtype={array_data['dtype']}", "dtype"))

    # Add device if requested and it's a tensor with device info
    if device and array_data["is_tensor"] and array_data["device"]:
        result_parts.append(
            colorize(f"device{eq_char}{array_data['device']}", "device")
        )

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
