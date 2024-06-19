def replace_typing_aliases(filename):
    # Dictionary to map old types from the typing module to the new built-in types
    replacements = {
        "typing.List": "list",
        "typing.Dict": "dict",
        "typing.Set": "set",
        "typing.Tuple": "tuple"
    }
    
    # Read the file content
    with open(filename, 'r') as file:
        content = file.read()
    
    # Replace all occurrences of the typing module types with built-in types
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Print the modified content to stdout
    print(content)
    
if __name__ == "__main__":
	import sys
	replace_typing_aliases(sys.argv[1])