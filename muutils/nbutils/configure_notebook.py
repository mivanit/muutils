"""shared utilities for setting up a notebook"""

from __future__ import annotations

import os
import typing
import warnings

import matplotlib.pyplot as plt  # type: ignore[import]


class PlotlyNotInstalledWarning(UserWarning):
    pass


# handle plotly importing
PLOTLY_IMPORTED: bool
try:
    import plotly.io as pio  # type: ignore[import]
except ImportError:
    warnings.warn(
        "Plotly not installed. Plotly plots will not be available.",
        PlotlyNotInstalledWarning,
    )
    PLOTLY_IMPORTED = False
else:
    PLOTLY_IMPORTED = True

# figure out if we're in a jupyter notebook
try:
    from IPython import get_ipython  # type: ignore[import-not-found]

    IN_JUPYTER = get_ipython() is not None
except ImportError:
    IN_JUPYTER = False

# muutils imports
from muutils.mlutils import get_device, set_reproducibility  # noqa: E402

# handling figures
PlottingMode = typing.Literal["ignore", "inline", "widget", "save"]
PLOT_MODE: PlottingMode = "inline"
CONVERSION_PLOTMODE_OVERRIDE: PlottingMode | None = None
FIG_COUNTER: int = 0
FIG_OUTPUT_FMT: str | None = None
FIG_NUMBERED_FNAME: str = "figure-{num}"
FIG_CONFIG: dict | None = None
FIG_BASEPATH: str | None = None
CLOSE_AFTER_PLOTSHOW: bool = False

MATPLOTLIB_FORMATS = ["pdf", "png", "jpg", "jpeg", "svg", "eps", "ps", "tif", "tiff"]
TIKZPLOTLIB_FORMATS = ["tex", "tikz"]


class UnknownFigureFormatWarning(UserWarning):
    pass


def universal_savefig(fname: str, fmt: str | None = None) -> None:
    # try to infer format from fname
    if fmt is None:
        fmt = fname.split(".")[-1]

    if not (fmt in MATPLOTLIB_FORMATS or fmt in TIKZPLOTLIB_FORMATS):
        warnings.warn(
            f"Unknown format '{fmt}', defaulting to '{FIG_OUTPUT_FMT}'",
            UnknownFigureFormatWarning,
        )
        fmt = FIG_OUTPUT_FMT

    # not sure why linting is throwing an error here
    if not fname.endswith(fmt):  # type: ignore[arg-type]
        fname += f".{fmt}"

    if fmt in MATPLOTLIB_FORMATS:
        plt.savefig(fname, format=fmt, bbox_inches="tight")
    elif fmt in TIKZPLOTLIB_FORMATS:
        import tikzplotlib  # type: ignore[import]

        tikzplotlib.save(fname)
    else:
        warnings.warn(f"Unknown format '{fmt}', going with matplotlib default")
        plt.savefig(fname, bbox_inches="tight")


def setup_plots(
    plot_mode: PlottingMode = "inline",
    fig_output_fmt: str | None = "pdf",
    fig_numbered_fname: str = "figure-{num}",
    fig_config: dict | None = None,
    fig_basepath: str | None = None,
    close_after_plotshow: bool = False,
) -> None:
    """Set up plot saving/rendering options"""
    global \
        PLOT_MODE, \
        CONVERSION_PLOTMODE_OVERRIDE, \
        FIG_COUNTER, \
        FIG_OUTPUT_FMT, \
        FIG_NUMBERED_FNAME, \
        FIG_CONFIG, \
        FIG_BASEPATH, \
        CLOSE_AFTER_PLOTSHOW

    # set plot mode, handling override
    if CONVERSION_PLOTMODE_OVERRIDE is not None:
        # override if set
        PLOT_MODE = CONVERSION_PLOTMODE_OVERRIDE
    else:
        # otherwise use the given plot mode
        PLOT_MODE = plot_mode

    FIG_COUNTER = 0
    CLOSE_AFTER_PLOTSHOW = close_after_plotshow

    if PLOT_MODE == "inline":
        if IN_JUPYTER:
            ipython = get_ipython()
            ipython.magic("matplotlib inline")
        else:
            raise RuntimeError(
                f"Cannot use inline plotting outside of Jupyter\n{PLOT_MODE = }\t{CONVERSION_PLOTMODE_OVERRIDE = }"
            )
        return
    elif PLOT_MODE == "widget":
        if IN_JUPYTER:
            ipython = get_ipython()
            ipython.magic("matplotlib widget")
        else:
            # matplotlib outside of jupyter will bring up a new window by default
            pass
        return
    elif PLOT_MODE == "ignore":
        # disable plotting
        plt.show = lambda: None  # type: ignore[misc]
        return

    # everything except saving handled up to this point
    assert PLOT_MODE == "save", f"Invalid plot mode: {PLOT_MODE}"

    FIG_OUTPUT_FMT = fig_output_fmt
    FIG_NUMBERED_FNAME = fig_numbered_fname
    FIG_CONFIG = fig_config

    # set default figure format in rcParams savefig.format
    plt.rcParams["savefig.format"] = FIG_OUTPUT_FMT
    if FIG_OUTPUT_FMT in TIKZPLOTLIB_FORMATS:
        try:
            import tikzplotlib  # type: ignore[import] # noqa: F401
        except ImportError:
            warnings.warn(
                f"Tikzplotlib not installed. Cannot save figures in Tikz format '{FIG_OUTPUT_FMT}', things might break."
            )
    else:
        if FIG_OUTPUT_FMT not in MATPLOTLIB_FORMATS:
            warnings.warn(
                f'Unknown figure format, things might break: {plt.rcParams["savefig.format"] = }'
            )

    # if base path not given, make one
    if fig_basepath is None:
        if fig_config is None:
            # if no config, use the current time
            from datetime import datetime

            fig_basepath = f"figures/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        else:
            # if config given, convert to string
            from muutils.misc import dict_to_filename

            fig_basepath = f"figures/{dict_to_filename(fig_config)}"

    FIG_BASEPATH = fig_basepath
    os.makedirs(fig_basepath, exist_ok=True)

    # if config given, serialize and save that config
    if fig_config is not None:
        import json

        from muutils.json_serialize import json_serialize

        with open(f"{fig_basepath}/config.json", "w") as f:
            json.dump(
                json_serialize(fig_config),
                f,
                indent="\t",
            )

    print(f"Figures will be saved to: '{fig_basepath}'")


def configure_notebook(
    *args,
    seed: int = 42,
    device: typing.Any = None,  # this can be a string, torch.device, or None
    dark_mode: bool = True,
    plot_mode: PlottingMode = "inline",
    fig_output_fmt: str | None = "pdf",
    fig_numbered_fname: str = "figure-{num}",
    fig_config: dict | None = None,
    fig_basepath: str | None = None,
    close_after_plotshow: bool = False,
) -> "torch.device|None":  # type: ignore[name-defined] # noqa: F821
    """Shared Jupyter notebook setup steps

    - Set random seeds and library reproducibility settings
    - Set device based on availability
    - Set module reloading before code execution
    - Set plot formatting
    - Set plot saving/rendering options

    # Parameters:
     - `seed : int`
        random seed across libraries including torch, numpy, and random (defaults to `42`)
       (defaults to `42`)
     - `device : typing.Any`
       pytorch device to use
       (defaults to `None`)
     - `dark_mode : bool`
       figures in dark mode
       (defaults to `True`)
     - `plot_mode : PlottingMode`
       how to display plots, one of `PlottingMode` or `["ignore", "inline", "widget", "save"]`
       (defaults to `"inline"`)
     - `fig_output_fmt : str | None`
       format for saving figures
       (defaults to `"pdf"`)
     - `fig_numbered_fname : str`
        format for saving figures with numbers (if they aren't named)
       (defaults to `"figure-{num}"`)
     - `fig_config : dict | None`
       metadata to save with the figures
       (defaults to `None`)
     - `fig_basepath : str | None`
        base path for saving figures
       (defaults to `None`)
     - `close_after_plotshow : bool`
        close figures after showing them
       (defaults to `False`)

    # Returns:
     - `torch.device|None`
       the device set, if torch is installed
    """

    # set some globals related to plotting
    setup_plots(
        plot_mode=plot_mode,
        fig_output_fmt=fig_output_fmt,
        fig_numbered_fname=fig_numbered_fname,
        fig_config=fig_config,
        fig_basepath=fig_basepath,
        close_after_plotshow=close_after_plotshow,
    )

    global PLOT_MODE, FIG_OUTPUT_FMT, FIG_BASEPATH

    print(f"set up plots with {PLOT_MODE = }, {FIG_OUTPUT_FMT = }, {FIG_BASEPATH = }")

    # Set seeds and other reproducibility-related library options
    set_reproducibility(seed)

    # Reload modules before executing user code
    if IN_JUPYTER:
        ipython = get_ipython()
        if "IPython.extensions.autoreload" not in ipython.extension_manager.loaded:
            ipython.magic("load_ext autoreload")
            ipython.magic("autoreload 2")

        # Specify plotly renderer for vscode
        if PLOTLY_IMPORTED:
            pio.renderers.default = "notebook_connected"

            if dark_mode:
                pio.templates.default = "plotly_dark"
                plt.style.use("dark_background")

    try:
        # Set device
        device = get_device(device)
        return device
    except ImportError:
        warnings.warn("Torch not installed. Cannot get/set device.")
        return None


def plotshow(
    fname: str | None = None,
    plot_mode: PlottingMode | None = None,
    fmt: str | None = None,
):
    """Show the active plot, depending on global configs"""
    global FIG_COUNTER, CLOSE_AFTER_PLOTSHOW, PLOT_MODE
    FIG_COUNTER += 1

    if plot_mode is None:
        plot_mode = PLOT_MODE

    if plot_mode == "save":
        # get numbered figure name if not given
        if fname is None:
            fname = FIG_NUMBERED_FNAME.format(num=FIG_COUNTER)

        # save figure
        assert FIG_BASEPATH is not None
        universal_savefig(os.path.join(FIG_BASEPATH, fname), fmt=fmt)
    elif plot_mode == "ignore":
        # do nothing
        pass
    elif plot_mode == "inline":
        # show figure
        plt.show()
    elif plot_mode == "widget":
        # show figure
        plt.show()
    else:
        warnings.warn(f"Invalid plot mode: {plot_mode}")

    if CLOSE_AFTER_PLOTSHOW:
        plt.close()
