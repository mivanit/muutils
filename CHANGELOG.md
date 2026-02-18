# Changelog

## [Unreleased]

### Fixed

- **`muutils.json_serialize.util.dc_eq`**: Fixed docstring that incorrectly stated `except_when_field_mismatch` defaults to `True` (actual default is `False`), and that it raises `TypeError` (it actually raises `AttributeError`)
- **`muutils.json_serialize.util.dc_eq`**: Updated flowchart in docstring to accurately reflect the control flow, including the missing `false_when_class_mismatch` decision branch

### Breaking Changes

- **`muutils.logger`**: `Logger.log()` and `SimpleLogger.log()` now require keyword arguments for all parameters after `msg`. This change was made to fix type checker compatibility between the two classes.

  **Before:**
  ```python
  logger.log("message", -10)  # lvl as positional arg
  ```

  **After:**
  ```python
  logger.log("message", lvl=-10)  # lvl as keyword arg
  ```
