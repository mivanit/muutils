from __future__ import annotations


from muutils.misc.hashing import stable_hash


def sanitize_name(
    name: str | None,
    additional_allowed_chars: str = "",
    replace_invalid: str = "",
    when_none: str | None = "_None_",
    leading_digit_prefix: str = "",
) -> str:
    """sanitize a string, leaving only alphanumerics and `additional_allowed_chars`

    # Parameters:
     - `name : str | None`
       input string
     - `additional_allowed_chars : str`
       additional characters to allow, none by default
       (defaults to `""`)
     - `replace_invalid : str`
        character to replace invalid characters with
       (defaults to `""`)
     - `when_none : str | None`
        string to return if `name` is `None`. if `None`, raises an exception
       (defaults to `"_None_"`)
     - `leading_digit_prefix : str`
        character to prefix the string with if it starts with a digit
       (defaults to `""`)

    # Returns:
     - `str`
        sanitized string
    """

    if name is None:
        if when_none is None:
            raise ValueError("name is None")
        else:
            return when_none

    sanitized: str = ""
    for char in name:
        if char.isalnum():
            sanitized += char
        elif char in additional_allowed_chars:
            sanitized += char
        else:
            sanitized += replace_invalid

    if sanitized[0].isdigit():
        sanitized = leading_digit_prefix + sanitized

    return sanitized


def sanitize_fname(fname: str | None, **kwargs) -> str:
    """sanitize a filename to posix standards

    - leave only alphanumerics, `_` (underscore), '-' (dash) and `.` (period)
    """
    return sanitize_name(fname, additional_allowed_chars="._-", **kwargs)


def sanitize_identifier(fname: str | None, **kwargs) -> str:
    """sanitize an identifier (variable or function name)

    - leave only alphanumerics and `_` (underscore)
    - prefix with `_` if it starts with a digit
    """
    return sanitize_name(
        fname, additional_allowed_chars="_", leading_digit_prefix="_", **kwargs
    )


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


def dynamic_docstring(**doc_params):
    def decorator(func):
        if func.__doc__:
            func.__doc__ = func.__doc__.format(**doc_params)
        return func

    return decorator
