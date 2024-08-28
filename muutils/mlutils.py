"miscellaneous utilities for ML pipelines"

from __future__ import annotations

import json
import os
import random
import typing
import warnings
from itertools import islice
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, Union

ARRAY_IMPORTS: bool
try:
    import numpy as np
    import torch

    ARRAY_IMPORTS = True
except ImportError as e:
    warnings.warn(
        f"Numpy or torch not installed. Array operations will not be available.\n{e}"
    )
    ARRAY_IMPORTS = False

DEFAULT_SEED: int = 42
GLOBAL_SEED: int = DEFAULT_SEED


def get_device(device: "Union[str,torch.device,None]" = None) -> "torch.device":
    """Get the torch.device instance on which `torch.Tensor`s should be allocated."""
    if not ARRAY_IMPORTS:
        raise ImportError(
            "Numpy or torch not installed. Array operations will not be available."
        )
    try:
        # if device is given
        if device is not None:
            device = torch.device(device)
            if any(
                [
                    torch.cuda.is_available() and device.type == "cuda",
                    torch.backends.mps.is_available() and device.type == "mps",
                    device.type == "cpu",
                ]
            ):
                # if device is given and available
                pass
            else:
                warnings.warn(
                    f"Specified device {device} is not available, falling back to CPU"
                )
                return torch.device("cpu")

        # no device given, infer from availability
        else:
            if torch.cuda.is_available():
                device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                device = torch.device("mps")
            else:
                device = torch.device("cpu")

        # put a dummy tensor on the device to check if it is available
        _dummy = torch.zeros(1, device=device)

        return device

    except Exception as e:
        warnings.warn(
            f"Error while getting device, falling back to CPU. Error: {e}",
            RuntimeWarning,
        )
        return torch.device("cpu")


def set_reproducibility(seed: int = DEFAULT_SEED):
    """
    Improve model reproducibility. See https://github.com/NVIDIA/framework-determinism for more information.

    Deterministic operations tend to have worse performance than nondeterministic operations, so this method trades
    off performance for reproducibility. Set use_deterministic_algorithms to True to improve performance.
    """
    global GLOBAL_SEED

    GLOBAL_SEED = seed

    random.seed(seed)

    if ARRAY_IMPORTS:
        np.random.seed(seed)
        torch.manual_seed(seed)

        torch.use_deterministic_algorithms(True)
        # Ensure reproducibility for concurrent CUDA streams
        # see https://docs.nvidia.com/cuda/cublas/index.html#cublasApi_reproducibility.
        os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"


def chunks(it, chunk_size):
    """Yield successive chunks from an iterator."""
    # https://stackoverflow.com/a/61435714
    iterator = iter(it)
    while chunk := list(islice(iterator, chunk_size)):
        yield chunk


def get_checkpoint_paths_for_run(
    run_path: Path,
    extension: typing.Literal["pt", "zanj"],
    checkpoints_format: str = "checkpoints/model.iter_*.{extension}",
) -> list[tuple[int, Path]]:
    """get checkpoints of the format from the run_path

    note that `checkpoints_format` should contain a glob pattern with:
     - unresolved "{extension}" format term for the extension
     - a wildcard for the iteration number
    """

    assert run_path.is_dir(), f"Model path {run_path} is not a directory (expect run directory, not model files)"

    return [
        (int(checkpoint_path.stem.split("_")[-1].split(".")[0]), checkpoint_path)
        for checkpoint_path in sorted(
            Path(run_path).glob(checkpoints_format.format(extension=extension))
        )
    ]


F = TypeVar("F", bound=Callable[..., Any])


def register_method(
    method_dict: dict[str, Callable[..., Any]],
    custom_name: Optional[str] = None,
) -> Callable[[F], F]:
    """Decorator to add a method to the method_dict"""

    def decorator(method: F) -> F:
        method_name: str
        if custom_name is None:
            method_name_orig: str | None = getattr(method, "__name__", None)
            if method_name_orig is None:
                warnings.warn(
                    f"Method {method} does not have a name, using sanitized repr"
                )
                from muutils.misc import sanitize_identifier

                method_name = sanitize_identifier(repr(method))
            else:
                method_name = method_name_orig
        else:
            method_name = custom_name
            method.__name__ = custom_name
        assert (
            method_name not in method_dict
        ), f"Method name already exists in method_dict: {method_name = }, {list(method_dict.keys()) = }"
        method_dict[method_name] = method
        return method

    return decorator


def pprint_summary(summary: dict):
    print(json.dumps(summary, indent=2))
