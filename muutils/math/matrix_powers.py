from __future__ import annotations

from typing import List, Sequence, TYPE_CHECKING

import numpy as np
from jaxtyping import Float, Int

if TYPE_CHECKING:
    pass


def matrix_powers(
    A: Float[np.ndarray, "n n"],
    powers: Sequence[int],
) -> Float[np.ndarray, "n_powers n n"]:
    """Compute multiple powers of a matrix efficiently.

    Uses binary exponentiation to compute powers in O(log max(powers))
    matrix multiplications, avoiding redundant calculations when
    computing multiple powers.

    # Parameters:
     - `A : Float[np.ndarray, "n n"]`
            Square matrix to exponentiate
     - `powers : Sequence[int]`
            List of powers to compute (non-negative integers)

    # Returns:
     - `dict[int, Float[np.ndarray, "n n"]]`
            Dictionary mapping each requested power to the corresponding matrix power
    """
    dim_n: int = A.shape[0]
    assert A.shape[0] == A.shape[1], f"Matrix must be square, but got {A.shape = }"
    powers_np: Int[np.ndarray, "n_powers_unique"] = np.array(
        sorted(set(powers)), dtype=int
    )
    n_powers_unique: int = len(powers_np)

    if n_powers_unique < 1:
        raise ValueError(f"No powers requested: {powers = }")

    output: Float[np.ndarray, "n_powers_unique n n"] = np.full(
        (n_powers_unique, dim_n, dim_n),
        fill_value=np.nan,
        dtype=A.dtype,
    )

    # Find the maximum power to compute
    max_power: int = max(powers_np)

    # Precompute all powers of 2 up to the largest power needed
    # This forms our basis for binary decomposition
    powers_of_two: dict[int, Float[np.ndarray, "n n"]] = {}
    powers_of_two[0] = np.eye(dim_n, dtype=A.dtype)
    powers_of_two[1] = A.copy()

    # Compute powers of 2: A^2, A^4, A^8, ...
    p: int = 1
    while p < max_power:
        if p <= max_power:
            A_power_p = powers_of_two[p]
            powers_of_two[p * 2] = A_power_p @ A_power_p
        p = p * 2

    # For each requested power, compute it using the powers of 2
    for p_idx, power in enumerate(powers_np):
        # Decompose power into sum of powers of 2
        temp_result: Float[np.ndarray, "n n"] = powers_of_two[0].copy()
        temp_power: int = power
        p_temp: int = 1

        while temp_power > 0:
            if temp_power % 2 == 1:
                temp_result = temp_result @ powers_of_two[p_temp]
            temp_power = temp_power // 2
            p_temp *= 2

        output[p_idx] = temp_result

    return output


# BUG: breaks with integer matrices???
# TYPING: jaxtyping hints not working here, separate file for torch implementation?
def matrix_powers_torch(
    A,  # : Float["torch.Tensor", "n n"],
    powers: Sequence[int],
):  # Float["torch.Tensor", "n_powers n n"]:
    """Compute multiple powers of a matrix efficiently.

    Uses binary exponentiation to compute powers in O(log max(powers))
    matrix multiplications, avoiding redundant calculations when
    computing multiple powers.

    # Parameters:
     - `A : Float[torch.Tensor, "n n"]`
        Square matrix to exponentiate
     - `powers : Sequence[int]`
        List of powers to compute (non-negative integers)

    # Returns:
     - `Float[torch.Tensor, "n_powers n n"]`
        Tensor containing the requested matrix powers stacked along the first dimension

    # Raises:
     - `ValueError` : If no powers are requested or if A is not a square matrix
    """

    import torch

    if len(A.shape) != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix must be square, but got {A.shape = }")

    dim_n: int = A.shape[0]
    # Get unique powers and sort them
    unique_powers: List[int] = sorted(set(powers))
    n_powers_unique: int = len(unique_powers)
    powers_tensor: Int[torch.Tensor, "n_powers_unique"] = torch.tensor(
        unique_powers, dtype=torch.int64, device=A.device
    )

    if n_powers_unique < 1:
        raise ValueError(f"No powers requested: {powers = }")

    output: Float[torch.Tensor, "n_powers_unique n n"] = torch.full(
        (n_powers_unique, dim_n, dim_n),
        float("nan"),
        dtype=A.dtype,
        device=A.device,
    )

    # Find the maximum power to compute
    max_power: int = int(powers_tensor.max().item())

    # Precompute all powers of 2 up to the largest power needed
    # This forms our basis for binary decomposition
    powers_of_two: dict[int, Float[torch.Tensor, "n n"]] = {}
    powers_of_two[0] = torch.eye(dim_n, dtype=A.dtype, device=A.device)
    powers_of_two[1] = A.clone()

    # Compute powers of 2: A^2, A^4, A^8, ...
    p: int = 1
    while p < max_power:
        if p <= max_power:
            A_power_p: Float[torch.Tensor, "n n"] = powers_of_two[p]
            powers_of_two[p * 2] = A_power_p @ A_power_p
        p = p * 2

    # For each requested power, compute it using the powers of 2
    for p_idx, power in enumerate(unique_powers):
        # Decompose power into sum of powers of 2
        temp_result: Float[torch.Tensor, "n n"] = powers_of_two[0].clone()
        temp_power: int = power
        p_temp: int = 1

        while temp_power > 0:
            if temp_power % 2 == 1:
                temp_result = temp_result @ powers_of_two[p_temp]
            temp_power = temp_power // 2
            p_temp *= 2

        output[p_idx] = temp_result

    return output
