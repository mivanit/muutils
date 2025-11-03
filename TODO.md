# Type Error Fixing TODO

## Instructions

1. Read the entire file `.meta/typing-summary.txt` to get an overview of the current type errors in the codebase.

2. Read the type checker output files:
   - `.meta/.type-errors/mypy.txt`
   - `.meta/.type-errors/basedpyright.txt`
   - `.meta/.type-errors/ty.txt`

   NOTE: the files are many thousands of lines, you will have to pick a *random* few hundred lines to read. it is important that you pick a random set of lines, since you will be working in parallel with other Claude instances, and we want to avoid everyone working on the same errors.

3. Decide on a good fix to make. For example, you might pick:
   - the fix with the best **"number of errors / complexity of change" ratio**
   - a fix that gets us closer to having no errors in a specific file (or group of files)
   - a fix that gets us closer to removing an entire category of errors

4. Implement that fix

run type checking only on the specific file you are changing to verify that the errors are fixed.


# Guidelines:

- make sure all type hints are python>=3.8 compatible
- always err on the side of STRICTER type hints!