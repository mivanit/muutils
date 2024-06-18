from __future__ import annotations

from muutils.group_equiv import group_by_equivalence


def test_group_by_equivalence_simple():
    # Test with integers and simple equality
    assert group_by_equivalence([1, 1, 2, 2, 3, 3], lambda x, y: x == y) == [
        [1, 1],
        [2, 2],
        [3, 3],
    ]
    assert group_by_equivalence([1, 1, 2, 4, 5, 5], lambda x, y: x == y) == [
        [1, 1],
        [2],
        [4],
        [5, 5],
    ]

    # Test with strings and simple equality
    assert group_by_equivalence(
        ["a", "a", "b", "b", "c", "c"], lambda x, y: x == y
    ) == [["a", "a"], ["b", "b"], ["c", "c"]]


def _non_transitive_relation(x: int, y: int) -> bool:
    return abs(x - y) <= 1


def test_group_by_equivalence_non_transitive():
    assert group_by_equivalence(list(range(5)), _non_transitive_relation) == [
        [0, 1, 2, 3, 4]
    ]

    assert group_by_equivalence([0, 1, 10, 11], _non_transitive_relation) == [
        [0, 1],
        [10, 11],
    ]

    assert group_by_equivalence(
        [0, 1, 5, 4, 10, 11, 3, 2], _non_transitive_relation
    ) == [[10, 11], [0, 1, 5, 4, 3, 2]]

    assert group_by_equivalence(
        [0, 1, 5, 4, 10, 11, 3, 2], _non_transitive_relation
    ) == [[10, 11], [0, 1, 5, 4, 3, 2]]
