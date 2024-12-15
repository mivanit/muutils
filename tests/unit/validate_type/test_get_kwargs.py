import os

from muutils.validate_type import get_fn_allowed_kwargs


def test_with_positional_args_only():
    def fn(a, b, c):
        pass

    assert get_fn_allowed_kwargs(fn) == {"a", "b", "c"}


def test_with_keyword_args_only():
    def fn(*, a, b, c):
        pass

    assert get_fn_allowed_kwargs(fn) == {"a", "b", "c"}


def test_with_mixed_args():
    def fn(a, b, *, c, d):
        pass

    assert get_fn_allowed_kwargs(fn) == {"a", "b", "c", "d"}


def test_with_positional_only_args():
    def fn(a, b, /, c, d):
        pass

    assert get_fn_allowed_kwargs(fn) == {"c", "d"}


def test_with_var_args():
    def fn(a, b, *args, c, d, **kwargs):
        pass

    assert get_fn_allowed_kwargs(fn) == {"a", "b", "c", "d"}


def test_with_no_args():
    def fn():
        pass

    assert get_fn_allowed_kwargs(fn) == set()


def test_with_builtin_function():
    try:
        get_fn_allowed_kwargs(len)
    except ValueError as e:
        assert "Cannot retrieve signature" in str(e)


def test_with_problematic_function():
    try:
        get_fn_allowed_kwargs(os.path.basename)
    except ValueError as e:
        assert "Cannot retrieve signature" in str(e)


def test_with_class_method():
    class MyClass:
        @classmethod
        def cls_method(cls, a, b=2, *, c=3):
            pass

    assert get_fn_allowed_kwargs(MyClass.cls_method) == {"a", "b", "c"}


def test_with_lambda():
    lambda_fn = lambda a, b, c=3: a + b + c  # noqa: E731
    assert get_fn_allowed_kwargs(lambda_fn) == {"a", "b", "c"}


def test_with_function_defaults():
    def fn(a, b=2, *, c=3):
        pass

    assert get_fn_allowed_kwargs(fn) == {"a", "b", "c"}


def test_with_complicated_defaults_and_types():
    def fn(
        a: int, b: str = "default", *, c: list = [1, 2, 3], d: dict = {"key": "value"}
    ):
        pass

    assert get_fn_allowed_kwargs(fn) == {"a", "b", "c", "d"}
