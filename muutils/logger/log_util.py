from muutils.jsonlines import jsonl_load_log


def get_any_from_stream(stream: list[dict], key: str) -> None:
    """get the first value of a key from a stream. errors if not found"""
    for msg in stream:
        if key in msg:
            return msg[key]

    raise KeyError(f"key '{key}' not found in stream")


def gather_log(file: str) -> dict[str, list[dict]]:
    """gathers and sorts all streams from a log"""
    data: list[dict] = jsonl_load_log(file)
    output: dict[str, list[dict]] = dict()

    for item in data:
        stream: str = item.get("_stream", None)
        if stream not in output:
            output[stream] = list()
        output[stream].append(item)

    return output


def gather_stream(
    file: str,
    stream: str,
) -> list[dict]:
    """gets all entries from a specific stream in a log file"""
    data: list[dict] = jsonl_load_log(file)

    output: list[dict] = list()

    for item in data:
        # select for the stream
        if ("_stream" in item) and (item["_stream"] == stream):
            output.append(item)
    return output


def gather_val(
    file: str,
    stream: str,
    keys: tuple[str],
    allow_skip: bool = True,
) -> list[list]:
    """gather specific keys from a specific stream in a log file

    example:
    if "log.jsonl" has contents:
    ```jsonl
    {"a": 1, "b": 2, "c": 3, "_stream": "s1"}
    {"a": 4, "b": 5, "c": 6, "_stream": "s1"}
    {"a": 7, "b": 8, "c": 9, "_stream": "s2"}
    ```
    then `gather_val("log.jsonl", "s1", ("a", "b"))` will return
    ```python
    [
        [1, 2],
        [4, 5]
    ]
    ```

    """
    data: list[dict] = jsonl_load_log(file)

    output: list[list] = list()

    for item in data:
        # select for the stream
        if ("_stream" in item) and (item["_stream"] == stream):
            # select for the keys
            if all(k in item for k in keys):
                output.append(list(item[k] for k in keys))
            elif not allow_skip:
                raise ValueError(f"missing keys '{keys = }' in '{item = }'")

    return output
