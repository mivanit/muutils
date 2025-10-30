# Type Error Fixing TODO

## Instructions

1. Read the type checker output files:
   - `.meta/.type-errors/mypy.txt`
   - `.meta/.type-errors/basedpyright.txt`
   - `.meta/.type-errors/ty.txt`

   NOTE: the latter two files are many thousands of lines, you will have to pick the first few or last few hundred lines to get a sense of the errors.

2. Find the fix with the best **"number of errors / complexity of change" ratio**

3. Implement that fix

run type checking only on the specific file you are changing to verify that the errors are fixed.