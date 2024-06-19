from __future__ import annotations

import typing
from typing import Any, Optional, Union

import pytest

from muutils.validate_type import validate_type


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (5, int | str, True),
        ("hello", int | str, True),
        (5.0, int | str, False),
        (None, typing.Union[int, type(None)], True),
        (None, typing.Union[int, str], False),
        (None, int | str, False),
        (42, int | None, True),
        ("hello", int | None, False),
        (3.14, int | None, False),
        ([1], typing.List[int] | None, True),
        (None, int | None, True),
        (None, str | None, True),
        (None, None | str, True),
        (None, None | int, True),
        (None, str | int, False),
        (None, None | typing.List[typing.Dict[str, int]], True),
    ],
)
def test_validate_type_union(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e
