import pytest

from muutils.dictmagic import dotlist_to_nested_dict, update_with_nested_dict, kwargs_to_nested_dict
from muutils.json_serialize import SerializableDataclass, serializable_dataclass


def test_dotlist_to_nested_dict():
    # Positive case
    assert dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}) == {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
    
    # Negative case
    with pytest.raises(TypeError):
        dotlist_to_nested_dict({1: 1})

    # Test with different separator
    assert dotlist_to_nested_dict({'a/b/c': 1, 'a/b/d': 2, 'a/e': 3}, sep='/') == {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}

def test_update_with_nested_dict():
    # Positive case
    assert update_with_nested_dict({'a': {'b': 1}, "c": -1}, {'a': {"b": 2}}) == {'a': {'b': 2}, 'c': -1}
    
    # Case where the key is not present in original dict
    assert update_with_nested_dict({'a': {'b': 1}, "c": -1}, {'d': 3}) == {'a': {'b': 1}, 'c': -1, 'd': 3}
    
    # Case where a nested value is overridden
    assert update_with_nested_dict({'a': {'b': 1, 'd': 3}, "c": -1}, {'a': {"b": 2}}) == {'a': {'b': 2, 'd': 3}, 'c': -1}
    
    # Case where the dict we are trying to update does not exist
    assert update_with_nested_dict({'a': 1}, {'b': {"c": 2}}) == {'a': 1, 'b': {'c': 2}}

def test_kwargs_to_nested_dict():
    # Positive case
    assert kwargs_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}) == {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}

    # Case where strip_prefix is not None
    assert kwargs_to_nested_dict({'prefix.a.b.c': 1, 'prefix.a.b.d': 2, 'prefix.a.e': 3}, strip_prefix='prefix.') == {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}

    # Negative case
    with pytest.raises(ValueError):
        kwargs_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}, strip_prefix='prefix.', when_unknown_prefix='raise')
    
    # Case where -- and - prefix
    assert kwargs_to_nested_dict({'--a.b.c': 1, '--a.b.d': 2, 'a.e': 3}, strip_prefix='--', when_unknown_prefix='ignore') == {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
    
    # Case where -- and - prefix with warning
    with pytest.warns(UserWarning):
        kwargs_to_nested_dict({'--a.b.c': 1, '-a.b.d': 2, 'a.e': 3}, strip_prefix='-', when_unknown_prefix='warn')


def test_kwargs_to_nested_dict_transform_key():

    # Case where transform_key is not None, changing dashes to underscores
    assert kwargs_to_nested_dict(
        {'a-b-c': 1, 'a-b-d': 2, 'a-e': 3}, 
        transform_key=lambda x: x.replace('-', '_')
    ) == {'a_b_c': 1, 'a_b_d': 2, 'a_e': 3}

    # Case where strip_prefix and transform_key are both used
    assert kwargs_to_nested_dict(
        {'prefix.a-b-c': 1, 'prefix.a-b-d': 2, 'prefix.a-e': 3}, 
        strip_prefix='prefix.', 
        transform_key=lambda x: x.replace('-', '_')
    ) == {'a_b_c': 1, 'a_b_d': 2, 'a_e': 3}

    # Case where strip_prefix, transform_key and when_unknown_prefix='raise' are all used
    with pytest.raises(ValueError):
        kwargs_to_nested_dict(
            {'a-b-c': 1, 'prefix.a-b-d': 2, 'prefix.a-e': 3}, 
            strip_prefix='prefix.', 
            transform_key=lambda x: x.replace('-', '_'), 
            when_unknown_prefix='raise'
        )
    
    # Case where strip_prefix, transform_key and when_unknown_prefix='warn' are all used
    with pytest.warns(UserWarning):
        assert kwargs_to_nested_dict(
            {'a-b-c': 1, 'prefix.a-b-d': 2, 'prefix.a-e': 3}, 
            strip_prefix='prefix.', 
            transform_key=lambda x: x.replace('-', '_'), 
            when_unknown_prefix='warn'
        ) == {'a_b_c': 1, 'a_b_d': 2, 'a_e': 3}


@serializable_dataclass
class ChildData(SerializableDataclass):
    x: int
    y: int


@serializable_dataclass
class ParentData(SerializableDataclass):
    a: int
    b: ChildData


def test_update_from_nested_dict():
    parent = ParentData(a=1, b=ChildData(x=2, y=3))
    update_data = {"a": 5, "b": {"x": 6}}
    parent.update_from_nested_dict(update_data)

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 3

    update_data2 = {"b": {"y": 7}}
    parent.update_from_nested_dict(update_data2)

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 7


def test_update_from_dotlists():
    parent = ParentData(a=1, b=ChildData(x=2, y=3))
    update_data = {"a": 5, "b.x": 6}
    parent.update_from_nested_dict(dotlist_to_nested_dict(update_data))

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 3

    update_data2 = {"b.y": 7}
    parent.update_from_nested_dict(dotlist_to_nested_dict(update_data2))

    assert parent.a == 5
    assert parent.b.x == 6
    assert parent.b.y == 7
