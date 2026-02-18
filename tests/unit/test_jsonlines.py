from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from muutils.json_serialize import JSONitem
from muutils.jsonlines import jsonl_load, jsonl_load_log, jsonl_write

TEMP_PATH: Path = Path("tests/_temp/jsonl")


def test_jsonl_load():
    """Test loading jsonlines file - write data, load it back, verify it matches."""
    # Create temp directory
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    test_file = TEMP_PATH / "test_load.jsonl"

    # Create test data
    test_data = [
        {"id": 1, "name": "Alice", "value": 42.5},
        {"id": 2, "name": "Bob", "value": 17.3},
        {"id": 3, "name": "Charlie", "value": None},
        {"list": [1, 2, 3], "nested": {"a": 1, "b": 2}},
    ]

    # Write the data manually
    with open(test_file, "w", encoding="UTF-8") as f:
        for item in test_data:
            f.write(json.dumps(item) + "\n")

    # Load it back using jsonl_load
    loaded_data = jsonl_load(str(test_file))

    # Verify the data matches
    assert loaded_data == test_data
    assert len(loaded_data) == 4
    loaded_item_0 = loaded_data[0]
    assert isinstance(loaded_item_0, dict)
    assert loaded_item_0["name"] == "Alice"  # ty: ignore[invalid-argument-type, invalid-key]
    loaded_item_3 = loaded_data[3]
    assert isinstance(loaded_item_3, dict)
    loaded_item_3_nested = loaded_item_3["nested"]  # ty: ignore[invalid-argument-type, invalid-key]
    assert isinstance(loaded_item_3_nested, dict)
    assert loaded_item_3_nested["b"] == 2


def test_jsonl_write():
    """Test writing jsonlines data - write using jsonl_write, read raw contents, verify format."""
    # Create temp directory
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    test_file = TEMP_PATH / "test_write.jsonl"

    # Test data
    test_data: list[JSONitem] = [
        {"id": 1, "status": "active"},
        {"id": 2, "status": "inactive"},
        {"id": 3, "status": "pending", "metadata": {"priority": "high"}},
    ]

    # Write using jsonl_write
    jsonl_write(str(test_file), test_data)

    # Read raw contents
    with open(test_file, "r", encoding="UTF-8") as f:
        lines = f.readlines()

    # Verify format
    assert len(lines) == 3

    # Each line should be valid JSON
    for i, line in enumerate(lines):
        assert line.endswith("\n")
        parsed = json.loads(line)
        assert parsed == test_data[i]

    # Verify specific content
    assert json.loads(lines[0]) == {"id": 1, "status": "active"}
    assert json.loads(lines[2])["metadata"]["priority"] == "high"


def test_gzip_support():
    """Test .gz extension auto-detection for both reading and writing."""
    # Create temp directory
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    test_file_gz = TEMP_PATH / "test_gzip.jsonl.gz"
    test_file_gzip = TEMP_PATH / "test_gzip2.jsonl.gzip"

    # Test data
    test_data: list[JSONitem] = [
        {"compressed": True, "value": 123},
        {"compressed": True, "value": 456},
    ]

    # Test with .gz extension - auto-detection
    jsonl_write(str(test_file_gz), test_data)

    # Verify it's actually gzipped by trying to read with gzip
    with gzip.open(test_file_gz, "rt", encoding="UTF-8") as f:
        lines = f.readlines()
    assert len(lines) == 2

    # Load back using jsonl_load with auto-detection
    loaded_data = jsonl_load(str(test_file_gz))
    assert loaded_data == test_data

    # Test with .gzip extension
    jsonl_write(str(test_file_gzip), test_data)
    loaded_data_gzip = jsonl_load(str(test_file_gzip))
    assert loaded_data_gzip == test_data

    # Test explicit use_gzip parameter
    test_file_explicit = TEMP_PATH / "test_explicit.jsonl"
    jsonl_write(str(test_file_explicit), test_data, use_gzip=True)

    # Should be gzipped even without .gz extension
    with gzip.open(test_file_explicit, "rt", encoding="UTF-8") as f:
        lines = f.readlines()
    assert len(lines) == 2

    loaded_explicit = jsonl_load(str(test_file_explicit), use_gzip=True)
    assert loaded_explicit == test_data


def test_jsonl_load_log():
    """Test jsonl_load_log with dict assertion - test with valid dicts and non-dict items."""
    # Create temp directory
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    # Test with valid dict data
    test_file_valid = TEMP_PATH / "test_log_valid.jsonl"
    valid_data: list[JSONitem] = [
        {"level": "INFO", "message": "Starting process"},
        {"level": "WARNING", "message": "Low memory"},
        {"level": "ERROR", "message": "Connection failed"},
    ]

    jsonl_write(str(test_file_valid), valid_data)
    loaded_log = jsonl_load_log(str(test_file_valid))

    assert loaded_log == valid_data
    assert all(isinstance(item, dict) for item in loaded_log)

    # Test with non-dict items - should raise AssertionError
    test_file_invalid = TEMP_PATH / "test_log_invalid.jsonl"
    invalid_data: list[JSONitem] = [
        {"level": "INFO", "message": "Valid entry"},
        "not a dict",  # This is invalid
        {"level": "ERROR", "message": "Another valid entry"},
    ]

    jsonl_write(str(test_file_invalid), invalid_data)

    with pytest.raises(AssertionError) as exc_info:
        jsonl_load_log(str(test_file_invalid))

    # Verify the error message contains useful information
    error_msg = str(exc_info.value)
    assert "idx = 1" in error_msg
    assert "is not a dict" in error_msg

    # Test with list item
    test_file_list = TEMP_PATH / "test_log_list.jsonl"
    list_data: list[JSONitem] = [
        {"level": "INFO"},
        [1, 2, 3],  # List instead of dict
    ]

    jsonl_write(str(test_file_list), list_data)

    with pytest.raises(AssertionError) as exc_info:
        jsonl_load_log(str(test_file_list))

    error_msg = str(exc_info.value)
    assert "idx = 1" in error_msg
    assert "is not a dict" in error_msg


def test_gzip_compresslevel():
    """Test that gzip_compresslevel parameter works without errors."""
    # Create temp directory
    TEMP_PATH.mkdir(parents=True, exist_ok=True)

    test_file = TEMP_PATH / "test_compresslevel.jsonl.gz"

    # Create test data
    test_data: list[JSONitem] = [{"value": i, "data": "content"} for i in range(10)]

    # Write with different compression levels - should not error
    jsonl_write(str(test_file), test_data, gzip_compresslevel=1)
    loaded_data = jsonl_load(str(test_file))
    assert loaded_data == test_data

    jsonl_write(str(test_file), test_data, gzip_compresslevel=9)
    loaded_data = jsonl_load(str(test_file))
    assert loaded_data == test_data
