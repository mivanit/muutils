from __future__ import annotations

import typing

import pytest

from muutils.validate_type import validate_type


@pytest.mark.parametrize(
    "value, expected_type, expected_result",
    [
        (5, int | str, True),  # type: ignore[operator]
        ("hello", int | str, True),  # type: ignore[operator]
        (5.0, int | str, False),  # type: ignore[operator]
        (None, typing.Union[int, type(None)], True),  # type: ignore[operator]
        (None, typing.Union[int, str], False),  # type: ignore[operator]
        (None, int | str, False),  # type: ignore[operator]
        (42, int | None, True),  # type: ignore[operator]
        ("hello", int | None, False),  # type: ignore[operator]
        (3.14, int | None, False),  # type: ignore[operator]
        ([1], typing.List[int] | None, True),  # type: ignore[operator]
        (None, int | None, True),  # type: ignore[operator]
        (None, str | None, True),  # type: ignore[operator]
        (None, None | str, True),  # type: ignore[operator]
        (None, None | int, True),  # type: ignore[operator]
        (None, str | int, False),  # type: ignore[operator]
        (None, None | typing.List[typing.Dict[str, int]], True),  # type: ignore[operator]
    ],
)
def test_validate_type_union(value, expected_type, expected_result):
    try:
        assert validate_type(value, expected_type) == expected_result
    except Exception as e:
        raise Exception(
            f"{value = }, {expected_type = }, {expected_result = }, {e}"
        ) from e


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (42, list[int, str]),  # type: ignore[misc]
        ([1, 2, 3], list[int, str]),  # type: ignore[misc]
        ({"a": 1, "b": 2}, set[str, int]),  # type: ignore[misc]
        ({1: "a", 2: "b"}, set[int, str]),  # type: ignore[misc]
        ({"a": 1, "b": 2}, set[str, int, str]),  # type: ignore[misc]
        ({1: "a", 2: "b"}, set[int, str, int]),  # type: ignore[misc]
        ({1, 2, 3}, set[int, str]),  # type: ignore[misc]
        ({"a"}, set[int, str]),  # type: ignore[misc]
        (42, dict[int, str, bool]),  # type: ignore[misc]
    ],
)
def test_validate_type_unsupported_generic_alias(value, expected_type):
    with pytest.raises(TypeError):
        validate_type(value, expected_type)
        print(f"Failed to except: {value = }, {expected_type = }")
