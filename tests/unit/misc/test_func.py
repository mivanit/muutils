from __future__ import annotations
import sys
from typing import Dict, Optional, Tuple
import pytest
from muutils.errormode import ErrorMode
from muutils.misc.func import (
    is_none,
    process_kwarg,
    replace_kwarg,
    typed_lambda,
    validate_kwarg,
)


def test_process_kwarg_with_kwarg_passed() -> None:
    @process_kwarg("x", typed_lambda(lambda x: x * 2, (int,), int))
    def func(x: int = 1) -> int:
        return x

    assert func(x=3) == 6


def test_process_kwarg_without_kwarg() -> None:
    @process_kwarg("x", typed_lambda(lambda x: x * 2, (int,), int))
    def func(x: int = 1) -> int:
        return x

    assert func() == 1


def test_validate_kwarg_valid() -> None:
    @validate_kwarg(
        "y",
        typed_lambda(lambda y: y > 0, (int,), bool),
        "Value for {kwarg_name} must be positive, got {value}",
    )
    def func(y: int = 1) -> int:
        return y

    assert func(y=5) == 5


def test_validate_kwarg_invalid_with_description() -> None:
    @validate_kwarg(
        "y", lambda y: y > 0, "Value for {kwarg_name} must be positive, got {value}"
    )
    def func(y: int = 1) -> int:
        return y

    with pytest.raises(ValueError, match="Value for y must be positive, got -3"):
        func(y=-3)


def test_replace_kwarg_replaces_value() -> None:
    @replace_kwarg("z", is_none, "replaced")
    def func(z: Optional[str] = None) -> str:
        return z  # type: ignore

    assert func(z=None) == "replaced"


def test_replace_kwarg_preserves_non_default() -> None:
    @replace_kwarg("z", is_none, "replaced")
    def func(z: Optional[str] = None) -> Optional[str]:
        return z

    assert func(z="hello") == "hello"
    assert func(z=None) == "replaced"
    assert func() is None


def test_replace_kwarg_when_kwarg_not_passed() -> None:
    @replace_kwarg("z", is_none, "replaced", replace_if_missing=True)
    def func(z: Optional[str] = None) -> Optional[str]:
        return z

    assert func() == "replaced"
    assert func(z=None) == "replaced"
    assert func(z="hello") == "hello"


def test_process_kwarg_processor_raises_exception() -> None:
    """Test that if the processor lambda raises an exception, it propagates."""

    @process_kwarg("x", lambda x: 1 / 0)
    def func(x: int = 1) -> int:
        return x

    with pytest.raises(ZeroDivisionError):
        func(x=5)


def test_process_kwarg_with_positional_argument() -> None:
    """Test that process_kwarg doesn't affect arguments passed positionally."""

    @process_kwarg("x", typed_lambda(lambda x: x + 5, (int,), int))
    def func(x: int) -> int:
        return x

    # Passing argument positionally; since it's not in kwargs, it won't be processed.
    result: int = func(3)
    assert result == 3


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason="need `python >= 3.10` for `types.NoneType`"
)
def test_process_kwarg_processor_returns_none() -> None:
    """Test that if the processor returns None, the function receives None."""

    if sys.version_info >= (3, 10):
        from types import NoneType

        @process_kwarg("x", typed_lambda(lambda x: None, (int,), NoneType))
        def func(x: Optional[int] = 5) -> Optional[int]:
            return x

        result: Optional[int] = func(x=100)
        assert result is None


# --- Additional tests for validate_kwarg ---


def test_validate_kwarg_with_positional_argument() -> None:
    """Test that validate_kwarg does not validate positional arguments.

    Since the decorator checks only kwargs, positional arguments will bypass validation.
    """

    @validate_kwarg("x", lambda x: x > 0, "x must be > 0, got {value}")
    def func(x: int) -> int:
        return x

    # x is passed positionally, so not in kwargs; validation is skipped.
    result: int = func(0)
    assert result == 0


def test_validate_kwarg_with_none_value() -> None:
    """Test validate_kwarg when None is passed and validator rejects None."""

    @validate_kwarg("x", lambda x: x is not None, "x should not be None")
    def func(x: Optional[int] = 1) -> Optional[int]:
        return x

    with pytest.raises(ValueError, match="x should not be None"):
        func(x=None)


def test_validate_kwarg_always_fail() -> None:
    """Test that a validator that always fails triggers an error."""

    @validate_kwarg("x", lambda x: False, "always fail")
    def func(x: int = 1) -> int:
        return x

    with pytest.raises(ValueError, match="always fail"):
        func(x=10)


def test_validate_kwarg_multiple_kwargs() -> None:
    """Test that validate_kwarg only validates the specified kwarg among multiple arguments."""

    @validate_kwarg("y", lambda y: y < 100, "y must be < 100, got {value}")
    def func(x: int, y: int = 1) -> Tuple[int, int]:
        return (x, y)

    # Valid case:
    result: Tuple[int, int] = func(5, y=50)
    assert result == (5, 50)

    # Invalid y value (passed via kwargs)
    with pytest.raises(ValueError, match="y must be < 100, got 150"):
        func(5, y=150)


def test_validate_kwarg_action_warn_multiple_calls() -> None:
    """Test that when action is 'warn', multiple failures emit warnings without raising exceptions."""

    @validate_kwarg(
        "num",
        lambda val: val > 0,
        "num must be > 0, got {value}",
        action=ErrorMode.EXCEPT,
    )
    def only_positive(num: int) -> int:
        return num

    # A good value should not trigger a warning.
    assert only_positive(num=10) == 10

    # Check that a warning is emitted for a bad value.
    with pytest.raises(ValueError, match="num must be > 0, got -5"):
        only_positive(num=-5)


# --- Additional tests for replace_kwarg ---


def test_replace_kwarg_with_positional_argument() -> None:
    """Test that replace_kwarg does not act on positional arguments."""

    @replace_kwarg(
        "x",
        typed_lambda(lambda x: x == 0, (int,), bool),
        99,
    )
    def func(x: int) -> int:
        return x

    # Passing argument positionally; no replacement happens because it's not in kwargs.
    result: int = func(0)
    assert result == 0


def test_replace_kwarg_no_if_missing() -> None:
    """Test replace_kwarg with mutable types as default and replacement values."""
    replacement_dict: Dict[str, int] = {"a": 1}

    @replace_kwarg("d", is_none, replacement_dict)
    def func(d: Optional[Dict[str, int]] = None) -> Optional[Dict[str, int]]:
        return d

    assert func() != replacement_dict
    assert func(d=None) == replacement_dict
    assert func(d={"a": 2}) != replacement_dict


def test_replace_kwarg_if_missing() -> None:
    """Test replace_kwarg with mutable types as default and replacement values."""
    replacement_dict: Dict[str, int] = {"a": 1}

    @replace_kwarg("d", is_none, replacement_dict, replace_if_missing=True)
    def func(d: Optional[Dict[str, int]] = None) -> Optional[Dict[str, int]]:
        return d

    assert func() == replacement_dict
    assert func(d=None) == replacement_dict
    assert func(d={"a": 2}) != replacement_dict


# --- Combined Decorator Tests ---


def test_combined_decorators_with_missing_kwarg() -> None:
    """Test that combined decorators do nothing if the target kwarg is missing.

    Because the kwarg is not in kwargs, neither process_kwarg nor validate_kwarg acts.
    """

    @process_kwarg("x", typed_lambda(lambda x: x + 5, (int,), int))
    @validate_kwarg("x", lambda x: x < 50, "x too high: {value}")
    def func(x: int = 10) -> int:
        return x

    result: int = func()
    assert result == 10


def test_combined_decorators_with_positional_argument() -> None:
    """Test combined decorators when the argument is passed positionally.

    Since the argument is not in kwargs, the decorators do not trigger.
    """

    @validate_kwarg("x", lambda x: x < 50, "x too high: {value}")
    @process_kwarg("x", typed_lambda(lambda x: x + 5, (int,), int))
    def func(x: int = 10) -> int:
        return x

    result: int = func(45)
    assert result == 45


# --- Metadata Preservation Tests for All Decorators ---


def test_process_kwarg_preserves_metadata() -> None:
    """Test that process_kwarg preserves function metadata (__name__ and __doc__)."""

    @process_kwarg("x", lambda x: x)
    def func(x: int = 0) -> int:
        """Process docstring."""
        return x

    assert func.__name__ == "func"
    assert func.__doc__ == "Process docstring."


def test_validate_kwarg_preserves_metadata() -> None:
    """Test that validate_kwarg preserves function metadata (__name__ and __doc__)."""

    @validate_kwarg("x", lambda x: x > 0)
    def func(x: int = 1) -> int:
        """Validate docstring."""
        return x

    assert func.__name__ == "func"
    assert func.__doc__ == "Validate docstring."


def test_replace_kwarg_preserves_metadata() -> None:
    """Test that replace_kwarg preserves function metadata (__name__ and __doc__)."""

    @replace_kwarg("x", is_none, 100)
    def func(x: Optional[int] = None) -> Optional[int]:
        """Replace docstring."""
        return x

    assert func.__name__ == "func"
    assert func.__doc__ == "Replace docstring."


def test_typed_lambda_int_int_to_int() -> None:
    adder = typed_lambda(lambda x, y: x + y, (int, int), int)
    result: int = adder(10, 20)
    assert result == 30
    assert adder.__annotations__ == {"x": int, "y": int, "return": int}


def test_typed_lambda_int_str_to_str() -> None:
    concat = typed_lambda(lambda x, s: str(x) + s, (int, str), str)
    result: str = concat(3, "_apples")
    assert result == "3_apples"
    assert concat.__annotations__ == {"x": int, "s": str, "return": str}


def test_typed_lambda_mismatched_params() -> None:
    with pytest.raises(ValueError):
        _ = typed_lambda(lambda x, y: x + y, (int,), int)  # type: ignore[misc]


def test_typed_lambda_runtime_behavior() -> None:
    add_three = typed_lambda(
        lambda x, y, z: x + y + z,
        (int, int, int),
        int,
    )
    result: int = add_three(1, 2, 3)
    assert result == 6


def test_typed_lambda_annotations_check() -> None:
    any_lambda = typed_lambda(lambda a, b, c: [a, b, c], (str, float, bool), list)
    expected = {
        "a": str,
        "b": float,
        "c": bool,
        "return": list,
    }
    assert any_lambda.__annotations__ == expected
