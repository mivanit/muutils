from __future__ import annotations

import os
from pathlib import Path

import pytest

from muutils.json_serialize import JSONitem
from muutils.jsonlines import jsonl_write
from muutils.logger.log_util import (
    gather_log,
    gather_stream,
    gather_val,
    get_any_from_stream,
)

TEMP_PATH: Path = Path("tests/_temp/logger")


def test_gather_log():
    """Test gathering and sorting all streams from a multi-stream log file"""
    # Create test directory
    os.makedirs(TEMP_PATH, exist_ok=True)
    log_file = TEMP_PATH / "test_gather_log.jsonl"

    # Create test data with multiple streams
    test_data: list[JSONitem] = [
        {"msg": "stream1_msg1", "value": 1, "_stream": "stream1"},
        {"msg": "stream2_msg1", "value": 10, "_stream": "stream2"},
        {"msg": "stream1_msg2", "value": 2, "_stream": "stream1"},
        {"msg": "default_msg1", "value": 100},  # no _stream key
        {"msg": "stream2_msg2", "value": 20, "_stream": "stream2"},
        {"msg": "stream1_msg3", "value": 3, "_stream": "stream1"},
    ]

    jsonl_write(str(log_file), test_data)

    # Gather all streams
    result = gather_log(str(log_file))

    # Verify correct streams are present
    assert "stream1" in result
    assert "stream2" in result
    assert "default" in result

    # Verify stream separation
    assert len(result["stream1"]) == 3
    assert len(result["stream2"]) == 2
    assert len(result["default"]) == 1

    # Verify data integrity
    assert result["stream1"][0]["msg"] == "stream1_msg1"
    assert result["stream1"][1]["msg"] == "stream1_msg2"
    assert result["stream1"][2]["msg"] == "stream1_msg3"

    assert result["stream2"][0]["msg"] == "stream2_msg1"
    assert result["stream2"][1]["msg"] == "stream2_msg2"

    assert result["default"][0]["msg"] == "default_msg1"
    assert result["default"][0]["value"] == 100


def test_gather_stream():
    """Test extracting a specific stream from a log file"""
    os.makedirs(TEMP_PATH, exist_ok=True)
    log_file = TEMP_PATH / "test_gather_stream.jsonl"

    # Create test data with multiple streams
    test_data: list[JSONitem] = [
        {"msg": "stream1_msg1", "idx": 1, "_stream": "target"},
        {"msg": "stream2_msg1", "idx": 2, "_stream": "other"},
        {"msg": "stream1_msg2", "idx": 3, "_stream": "target"},
        {"msg": "no_stream", "idx": 4},  # no _stream key
        {"msg": "stream2_msg2", "idx": 5, "_stream": "other"},
        {"msg": "stream1_msg3", "idx": 6, "_stream": "target"},
    ]

    jsonl_write(str(log_file), test_data)

    # Gather only the "target" stream
    result = gather_stream(str(log_file), "target")

    # Verify filtering
    assert len(result) == 3

    # Verify correct items were selected
    assert result[0]["msg"] == "stream1_msg1"
    assert result[0]["idx"] == 1
    assert result[1]["msg"] == "stream1_msg2"
    assert result[1]["idx"] == 3
    assert result[2]["msg"] == "stream1_msg3"
    assert result[2]["idx"] == 6

    # Verify all items have the correct stream
    for item in result:
        assert item["_stream"] == "target"

    # Test with non-existent stream
    empty_result = gather_stream(str(log_file), "nonexistent")
    assert len(empty_result) == 0


def test_gather_val():
    """Test extracting specific keys from a specific stream"""
    os.makedirs(TEMP_PATH, exist_ok=True)
    log_file = TEMP_PATH / "test_gather_val.jsonl"

    # Create test data matching the example from the docstring
    test_data: list[JSONitem] = [
        {"a": 1, "b": 2, "c": 3, "_stream": "s1"},
        {"a": 4, "b": 5, "c": 6, "_stream": "s1"},
        {"a": 7, "b": 8, "c": 9, "_stream": "s2"},
        {"a": 10, "b": 11, "_stream": "s1"},  # missing key 'c'
        {"a": 13, "b": 14, "c": 15, "_stream": "s1"},
    ]

    jsonl_write(str(log_file), test_data)

    # Test basic key extraction
    result = gather_val(str(log_file), "s1", ("a", "b"))

    # Verify data structure
    assert len(result) == 4  # s1 has 4 entries
    assert result[0] == [1, 2]
    assert result[1] == [4, 5]
    assert result[2] == [10, 11]
    assert result[3] == [13, 14]

    # Test with three keys (should skip the entry missing 'c')
    result_three_keys = gather_val(str(log_file), "s1", ("a", "b", "c"))
    assert len(result_three_keys) == 3  # one entry missing 'c' is skipped
    assert result_three_keys[0] == [1, 2, 3]
    assert result_three_keys[1] == [4, 5, 6]
    assert result_three_keys[2] == [13, 14, 15]

    # Test with allow_skip=False - should raise error on missing key
    with pytest.raises(ValueError, match="missing keys"):
        gather_val(str(log_file), "s1", ("a", "b", "c"), allow_skip=False)

    # Test with different stream
    result_s2 = gather_val(str(log_file), "s2", ("a", "c"))
    assert len(result_s2) == 1
    assert result_s2[0] == [7, 9]

    # Test with non-existent stream
    empty_result = gather_val(str(log_file), "nonexistent", ("a", "b"))
    assert len(empty_result) == 0


def test_get_any_from_stream():
    """Test extracting first value of a key from stream and KeyError on missing key"""
    # Test with a list of dicts
    stream = [
        {"foo": "bar", "value": 1},
        {"foo": "baz", "value": 2},
        {"other": "data", "value": 3},
    ]

    # Test successful key extraction (first occurrence)
    result = get_any_from_stream(stream, "foo")
    assert result == "bar"  # should get the first one

    # Test key that exists later
    result_value = get_any_from_stream(stream, "value")
    assert result_value == 1  # first occurrence

    # Test key that appears only in later entry
    result_other = get_any_from_stream(stream, "other")
    assert result_other == "data"

    # Test KeyError on missing key
    with pytest.raises(KeyError, match="key 'nonexistent' not found in stream"):
        get_any_from_stream(stream, "nonexistent")

    # Test with empty stream
    with pytest.raises(KeyError, match="key 'foo' not found in stream"):
        get_any_from_stream([], "foo")
