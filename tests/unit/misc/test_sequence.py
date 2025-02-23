import pytest

from muutils.misc.sequence import (
    list_split,
    list_join,
    flatten,
    apply_mapping_chain,
    apply_mapping,
)

# Test data
simple_mapping = {1: "one", 2: "two", 3: "three"}
chain_mapping = {1: ["one", "uno"], 2: ["two", "dos"], 3: ["three", "tres"]}


def test_list_split():
    # with integers
    assert list_split([1, 2, 3, 2, 4], 2) == [
        [1],
        [3],
        [4],
    ], "List should be split correctly"
    assert list_split([1, 2, 2, 2, 4], 2) == [
        [1],
        [],
        [],
        [4],
    ], "Empty sublists should be created for consecutive delimiters"
    assert list_split([], 2) == [
        []
    ], "Empty list should return a list with one empty sublist"

    # with strings
    assert list_split(["a", "b", "c", "b", "d"], "b") == [
        ["a"],
        ["c"],
        ["d"],
    ], "List should be split correctly"
    assert list_split(["a", "b", "b", "b", "d"], "b") == [
        ["a"],
        [],
        [],
        ["d"],
    ], "Empty sublists should be created for consecutive delimiters"
    assert list_split([], "b") == [
        []
    ], "Empty list should return a list with one empty sublist"

    # mixed types
    assert list_split([1, "b", 3, "b", 4], "b") == [
        [1],
        [3],
        [4],
    ], "List should be split correctly"
    assert list_split([1, "b", "b", "b", 4], "b") == [
        [1],
        [],
        [],
        [4],
    ], "Empty sublists should be created for consecutive delimiters"
    assert list_split([], "b") == [
        []
    ], "Empty list should return a list with one empty sublist"

    assert list_split([1, 2, 3, 0, 4, 5, 0, 6], 0) == [[1, 2, 3], [4, 5], [6]]
    assert list_split([0, 1, 2, 3], 0) == [[], [1, 2, 3]]
    assert list_split([1, 2, 3], 0) == [[1, 2, 3]]
    assert list_split([], 0) == [[]]


def test_list_join():
    # with integers
    assert list_join([1, 2, 3], lambda: 0) == [
        1,
        0,
        2,
        0,
        3,
    ], "Items should be joined correctly with factory-produced values"
    assert list_join([1], lambda: 0) == [1], "Single item list should remain unchanged"
    assert list_join([], lambda: 0) == [], "Empty list should remain unchanged"

    # with strings
    assert list_join(["a", "b", "c"], lambda: "x") == [
        "a",
        "x",
        "b",
        "x",
        "c",
    ], "Items should be joined correctly with factory-produced values"
    assert list_join(["a"], lambda: "x") == [
        "a"
    ], "Single item list should remain unchanged"
    assert list_join([], lambda: "x") == [], "Empty list should remain unchanged"

    # mixed types
    assert list_join([1, "b", 3], lambda: "x") == [
        1,
        "x",
        "b",
        "x",
        3,
    ], "Items should be joined correctly with factory-produced values"
    assert list_join([1], lambda: "x") == [
        1
    ], "Single item list should remain unchanged"
    assert list_join([], lambda: "x") == [], "Empty list should remain unchanged"


# Testing the flatten function
def test_flatten_full_flattening():
    assert list(flatten([1, [2, [3, 4]], 5])) == [1, 2, 3, 4, 5]
    assert list(flatten([1, [2, [3, [4, [5]]]]])) == [1, 2, 3, 4, 5]
    assert list(flatten([])) == []


def test_flatten_partial_flattening():
    assert list(flatten([1, [2, [3, 4]], 5], levels_to_flatten=1)) == [1, 2, [3, 4], 5]
    assert list(flatten([1, [2, [3, [4, [5]]]]], levels_to_flatten=2)) == [
        1,
        2,
        3,
        [4, [5]],
    ]


def test_flatten_with_non_iterables():
    assert list(flatten([1, 2, 3])) == [1, 2, 3]
    assert list(flatten([1, "abc", 2, [3, 4], 5])) == [1, "abc", 2, 3, 4, 5]


def test_apply_mapping_basic():
    assert apply_mapping(simple_mapping, [1, 2, 3]) == ["one", "two", "three"]


def test_apply_mapping_missing_skip():
    assert apply_mapping(simple_mapping, [1, 4, 2], when_missing="skip") == [
        "one",
        "two",
    ]


def test_apply_mapping_missing_include():
    assert apply_mapping(simple_mapping, [1, 4, 2], when_missing="include") == [
        "one",
        4,
        "two",
    ]


def test_apply_mapping_missing_except():
    with pytest.raises(KeyError):
        apply_mapping(simple_mapping, [1, 4, 2], when_missing="except")


def test_apply_mapping_invalid_when_missing():
    with pytest.raises(ValueError):
        apply_mapping(simple_mapping, [1, 2, 3, 4], when_missing="invalid")  # type: ignore[arg-type]


def test_apply_mapping_empty_input():
    assert apply_mapping(simple_mapping, []) == []


def test_apply_mapping_empty_mapping():
    assert apply_mapping({}, [1, 2, 3], when_missing="include") == [1, 2, 3]


def test_apply_mapping_chain_basic():
    assert apply_mapping_chain(chain_mapping, [1, 2, 3]) == [
        "one",
        "uno",
        "two",
        "dos",
        "three",
        "tres",
    ]


def test_apply_mapping_chain_missing_skip():
    assert apply_mapping_chain(chain_mapping, [1, 4, 2], when_missing="skip") == [
        "one",
        "uno",
        "two",
        "dos",
    ]


def test_apply_mapping_chain_missing_include():
    assert apply_mapping_chain(chain_mapping, [1, 4, 2], when_missing="include") == [
        "one",
        "uno",
        4,
        "two",
        "dos",
    ]


def test_apply_mapping_chain_missing_except():
    with pytest.raises(KeyError):
        apply_mapping_chain(chain_mapping, [1, 4, 2], when_missing="except")


def test_apply_mapping_chain_invalid_when_missing():
    with pytest.raises(ValueError):
        apply_mapping_chain(chain_mapping, [1, 2, 3, 4], when_missing="invalid")  # type: ignore[arg-type]


def test_apply_mapping_chain_empty_input():
    assert apply_mapping_chain(chain_mapping, []) == []


def test_apply_mapping_chain_empty_mapping():
    assert apply_mapping_chain({}, [1, 2, 3], when_missing="include") == [1, 2, 3]


def test_apply_mapping_chain_empty_values():
    empty_chain_mapping = {1: [], 2: ["two"], 3: []}
    assert apply_mapping_chain(empty_chain_mapping, [1, 2, 3]) == ["two"]
