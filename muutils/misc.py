import typing


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
    key=lambda x: x[0],
)


def shorten_numerical_to_str(num: int | float, small_as_decimal: bool = True) -> str:
    """shorten a large numerical value to a string
    1234 -> 1K
    """

    if num < 1e3:
        return str(num)

    for i, (val, suffix) in enumerate(_SHORTEN_TUPLES):
        if num > val:
            if (num < val * 10) and small_as_decimal:
                return f"{num / val:.1f}{suffix}"
            elif num < val * 1e3:
                return f"{int(round(num / val))}{suffix}"

    return f"{num}"


def list_split(lst: list, val) -> list[list]:
    """split a list into n sublists. similar to str().split(val)"""

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
