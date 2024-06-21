def replace_typing_aliases(filename: str) -> str:
    # Dictionary to map old types from the typing module to the new built-in types
    replacements = {
        "typing.List": "list",
        "typing.Dict": "dict",
        "typing.Set": "set",
        "typing.Tuple": "tuple",
    }

    # Read the file content
    with open(filename, "r") as file:
        content = file.read()

    # Replace all occurrences of the typing module types with built-in types
    for old, new in replacements.items():
        content = content.replace(old, new)

    # return the modified content
    return content


if __name__ == "__main__":
    import sys

    file: str = sys.argv[1]
    prefix: str = ""
    if len(sys.argv) > 1:
        prefix = "\n".join(sys.argv[2:])

    print(prefix + "\n" + replace_typing_aliases(file))
