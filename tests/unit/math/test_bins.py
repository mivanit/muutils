from __future__ import annotations

import math
from typing import Final

import numpy as np
import pytest
from numpy.testing import assert_allclose

from muutils.math.bins import Bins


_LOG_MIN: Final[float] = 1e-3


def _expected_log_edges(
    start: float,
    stop: float,
    n_bins: int,
    *,
    log_min: float = _LOG_MIN,
) -> np.ndarray:
    """Mimic the precise branch logic of `Bins.edges` for log scale."""
    if math.isclose(start, 0.0):
        return np.concatenate(
            [
                np.array([0.0]),
                np.logspace(math.log10(log_min), math.log10(stop), n_bins),
            ]
        )
    if start < log_min:
        return np.concatenate(
            [np.array([0.0]), np.logspace(math.log10(start), math.log10(stop), n_bins)]
        )
    return np.logspace(math.log10(start), math.log10(stop), n_bins + 1)


@pytest.mark.parametrize(
    "n_bins,start,stop",
    [(1, 0.0, 1.0), (4, -3.0, 5.0), (10, 2.5, 7.5)],
)
def test_edges_linear(n_bins: int, start: float, stop: float) -> None:
    bins = Bins(n_bins=n_bins, start=start, stop=stop, scale="lin")
    expected = np.linspace(start, stop, n_bins + 1)
    assert_allclose(bins.edges, expected)
    assert bins.edges.shape == (n_bins + 1,)


@pytest.mark.parametrize("n_bins", [1, 4, 16])
def test_centers_linear(n_bins: int) -> None:
    bins = Bins(n_bins=n_bins, start=0.0, stop=1.0, scale="lin")
    expected_centers = (bins.edges[:-1] + bins.edges[1:]) / 2
    assert_allclose(bins.centers, expected_centers)
    assert bins.centers.shape == (n_bins,)


@pytest.mark.parametrize("start", [1e-2, 0.1, 1.0])
def test_edges_log_standard(start: float) -> None:
    n_bins, stop = 8, 10.0
    bins = Bins(n_bins=n_bins, start=start, stop=stop, scale="log")
    expected = _expected_log_edges(start, stop, n_bins)
    assert_allclose(bins.edges, expected)
    assert bins.edges.shape == (n_bins + 1,)


def test_edges_log_start_zero() -> None:
    n_bins, stop = 6, 1.0
    bins = Bins(n_bins=n_bins, start=0.0, stop=stop, scale="log")
    expected = _expected_log_edges(0.0, stop, n_bins)
    assert_allclose(bins.edges, expected)
    assert bins.edges[0] == 0.0


def test_edges_log_small_start_include_zero() -> None:
    n_bins, start, stop = 5, 1e-4, 1.0
    bins = Bins(n_bins=n_bins, start=start, stop=stop, scale="log")
    expected = _expected_log_edges(start, stop, n_bins)
    assert_allclose(bins.edges, expected)
    assert bins.edges[0] == 0.0


def test_log_negative_start_raises() -> None:
    with pytest.raises(ValueError):
        _ = Bins(n_bins=3, start=-0.1, stop=1.0, scale="log").edges


def test_invalid_scale_raises() -> None:
    with pytest.raises(ValueError):
        _ = Bins(n_bins=3, start=0.0, stop=1.0, scale="strange").edges  # type: ignore[arg-type]


def test_changed_n_bins_copy() -> None:
    original = Bins(n_bins=4, start=0.0, stop=1.0, scale="lin")
    new_bins = original.changed_n_bins_copy(10)

    assert new_bins is not original
    assert new_bins.n_bins == 10
    for attr in ("start", "stop", "scale", "_log_min", "_zero_in_small_start_log"):
        assert getattr(new_bins, attr) == getattr(original, attr)

    assert new_bins.edges.shape == (11,)


@pytest.mark.parametrize("n_bins,scale", [(1, "lin"), (3, "lin"), (7, "log")])
def test_edges_shape(n_bins: int, scale: str) -> None:
    bins = Bins(
        n_bins=n_bins,
        start=0.1 if scale == "log" else 0.0,
        stop=2.0,
        scale=scale,  # type: ignore
    )
    assert bins.edges.shape == (n_bins + 1,)
