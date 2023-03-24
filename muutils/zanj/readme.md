
# Overview

The `ZANJ` format is meant to be a way of saving arbitrary objects to disk, in a way that is flexible, allows to keep configuration and data together, and is human readable. It is loosely inspired by HDF5 and the derived `exdir` format, and the implementation is similar to `npz` files. The on-disk format is as follows:

a file `<filename>.zanj` is a zip file containing:

- `__zanj_meta__.json`: a file containing zanj-specific metadata including:
	- system information
	- installed packages
	- information about external files
- `__zanj__.json`: a file containing user-specified data
	- when an element is too big, it can be moved to an external file
		- `.npy` for numpy arrays or torch tensors
		- `.jsonl` for pandas dataframes or large sequences
	- list of external files stored in `__zanj_meta__.json`
	- "$ref" key will have value pointing to external file
	- `__format__` key will detail an external format type


# Implementation

## `ZANJ`

> located in `muutils.zanj.zanj`

main class for saving and loading zanj files

contains some configuration info about saving, such as:

- thresholds for how big an array/table has to be before moving to external file
- compression settings
- error modes
- handlers for serialization

