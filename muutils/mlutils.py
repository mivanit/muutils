import json
import os
import random
import typing
import warnings
from itertools import islice
from pathlib import Path
from typing import Any, Callable, TypeVar

import numpy as np
import torch

DEFAULT_SEED: int = 42
GLOBAL_SEED: int = DEFAULT_SEED


def get_device() -> torch.device:
    """Get the torch.device instance on which torch.Tensors should be allocated."""
    try:
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")
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

    assert (
        run_path.is_dir()
    ), f"Model path {run_path} is not a directory (expect run directory, not model files)"

    return [
        (int(checkpoint_path.stem.split("_")[-1].split(".")[0]), checkpoint_path)
        for checkpoint_path in sorted(
            Path(run_path).glob(checkpoints_format.format(extension=extension))
        )
    ]


F = TypeVar("F", bound=Callable[..., Any])


def register_method(
    method_dict: dict[str, Callable[..., Any]],
    custom_name: str | None = None,
) -> Callable[[F], F]:
    """Decorator to add a method to the method_dict"""

    def decorator(method: F) -> F:
        if custom_name is None:
            method_name: str = method.__name__
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
