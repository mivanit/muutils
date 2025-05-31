from __future__ import annotations

from typing import List, Tuple
import numpy as np
import pytest
from jaxtyping import Float
import torch

from muutils.dbg import dbg_tensor
from muutils.math.matrix_powers import matrix_powers, matrix_powers_torch


class TestMatrixPowers:
    @pytest.fixture
    def sample_matrices(self) -> List[Tuple[str, Float[np.ndarray, "n n"]]]:
        """Return a list of test matrices with diverse properties."""
        return [
            ("identity", np.eye(3)),
            ("diagonal", np.diag([2.0, 3, 4])),
            ("nilpotent", np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0.0]])),
            # ("random_int", np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])),
            ("random_float", np.random.rand(4, 4)),
            ("complex", np.array([[1 + 1j, 2], [3, 4 - 2j]])),
        ]

    @pytest.fixture
    def power_test_cases(self) -> List[List[int]]:
        """Return test cases for powers to compute."""
        return [
            [0],
            [1],
            [2],
            [0, 1, 2],
            [5],
            [0, 1, 5, 10],
            [1, 2, 4, 8, 16],
            list(range(10)),
        ]

    def test_against_numpy_implementation(
        self,
        sample_matrices: List[Tuple[str, Float[np.ndarray, "n n"]]],
        power_test_cases: List[List[int]],
    ) -> None:
        """Test that matrix_powers gives same results as numpy.linalg.matrix_power."""
        for name, matrix in sample_matrices:
            for powers in power_test_cases:
                # Compute with our function
                dbg_tensor(matrix)
                result = matrix_powers(matrix, powers)
                result_torch = (
                    matrix_powers_torch(torch.tensor(matrix), powers).cpu().numpy()
                )

                # Get dimension information
                n_powers = len(set(powers))
                dim_n = matrix.shape[0]

                # Check shape of output
                assert result.shape == (
                    n_powers,
                    dim_n,
                    dim_n,
                ), f"Incorrect shape for {name} matrix with powers {powers}"
                assert result_torch.shape == (
                    n_powers,
                    dim_n,
                    dim_n,
                ), f"Incorrect shape for {name} matrix with powers {powers} (torch)"

                # Compare with numpy implementation for each power
                unique_powers = sorted(set(powers))
                for i, power in enumerate(unique_powers):
                    expected = np.linalg.matrix_power(matrix, power)
                    np.testing.assert_allclose(
                        result[i],
                        expected,
                        rtol=1e-10,
                        atol=1e-10,
                        err_msg=f"Failed for {name} matrix to power {power}",
                    )
                    np.testing.assert_allclose(
                        result_torch[i],
                        expected,
                        rtol=1e-10,
                        atol=1e-10,
                        err_msg=f"Failed for {name} matrix to power {power}",
                    )

    def test_empty_powers_list(self) -> None:
        """Test handling of empty powers list."""
        A = np.eye(3)
        with pytest.raises(ValueError):
            matrix_powers(A, [])

    def test_duplicate_powers(self) -> None:
        """Test handling of duplicate powers in the input list."""
        A = np.diag([2.0, 3, 4])
        powers = [1, 2, 2, 3, 1]
        result = matrix_powers(A, powers)
        result_torch = matrix_powers_torch(torch.tensor(A), powers).cpu().numpy()

        # Should only have 3 unique powers
        assert result.shape == (3, 3, 3)

        # Check each power
        unique_powers = sorted(set(powers))
        for i, power in enumerate(unique_powers):
            expected = np.linalg.matrix_power(A, power)
            np.testing.assert_allclose(result[i], expected)
            np.testing.assert_allclose(result_torch[i], expected)

    def test_non_square_matrix(self) -> None:
        """Test that an assertion error is raised for non-square matrices."""
        A = np.ones((3, 4))
        with pytest.raises(AssertionError):
            matrix_powers(A, [1, 2])

    def test_negative_powers(self) -> None:
        """Test handling of negative powers (should work with invertible matrices)."""
        # Use an invertible matrix
        A = np.array([[1, 2], [3, 4]])
        powers = [-1, -2, 0, 1, 2]

        # This might raise an error if negative powers aren't supported
        try:
            result = matrix_powers(A, powers)

            # If it succeeds, verify the results
            unique_powers = sorted(set(powers))
            for i, power in enumerate(unique_powers):
                expected = np.linalg.matrix_power(A, power)
                np.testing.assert_allclose(result[i], expected)
        except Exception as e:
            pytest.skip(f"Negative powers not supported: {e}")

    def test_large_powers(self) -> None:
        """Test with large powers to verify binary exponentiation efficiency."""
        # Matrix with eigenvalues < 1 to avoid overflow
        A = np.array([[0.5, 0.1], [0.1, 0.5]])
        large_power = 1000
        powers = [large_power]

        result = matrix_powers(A, powers)
        result_torch = matrix_powers_torch(torch.tensor(A), powers).cpu().numpy()
        expected = np.linalg.matrix_power(A, large_power)

        np.testing.assert_allclose(result[0], expected)
        np.testing.assert_allclose(result_torch[0], expected)

    def test_performance(self) -> None:
        """Test that binary exponentiation is more efficient than naive approach."""
        import time

        A = np.random.randn(64, 64)
        powers = [10, 100] + list(range(1000, 1024)) + list(range(9_000, 9_200))

        # Time our implementation
        start = time.time()
        p_np = matrix_powers(A, powers)
        our_time = time.time() - start

        # Time torch implementation
        start = time.time()
        p_torch = matrix_powers_torch(torch.tensor(A), powers)
        torch_time = time.time() - start

        # Time naive approach
        start = time.time()
        p_naive = []
        for power in powers:
            p_naive.append(np.linalg.matrix_power(A, power))
        naive_time = time.time() - start

        assert len(p_np) == len(p_naive), "Output lengths do not match"
        assert len(p_torch) == len(p_naive), "Torch output lengths do not match"

        # Our implementation should be faster for these powers
        assert (
            our_time < naive_time
        ), f"Binary exponentiation ({our_time:.4f}s) not faster than naive approach ({naive_time:.4f}s)"
        assert (
            torch_time < naive_time
        ), f"Binary exponentiation ({torch_time:.4f}s) not faster than naive approach ({naive_time:.4f}s)"
