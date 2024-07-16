from __future__ import annotations

import math
import typing
from typing import Optional, Iterable, Sequence, Union, Any
import warnings

from muutils.misc import str_to_numeric

_EPSILON: float = 1e-10


class Interval:
    """
    Represents a mathematical interval, open by default.

    The Interval class can represent both open and closed intervals, as well as half-open intervals.
    It supports various initialization methods and provides containment checks.

    Examples:
        >>> i1 = Interval(1, 5)  # Default open interval (1, 5)
        >>> 3 in i1
        True
        >>> 1 in i1
        False
        >>> i2 = Interval([1, 5])  # Closed interval [1, 5]
        >>> 1 in i2
        True
        >>> i3 = Interval(1, 5, closed_L=True)  # Half-open interval [1, 5)
        >>> str(i3)
        '[1, 5)'
        >>> i4 = ClosedInterval(1, 5)  # Closed interval [1, 5]
        >>> i5 = OpenInterval(1, 5)  # Open interval (1, 5)
    """

    def __init__(
        self,
        *args: Union[Sequence[float], float],
        is_closed: Optional[bool] = None,
        closed_L: Optional[bool] = None,
        closed_R: Optional[bool] = None,
    ):
        try:
            # Handle different types of input arguments
            if len(args) == 1 and isinstance(
                args[0], (list, tuple, Sequence, Iterable)
            ):
                assert (
                    len(args[0]) == 2
                ), "if arg is a list or tuple, it must have length 2"
                self.lower = args[0][0]
                self.upper = args[0][1]
                # Determine closure type based on the container type
                default_closed = isinstance(args[0], list)
            elif len(args) == 2:
                self.lower, self.upper = args
                default_closed = False  # Default to open interval if two args
            else:
                raise ValueError(f"Invalid input arguments: {args}")

            # Ensure lower bound is less than upper bound
            if self.lower > self.upper:
                raise ValueError("Lower bound must be less than upper bound")

            if math.isnan(self.lower) or math.isnan(self.upper):
                raise ValueError("NaN is not allowed as an interval bound")

            # Determine closure properties
            if is_closed is not None:
                # can't specify both is_closed and closed_L/R
                if (closed_L is not None) or (closed_R is not None):
                    raise ValueError("Cannot specify both is_closed and closed_L/R")
                self.closed_L = is_closed
                self.closed_R = is_closed
            else:
                self.closed_L = closed_L if closed_L is not None else default_closed
                self.closed_R = closed_R if closed_R is not None else default_closed

        except (AssertionError, ValueError) as e:
            raise ValueError(
                f"Invalid input arguments to Interval:\n{e}\nUsage:\n{self.__doc__}"
            ) from e

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, Interval):
            return self.lower <= item.lower and self.upper >= item.upper
        elif isinstance(item, (float, int, typing.SupportsFloat, typing.SupportsInt)):
            if math.isnan(item):
                raise ValueError("NaN cannot be checked for containment in an interval")
            return ((self.closed_L and item >= self.lower) or item > self.lower) and (
                (self.closed_R and item <= self.upper) or item < self.upper
            )
        else:
            raise TypeError(f"Unsupported type for containment check: {type(item)}")

    def __repr__(self) -> str:
        return f"{'[' if self.closed_L else '('}{self.lower}, {self.upper}{']' if self.closed_R else ')'}"

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def from_str(cls, input_str: str) -> Interval:
        input_str = input_str.strip()
        assert input_str.count(",") == 1, "Invalid input string"
        lower, upper = input_str.strip("[]()").split(",")
        lower = lower.strip()
        upper = upper.strip()

        lower = str_to_numeric(lower)
        upper = str_to_numeric(upper)

        if input_str[0] == "[":
            closed_L = True
        elif input_str[0] == "(":
            closed_L = False
        else:
            raise ValueError("Invalid input string")

        if input_str[-1] == "]":
            closed_R = True
        elif input_str[-1] == ")":
            closed_R = False
        else:
            raise ValueError("Invalid input string")

        return cls(lower, upper, closed_L=closed_L, closed_R=closed_R)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Interval):
            return False
        return (self.lower, self.upper, self.closed_L, self.closed_R) == (
            other.lower,
            other.upper,
            other.closed_L,
            other.closed_R,
        )

    def __iter__(self):
        yield self.lower
        yield self.upper

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.lower
        elif index == 1:
            return self.upper
        else:
            raise IndexError("Interval index out of range")

    def __len__(self) -> int:
        return 2

    def size(self) -> float:
        """
        Returns the size of the interval.

        # Returns:
         - `float`
            the size of the interval
        """
        return self.upper - self.lower

    def clamp(self, value: Union[int, float], epsilon: float = _EPSILON) -> float:
        """
        Clamp the given value to the interval bounds.

        For open bounds, the clamped value will be slightly inside the interval (by epsilon).

        # Parameters:
         - `value : Union[int, float]`
           the value to clamp.
         - `epsilon : float`
           margin for open bounds
           (defaults to `_EPSILON`)

        # Returns:
         - `float`
            the clamped value

        # Raises:
         - `ValueError` : If the input value is NaN.
        """

        if math.isnan(value):
            raise ValueError("Cannot clamp NaN value")

        if epsilon < 0:
            raise ValueError(f"Epsilon must be non-negative: {epsilon = }")

        if epsilon > self.size():
            warnings.warn(
                f"Warning: epsilon is greater than the size of the interval: {epsilon = }, {self.size() = }, {self = }"
            )

        if self.closed_L:
            clamped_min = self.lower
        else:
            clamped_min = self.lower + epsilon

        if self.closed_R:
            clamped_max = self.upper
        else:
            clamped_max = self.upper - epsilon

        return max(clamped_min, min(value, clamped_max))


class ClosedInterval(Interval):
    def __init__(self, *args: Union[Sequence[float], float], **kwargs: Any):
        if any(key in kwargs for key in ("is_closed", "closed_L", "closed_R")):
            raise ValueError("Cannot specify closure properties for ClosedInterval")
        super().__init__(*args, is_closed=True)


class OpenInterval(Interval):
    def __init__(self, *args: Union[Sequence[float], float], **kwargs: Any):
        if any(key in kwargs for key in ("is_closed", "closed_L", "closed_R")):
            raise ValueError("Cannot specify closure properties for OpenInterval")
        super().__init__(*args, is_closed=False)
