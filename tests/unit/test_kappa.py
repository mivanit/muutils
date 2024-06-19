from typing import Mapping

import pytest

from muutils.kappa import _BASE_DOC, Kappa


def test_Kappa_returns_Kappa_instance():
    func = lambda x: x**2  # noqa: E731
    result = Kappa(func)
    assert isinstance(result, Mapping), "Kappa did not return a Mapping instance"


def test_Kappa_getitem_calls_func():
    func = lambda x: x**2  # noqa: E731
    result = Kappa(func)
    assert result[2] == 4, "__getitem__ did not correctly call the input function"


def test_Kappa_doc_is_correctly_formatted():
    func = lambda x: x**2  # noqa: E731
    result = Kappa(func)
    expected_doc = _BASE_DOC + "None"
    assert result.doc == expected_doc, "doc was not correctly formatted"


def test_Kappa_getitem_works_with_different_functions():
    func = lambda x: x + 1  # noqa: E731
    result = Kappa(func)
    assert result[2] == 3, "__getitem__ did not correctly call the input function"

    func = lambda x: str(x)  # noqa: E731
    result = Kappa(func)
    assert result[2] == "2", "__getitem__ did not correctly call the input function"


def test_Kappa_iter_raises_NotImplementedError():
    func = lambda x: x**2  # noqa: E731
    result = Kappa(func)
    with pytest.raises(NotImplementedError):
        iter(result)


def test_Kappa_len_raises_NotImplementedError():
    func = lambda x: x**2  # noqa: E731
    result = Kappa(func)
    with pytest.raises(NotImplementedError):
        len(result)


def test_Kappa_doc_works_with_function_with_docstring():
    func = lambda x: x**2  # noqa: E731
    func.__doc__ = "This is a test function"
    result = Kappa(func)
    expected_doc = _BASE_DOC + "This is a test function"
    assert (
        result.doc == expected_doc
    ), "doc was not correctly formatted with function with docstring"
