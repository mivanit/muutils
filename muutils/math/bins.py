from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Literal

import numpy as np
from jaxtyping import Float


@dataclass(frozen=True)
class Bins:
    n_bins: int = 32
    start: float = 0
    stop: float = 1.0
    scale: Literal["lin", "log"] = "log"

    _log_min: float = 1e-3
    _zero_in_small_start_log: bool = True

    @cached_property
    def edges(self) -> Float[np.ndarray, "n_bins+1"]:
        if self.scale == "lin":
            return np.linspace(self.start, self.stop, self.n_bins + 1)
        elif self.scale == "log":
            if self.start < 0:
                raise ValueError(
                    f"start must be positive for log scale, got {self.start}"
                )
            if self.start == 0:
                return np.concatenate(
                    [  # pyright: ignore[reportUnknownArgumentType]
                        np.array([0]),
                        np.logspace(
                            np.log10(self._log_min),  # pyright: ignore[reportAny]
                            np.log10(self.stop),  # pyright: ignore[reportAny]
                            self.n_bins,
                        ),
                    ]
                )
            elif self.start < self._log_min and self._zero_in_small_start_log:
                return np.concatenate(
                    [  # pyright: ignore[reportUnknownArgumentType]
                        np.array([0]),
                        np.logspace(
                            np.log10(self.start),  # pyright: ignore[reportAny]
                            np.log10(self.stop),  # pyright: ignore[reportAny]
                            self.n_bins,
                        ),
                    ]
                )
            else:
                return np.logspace(  # pyright: ignore[reportUnknownVariableType]
                    np.log10(self.start),  # pyright: ignore[reportAny]
                    np.log10(self.stop),  # pyright: ignore[reportAny]
                    self.n_bins + 1,
                )
        else:
            raise ValueError(f"Invalid scale {self.scale}, expected lin or log")

    @cached_property
    def centers(self) -> Float[np.ndarray, "n_bins"]:
        return (self.edges[:-1] + self.edges[1:]) / 2

    def changed_n_bins_copy(self, n_bins: int) -> "Bins":
        return Bins(
            n_bins=n_bins,
            start=self.start,
            stop=self.stop,
            scale=self.scale,
            _log_min=self._log_min,
            _zero_in_small_start_log=self._zero_in_small_start_log,
        )
