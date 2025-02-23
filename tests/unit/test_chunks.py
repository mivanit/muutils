from muutils.mlutils import chunks


def test_chunks_empty():
    input_list: list = []
    chunk_size: int = 3
    expected_output: list = []
    assert list(chunks(input_list, chunk_size)) == expected_output


def test_chunks_single():
    input_list = ["a"]
    expected_output = [["a"]]
    assert list(chunks(input_list, 1)) == expected_output
    assert list(chunks(input_list, 2)) == expected_output


def test_chunks_batch_multiple():
    input_list = list(range(6))
    chunk_size = 3
    expected_output = [[0, 1, 2], [3, 4, 5]]
    assert list(chunks(input_list, chunk_size)) == expected_output


def test_chunks_batch_remainder():
    input_list = list(range(7))
    chunk_size = 3
    expected_output = [[0, 1, 2], [3, 4, 5], [6]]
    assert list(chunks(input_list, chunk_size)) == expected_output


def test_chunks_longer():
    input_list = list(range(10))
    chunk_size = 3
    expected_output = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    assert list(chunks(input_list, chunk_size)) == expected_output


def test_chunks_strings():
    input_list = ["a", "b", "c", "d", "e"]
    chunk_size = 2
    expected_output = [["a", "b"], ["c", "d"], ["e"]]
    assert list(chunks(input_list, chunk_size)) == expected_output
