import hashlib
import typing


def stable_hash(s: str) -> int:
    """Returns a stable hash of the given string. not cryptographically secure, but stable between runs"""
    # init hash object and update with string
    hash_obj: hashlib._Hash = hashlib.sha256()
    hash_obj.update(bytes(s, "UTF-8"))
    # get digest and convert to int
    return int.from_bytes(hash_obj.digest(), "big")


def sanitize_fname(fname: str | None) -> str:
    """sanitize a filename for use in a path"""
    if fname is None:
        return "_None_"

    fname_sanitized: str = ""
    for char in fname:
        if char.isalnum():
            fname_sanitized += char
        elif char in ("-", "_", "."):
            fname_sanitized += char
        else:
            fname_sanitized += ""

    return fname_sanitized


def dict_to_filename(
    data: dict,
    format_str: str = "{key}_{val}",
    separator: str = ".",
    max_length: int = 255,
):
    # Convert the dictionary items to a list of strings using the format string
    formatted_items: list[str] = [
        format_str.format(key=k, val=v) for k, v in data.items()
    ]

    # Join the formatted items using the separator
    joined_str: str = separator.join(formatted_items)

    # Remove special characters and spaces
    sanitized_str: str = sanitize_fname(joined_str)

    # Check if the length is within limits
    if len(sanitized_str) <= max_length:
        return sanitized_str

    # If the string is too long, generate a hash
    return f"h_{stable_hash(sanitized_str)}"


def freeze(obj: typing.Any) -> typing.Any:
    """decorator to prevent writing to an object's members"""

    def new_setattr(self, name, value):
        raise AttributeError(f"{self.__class__.__name__} is frozen")

    obj.__setattr__ = new_setattr

    return obj


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


_REVERSE_SHORTEN_MAP: dict[str, int|float] = {v: k for k, v in _SHORTEN_MAP.items()}

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
        mapping: None|bool|dict[str, int|float] = True,
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
        raise TypeError(f"quantity must be a string, got '{type(quantity) = }' '{quantity = }'")
    
    # basic float conversion
    try:
        quantity_float: float = float(quantity)
        return quantity_float
    except ValueError:
        pass

    # mapping
    if mapping is True or mapping is None:
        mapping = _REVERSE_SHORTEN_MAP

    quantity_original: str = quantity

    quantity = quantity.strip()

    result: int|float
    multiplier: int|float = 1

    # detect if it has a suffix
    suffixes_detected: list[bool] = [suffix in quantity for suffix in mapping]
    match sum(suffixes_detected):
        case 0:
            # no suffix
            pass
        case 1:
            # find multiplier
            for suffix, mult in mapping.items():
                if quantity.endswith(suffix):
                    # remove suffix, store multiplier, and break
                    quantity = quantity.removesuffix(suffix).strip()
                    multiplier = mult
                    break
            else:
                raise ValueError(f"Invalid suffix in {quantity_original}")
        case _:
            # multiple suffixes
            raise ValueError(f"Multiple suffixes detected in {quantity_original}")        
    
    # fractions
    if "/" in quantity:
        try:
            assert quantity.count("/") == 1, f"too many '/'"
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
            assert num.isdigit() and den.isdigit(), f"numerator and denominator must be digits"
            # return the fraction
            result = num_sign * (int(num) / int(den)) # this allows for fractions with suffixes, which is weird, but whatever
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
                raise ValueError(f"Invalid quantity {quantity_original} ({quantity})") from e

    return result * multiplier


def list_split(lst: list, val) -> list[list]:
    """split a list into n sublists. similar to "a_b_c".split("_")"""

    output: list[list] = [
        [],
    ]

    for x in lst:
        if x == val:
            output.append([])
        else:
            output[-1].append(x)
    return output


def list_join(lst: list, factory: typing.Callable) -> list:
    """add a *new* instance of `val` between each element of `lst`

    ```
    >>> list_join([1,2,3], lambda : 0)
    [1,0,2,0,3]
    >>> list_join([1,2,3], lambda: [time.sleep(0.1), time.time()][1])
    [1, 1600000000.0, 2, 1600000000.1, 3]
    ```
    """

    output: list = [
        lst[0],
    ]

    for x in lst[1:]:
        output.append(factory())
        output.append(x)

    return output
