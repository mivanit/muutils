# Changelog

## [Unreleased]

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
