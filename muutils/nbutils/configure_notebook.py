import os
import typing
import warnings

import matplotlib.pyplot as plt  # type: ignore[import]

# handle plotly importing
PLOTLY_IMPORTED: bool
try:
    import plotly.io as pio  # type: ignore[import]
except ImportError:
    warnings.warn("Plotly not installed. Plotly plots will not be available.")
    PLOTLY_IMPORTED = False
else:
    PLOTLY_IMPORTED = True

# figure out if we're in a jupyter notebook
IN_JUPYTER: bool = not "_" in os.environ
if IN_JUPYTER:
    from IPython import get_ipython  # type: ignore[import]

# muutils imports
from muutils.mlutils import get_device, set_reproducibility

# handling figures
PlottingMode = typing.Literal["ignore", "inline", "widget", "save"]
PLOT_MODE: PlottingMode
FIG_COUNTER: int
FIG_OUTPUT_FMT: str | None
FIG_NUMBERED_FNAME: str = "figure-{num}"
FIG_CONFIG: dict | None = None
FIG_BASEPATH: str | None = None
CLOSE_AFTER_PLOTSHOW: bool = False

KNOWN_FORMATS = ["pdf", "png", "jpg", "jpeg", "svg", "eps", "ps", "tif", "tiff"]


def setup_plots(
    plot_mode: PlottingMode = "inline",
    fig_output_fmt: str | None = "pdf",
    fig_numbered_fname: str = "figure-{num}",
    fig_config: dict | None = None,
    fig_basepath: str | None = None,
    close_after_plotshow: bool = False,
) -> None:
    """Set up plot saving/rendering options"""
    global PLOT_MODE, FIG_COUNTER, FIG_OUTPUT_FMT, FIG_NUMBERED_FNAME, FIG_CONFIG, FIG_BASEPATH, CLOSE_AFTER_PLOTSHOW

    # set plot mode
    PLOT_MODE = plot_mode
    FIG_COUNTER = 0
    CLOSE_AFTER_PLOTSHOW = close_after_plotshow

    if PLOT_MODE == "inline":
        if IN_JUPYTER:
            ipython = get_ipython()
            ipython.magic("matplotlib inline")
        else:
            raise RuntimeError("Cannot use inline plotting outside of Jupyter")
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
        plt.show = lambda: None
        return

    # everything except saving handled up to this point
    assert PLOT_MODE == "save", f"Invalid plot mode: {PLOT_MODE}"

    FIG_OUTPUT_FMT = fig_output_fmt
    FIG_NUMBERED_FNAME = fig_numbered_fname
    FIG_CONFIG = fig_config

    # set default figure format in rcParams savefig.format
    plt.rcParams["savefig.format"] = FIG_OUTPUT_FMT
    if FIG_OUTPUT_FMT not in KNOWN_FORMATS:
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
) -> "torch.device|None":  # type: ignore[name-defined]
    """Shared Jupyter notebook setup steps:
    - Set random seeds and library reproducibility settings
    - Set device based on availability
    - Set module reloading before code execution
    - Set plot formatting
    - Set plot saving/rendering options
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
):
    """Show the active plot, depending on global configs"""
    global FIG_COUNTER, CLOSE_AFTER_PLOTSHOW
    FIG_COUNTER += 1

    if PLOT_MODE == "save":
        # get numbered figure name if not given
        if fname is None:
            fname = FIG_NUMBERED_FNAME.format(num=FIG_COUNTER)

        # save figure
        assert FIG_BASEPATH is not None
        plt.savefig(os.path.join(FIG_BASEPATH, fname))
    elif PLOT_MODE == "ignore":
        # do nothing
        pass
    elif PLOT_MODE == "inline":
        # show figure
        plt.show()
    elif PLOT_MODE == "widget":
        # show figure
        plt.show()
    else:
        warnings.warn(f"Invalid plot mode: {PLOT_MODE}")

    if CLOSE_AFTER_PLOTSHOW:
        plt.close()
