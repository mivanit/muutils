from __future__ import annotations


_SHORTEN_MAP: dict[int | float, str] = {
    1e3: "K",
    1e6: "M",
    1e9: "B",
    1e12: "t",
    1e15: "q",
    1e18: "Q",
}

_SHORTEN_TUPLES: list[tuple[int | float, str]] = sorted(
    ((val, suffix) for val, suffix in _SHORTEN_MAP.items()),
    key=lambda x: -x[0],
)


_REVERSE_SHORTEN_MAP: dict[str, int | float] = {v: k for k, v in _SHORTEN_MAP.items()}


def shorten_numerical_to_str(
    num: int | float,
    small_as_decimal: bool = True,
    precision: int = 1,
) -> str:
    """shorten a large numerical value to a string
    1234 -> 1K

    precision guaranteed to 1 in 10, but can be higher. reverse of `str_to_numeric`
    """

    # small values are returned as is
    num_abs: float = abs(num)
    if num_abs < 1e3:
        return str(num)

    # iterate over suffixes from largest to smallest
    for i, (val, suffix) in enumerate(_SHORTEN_TUPLES):
        if num_abs > val or i == len(_SHORTEN_TUPLES) - 1:
            if (num_abs < val * 10) and small_as_decimal:
                return f"{num / val:.{precision}f}{suffix}"
            elif num_abs < val * 1e3:
                return f"{int(round(num / val))}{suffix}"

    return f"{num:.{precision}f}"


def str_to_numeric(
    quantity: str,
    mapping: None | bool | dict[str, int | float] = True,
) -> int | float:
    """Convert a string representing a quantity to a numeric value.

    The string can represent an integer, python float, fraction, or shortened via `shorten_numerical_to_str`.

    # Examples:
    ```
    >>> str_to_numeric("5")
    5
    >>> str_to_numeric("0.1")
    0.1
    >>> str_to_numeric("1/5")
    0.2
    >>> str_to_numeric("-1K")
    -1000.0
    >>> str_to_numeric("1.5M")
    1500000.0
    >>> str_to_numeric("1.2e2")
    120.0
    ```

    """

    # check is string
    if not isinstance(quantity, str):
        raise TypeError(
            f"quantity must be a string, got '{type(quantity) = }' '{quantity = }'"
        )

    # basic int conversion
    try:
        quantity_int: int = int(quantity)
        return quantity_int
    except ValueError:
        pass

    # basic float conversion
    try:
        quantity_float: float = float(quantity)
        return quantity_float
    except ValueError:
        pass

    # mapping
    _mapping: dict[str, int | float]
    if mapping is True or mapping is None:
        _mapping = _REVERSE_SHORTEN_MAP
    else:
        _mapping = mapping  # type: ignore[assignment]

    quantity_original: str = quantity

    quantity = quantity.strip()

    result: int | float
    multiplier: int | float = 1

    # detect if it has a suffix
    suffixes_detected: list[bool] = [suffix in quantity for suffix in _mapping]
    n_suffixes_detected: int = sum(suffixes_detected)
    if n_suffixes_detected == 0:
        # no suffix
        pass
    elif n_suffixes_detected == 1:
        # find multiplier
        for suffix, mult in _mapping.items():
            if quantity.endswith(suffix):
                # remove suffix, store multiplier, and break
                quantity = quantity[: -len(suffix)].strip()
                multiplier = mult
                break
        else:
            raise ValueError(f"Invalid suffix in {quantity_original}")
    else:
        # multiple suffixes
        raise ValueError(f"Multiple suffixes detected in {quantity_original}")

    # fractions
    if "/" in quantity:
        try:
            assert quantity.count("/") == 1, "too many '/'"
            # split and strip
            num, den = quantity.split("/")
            num = num.strip()
            den = den.strip()
            num_sign: int = 1
            # negative numbers
            if num.startswith("-"):
                num_sign = -1
                num = num[1:]
            # assert that both are digits
            assert (
                num.isdigit() and den.isdigit()
            ), "numerator and denominator must be digits"
            # return the fraction
            result = num_sign * (
                int(num) / int(den)
            )  # this allows for fractions with suffixes, which is weird, but whatever
        except AssertionError as e:
            raise ValueError(f"Invalid fraction {quantity_original}: {e}") from e

    # decimals
    else:
        try:
            result = int(quantity)
        except ValueError:
            try:
                result = float(quantity)
            except ValueError as e:
                raise ValueError(
                    f"Invalid quantity {quantity_original} ({quantity})"
                ) from e

    return result * multiplier
