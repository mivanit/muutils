
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


# Comparison to other formats



| Format                  | Safe | Zero-copy | Lazy loading | No file size limit | Layout control | Flexibility | Bfloat16 |
| ----------------------- | ---- | --------- | ------------ | ------------------ | -------------- | ----------- | -------- |
| pickle (PyTorch)        | ❌   | ❌        | ❌           | ✅                 | ❌             | ✅          | ✅       |
| H5 (Tensorflow)         | ✅   | ❌        | ✅           | ✅                 | ~              | ~           | ❌       |
| HDF5                    | ✅   | ?         | ✅           | ✅                 | ~              | ✅          | ❌       |
| SavedModel (Tensorflow) | ✅   | ❌        | ❌           | ✅                 | ✅             | ❌          | ✅       |
| MsgPack (flax)          | ✅   | ✅        | ❌           | ✅                 | ❌             | ❌          | ✅       |
| Protobuf (ONNX)         | ✅   | ❌        | ❌           | ❌                 | ❌             | ❌          | ✅       |
| Cap'n'Proto             | ✅   | ✅        | ~            | ✅                 | ✅             | ~           | ❌       |
| Numpy (npy,npz)         | ✅   | ?         | ?            | ❌                 | ✅             | ❌          | ❌       |
| SafeTensors             | ✅   | ✅        | ✅           | ✅                 | ✅             | ❌          | ✅       |
| exdir                   | ✅   | ?         | ?            | ?                  | ?              | ✅          | ❌       |
| ZANJ                    | ✅   | ?         | ❌*          | ✅                 | ✅             | ✅          | ❌       |


- Safe: Can I use a file randomly downloaded and expect not to run arbitrary code ?
- Zero-copy: Does reading the file require more memory than the original file ?
- Lazy loading: Can I inspect the file without loading everything ? And loading only some tensors in it without scanning the whole file (distributed setting) ?
- Layout control: Lazy loading, is not necessarily enough since if the information about tensors is spread out in your file, then even if the information is lazily accessible you might have to access most of your file to read the available tensors (incurring many DISK -> RAM copies). Controlling the layout to keep fast access to single tensors is important.
- No file size limit: Is there a limit to the file size ?
- Flexibility: Can I save custom code in the format and be able to use it later with zero extra code ? (~ means we can store more than pure tensors, but no custom code)
- Bfloat16: Does the format support native bfloat16 (meaning no weird workarounds are necessary)? This is becoming increasingly important in the ML world.


(This table was Stolen from [safetensors](https://github.com/huggingface/safetensors/blob/main/README.md))
