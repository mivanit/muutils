from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from muutils.tensor_info import array_summary, generate_sparkline


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
    when given non-array inputs.
    """
    summary = array_summary(bad_input)  # type: ignore[call-overload]
    summary_str: str = summary if isinstance(summary, str) else " ".join(summary)
    assert summary_str


def test_generate_sparkline_basic() -> None:
    """
    Test the sparkline generator with a fixed histogram.
    """
    histogram: np.ndarray = np.array([1, 3, 5, 2, 0])
    spark, logy = generate_sparkline(histogram, format="unicode", log_y=None)
    assert isinstance(spark, str)
    assert isinstance(logy, bool)
    assert not logy
    assert len(spark) == len(histogram)
    # Test with log_y=True
    spark_log, logy_true = generate_sparkline(histogram, format="ascii", log_y=True)
    assert isinstance(spark_log, str)
    assert len(spark_log) == len(histogram)
    assert logy_true


def test_generate_sparkline_logy() -> None:
    """
    Test the sparkline generator with a fixed histogram.
    """
    histogram: np.ndarray = np.array([99999, 3, 5, 2, 0])
    spark, logy = generate_sparkline(histogram, format="unicode", log_y=None)
    assert isinstance(spark, str)
    assert isinstance(logy, bool)
    assert logy
    assert len(spark) == len(histogram)
    # Test with log_y=True
    spark_log, logy_true = generate_sparkline(histogram, format="ascii", log_y=True)
    assert isinstance(spark_log, str)
    assert len(spark_log) == len(histogram)
    assert logy_true


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(["--maxfail=1", "--disable-warnings", "-q"]))
