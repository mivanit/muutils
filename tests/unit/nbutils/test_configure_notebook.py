import os
import warnings

import matplotlib.pyplot as plt  # type: ignore[import]
import pytest
import torch

from muutils.nbutils.configure_notebook import (
    UnknownFigureFormatWarning,
    configure_notebook,
    plotshow,
    setup_plots,
)

JUNK_DATA_PATH: str = "tests/_temp/test_cfg_notebook"


@pytest.mark.parametrize(
    "plot_mode",
    [
        # "inline", # cant use outside a jupyter notebook
        "widget",
        "ignore",
    ],
)
def test_setup_plots_donothing(plot_mode):
    setup_plots(plot_mode=plot_mode)


def test_no_inline_outside_nb():
    with pytest.raises(RuntimeError):
        configure_notebook(plot_mode="inline")


def test_setup_plots_save():
    setup_plots(plot_mode="save", fig_basepath=JUNK_DATA_PATH)
    assert os.path.exists(JUNK_DATA_PATH)


def test_configure_notebook():
    device = configure_notebook(seed=42, plot_mode="ignore")
    assert isinstance(device, torch.device)  # Assumes 'torch' is imported


def test_plotshow_save():
    setup_plots(plot_mode="save", fig_basepath=JUNK_DATA_PATH)
    with pytest.warns(UnknownFigureFormatWarning):
        plt.plot([1, 2, 3], [1, 2, 3])
        plotshow()
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "figure-1.pdf"))
    with pytest.warns(UnknownFigureFormatWarning):
        plt.plot([3, 6, 9], [2, 4, 8])
        plotshow()
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "figure-2.pdf"))


def test_plotshow_save_named():
    setup_plots(plot_mode="save", fig_basepath=JUNK_DATA_PATH)
    plt.plot([1, 2, 3], [1, 2, 3])
    plotshow(fname="test.pdf")
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "test.pdf"))
    plt.plot([3, 6, 9], [2, 4, 8])
    plotshow(fname="another-test.pdf")
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "another-test.pdf"))


def test_plotshow_save_mixed():
    setup_plots(
        plot_mode="save",
        fig_basepath=JUNK_DATA_PATH,
        fig_numbered_fname="mixedfig-{num}",
    )
    with pytest.warns(UnknownFigureFormatWarning):
        plt.plot([1, 2, 3], [1, 2, 3])
        plotshow()
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "mixedfig-1.pdf"))
    plt.plot([3, 6, 9], [2, 4, 8])
    plotshow(fname="mixed-test.pdf")
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "mixed-test.pdf"))
    with pytest.warns(UnknownFigureFormatWarning):
        plt.plot([1, 1, 1], [1, 9, 9])
        plotshow()
    assert os.path.exists(os.path.join(JUNK_DATA_PATH, "mixedfig-3.pdf"))


def test_warn_unknown_format():
    with pytest.warns(UnknownFigureFormatWarning):
        setup_plots(
            plot_mode="save",
            fig_basepath=JUNK_DATA_PATH,
            fig_numbered_fname="mixedfig-{num}",
        )
        plt.plot([1, 2, 3], [1, 2, 3])
        plotshow()


def test_no_warn_unknown_format_2():
    with pytest.warns(UnknownFigureFormatWarning):
        setup_plots(
            plot_mode="save",
            fig_basepath=JUNK_DATA_PATH,
            fig_numbered_fname="mixedfig-{num}",
        )
        plt.plot([1, 2, 3], [1, 2, 3])
        plotshow("no-format")


def test_no_warn_pdf_format():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        setup_plots(
            plot_mode="save",
            fig_basepath="JUNK_DATA_PATH",
            fig_numbered_fname="fig-{num}.pdf",
        )
        plt.plot([1, 2, 3], [1, 2, 3])
        plotshow()


def test_plotshow_ignore():
    setup_plots(plot_mode="ignore")
    plt.plot([1, 2, 3], [1, 2, 3])
    plotshow()
    # this should do nothing
