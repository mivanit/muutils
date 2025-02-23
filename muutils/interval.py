"represents a mathematical `Interval` over the real numbers"

from __future__ import annotations

import math
import typing
from typing import Optional, Iterable, Sequence, Union, Any

from muutils.misc import str_to_numeric

_EPSILON: float = 1e-10

Number = Union[float, int]
# TODO: make this also work with decimals, fractions, numpy types, etc.
# except we must somehow avoid importing them? idk

_EMPTY_INTERVAL_ARGS: tuple[Number, Number, bool, bool, set[Number]] = (
    math.nan,
    math.nan,
    False,
    False,
    set(),
)


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
        *args: Union[Sequence[Number], Number],
        is_closed: Optional[bool] = None,
        closed_L: Optional[bool] = None,
        closed_R: Optional[bool] = None,
    ):
        self.lower: Number
        self.upper: Number
        self.closed_L: bool
        self.closed_R: bool
        self.singleton_set: Optional[set[Number]] = None
        try:
            if len(args) == 0:
                (
                    self.lower,
                    self.upper,
                    self.closed_L,
                    self.closed_R,
                    self.singleton_set,
                ) = _EMPTY_INTERVAL_ARGS
                return
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
            elif len(args) == 1 and isinstance(
                args[0], (int, float, typing.SupportsFloat, typing.SupportsInt)
            ):
                # a singleton, but this will be handled later
                self.lower = args[0]
                self.upper = args[0]
                default_closed = False
            elif len(args) == 2:
                self.lower, self.upper = args  # type: ignore[assignment]
                default_closed = False  # Default to open interval if two args
            else:
                raise ValueError(f"Invalid input arguments: {args}")

            # if both of the bounds are NaN or None, return an empty interval
            if any(x is None for x in (self.lower, self.upper)) or any(
                math.isnan(x) for x in (self.lower, self.upper)
            ):
                if (self.lower is None and self.upper is None) or (
                    math.isnan(self.lower) and math.isnan(self.upper)
                ):
                    (
                        self.lower,
                        self.upper,
                        self.closed_L,
                        self.closed_R,
                        self.singleton_set,
                    ) = _EMPTY_INTERVAL_ARGS
                    return
                else:
                    raise ValueError(
                        "Both bounds must be NaN or None to create an empty interval. Also, just use `Interval.get_empty()` instead."
                    )

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

            # handle singleton/empty case
            if self.lower == self.upper and not (self.closed_L or self.closed_R):
                (
                    self.lower,
                    self.upper,
                    self.closed_L,
                    self.closed_R,
                    self.singleton_set,
                ) = _EMPTY_INTERVAL_ARGS
                return

            elif self.lower == self.upper and (self.closed_L or self.closed_R):
                self.singleton_set = {self.lower}  # Singleton interval
                self.closed_L = True
                self.closed_R = True
                return
            # otherwise `singleton_set` is `None`

        except (AssertionError, ValueError) as e:
            raise ValueError(
                f"Invalid input arguments to Interval: {args = }, {is_closed = }, {closed_L = }, {closed_R = }\n{e}\nUsage:\n{self.__doc__}"
            ) from e

    @property
    def is_closed(self) -> bool:
        if self.is_empty:
            return True
        if self.is_singleton:
            return True
        return self.closed_L and self.closed_R

    @property
    def is_open(self) -> bool:
        if self.is_empty:
            return True
        if self.is_singleton:
            return False
        return not self.closed_L and not self.closed_R

    @property
    def is_half_open(self) -> bool:
        return (self.closed_L and not self.closed_R) or (
            not self.closed_L and self.closed_R
        )

    @property
    def is_singleton(self) -> bool:
        return self.singleton_set is not None and len(self.singleton_set) == 1

    @property
    def is_empty(self) -> bool:
        return self.singleton_set is not None and len(self.singleton_set) == 0

    @property
    def is_finite(self) -> bool:
        return not math.isinf(self.lower) and not math.isinf(self.upper)

    @property
    def singleton(self) -> Number:
        if not self.is_singleton:
            raise ValueError("Interval is not a singleton")
        return next(iter(self.singleton_set))  # type: ignore[arg-type]

    @staticmethod
    def get_empty() -> Interval:
        return Interval(math.nan, math.nan, closed_L=None, closed_R=None)

    @staticmethod
    def get_singleton(value: Number) -> Interval:
        if math.isnan(value) or value is None:
            return Interval.get_empty()
        return Interval(value, value, closed_L=True, closed_R=True)

    def numerical_contained(self, item: Number) -> bool:
        if self.is_empty:
            return False
        if math.isnan(item):
            raise ValueError("NaN cannot be checked for containment in an interval")
        if self.is_singleton:
            return item in self.singleton_set  # type: ignore[operator]
        return ((self.closed_L and item >= self.lower) or item > self.lower) and (
            (self.closed_R and item <= self.upper) or item < self.upper
        )

    def interval_contained(self, item: Interval) -> bool:
        if item.is_empty:
            return True
        if self.is_empty:
            return False
        if item.is_singleton:
            return self.numerical_contained(item.singleton)
        if self.is_singleton:
            if not item.is_singleton:
                return False
            return self.singleton == item.singleton

        lower_contained: bool = (
            # either strictly wider bound
            self.lower < item.lower
            # if same, then self must be closed if item is open
            or (self.lower == item.lower and self.closed_L >= item.closed_L)
        )

        upper_contained: bool = (
            # either strictly wider bound
            self.upper > item.upper
            # if same, then self must be closed if item is open
            or (self.upper == item.upper and self.closed_R >= item.closed_R)
        )

        return lower_contained and upper_contained

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, Interval):
            return self.interval_contained(item)
        else:
            return self.numerical_contained(item)

    def __repr__(self) -> str:
        if self.is_empty:
            return r"∅"
        if self.is_singleton:
            return "{" + str(self.singleton) + "}"
        left: str = "[" if self.closed_L else "("
        right: str = "]" if self.closed_R else ")"
        return f"{left}{self.lower}, {self.upper}{right}"

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def from_str(cls, input_str: str) -> Interval:
        input_str = input_str.strip()
        # empty and singleton
        if input_str.count(",") == 0:
            # empty set
            if input_str == "∅":
                return cls.get_empty()
            assert input_str.startswith("{") and input_str.endswith(
                "}"
            ), "Invalid input string"
            input_str_set_interior: str = input_str.strip("{}").strip()
            if len(input_str_set_interior) == 0:
                return cls.get_empty()
            # singleton set
            return cls.get_singleton(str_to_numeric(input_str_set_interior))

        # expect commas
        if not input_str.count(",") == 1:
            raise ValueError("Invalid input string")

        # get bounds
        lower: str
        upper: str
        lower, upper = input_str.strip("[]()").split(",")
        lower = lower.strip()
        upper = upper.strip()

        lower_num: Number = str_to_numeric(lower)
        upper_num: Number = str_to_numeric(upper)

        # figure out closure
        closed_L: bool
        closed_R: bool
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

        return cls(lower_num, upper_num, closed_L=closed_L, closed_R=closed_R)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Interval):
            return False
        if self.is_empty and other.is_empty:
            return True
        if self.is_singleton and other.is_singleton:
            return self.singleton == other.singleton
        return (self.lower, self.upper, self.closed_L, self.closed_R) == (
            other.lower,
            other.upper,
            other.closed_L,
            other.closed_R,
        )

    def __iter__(self):
        if self.is_empty:
            return
        elif self.is_singleton:
            yield self.singleton
            return
        else:
            yield self.lower
            yield self.upper

    def __getitem__(self, index: int) -> float:
        if self.is_empty:
            raise IndexError("Empty interval has no bounds")
        if self.is_singleton:
            if index == 0:
                return self.singleton
            else:
                raise IndexError("Singleton interval has only one bound")
        if index == 0:
            return self.lower
        elif index == 1:
            return self.upper
        else:
            raise IndexError("Interval index out of range")

    def __len__(self) -> int:
        return 0 if self.is_empty else 1 if self.is_singleton else 2

    def copy(self) -> Interval:
        if self.is_empty:
            return Interval.get_empty()
        if self.is_singleton:
            return Interval.get_singleton(self.singleton)
        return Interval(
            self.lower, self.upper, closed_L=self.closed_L, closed_R=self.closed_R
        )

    def size(self) -> float:
        """
        Returns the size of the interval.

        # Returns:

         - `float`
            the size of the interval
        """
        if self.is_empty or self.is_singleton:
            return 0
        else:
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

        if math.isnan(epsilon):
            raise ValueError("Epsilon cannot be NaN")

        if epsilon < 0:
            raise ValueError(f"Epsilon must be non-negative: {epsilon = }")

        if self.is_empty:
            raise ValueError("Cannot clamp to an empty interval")

        if self.is_singleton:
            return self.singleton

        if epsilon > self.size():
            raise ValueError(
                f"epsilon is greater than the size of the interval: {epsilon = }, {self.size() = }, {self = }"
            )

        # make type work with decimals and stuff
        if not isinstance(value, (int, float)):
            epsilon = value.__class__(epsilon)

        clamped_min: Number
        if self.closed_L:
            clamped_min = self.lower
        else:
            clamped_min = self.lower + epsilon

        clamped_max: Number
        if self.closed_R:
            clamped_max = self.upper
        else:
            clamped_max = self.upper - epsilon

        return max(clamped_min, min(value, clamped_max))

    def intersection(self, other: Interval) -> Interval:
        if not isinstance(other, Interval):
            raise TypeError("Can only intersect with another Interval")

        if self.is_empty or other.is_empty:
            return Interval.get_empty()

        if self.is_singleton:
            if other.numerical_contained(self.singleton):
                return self.copy()
            else:
                return Interval.get_empty()

        if other.is_singleton:
            if self.numerical_contained(other.singleton):
                return other.copy()
            else:
                return Interval.get_empty()

        if self.upper < other.lower or other.upper < self.lower:
            return Interval.get_empty()

        lower: Number = max(self.lower, other.lower)
        upper: Number = min(self.upper, other.upper)
        closed_L: bool = self.closed_L if self.lower > other.lower else other.closed_L
        closed_R: bool = self.closed_R if self.upper < other.upper else other.closed_R

        return Interval(lower, upper, closed_L=closed_L, closed_R=closed_R)

    def union(self, other: Interval) -> Interval:
        if not isinstance(other, Interval):
            raise TypeError("Can only union with another Interval")

        # empty set case
        if self.is_empty:
            return other.copy()
        if other.is_empty:
            return self.copy()

        # special case where the intersection is empty but the intervals are contiguous
        if self.upper == other.lower:
            if self.closed_R or other.closed_L:
                return Interval(
                    self.lower,
                    other.upper,
                    closed_L=self.closed_L,
                    closed_R=other.closed_R,
                )
        elif other.upper == self.lower:
            if other.closed_R or self.closed_L:
                return Interval(
                    other.lower,
                    self.upper,
                    closed_L=other.closed_L,
                    closed_R=self.closed_R,
                )

        # non-intersecting nonempty and non-contiguous intervals
        if self.intersection(other) == Interval.get_empty():
            raise NotImplementedError(
                "Union of non-intersecting nonempty non-contiguous intervals is not implemented "
                + f"{self = }, {other = }, {self.intersection(other) = }"
            )

        # singleton case
        if self.is_singleton:
            return other.copy()
        if other.is_singleton:
            return self.copy()

        # regular case
        lower: Number = min(self.lower, other.lower)
        upper: Number = max(self.upper, other.upper)
        closed_L: bool = self.closed_L if self.lower < other.lower else other.closed_L
        closed_R: bool = self.closed_R if self.upper > other.upper else other.closed_R

        return Interval(lower, upper, closed_L=closed_L, closed_R=closed_R)


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
