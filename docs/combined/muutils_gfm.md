> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

[![PyPI](https://img.shields.io/pypi/v/muutils)](https://pypi.org/project/muutils/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/muutils)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/muutils)

[![Checks](https://github.com/mivanit/muutils/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/checks.yml)
[![Checks](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCI+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgyPSIwIiB5Mj0iMTAwJSI+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPG1hc2sgaWQ9ImEiPgogICAgICAgIDxyZWN0IHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCIgcng9IjMiIGZpbGw9IiNmZmYiLz4KICAgIDwvbWFzaz4KICAgIDxnIG1hc2s9InVybCgjYSkiPgogICAgICAgIDxwYXRoIGZpbGw9IiM1NTUiIGQ9Ik0wIDBoNjN2MjBIMHoiLz4KICAgICAgICA8cGF0aCBmaWxsPSIjYTRhNjFkIiBkPSJNNjMgMGgzNnYyMEg2M3oiLz4KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+CiAgICA8L2c+CiAgICA8ZyBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iRGVqYVZ1IFNhbnMsVmVyZGFuYSxHZW5ldmEsc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMSI+CiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0PgogICAgICAgIDx0ZXh0IHg9IjMxLjUiIHk9IjE0Ij5jb3ZlcmFnZTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPjg1JTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjg1JTwvdGV4dD4KICAgIDwvZz4KPC9zdmc+Cg==)](docs/coverage/html/)

![GitHub
commits](https://img.shields.io/github/commit-activity/t/mivanit/muutils)
![GitHub commit
activity](https://img.shields.io/github/commit-activity/m/mivanit/muutils)
![GitHub closed pull
requests](https://img.shields.io/github/issues-pr-closed/mivanit/muutils)
![code size,
bytes](https://img.shields.io/github/languages/code-size/mivanit/muutils)
<!-- ![Lines of code](https://img.shields.io/tokei/lines/github.com/mivanit/muutils) -->

`muutils`, stylized as “$\mu$utils” or “μutils”, is a collection of
miscellaneous python utilities, meant to be small and with no
dependencies outside of standard python.

# installation

PyPi: [muutils](https://pypi.org/project/muutils/)

    pip install muutils

Note that for using `mlutils`, `tensor_utils`,
`nbutils.configure_notebook`, or the array serialization features of
`json_serialize`, you will need to install with optional `array`
dependencies:

    pip install muutils[array]

# documentation

[**hosted html docs:**](https://miv.name/muutils)
https://miv.name/muutils

- [single-page html
  docs](https://miv.name/muutils/combined/muutils.html) [(absolute
  source
  link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.html)
- [single-page markdown
  docs](https://miv.name/muutils/combined/muutils.md) [(absolute source
  link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.md)
- Test coverage: [![Test
  Coverage](https://miv.name/muutils/coverage/coverage.svg)](https://miv.name/muutils/coverage/html/)
  [webpage](https://miv.name/muutils/coverage/html/) [(absolute source
  link)](https://github.com/mivanit/muutils/tree/main/docs/coverage/html/)
  [(plain
  text)](https://github.com/mivanit/muutils/tree/main/docs/coverage/coverage.txt)

# modules

## [`statcounter`](https://github.com/mivanit/muutils/tree/main/muutils/statcounter.py)

an extension of `collections.Counter` that provides “smart” computation
of stats (mean, variance, median, other percentiles) from the counter
object without using `Counter.elements()`

## [`dictmagic`](https://github.com/mivanit/muutils/tree/main/muutils/dictmagic.py)

has utilities for working with dictionaries, like:

- converting dotlist-dictionaries to nested dictionaries and back:
  `python       >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})       {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}       >>> nested_dict_to_dotlist({'a': {'b': {'c': 1, 'd': 2}, 'e': 3}})       {'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}`
- `DefaulterDict` which works like a `defaultdict` but can generate the
  default value based on the key
- `condense_tensor_dict` takes a dict of dotlist-tensors and gives a
  more human-readable summary:
  `python       >>> model = MyGPT()       >>> print(condense_tensor_dict(model.named_parameters(), 'yaml'))`
  `yaml       embed:           W_E: (50257, 768)       pos_embed:           W_pos: (1024, 768)       blocks:         '[0-11]':           attn:             '[W_Q, W_K, W_V]': (12, 768, 64)           W_O: (12, 64, 768)             '[b_Q, b_K, b_V]': (12, 64)           b_O: (768,)       <...>`

## [`kappa`](https://github.com/mivanit/muutils/tree/main/muutils/kappa.py)

Anonymous gettitem, so you can do things like

``` python
>>> k = Kappa(lambda x: x**2)
>>> k[2]
4
```

## [`sysinfo`](https://github.com/mivanit/muutils/tree/main/muutils/sysinfo.py)

utility for getting a bunch of system information. useful for logging.

## `misc`:

contains a few utilities: - `stable_hash()` uses `hashlib.sha256` to
compute a hash of an object that is stable across runs of python -
`list_join` and `list_split` which behave like `str.join` and
`str.split` but for lists - `sanitize_fname` and `dict_to_filename` for
simplifying the creation of unique filename -
`shorten_numerical_to_str()` and `str_to_numeric` turns numbers like
`123456789` into `"123M"` and back - `freeze`, which prevents an object
from being modified. Also see
[gelidum](https://github.com/diegojromerolopez/gelidum/)

## [`nbutils`](https://github.com/mivanit/muutils/tree/main/muutils/nbutils)

contains utilities for working with jupyter notebooks, such as:

- quickly converting notebooks to python scripts (and running those
  scripts) for testing in CI
- configuring notebooks, to make it easier to switch between figure
  output formats, locations, and more
- shorthand for displaying mermaid diagrams and TeX

## [`json_serialize`](https://github.com/mivanit/muutils/tree/main/muutils/json_serialize.py)

a tool for serializing and loading arbitrary python objects into json.
plays nicely with [`ZANJ`](https://github.com/mivanit/ZANJ/)

## \[`tensor_utils`\]

contains minor utilities for working with pytorch tensors and numpy
arrays, mostly for making type conversions easier

## [`group_equiv`](https://github.com/mivanit/muutils/tree/main/muutils/group_equiv.py)

groups elements from a sequence according to a given equivalence
relation, without assuming that the equivalence relation obeys the
transitive property

## [`jsonlines`](https://github.com/mivanit/muutils/tree/main/muutils/jsonlines.py)

an extremely simple utility for reading/writing `jsonl` files

## [`ZANJ`](https://github.com/mivanit/ZANJ/)

is a human-readable and simple format for ML models, datasets, and
arbitrary objects. It’s build around having a zip file with `json` and
`npy` files, and has been spun off into its [own
project](https://github.com/mivanit/ZANJ/).

There are a couple work-in-progress utilities in
[`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/)
that aren’t ready for anything, but nothing in this repo is suitable for
production. Use at your own risk!

## Submodules

- [`json_serialize`](#json_serialize)
- [`logger`](#logger)
- [`math`](#math)
- [`misc`](#misc)
- [`nbutils`](#nbutils)
- [`web`](#web)
- [`collect_warnings`](#collect_warnings)
- [`console_unicode`](#console_unicode)
- [`dbg`](#dbg)
- [`dictmagic`](#dictmagic)
- [`errormode`](#errormode)
- [`group_equiv`](#group_equiv)
- [`interval`](#interval)
- [`jsonlines`](#jsonlines)
- [`kappa`](#kappa)
- [`mlutils`](#mlutils)
- [`parallel`](#parallel)
- [`spinner`](#spinner)
- [`statcounter`](#statcounter)
- [`sysinfo`](#sysinfo)
- [`tensor_info`](#tensor_info)
- [`tensor_utils`](#tensor_utils)
- [`timeit_fancy`](#timeit_fancy)
- [`validate_type`](#validate_type)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/__init__.py)

# `muutils`

[![PyPI](https://img.shields.io/pypi/v/muutils)](https://pypi.org/project/muutils/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/muutils)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/muutils)

[![Checks](https://github.com/mivanit/muutils/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/checks.yml)
[![Checks](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCI+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgyPSIwIiB5Mj0iMTAwJSI+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICAgICAgPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLW9wYWNpdHk9Ii4xIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPG1hc2sgaWQ9ImEiPgogICAgICAgIDxyZWN0IHdpZHRoPSI5OSIgaGVpZ2h0PSIyMCIgcng9IjMiIGZpbGw9IiNmZmYiLz4KICAgIDwvbWFzaz4KICAgIDxnIG1hc2s9InVybCgjYSkiPgogICAgICAgIDxwYXRoIGZpbGw9IiM1NTUiIGQ9Ik0wIDBoNjN2MjBIMHoiLz4KICAgICAgICA8cGF0aCBmaWxsPSIjYTRhNjFkIiBkPSJNNjMgMGgzNnYyMEg2M3oiLz4KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+CiAgICA8L2c+CiAgICA8ZyBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iRGVqYVZ1IFNhbnMsVmVyZGFuYSxHZW5ldmEsc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMSI+CiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0PgogICAgICAgIDx0ZXh0IHg9IjMxLjUiIHk9IjE0Ij5jb3ZlcmFnZTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPjg1JTwvdGV4dD4KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjg1JTwvdGV4dD4KICAgIDwvZz4KPC9zdmc+Cg==)](docs/coverage/html/)

![GitHub
commits](https://img.shields.io/github/commit-activity/t/mivanit/muutils)
![GitHub commit
activity](https://img.shields.io/github/commit-activity/m/mivanit/muutils)
![GitHub closed pull
requests](https://img.shields.io/github/issues-pr-closed/mivanit/muutils)
![code size,
bytes](https://img.shields.io/github/languages/code-size/mivanit/muutils)
<!-- ![Lines of code](https://img.shields.io/tokei/lines/github.com/mivanit/muutils) -->

`muutils`, stylized as “$\mu$utils” or “μutils”, is a collection of
miscellaneous python utilities, meant to be small and with no
dependencies outside of standard python.

### installation

PyPi: [muutils](https://pypi.org/project/muutils/)

    pip install muutils

Note that for using `mlutils`, `tensor_utils`,
`nbutils.configure_notebook`, or the array serialization features of
`json_serialize`, you will need to install with optional `array`
dependencies:

    pip install muutils[array]

### documentation

[**hosted html docs:**](https://miv.name/muutils)
https://miv.name/muutils

- [single-page html
  docs](https://miv.name/muutils/combined/muutils.html) [(absolute
  source
  link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.html)
- [single-page markdown
  docs](https://miv.name/muutils/combined/muutils.md) [(absolute source
  link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.md)
- Test coverage: [![Test
  Coverage](https://miv.name/muutils/coverage/coverage.svg)](https://miv.name/muutils/coverage/html/)
  [webpage](https://miv.name/muutils/coverage/html/) [(absolute source
  link)](https://github.com/mivanit/muutils/tree/main/docs/coverage/html/)
  [(plain
  text)](https://github.com/mivanit/muutils/tree/main/docs/coverage/coverage.txt)

### modules

#### [`statcounter`](https://github.com/mivanit/muutils/tree/main/muutils/statcounter.py)

an extension of `collections.Counter` that provides “smart” computation
of stats (mean, variance, median, other percentiles) from the counter
object without using `Counter.elements()`

#### [`dictmagic`](https://github.com/mivanit/muutils/tree/main/muutils/dictmagic.py)

has utilities for working with dictionaries, like:

- converting dotlist-dictionaries to nested dictionaries and back:
  `python       >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})       {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}       >>> nested_dict_to_dotlist({'a': {'b': {'c': 1, 'd': 2}, 'e': 3}})       {'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}`
- `DefaulterDict` which works like a `defaultdict` but can generate the
  default value based on the key
- `condense_tensor_dict` takes a dict of dotlist-tensors and gives a
  more human-readable summary:
  `python       >>> model = MyGPT()       >>> print(condense_tensor_dict(model.named_parameters(), 'yaml'))`
  `yaml       embed:           W_E: (50257, 768)       pos_embed:           W_pos: (1024, 768)       blocks:         '[0-11]':           attn:             '[W_Q, W_K, W_V]': (12, 768, 64)           W_O: (12, 64, 768)             '[b_Q, b_K, b_V]': (12, 64)           b_O: (768,)       <...>`

#### [`kappa`](https://github.com/mivanit/muutils/tree/main/muutils/kappa.py)

Anonymous gettitem, so you can do things like

``` python
>>> k = Kappa(lambda x: x**2)
>>> k[2]
4
```

#### [`sysinfo`](https://github.com/mivanit/muutils/tree/main/muutils/sysinfo.py)

utility for getting a bunch of system information. useful for logging.

#### `misc`:

contains a few utilities: - `stable_hash()` uses `hashlib.sha256` to
compute a hash of an object that is stable across runs of python -
`list_join` and `list_split` which behave like `str.join` and
`str.split` but for lists - `sanitize_fname` and `dict_to_filename` for
simplifying the creation of unique filename -
`shorten_numerical_to_str()` and `str_to_numeric` turns numbers like
`123456789` into `"123M"` and back - `freeze`, which prevents an object
from being modified. Also see
[gelidum](https://github.com/diegojromerolopez/gelidum/)

#### [`nbutils`](https://github.com/mivanit/muutils/tree/main/muutils/nbutils)

contains utilities for working with jupyter notebooks, such as:

- quickly converting notebooks to python scripts (and running those
  scripts) for testing in CI
- configuring notebooks, to make it easier to switch between figure
  output formats, locations, and more
- shorthand for displaying mermaid diagrams and TeX

#### [`json_serialize`](https://github.com/mivanit/muutils/tree/main/muutils/json_serialize.py)

a tool for serializing and loading arbitrary python objects into json.
plays nicely with [`ZANJ`](https://github.com/mivanit/ZANJ/)

#### \[`tensor_utils`\]

contains minor utilities for working with pytorch tensors and numpy
arrays, mostly for making type conversions easier

#### [`group_equiv`](https://github.com/mivanit/muutils/tree/main/muutils/group_equiv.py)

groups elements from a sequence according to a given equivalence
relation, without assuming that the equivalence relation obeys the
transitive property

#### [`jsonlines`](https://github.com/mivanit/muutils/tree/main/muutils/jsonlines.py)

an extremely simple utility for reading/writing `jsonl` files

#### [`ZANJ`](https://github.com/mivanit/ZANJ/)

is a human-readable and simple format for ML models, datasets, and
arbitrary objects. It’s build around having a zip file with `json` and
`npy` files, and has been spun off into its [own
project](https://github.com/mivanit/ZANJ/).

There are a couple work-in-progress utilities in
[`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/)
that aren’t ready for anything, but nothing in this repo is suitable for
production. Use at your own risk!

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/__init__.py#L0-L33)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`CollateWarnings`](#CollateWarnings)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/collect_warnings.py)

# `muutils.collect_warnings`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/collect_warnings.py#L0-L131)

### `class CollateWarnings(contextlib.AbstractContextManager[&#39;CollateWarnings&#39;]):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/collect_warnings.py#L11-L132)

Capture every warning issued inside a `with` block and print a collated
summary when the block exits.

Internally this wraps `warnings.catch_warnings(record=True)` so that all
warnings raised in the block are recorded. When the context exits,
identical warnings are grouped and (optionally) printed with a
user-defined format.

### Parameters:

- `print_on_exit : bool` Whether to print the summary when the context
  exits (defaults to `True`)

- `fmt : str` Format string used for printing each line of the summary.
  Available fields are:

  - `{count}` : number of occurrences
  - `{filename}` : file where the warning originated
  - `{lineno}` : line number
  - `{category}` : warning class name
  - `{message}` : warning message text

  (defaults to `"({count}x) {filename}:{lineno} {category}: {message}"`)

### Returns:

- `CollateWarnings` The context-manager instance. After exit, the
  attribute `counts` holds a mapping

  ``` python
  {(filename, lineno, category, message): count}
  ```

### Usage:

``` python
>>> import warnings
>>> with CollateWarnings() as cw:
...     warnings.warn("deprecated", DeprecationWarning)
...     warnings.warn("deprecated", DeprecationWarning)
...     warnings.warn("other", UserWarning)
(2x) /tmp/example.py:42 DeprecationWarning: deprecated
(1x) /tmp/example.py:43 UserWarning: other
>>> cw.counts
{('/tmp/example.py', 42, 'DeprecationWarning', 'deprecated'): 2,
 ('/tmp/example.py', 43, 'UserWarning', 'other'): 1}
```

### `CollateWarnings`

``` python
(
    print_on_exit: bool = True,
    fmt: str = '({count}x) {filename}:{lineno} {category}: {message}'
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/collect_warnings.py#L73-L82)

- `counts: collections.Counter[tuple[str, int, str, str]]`

- `print_on_exit: bool`

- `fmt: str`

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`get_console_safe_str`](#get_console_safe_str)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/console_unicode.py)

# `muutils.console_unicode`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/console_unicode.py#L0-L33)

### `def get_console_safe_str`

``` python
(default: str, fallback: str) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/console_unicode.py#L4-L34)

Determine a console-safe string based on the preferred encoding.

This function attempts to encode a given `default` string using the
system’s preferred encoding. If encoding is successful, it returns the
`default` string; otherwise, it returns a `fallback` string.

### Parameters:

- `default : str` The primary string intended for use, to be tested
  against the system’s preferred encoding.
- `fallback : str` The alternative string to be used if `default` cannot
  be encoded in the system’s preferred encoding.

### Returns:

- `str` Either `default` or `fallback` based on whether `default` can be
  encoded safely.

### Usage:

``` python
>>> get_console_safe_str("café", "cafe")
"café"  # This result may vary based on the system's preferred encoding.
```

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

this code is based on an implementation of the Rust builtin `dbg!` for
Python, originally from
https://github.com/tylerwince/pydbg/blob/master/pydbg.py although it has
been significantly modified

licensed under MIT:

Copyright (c) 2019 Tyler Wince

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## API Documentation

- [`PATH_MODE`](#PATH_MODE)
- [`DEFAULT_VAL_JOINER`](#DEFAULT_VAL_JOINER)
- [`dbg`](#dbg)
- [`DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS`](#DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS)
- [`DBG_TENSOR_VAL_JOINER`](#DBG_TENSOR_VAL_JOINER)
- [`tensor_info`](#tensor_info)
- [`DBG_DICT_DEFAULTS`](#DBG_DICT_DEFAULTS)
- [`DBG_LIST_DEFAULTS`](#DBG_LIST_DEFAULTS)
- [`list_info`](#list_info)
- [`TENSOR_STR_TYPES`](#TENSOR_STR_TYPES)
- [`dict_info`](#dict_info)
- [`info_auto`](#info_auto)
- [`dbg_tensor`](#dbg_tensor)
- [`dbg_dict`](#dbg_dict)
- [`dbg_auto`](#dbg_auto)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py)

# `muutils.dbg`

this code is based on an implementation of the Rust builtin `dbg!` for
Python, originally from
https://github.com/tylerwince/pydbg/blob/master/pydbg.py although it has
been significantly modified

licensed under MIT:

Copyright (c) 2019 Tyler Wince

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py#L0-L318)

- `PATH_MODE: Literal['relative', 'absolute'] = 'relative'`

- `DEFAULT_VAL_JOINER: str = ' = '`

### `def dbg`

``` python
(
    exp: Union[~_ExpType, muutils.dbg._NoExpPassedSentinel] = <muutils.dbg._NoExpPassedSentinel object>,
    formatter: Optional[Callable[[Any], str]] = None,
    val_joiner: str = ' = '
) -> Union[~_ExpType, muutils.dbg._NoExpPassedSentinel]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py#L95-L182)

Call dbg with any variable or expression.

Calling dbg will print to stderr the current filename and lineno, as
well as the passed expression and what the expression evaluates to:

        from <a href="">muutils.dbg</a> import dbg

        a = 2
        b = 5

        dbg(a+b)

        def square(x: int) -> int:
                return x * x

        dbg(square(a))

- `DBG_TENSOR_ARRAY_SUMMARY_DEFAULTS: Dict[str, Union[NoneType, bool, int, str]] = {'fmt': 'unicode', 'precision': 2, 'stats': True, 'shape': True, 'dtype': True, 'device': True, 'requires_grad': True, 'sparkline': True, 'sparkline_bins': 7, 'sparkline_logy': None, 'colored': True, 'eq_char': '='}`

- `DBG_TENSOR_VAL_JOINER: str = ': '`

### `def tensor_info`

``` python
(tensor: Any) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py#L208-L211)

- `DBG_DICT_DEFAULTS: Dict[str, Union[str, int, bool]] = {'key_types': True, 'val_types': True, 'max_len': 32, 'indent': '  ', 'max_depth': 3}`

- `DBG_LIST_DEFAULTS: Dict[str, Union[str, int, bool]] = {'max_len': 16, 'summary_show_types': True}`

### `def list_info`

``` python
(lst: List[Any]) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py#L228-L243)

- `TENSOR_STR_TYPES: Set[str] = {"<class 'torch.Tensor'>", "<class 'numpy.ndarray'>"}`

### `def dict_info`

``` python
(d: Dict[Any, Any], depth: int = 0) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py#L252-L295)

### `def info_auto`

``` python
(obj: Any) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dbg.py#L298-L309)

Automatically format an object for debugging.

- `dbg_tensor = functools.partial(<function dbg>, formatter=<function tensor_info>, val_joiner=': ')`

- `dbg_dict = functools.partial(<function dbg>, formatter=<function dict_info>, val_joiner=': ')`

- `dbg_auto = functools.partial(<function dbg>, formatter=<function info_auto>, val_joiner=': ')`

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

making working with dictionaries easier

- `DefaulterDict`: like a defaultdict, but default_factory is passed the
  key as an argument
- various methods for working wit dotlist-nested dicts, converting to
  and from them
- `condense_nested_dicts`: condense a nested dict, by condensing numeric
  or matching keys with matching values to ranges
- `condense_tensor_dict`: convert a dictionary of tensors to a
  dictionary of shapes
- `kwargs_to_nested_dict`: given kwargs from fire, convert them to a
  nested dict

## API Documentation

- [`DefaulterDict`](#DefaulterDict)
- [`defaultdict_to_dict_recursive`](#defaultdict_to_dict_recursive)
- [`dotlist_to_nested_dict`](#dotlist_to_nested_dict)
- [`nested_dict_to_dotlist`](#nested_dict_to_dotlist)
- [`update_with_nested_dict`](#update_with_nested_dict)
- [`kwargs_to_nested_dict`](#kwargs_to_nested_dict)
- [`is_numeric_consecutive`](#is_numeric_consecutive)
- [`condense_nested_dicts_numeric_keys`](#condense_nested_dicts_numeric_keys)
- [`condense_nested_dicts_matching_values`](#condense_nested_dicts_matching_values)
- [`condense_nested_dicts`](#condense_nested_dicts)
- [`tuple_dims_replace`](#tuple_dims_replace)
- [`TensorDict`](#TensorDict)
- [`TensorIterable`](#TensorIterable)
- [`TensorDictFormats`](#TensorDictFormats)
- [`condense_tensor_dict`](#condense_tensor_dict)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py)

# `muutils.dictmagic`

making working with dictionaries easier

- `DefaulterDict`: like a defaultdict, but default_factory is passed the
  key as an argument
- various methods for working wit dotlist-nested dicts, converting to
  and from them
- `condense_nested_dicts`: condense a nested dict, by condensing numeric
  or matching keys with matching values to ranges
- `condense_tensor_dict`: convert a dictionary of tensors to a
  dictionary of shapes
- `kwargs_to_nested_dict`: given kwargs from fire, convert them to a
  nested dict

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L0-L521)

### `class DefaulterDict(typing.Dict[~_KT, ~_VT], typing.Generic[~_KT, ~_VT]):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L33-L50)

like a defaultdict, but default_factory is passed the key as an argument

- `default_factory: Callable[[~_KT], ~_VT]`

### Inherited Members

- [`get`](#DefaulterDict.get)
- [`setdefault`](#DefaulterDict.setdefault)
- [`pop`](#DefaulterDict.pop)
- [`popitem`](#DefaulterDict.popitem)
- [`keys`](#DefaulterDict.keys)
- [`items`](#DefaulterDict.items)
- [`values`](#DefaulterDict.values)
- [`update`](#DefaulterDict.update)
- [`fromkeys`](#DefaulterDict.fromkeys)
- [`clear`](#DefaulterDict.clear)
- [`copy`](#DefaulterDict.copy)

### `def defaultdict_to_dict_recursive`

``` python
(
    dd: Union[collections.defaultdict, muutils.dictmagic.DefaulterDict]
) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L57-L66)

Convert a defaultdict or DefaulterDict to a normal dict, recursively

### `def dotlist_to_nested_dict`

``` python
(dot_dict: Dict[str, Any], sep: str = '.') -> Dict[str, Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L69-L89)

Convert a dict with dot-separated keys to a nested dict

Example:

    >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})
    {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}

### `def nested_dict_to_dotlist`

``` python
(
    nested_dict: Dict[str, Any],
    sep: str = '.',
    allow_lists: bool = False
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L92-L122)

### `def update_with_nested_dict`

``` python
(
    original: dict[str, typing.Any],
    update: dict[str, typing.Any]
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L125-L154)

Update a dict with a nested dict

Example: \>\>\> update_with_nested_dict({‘a’: {‘b’: 1}, “c”: -1}, {‘a’:
{“b”: 2}}) {‘a’: {‘b’: 2}, ‘c’: -1}

### Arguments

- `original: dict[str, Any]` the dict to update (will be modified
  in-place)
- `update: dict[str, Any]` the dict to update with

### Returns

- `dict` the updated dict

### `def kwargs_to_nested_dict`

``` python
(
    kwargs_dict: dict[str, typing.Any],
    sep: str = '.',
    strip_prefix: Optional[str] = None,
    when_unknown_prefix: Union[muutils.errormode.ErrorMode, str] = ErrorMode.Warn,
    transform_key: Optional[Callable[[str], str]] = None
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L157-L211)

given kwargs from fire, convert them to a nested dict

if strip_prefix is not None, then all keys must start with the prefix.
by default, will warn if an unknown prefix is found, but can be set to
raise an error or ignore it: `when_unknown_prefix: ErrorMode`

Example:

``` python
def main(**kwargs):
    print(kwargs_to_nested_dict(kwargs))
fire.Fire(main)
```

running the above script will give:

``` bash
$ python test.py --a.b.c=1 --a.b.d=2 --a.e=3
{'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
```

### Arguments

- `kwargs_dict: dict[str, Any]` the kwargs dict to convert
- `sep: str = "."` the separator to use for nested keys
- `strip_prefix: Optional[str] = None` if not None, then all keys must
  start with this prefix
- `when_unknown_prefix: ErrorMode = ErrorMode.WARN` what to do when an
  unknown prefix is found
- `transform_key: Callable[[str], str] | None = None` a function to
  apply to each key before adding it to the dict (applied after
  stripping the prefix)

### `def is_numeric_consecutive`

``` python
(lst: list[str]) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L214-L220)

Check if the list of keys is numeric and consecutive.

### `def condense_nested_dicts_numeric_keys`

``` python
(data: dict[str, typing.Any]) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L223-L267)

condense a nested dict, by condensing numeric keys with matching values
to ranges

### Examples:

``` python
>>> condense_nested_dicts_numeric_keys({'1': 1, '2': 1, '3': 1, '4': 2, '5': 2, '6': 2})
{'[1-3]': 1, '[4-6]': 2}
>>> condense_nested_dicts_numeric_keys({'1': {'1': 'a', '2': 'a'}, '2': 'b'})
{"1": {"[1-2]": "a"}, "2": "b"}
```

### `def condense_nested_dicts_matching_values`

``` python
(
    data: dict[str, typing.Any],
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L270-L321)

condense a nested dict, by condensing keys with matching values

### Examples: TODO

### Parameters:

- `data : dict[str, Any]` data to process
- `val_condense_fallback_mapping : Callable[[Any], Hashable] | None` a
  function to apply to each value before adding it to the dict (if it’s
  not hashable) (defaults to `None`)

### `def condense_nested_dicts`

``` python
(
    data: dict[str, typing.Any],
    condense_numeric_keys: bool = True,
    condense_matching_values: bool = True,
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L324-L359)

condense a nested dict, by condensing numeric or matching keys with
matching values to ranges

combines the functionality of `condense_nested_dicts_numeric_keys()` and
`condense_nested_dicts_matching_values()`

### NOTE: this process is not meant to be reversible, and is intended for pretty-printing and visualization purposes

it’s not reversible because types are lost to make the printing pretty

### Parameters:

- `data : dict[str, Any]` data to process
- `condense_numeric_keys : bool` whether to condense numeric keys
  (e.g. “1”, “2”, “3”) to ranges (e.g. “\[1-3\]”) (defaults to `True`)
- `condense_matching_values : bool` whether to condense keys with
  matching values (defaults to `True`)
- `val_condense_fallback_mapping : Callable[[Any], Hashable] | None` a
  function to apply to each value before adding it to the dict (if it’s
  not hashable) (defaults to `None`)

### `def tuple_dims_replace`

``` python
(
    t: tuple[int, ...],
    dims_names_map: Optional[dict[int, str]] = None
) -> tuple[typing.Union[int, str], ...]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L362-L368)

- `TensorDict = typing.Dict[str, ForwardRef('torch.Tensor|np.ndarray')]`

- `TensorIterable = typing.Iterable[typing.Tuple[str, ForwardRef('torch.Tensor|np.ndarray')]]`

- `TensorDictFormats = typing.Literal['dict', 'json', 'yaml', 'yml']`

### `def condense_tensor_dict`

``` python
(
    data: 'TensorDict | TensorIterable',
    fmt: Literal['dict', 'json', 'yaml', 'yml'] = 'dict',
    *args,
    shapes_convert: Callable[[tuple], Any] = <function _default_shapes_convert>,
    drop_batch_dims: int = 0,
    sep: str = '.',
    dims_names_map: Optional[dict[int, str]] = None,
    condense_numeric_keys: bool = True,
    condense_matching_values: bool = True,
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None,
    return_format: Optional[Literal['dict', 'json', 'yaml', 'yml']] = None
) -> Union[str, dict[str, str | tuple[int, ...]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/dictmagic.py#L380-L522)

Convert a dictionary of tensors to a dictionary of shapes.

by default, values are converted to strings of their shapes (for nice
printing). If you want the actual shapes, set
`shapes_convert = lambda x: x` or `shapes_convert = None`.

### Parameters:

- `data : dict[str, "torch.Tensor|np.ndarray"] | Iterable[tuple[str, "torch.Tensor|np.ndarray"]]`
  a either a `TensorDict` dict from strings to tensors, or an
  `TensorIterable` iterable of (key, tensor) pairs (like you might get
  from a `dict().items())` )
- `fmt : TensorDictFormats` format to return the result in – either a
  dict, or dump to json/yaml directly for pretty printing. will crash if
  yaml is not installed. (defaults to `'dict'`)
- `shapes_convert : Callable[[tuple], Any]` conversion of a shape tuple
  to a string or other format (defaults to turning it into a string and
  removing quotes) (defaults to
  `lambdax:str(x).replace('"', '').replace("'", '')`)
- `drop_batch_dims : int` number of leading dimensions to drop from the
  shape (defaults to `0`)
- `sep : str` separator to use for nested keys (defaults to `'.'`)
- `dims_names_map : dict[int, str] | None` convert certain dimension
  values in shape. not perfect, can be buggy (defaults to `None`)
- `condense_numeric_keys : bool` whether to condense numeric keys
  (e.g. “1”, “2”, “3”) to ranges (e.g. “\[1-3\]”), passed on to
  `condense_nested_dicts` (defaults to `True`)
- `condense_matching_values : bool` whether to condense keys with
  matching values, passed on to `condense_nested_dicts` (defaults to
  `True`)
- `val_condense_fallback_mapping : Callable[[Any], Hashable] | None` a
  function to apply to each value before adding it to the dict (if it’s
  not hashable), passed on to `condense_nested_dicts` (defaults to
  `None`)
- `return_format : TensorDictFormats | None` legacy alias for `fmt`
  kwarg

### Returns:

- `str|dict[str, str|tuple[int, ...]]` dict if `return_format='dict'`, a
  string for `json` or `yaml` output

### Examples:

``` python
>>> model = transformer_lens.HookedTransformer.from_pretrained("gpt2")
>>> print(condense_tensor_dict(model.named_parameters(), return_format='yaml'))
```

``` yaml
embed:
  W_E: (50257, 768)
pos_embed:
  W_pos: (1024, 768)
blocks:
  '[0-11]':
    attn:
      '[W_Q, W_K, W_V]': (12, 768, 64)
      W_O: (12, 64, 768)
      '[b_Q, b_K, b_V]': (12, 64)
      b_O: (768,)
    mlp:
      W_in: (768, 3072)
      b_in: (3072,)
      W_out: (3072, 768)
      b_out: (768,)
unembed:
  W_U: (768, 50257)
  b_U: (50257,)
```

### Raises:

- `ValueError` : if `return_format` is not one of ‘dict’, ‘json’, or
  ‘yaml’, or if you try to use ‘yaml’ output without having PyYAML
  installed

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

provides `ErrorMode` enum for handling errors consistently

pass an `error_mode: ErrorMode` to a function to specify how to handle a
certain kind of exception. That function then instead of `raise`ing or
`warnings.warn`ing, calls `error_mode.process` with the message and the
exception.

you can also specify the exception class to raise, the warning class to
use, and the source of the exception/warning.

## API Documentation

- [`WarningFunc`](#WarningFunc)
- [`LoggingFunc`](#LoggingFunc)
- [`GLOBAL_WARN_FUNC`](#GLOBAL_WARN_FUNC)
- [`GLOBAL_LOG_FUNC`](#GLOBAL_LOG_FUNC)
- [`custom_showwarning`](#custom_showwarning)
- [`ErrorMode`](#ErrorMode)
- [`ERROR_MODE_ALIASES`](#ERROR_MODE_ALIASES)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py)

# `muutils.errormode`

provides `ErrorMode` enum for handling errors consistently

pass an `error_mode: ErrorMode` to a function to specify how to handle a
certain kind of exception. That function then instead of `raise`ing or
`warnings.warn`ing, calls `error_mode.process` with the message and the
exception.

you can also specify the exception class to raise, the warning class to
use, and the source of the exception/warning.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L0-L240)

### `class WarningFunc(typing.Protocol):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L19-L25)

Base class for protocol classes.

Protocol classes are defined as::

    class Proto(Protocol):
        def meth(self) -> int:
            ...

Such classes are primarily used with static type checkers that recognize
structural subtyping (static duck-typing).

For example::

    class C:
        def meth(self) -> int:
            return 0

    def func(x: Proto) -> int:
        return x.meth()

    func(C())  # Passes static type check

See PEP 544 for details. Protocol classes decorated with
@typing.runtime_checkable act as simple-minded runtime protocols that
check only the presence of given attributes, ignoring their type
signatures. Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...

### `WarningFunc`

``` python
(*args, **kwargs)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L1766-L1792)

- `LoggingFunc = typing.Callable[[str], NoneType]`

### `def GLOBAL_WARN_FUNC`

``` python
(unknown)
```

Issue a warning, or maybe ignore it or raise an exception.

message Text of the warning message. category The Warning category
subclass. Defaults to UserWarning. stacklevel How far up the call stack
to make this warning appear. A value of 2 for example attributes the
warning to the caller of the code calling warn(). source If supplied,
the destroyed object which emitted a ResourceWarning skip_file_prefixes
An optional tuple of module filename prefixes indicating frames to skip
during stacklevel computations for stack frame attribution.

### `def GLOBAL_LOG_FUNC`

``` python
(*args, sep=' ', end='\n', file=None, flush=False)
```

Prints the values to a stream, or to sys.stdout by default.

sep string inserted between values, default a space. end string appended
after the last value, default a newline. file a file-like object
(stream); defaults to the current sys.stdout. flush whether to forcibly
flush the stream.

### `def custom_showwarning`

``` python
(
    message: Warning | str,
    category: Optional[Type[Warning]] = None,
    filename: str | None = None,
    lineno: int | None = None,
    file: Optional[TextIO] = None,
    line: Optional[str] = None
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L34-L75)

### `class ErrorMode(enum.Enum):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L78-L212)

Enum for handling errors consistently

pass one of the instances of this enum to a function to specify how to
handle a certain kind of exception.

That function then instead of `raise`ing or `warnings.warn`ing, calls
`error_mode.process` with the message and the exception.

- `EXCEPT = ErrorMode.Except`

- `WARN = ErrorMode.Warn`

- `LOG = ErrorMode.Log`

- `IGNORE = ErrorMode.Ignore`

### `def process`

``` python
(
    self,
    msg: str,
    except_cls: Type[Exception] = <class 'ValueError'>,
    warn_cls: Type[Warning] = <class 'UserWarning'>,
    except_from: Optional[Exception] = None,
    warn_func: muutils.errormode.WarningFunc | None = None,
    log_func: Optional[Callable[[str], NoneType]] = None
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L91-L160)

process an exception or warning according to the error mode

### Parameters:

- `msg : str` message to pass to `except_cls` or `warn_func`
- `except_cls : typing.Type[Exception]` exception class to raise, must
  be a subclass of `Exception` (defaults to `ValueError`)
- `warn_cls : typing.Type[Warning]` warning class to use, must be a
  subclass of `Warning` (defaults to `UserWarning`)
- `except_from : typing.Optional[Exception]` will
  `raise except_cls(msg) from except_from` if not `None` (defaults to
  `None`)
- `warn_func : WarningFunc | None` function to use for warnings, must
  have the signature
  `warn_func(msg: str, category: typing.Type[Warning], source: typing.Any = None) -> None`
  (defaults to `None`)
- `log_func : LoggingFunc | None` function to use for logging, must have
  the signature `log_func(msg: str) -> None` (defaults to `None`)

### Raises:

- `except_cls` : *description*
- `except_cls` : *description*
- `ValueError` : *description*

### `def from_any`

``` python
(
    cls,
    mode: str | muutils.errormode.ErrorMode,
    allow_aliases: bool = True,
    allow_prefix: bool = True
) -> muutils.errormode.ErrorMode
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L162-L195)

initialize an `ErrorMode` from a string or an `ErrorMode` instance

### `def serialize`

``` python
(self) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L203-L204)

### `def load`

``` python
(cls, data: str) -> muutils.errormode.ErrorMode
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/errormode.py#L206-L212)

### Inherited Members

- [`name`](#ErrorMode.name)

- [`value`](#ErrorMode.value)

- `ERROR_MODE_ALIASES: dict[str, muutils.errormode.ErrorMode] = {'except': ErrorMode.Except, 'warn': ErrorMode.Warn, 'log': ErrorMode.Log, 'ignore': ErrorMode.Ignore, 'e': ErrorMode.Except, 'error': ErrorMode.Except, 'err': ErrorMode.Except, 'raise': ErrorMode.Except, 'w': ErrorMode.Warn, 'warning': ErrorMode.Warn, 'l': ErrorMode.Log, 'print': ErrorMode.Log, 'output': ErrorMode.Log, 'show': ErrorMode.Log, 'display': ErrorMode.Log, 'i': ErrorMode.Ignore, 'silent': ErrorMode.Ignore, 'quiet': ErrorMode.Ignore, 'nothing': ErrorMode.Ignore}`

map of string aliases to `ErrorMode` instances

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

group items by assuming that `eq_func` defines an equivalence relation

## API Documentation

- [`group_by_equivalence`](#group_by_equivalence)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/group_equiv.py)

# `muutils.group_equiv`

group items by assuming that `eq_func` defines an equivalence relation

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/group_equiv.py#L0-L65)

### `def group_by_equivalence`

``` python
(
    items_in: Sequence[~T],
    eq_func: Callable[[~T, ~T], bool]
) -> list[list[~T]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/group_equiv.py#L11-L66)

group items by assuming that `eq_func` implies an equivalence relation
but might not be transitive

so, if f(a,b) and f(b,c) then f(a,c) might be false, but we still want
to put \[a,b,c\] in the same class

note that lists are used to avoid the need for hashable items, and to
allow for duplicates

### Arguments

- `items_in: Sequence[T]` the items to group
- `eq_func: Callable[[T, T], bool]` a function that returns true if two
  items are equivalent. need not be transitive

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

represents a mathematical `Interval` over the real numbers

## API Documentation

- [`Number`](#Number)
- [`Interval`](#Interval)
- [`ClosedInterval`](#ClosedInterval)
- [`OpenInterval`](#OpenInterval)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py)

# `muutils.interval`

represents a mathematical `Interval` over the real numbers

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L0-L531)

- `Number = typing.Union[float, int]`

### `class Interval:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L26-L518)

Represents a mathematical interval, open by default.

The Interval class can represent both open and closed intervals, as well
as half-open intervals. It supports various initialization methods and
provides containment checks.

Examples:

    >>> i1 = Interval(1, 5)  # Default open interval (1, 5)
    >>> 3 in i1
    True
    >>> 1 in i1
    False
    >>> i2 = Interval([1, 5])  # Closed interval [1, 5]
    >>> 1 in i2
    True
    >>> i3 = Interval(1, 5, closed_L=True)  # Half-open interval [1, 5)
    >>> str(i3)
    '[1, 5)'
    >>> i4 = ClosedInterval(1, 5)  # Closed interval [1, 5]
    >>> i5 = OpenInterval(1, 5)  # Open interval (1, 5)

### `Interval`

``` python
(
    *args: Union[Sequence[Union[float, int]], float, int],
    is_closed: Optional[bool] = None,
    closed_L: Optional[bool] = None,
    closed_R: Optional[bool] = None
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L51-L156)

- `lower: Union[float, int]`

- `upper: Union[float, int]`

- `closed_L: bool`

- `closed_R: bool`

- `singleton_set: Optional[set[Union[float, int]]]`

- `is_closed: bool`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L158-L164)

- `is_open: bool`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L166-L172)

- `is_half_open: bool`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L174-L178)

- `is_singleton: bool`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L180-L182)

- `is_empty: bool`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L184-L186)

- `is_finite: bool`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L188-L190)

- `singleton: Union[float, int]`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L192-L196)

### `def get_empty`

``` python
() -> muutils.interval.Interval
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L198-L200)

### `def get_singleton`

``` python
(value: Union[float, int]) -> muutils.interval.Interval
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L202-L206)

### `def numerical_contained`

``` python
(self, item: Union[float, int]) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L208-L217)

### `def interval_contained`

``` python
(self, item: muutils.interval.Interval) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L219-L245)

### `def from_str`

``` python
(cls, input_str: str) -> muutils.interval.Interval
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L265-L313)

### `def copy`

``` python
(self) -> muutils.interval.Interval
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L357-L364)

### `def size`

``` python
(self) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L366-L378)

Returns the size of the interval.

### Returns:

- `float` the size of the interval

### `def clamp`

``` python
(self, value: Union[int, float], epsilon: float = 1e-10) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L380-L440)

Clamp the given value to the interval bounds.

For open bounds, the clamped value will be slightly inside the interval
(by epsilon).

### Parameters:

- `value : Union[int, float]` the value to clamp.
- `epsilon : float` margin for open bounds (defaults to `_EPSILON`)

### Returns:

- `float` the clamped value

### Raises:

- `ValueError` : If the input value is NaN.

### `def intersection`

``` python
(self, other: muutils.interval.Interval) -> muutils.interval.Interval
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L442-L469)

### `def union`

``` python
(self, other: muutils.interval.Interval) -> muutils.interval.Interval
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L471-L518)

### `class ClosedInterval(Interval):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L521-L525)

Represents a mathematical interval, open by default.

The Interval class can represent both open and closed intervals, as well
as half-open intervals. It supports various initialization methods and
provides containment checks.

Examples:

    >>> i1 = Interval(1, 5)  # Default open interval (1, 5)
    >>> 3 in i1
    True
    >>> 1 in i1
    False
    >>> i2 = Interval([1, 5])  # Closed interval [1, 5]
    >>> 1 in i2
    True
    >>> i3 = Interval(1, 5, closed_L=True)  # Half-open interval [1, 5)
    >>> str(i3)
    '[1, 5)'
    >>> i4 = ClosedInterval(1, 5)  # Closed interval [1, 5]
    >>> i5 = OpenInterval(1, 5)  # Open interval (1, 5)

### `ClosedInterval`

``` python
(*args: Union[Sequence[float], float], **kwargs: Any)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L522-L525)

### Inherited Members

- [`lower`](#ClosedInterval.lower)
- [`upper`](#ClosedInterval.upper)
- [`closed_L`](#ClosedInterval.closed_L)
- [`closed_R`](#ClosedInterval.closed_R)
- [`singleton_set`](#ClosedInterval.singleton_set)
- [`is_closed`](#ClosedInterval.is_closed)
- [`is_open`](#ClosedInterval.is_open)
- [`is_half_open`](#ClosedInterval.is_half_open)
- [`is_singleton`](#ClosedInterval.is_singleton)
- [`is_empty`](#ClosedInterval.is_empty)
- [`is_finite`](#ClosedInterval.is_finite)
- [`singleton`](#ClosedInterval.singleton)
- [`get_empty`](#ClosedInterval.get_empty)
- [`get_singleton`](#ClosedInterval.get_singleton)
- [`numerical_contained`](#ClosedInterval.numerical_contained)
- [`interval_contained`](#ClosedInterval.interval_contained)
- [`from_str`](#ClosedInterval.from_str)
- [`copy`](#ClosedInterval.copy)
- [`size`](#ClosedInterval.size)
- [`clamp`](#ClosedInterval.clamp)
- [`intersection`](#ClosedInterval.intersection)
- [`union`](#ClosedInterval.union)

### `class OpenInterval(Interval):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L528-L532)

Represents a mathematical interval, open by default.

The Interval class can represent both open and closed intervals, as well
as half-open intervals. It supports various initialization methods and
provides containment checks.

Examples:

    >>> i1 = Interval(1, 5)  # Default open interval (1, 5)
    >>> 3 in i1
    True
    >>> 1 in i1
    False
    >>> i2 = Interval([1, 5])  # Closed interval [1, 5]
    >>> 1 in i2
    True
    >>> i3 = Interval(1, 5, closed_L=True)  # Half-open interval [1, 5)
    >>> str(i3)
    '[1, 5)'
    >>> i4 = ClosedInterval(1, 5)  # Closed interval [1, 5]
    >>> i5 = OpenInterval(1, 5)  # Open interval (1, 5)

### `OpenInterval`

``` python
(*args: Union[Sequence[float], float], **kwargs: Any)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/interval.py#L529-L532)

### Inherited Members

- [`lower`](#OpenInterval.lower)
- [`upper`](#OpenInterval.upper)
- [`closed_L`](#OpenInterval.closed_L)
- [`closed_R`](#OpenInterval.closed_R)
- [`singleton_set`](#OpenInterval.singleton_set)
- [`is_closed`](#OpenInterval.is_closed)
- [`is_open`](#OpenInterval.is_open)
- [`is_half_open`](#OpenInterval.is_half_open)
- [`is_singleton`](#OpenInterval.is_singleton)
- [`is_empty`](#OpenInterval.is_empty)
- [`is_finite`](#OpenInterval.is_finite)
- [`singleton`](#OpenInterval.singleton)
- [`get_empty`](#OpenInterval.get_empty)
- [`get_singleton`](#OpenInterval.get_singleton)
- [`numerical_contained`](#OpenInterval.numerical_contained)
- [`interval_contained`](#OpenInterval.interval_contained)
- [`from_str`](#OpenInterval.from_str)
- [`copy`](#OpenInterval.copy)
- [`size`](#OpenInterval.size)
- [`clamp`](#OpenInterval.clamp)
- [`intersection`](#OpenInterval.intersection)
- [`union`](#OpenInterval.union)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

submodule for serializing things to json in a recoverable way

you can throw *any* object into `muutils.json_serialize.json_serialize`
and it will return a `JSONitem`, meaning a bool, int, float, str, None,
list of `JSONitem`s, or a dict mappting to `JSONitem`.

The goal of this is if you want to just be able to store something as
relatively human-readable JSON, and don’t care as much about recovering
it, you can throw it into `json_serialize` and it will just work. If you
want to do so in a recoverable way, check out
[`ZANJ`](https://github.com/mivanit/ZANJ).

it will do so by looking in `DEFAULT_HANDLERS`, which will keep it as-is
if its already valid, then try to find a `.serialize()` method on the
object, and then have a bunch of special cases. You can add handlers by
initializing a `JsonSerializer` object and passing a sequence of them to
`handlers_pre`

additionally, `SerializeableDataclass` is a special kind of dataclass
where you specify how to serialize each field, and a `.serialize()`
method is automatically added to the class. This is done by using the
`serializable_dataclass` decorator, inheriting from
`SerializeableDataclass`, and `serializable_field` in place of
`dataclasses.field` when defining non-standard fields.

This module plays nicely with and is a dependency of the
[`ZANJ`](https://github.com/mivanit/ZANJ) library, which extends this to
support saving things to disk in a more efficient way than just plain
json (arrays are saved as npy files, for example), and automatically
detecting how to load saved objects into their original classes.

## Submodules

- [`array`](#array)
- [`util`](#util)
- [`json_serialize`](#json_serialize)
- [`serializable_dataclass`](#serializable_dataclass)
- [`serializable_field`](#serializable_field)

## API Documentation

- [`json_serialize`](#json_serialize)
- [`serializable_dataclass`](#serializable_dataclass)
- [`serializable_field`](#serializable_field)
- [`arr_metadata`](#arr_metadata)
- [`load_array`](#load_array)
- [`BASE_HANDLERS`](#BASE_HANDLERS)
- [`JSONitem`](#JSONitem)
- [`JsonSerializer`](#JsonSerializer)
- [`try_catch`](#try_catch)
- [`dc_eq`](#dc_eq)
- [`SerializableDataclass`](#SerializableDataclass)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py)

# `muutils.json_serialize`

submodule for serializing things to json in a recoverable way

you can throw *any* object into
`<a href="json_serialize/json_serialize.html">muutils.json_serialize.json_serialize</a>`
and it will return a `JSONitem`, meaning a bool, int, float, str, None,
list of `JSONitem`s, or a dict mappting to `JSONitem`.

The goal of this is if you want to just be able to store something as
relatively human-readable JSON, and don’t care as much about recovering
it, you can throw it into `json_serialize` and it will just work. If you
want to do so in a recoverable way, check out
[`ZANJ`](https://github.com/mivanit/ZANJ).

it will do so by looking in `DEFAULT_HANDLERS`, which will keep it as-is
if its already valid, then try to find a `.serialize()` method on the
object, and then have a bunch of special cases. You can add handlers by
initializing a `JsonSerializer` object and passing a sequence of them to
`handlers_pre`

additionally, `SerializeableDataclass` is a special kind of dataclass
where you specify how to serialize each field, and a `.serialize()`
method is automatically added to the class. This is done by using the
`serializable_dataclass` decorator, inheriting from
`SerializeableDataclass`, and `serializable_field` in place of
`dataclasses.field` when defining non-standard fields.

This module plays nicely with and is a dependency of the
[`ZANJ`](https://github.com/mivanit/ZANJ) library, which extends this to
support saving things to disk in a more efficient way than just plain
json (arrays are saved as npy files, for example), and automatically
detecting how to load saved objects into their original classes.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L0-L50)

### `def json_serialize`

``` python
(
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L331-L333)

serialize object to json-serializable object with default config

### `def serializable_dataclass`

``` python
(
    _cls=None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    properties_to_serialize: Optional[list[str]] = None,
    register_handler: bool = True,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except,
    on_typecheck_mismatch: muutils.errormode.ErrorMode = ErrorMode.Warn,
    methods_no_override: list[str] | None = None,
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L558-L905)

decorator to make a dataclass serializable. **must also make it inherit
from `SerializableDataclass`!!**

types will be validated (like pydantic) unless `on_typecheck_mismatch`
is set to `ErrorMode.IGNORE`

behavior of most kwargs matches that of `dataclasses.dataclass`, but
with some additional kwargs. any kwargs not listed here are passed to
`dataclasses.dataclass`

Returns the same class as was passed in, with dunder methods added based
on the fields defined in the class.

Examines PEP 526 `__annotations__` to determine fields.

If init is true, an `__init__()` method is added to the class. If repr
is true, a `__repr__()` method is added. If order is true, rich
comparison dunder methods are added. If unsafe_hash is true, a
`__hash__()` method function is added. If frozen is true, fields may not
be assigned to after instance creation.

``` python
@serializable_dataclass(kw_only=True)
class Myclass(SerializableDataclass):
    a: int
    b: str
```

``` python
>>> Myclass(a=1, b="q").serialize()
{_FORMAT_KEY: 'Myclass(SerializableDataclass)', 'a': 1, 'b': 'q'}
```

### Parameters:

- `_cls : _type_` class to decorate. don’t pass this arg, just use this
  as a decorator (defaults to `None`)
- `init : bool` whether to add an `__init__` method *(passed to
  dataclasses.dataclass)* (defaults to `True`)
- `repr : bool` whether to add a `__repr__` method *(passed to
  dataclasses.dataclass)* (defaults to `True`)
- `order : bool` whether to add rich comparison methods *(passed to
  dataclasses.dataclass)* (defaults to `False`)
- `unsafe_hash : bool` whether to add a `__hash__` method *(passed to
  dataclasses.dataclass)* (defaults to `False`)
- `frozen : bool` whether to make the class frozen *(passed to
  dataclasses.dataclass)* (defaults to `False`)
- `properties_to_serialize : Optional[list[str]]` which properties to
  add to the serialized data dict **SerializableDataclass only**
  (defaults to `None`)
- `register_handler : bool` if true, register the class with ZANJ for
  loading **SerializableDataclass only** (defaults to `True`)
- `on_typecheck_error : ErrorMode` what to do if type checking throws an
  exception (except, warn, ignore). If `ignore` and an exception is
  thrown, type validation will still return false
  **SerializableDataclass only**
- `on_typecheck_mismatch : ErrorMode` what to do if a type mismatch is
  found (except, warn, ignore). If `ignore`, type validation will return
  `True` **SerializableDataclass only**
- `methods_no_override : list[str]|None` list of methods that should not
  be overridden by the decorator by default, `__eq__`, `serialize`,
  `load`, and `validate_fields_types` are overridden by this function,
  but you can disable this if you’d rather write your own.
  `dataclasses.dataclass` might still overwrite these, and those options
  take precedence **SerializableDataclass only** (defaults to `None`)
- `**kwargs` *(passed to dataclasses.dataclass)*

### Returns:

- `_type_` the decorated class

### Raises:

- `KWOnlyError` : only raised if `kw_only` is `True` and python version
  is \<3.9, since `dataclasses.dataclass` does not support this
- `NotSerializableFieldException` : if a field is not a
  `SerializableField`
- `FieldSerializationError` : if there is an error serializing a field
- `AttributeError` : if a property is not found on the class
- `FieldLoadingError` : if there is an error loading a field

### `def serializable_field`

``` python
(
    *_args,
    default: Union[Any, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    default_factory: Union[Any, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[mappingproxy] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    **kwargs: Any
) -> Any
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L187-L279)

Create a new `SerializableField`

    default: Sfield_T | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    default_factory: Callable[[], Sfield_T]
    | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: types.MappingProxyType | None = None,
    kw_only: bool | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    ### ----------------------------------------------------------------------
    ### new in `SerializableField`, not in `dataclasses.Field`
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    loading_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,

### new Parameters:

- `serialize`: whether to serialize this field when serializing the
  class’
- `serialization_fn`: function taking the instance of the field and
  returning a serializable object. If not provided, will iterate through
  the `SerializerHandler`s defined in
  `<a href="json_serialize/json_serialize.html">muutils.json_serialize.json_serialize</a>`
- `loading_fn`: function taking the serialized object and returning the
  instance of the field. If not provided, will take object as-is.
- `deserialize_fn`: new alternative to `loading_fn`. takes only the
  field’s value, not the whole class. if both `loading_fn` and
  `deserialize_fn` are provided, an error will be raised.
- `assert_type`: whether to assert the type of the field when loading.
  if `False`, will not check the type of the field.
- `custom_typecheck_fn`: function taking the type of the field and
  returning whether the type itself is valid. if not provided, will use
  the default type checking.

### Gotchas:

- `loading_fn` takes the dict of the **class**, not the field. if you
  wanted a `loading_fn` that does nothing, you’d write:

``` python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        loading_fn=lambda x["my_field"]: int(x)
    )
```

using `deserialize_fn` instead:

``` python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: int(x)
    )
```

In the above code, `my_field` is an int but will be serialized as a
string.

note that if not using ZANJ, and you have a class inside a container,
you MUST provide `serialization_fn` and `loading_fn` to serialize and
load the container. ZANJ will automatically do this for you.

### TODO: `custom_value_check_fn`: function taking the value of the field and returning whether the value itself is valid. if not provided, any value is valid as long as it passes the type test

### `def arr_metadata`

``` python
(arr) -> dict[str, list[int] | str | int]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L48-L56)

get metadata for a numpy array

### `def load_array`

``` python
(
    arr: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]],
    array_mode: Optional[Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']] = None
) -> Any
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L167-L226)

load a json-serialized array, infer the mode if not specified

- `BASE_HANDLERS = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'))`

- `JSONitem = typing.Union[bool, int, float, str, NoneType, typing.List[typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]], typing.Dict[str, typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]]]`

### `class JsonSerializer:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L235-L325)

Json serialization class (holds configs)

### Parameters:

- `array_mode : ArrayMode` how to write arrays (defaults to
  `"array_list_meta"`)
- `error_mode : ErrorMode` what to do when we can’t serialize an object
  (will use repr as fallback if “ignore” or “warn”) (defaults to
  `"except"`)
- `handlers_pre : MonoTuple[SerializerHandler]` handlers to use before
  the default handlers (defaults to `tuple()`)
- `handlers_default : MonoTuple[SerializerHandler]` default handlers to
  use (defaults to `DEFAULT_HANDLERS`)
- `write_only_format : bool` changes \_FORMAT_KEY keys in output to
  “**write_format**” (when you want to serialize something in a way that
  zanj won’t try to recover the object when loading) (defaults to
  `False`)

### Raises:

- `ValueError`: on init, if `args` is not empty
- `SerializationException`: on `json_serialize()`, if any error occurs
  when trying to serialize an object and `error_mode` is set to
  `ErrorMode.EXCEPT"`

### `JsonSerializer`

``` python
(
    *args,
    array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim'] = 'array_list_meta',
    error_mode: muutils.errormode.ErrorMode = ErrorMode.Except,
    handlers_pre: None = (),
    handlers_default: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function _serialize_override_serialize_func>, uid='.serialize override', desc='objects with .serialize method'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='namedtuple -> dict', desc='namedtuples as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dataclass -> dict', desc='dataclasses as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='path -> str', desc='Path objects as posix strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='obj -> str(obj)', desc='directly serialize objects in `SERIALIZE_DIRECT_AS_STR` to strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='numpy.ndarray', desc='numpy arrays'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='torch.Tensor', desc='pytorch tensors'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='pandas.DataFrame', desc='pandas DataFrames'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(set, list, tuple, Iterable) -> list', desc='sets, lists, tuples, and Iterables as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='fallback', desc='fallback handler -- serialize object attributes and special functions as strings')),
    write_only_format: bool = False
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L261-L281)

- `array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']`

- `error_mode: muutils.errormode.ErrorMode`

- `write_only_format: bool`

- `handlers: None`

### `def json_serialize`

``` python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L283-L313)

### `def hashify`

``` python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = (),
    force: bool = True
) -> Union[bool, int, float, str, tuple]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L315-L325)

try to turn any object into something hashable

### `def try_catch`

``` python
(func: Callable)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L98-L111)

wraps the function to catch exceptions, returns serialized error message
on exception

returned func will return normal result on success, or error message on
exception

### `def dc_eq`

``` python
(
    dc1,
    dc2,
    except_when_class_mismatch: bool = False,
    false_when_class_mismatch: bool = True,
    except_when_field_mismatch: bool = False
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L192-L281)

checks if two dataclasses which (might) hold numpy arrays are equal

### Parameters:

- `dc1`: the first dataclass
- `dc2`: the second dataclass
- `except_when_class_mismatch: bool` if `True`, will throw `TypeError`
  if the classes are different. if not, will return false by default or
  attempt to compare the fields if `false_when_class_mismatch` is
  `False` (default: `False`)
- `false_when_class_mismatch: bool` only relevant if
  `except_when_class_mismatch` is `False`. if `True`, will return
  `False` if the classes are different. if `False`, will attempt to
  compare the fields.
- `except_when_field_mismatch: bool` only relevant if
  `except_when_class_mismatch` is `False` and
  `false_when_class_mismatch` is `False`. if `True`, will throw
  `TypeError` if the fields are different. (default: `True`)

### Returns:

- `bool`: True if the dataclasses are equal, False otherwise

### Raises:

- `TypeError`: if the dataclasses are of different classes
- `AttributeError`: if the dataclasses have different fields

### TODO: after “except when class mismatch” is False, shouldn’t we then go to “field keys match”?

              [START]
                 ▼
           ┌───────────┐  ┌─────────┐
           │dc1 is dc2?├─►│ classes │
           └──┬────────┘No│ match?  │
      ────    │           ├─────────┤
     (True)◄──┘Yes        │No       │Yes
      ────                ▼         ▼
          ┌────────────────┐ ┌────────────┐
          │ except when    │ │ fields keys│
          │ class mismatch?│ │ match?     │
          ├───────────┬────┘ ├───────┬────┘
          │Yes        │No    │No     │Yes
          ▼           ▼      ▼       ▼
     ───────────  ┌──────────┐  ┌────────┐
    { raise     } │ except   │  │ field  │
    { TypeError } │ when     │  │ values │
     ───────────  │ field    │  │ match? │
                  │ mismatch?│  ├────┬───┘
                  ├───────┬──┘  │    │Yes
                  │Yes    │No   │No  ▼
                  ▼       ▼     │   ────
     ───────────────     ─────  │  (True)
    { raise         }   (False)◄┘   ────
    { AttributeError}    ─────
     ───────────────

### `class SerializableDataclass(abc.ABC):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L294-L490)

Base class for serializable dataclasses

only for linting and type checking, still need to call
`serializable_dataclass` decorator

### Usage:

``` python
@serializable_dataclass
class MyClass(SerializableDataclass):
    a: int
    b: str
```

and then you can call `my_obj.serialize()` to get a dict that can be
serialized to json. So, you can do:

    >>> my_obj = MyClass(a=1, b="q")
    >>> s = json.dumps(my_obj.serialize())
    >>> s
    '{_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}'
    >>> read_obj = MyClass.load(json.loads(s))
    >>> read_obj == my_obj
    True

This isn’t too impressive on its own, but it gets more useful when you
have nested classses, or fields that are not json-serializable by
default:

``` python
@serializable_dataclass
class NestedClass(SerializableDataclass):
    x: str
    y: MyClass
    act_fun: torch.nn.Module = serializable_field(
        default=torch.nn.ReLU(),
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: getattr(torch.nn, x)(),
    )
```

which gives us:

    >>> nc = NestedClass(x="q", y=MyClass(a=1, b="q"), act_fun=torch.nn.Sigmoid())
    >>> s = json.dumps(nc.serialize())
    >>> s
    '{_FORMAT_KEY: "NestedClass(SerializableDataclass)", "x": "q", "y": {_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}, "act_fun": "Sigmoid"}'
    >>> read_nc = NestedClass.load(json.loads(s))
    >>> read_nc == nc
    True

### `def serialize`

``` python
(self) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L347-L351)

returns the class as a dict, implemented by using
`@serializable_dataclass` decorator

### `def load`

``` python
(cls: Type[~T], data: Union[dict[str, Any], ~T]) -> ~T
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L353-L356)

takes in an appropriately structured dict and returns an instance of the
class, implemented by using `@serializable_dataclass` decorator

### `def validate_fields_types`

``` python
(
    self,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L358-L364)

validate the types of all the fields on a `SerializableDataclass`. calls
`SerializableDataclass__validate_field_type` for each field

### `def validate_field_type`

``` python
(
    self,
    field: muutils.json_serialize.serializable_field.SerializableField | str,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L366-L374)

given a dataclass, check the field matches the type hint

### `def diff`

``` python
(
    self,
    other: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    of_serialized: bool = False
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L383-L465)

get a rich and recursive diff between two instances of a serializable
dataclass

``` python
>>> Myclass(a=1, b=2).diff(Myclass(a=1, b=3))
{'b': {'self': 2, 'other': 3}}
>>> NestedClass(x="q1", y=Myclass(a=1, b=2)).diff(NestedClass(x="q2", y=Myclass(a=1, b=3)))
{'x': {'self': 'q1', 'other': 'q2'}, 'y': {'b': {'self': 2, 'other': 3}}}
```

### Parameters:

- `other : SerializableDataclass` other instance to compare against
- `of_serialized : bool` if true, compare serialized data and not raw
  values (defaults to `False`)

### Returns:

- `dict[str, Any]`

### Raises:

- `ValueError` : if the instances are not of the same type
- `ValueError` : if the instances are `dataclasses.dataclass` but not
  `SerializableDataclass`

### `def update_from_nested_dict`

``` python
(self, nested_dict: dict[str, typing.Any])
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/__init__.py#L467-L482)

update the instance from a nested dict, useful for configuration from
command line args

### Parameters:

    - `nested_dict : dict[str, Any]`
        nested dict to update the instance with

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

this utilities module handles serialization and loading of numpy and
torch arrays as json

- `array_list_meta` is less efficient (arrays are stored as nested
  lists), but preserves both metadata and human readability.
- `array_b64_meta` is the most efficient, but is not human readable.
- `external` is mostly for use in
  [`ZANJ`](https://github.com/mivanit/ZANJ)

## API Documentation

- [`ArrayMode`](#ArrayMode)
- [`array_n_elements`](#array_n_elements)
- [`arr_metadata`](#arr_metadata)
- [`serialize_array`](#serialize_array)
- [`infer_array_mode`](#infer_array_mode)
- [`load_array`](#load_array)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py)

# `muutils.json_serialize.array`

this utilities module handles serialization and loading of numpy and
torch arrays as json

- `array_list_meta` is less efficient (arrays are stored as nested
  lists), but preserves both metadata and human readability.
- `array_b64_meta` is the most efficient, but is not human readable.
- `external` is mostly for use in
  [`ZANJ`](https://github.com/mivanit/ZANJ)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py#L0-L225)

- `ArrayMode = typing.Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']`

### `def array_n_elements`

``` python
(arr) -> int
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py#L38-L45)

get the number of elements in an array

### `def arr_metadata`

``` python
(arr) -> dict[str, list[int] | str | int]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py#L48-L56)

get metadata for a numpy array

### `def serialize_array`

``` python
(
    jser: "'JsonSerializer'",
    arr: numpy.ndarray,
    path: Union[str, Sequence[str | int]],
    array_mode: Optional[Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']] = None
) -> Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py#L59-L133)

serialize a numpy or pytorch array in one of several modes

if the object is zero-dimensional, simply get the unique item

`array_mode: ArrayMode` can be one of: - `list`: serialize as a list of
values, no metadata (equivalent to `arr.tolist()`) - `array_list_meta`:
serialize dict with metadata, actual list under the key `data` -
`array_hex_meta`: serialize dict with metadata, actual hex string under
the key `data` - `array_b64_meta`: serialize dict with metadata, actual
base64 string under the key `data`

for `array_list_meta`, `array_hex_meta`, and `array_b64_meta`, the
serialized object is:

    {
        _FORMAT_KEY: <array_list_meta|array_hex_meta>,
        "shape": arr.shape,
        "dtype": str(arr.dtype),
        "data": <arr.tolist()|arr.tobytes().hex()|base64.b64encode(arr.tobytes()).decode()>,
    }

### Parameters:

- `arr : Any` array to serialize
- `array_mode : ArrayMode` mode in which to serialize the array
  (defaults to `None` and inheriting from `jser: JsonSerializer`)

### Returns:

- `JSONitem` json serialized array

### Raises:

- `KeyError` : if the array mode is not valid

### `def infer_array_mode`

``` python
(
    arr: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]
) -> Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py#L136-L164)

given a serialized array, infer the mode

assumes the array was serialized via `serialize_array()`

### `def load_array`

``` python
(
    arr: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]],
    array_mode: Optional[Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']] = None
) -> Any
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/array.py#L167-L226)

load a json-serialized array, infer the mode if not specified

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

provides the basic framework for json serialization of objects

notably:

- `SerializerHandler` defines how to serialize a specific type of object
- `JsonSerializer` handles configuration for which handlers to use
- `json_serialize` provides the default configuration if you don’t care
  – call it on any object!

## API Documentation

- [`SERIALIZER_SPECIAL_KEYS`](#SERIALIZER_SPECIAL_KEYS)
- [`SERIALIZER_SPECIAL_FUNCS`](#SERIALIZER_SPECIAL_FUNCS)
- [`SERIALIZE_DIRECT_AS_STR`](#SERIALIZE_DIRECT_AS_STR)
- [`ObjectPath`](#ObjectPath)
- [`SerializerHandler`](#SerializerHandler)
- [`BASE_HANDLERS`](#BASE_HANDLERS)
- [`DEFAULT_HANDLERS`](#DEFAULT_HANDLERS)
- [`JsonSerializer`](#JsonSerializer)
- [`GLOBAL_JSON_SERIALIZER`](#GLOBAL_JSON_SERIALIZER)
- [`json_serialize`](#json_serialize)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py)

# `muutils.json_serialize.json_serialize`

provides the basic framework for json serialization of objects

notably:

- `SerializerHandler` defines how to serialize a specific type of object
- `JsonSerializer` handles configuration for which handlers to use
- `json_serialize` provides the default configuration if you don’t care
  – call it on any object!

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L0-L332)

- `SERIALIZER_SPECIAL_KEYS: None = ('__name__', '__doc__', '__module__', '__class__', '__dict__', '__annotations__')`

- `SERIALIZER_SPECIAL_FUNCS: dict[str, typing.Callable] = {'str': <class 'str'>, 'dir': <built-in function dir>, 'type': <function <lambda>>, 'repr': <function <lambda>>, 'code': <function <lambda>>, 'sourcefile': <function <lambda>>}`

- `SERIALIZE_DIRECT_AS_STR: Set[str] = {"<class 'torch.dtype'>", "<class 'torch.device'>"}`

- `ObjectPath = tuple[typing.Union[str, int], ...]`

### `class SerializerHandler:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L72-L109)

a handler for a specific type of object

### Parameters:

    - `check : Callable[[JsonSerializer, Any], bool]` takes a JsonSerializer and an object, returns whether to use this handler
    - `serialize : Callable[[JsonSerializer, Any, ObjectPath], JSONitem]` takes a JsonSerializer, an object, and the current path, returns the serialized object
    - `desc : str` description of the handler (optional)

### `SerializerHandler`

``` python
(
    check: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], bool],
    serialize_func: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]],
    uid: str,
    desc: str
)
```

- `check: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], bool]`

- `serialize_func: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]]`

- `uid: str`

- `desc: str`

### `def serialize`

``` python
(self) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L91-L109)

serialize the handler info

- `BASE_HANDLERS: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'))`

- `DEFAULT_HANDLERS: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function _serialize_override_serialize_func>, uid='.serialize override', desc='objects with .serialize method'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='namedtuple -> dict', desc='namedtuples as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dataclass -> dict', desc='dataclasses as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='path -> str', desc='Path objects as posix strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='obj -> str(obj)', desc='directly serialize objects in`SERIALIZE_DIRECT_AS_STR`to strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='numpy.ndarray', desc='numpy arrays'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='torch.Tensor', desc='pytorch tensors'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='pandas.DataFrame', desc='pandas DataFrames'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(set, list, tuple, Iterable) -> list', desc='sets, lists, tuples, and Iterables as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='fallback', desc='fallback handler -- serialize object attributes and special functions as strings'))`

### `class JsonSerializer:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L235-L325)

Json serialization class (holds configs)

### Parameters:

- `array_mode : ArrayMode` how to write arrays (defaults to
  `"array_list_meta"`)
- `error_mode : ErrorMode` what to do when we can’t serialize an object
  (will use repr as fallback if “ignore” or “warn”) (defaults to
  `"except"`)
- `handlers_pre : MonoTuple[SerializerHandler]` handlers to use before
  the default handlers (defaults to `tuple()`)
- `handlers_default : MonoTuple[SerializerHandler]` default handlers to
  use (defaults to `DEFAULT_HANDLERS`)
- `write_only_format : bool` changes \_FORMAT_KEY keys in output to
  “**write_format**” (when you want to serialize something in a way that
  zanj won’t try to recover the object when loading) (defaults to
  `False`)

### Raises:

- `ValueError`: on init, if `args` is not empty
- `SerializationException`: on `json_serialize()`, if any error occurs
  when trying to serialize an object and `error_mode` is set to
  `ErrorMode.EXCEPT"`

### `JsonSerializer`

``` python
(
    *args,
    array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim'] = 'array_list_meta',
    error_mode: muutils.errormode.ErrorMode = ErrorMode.Except,
    handlers_pre: None = (),
    handlers_default: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function _serialize_override_serialize_func>, uid='.serialize override', desc='objects with .serialize method'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='namedtuple -> dict', desc='namedtuples as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dataclass -> dict', desc='dataclasses as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='path -> str', desc='Path objects as posix strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='obj -> str(obj)', desc='directly serialize objects in `SERIALIZE_DIRECT_AS_STR` to strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='numpy.ndarray', desc='numpy arrays'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='torch.Tensor', desc='pytorch tensors'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='pandas.DataFrame', desc='pandas DataFrames'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(set, list, tuple, Iterable) -> list', desc='sets, lists, tuples, and Iterables as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='fallback', desc='fallback handler -- serialize object attributes and special functions as strings')),
    write_only_format: bool = False
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L261-L281)

- `array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']`

- `error_mode: muutils.errormode.ErrorMode`

- `write_only_format: bool`

- `handlers: None`

### `def json_serialize`

``` python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L283-L313)

### `def hashify`

``` python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = (),
    force: bool = True
) -> Union[bool, int, float, str, tuple]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L315-L325)

try to turn any object into something hashable

- `GLOBAL_JSON_SERIALIZER: muutils.json_serialize.json_serialize.JsonSerializer = <muutils.json_serialize.json_serialize.JsonSerializer object>`

### `def json_serialize`

``` python
(
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/json_serialize.py#L331-L333)

serialize object to json-serializable object with default config

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

save and load objects to and from json or compatible formats in a
recoverable way

`d = dataclasses.asdict(my_obj)` will give you a dict, but if some
fields are not json-serializable, you will get an error when you call
`json.dumps(d)`. This module provides a way around that.

Instead, you define your class:

``` python
@serializable_dataclass
class MyClass(SerializableDataclass):
    a: int
    b: str
```

and then you can call `my_obj.serialize()` to get a dict that can be
serialized to json. So, you can do:

    >>> my_obj = MyClass(a=1, b="q")
    >>> s = json.dumps(my_obj.serialize())
    >>> s
    '{_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}'
    >>> read_obj = MyClass.load(json.loads(s))
    >>> read_obj == my_obj
    True

This isn’t too impressive on its own, but it gets more useful when you
have nested classses, or fields that are not json-serializable by
default:

``` python
@serializable_dataclass
class NestedClass(SerializableDataclass):
    x: str
    y: MyClass
    act_fun: torch.nn.Module = serializable_field(
        default=torch.nn.ReLU(),
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: getattr(torch.nn, x)(),
    )
```

which gives us:

    >>> nc = NestedClass(x="q", y=MyClass(a=1, b="q"), act_fun=torch.nn.Sigmoid())
    >>> s = json.dumps(nc.serialize())
    >>> s
    '{_FORMAT_KEY: "NestedClass(SerializableDataclass)", "x": "q", "y": {_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}, "act_fun": "Sigmoid"}'
    >>> read_nc = NestedClass.load(json.loads(s))
    >>> read_nc == nc
    True

## API Documentation

- [`CantGetTypeHintsWarning`](#CantGetTypeHintsWarning)
- [`ZanjMissingWarning`](#ZanjMissingWarning)
- [`zanj_register_loader_serializable_dataclass`](#zanj_register_loader_serializable_dataclass)
- [`FieldIsNotInitOrSerializeWarning`](#FieldIsNotInitOrSerializeWarning)
- [`SerializableDataclass__validate_field_type`](#SerializableDataclass__validate_field_type)
- [`SerializableDataclass__validate_fields_types__dict`](#SerializableDataclass__validate_fields_types__dict)
- [`SerializableDataclass__validate_fields_types`](#SerializableDataclass__validate_fields_types)
- [`SerializableDataclass`](#SerializableDataclass)
- [`get_cls_type_hints_cached`](#get_cls_type_hints_cached)
- [`get_cls_type_hints`](#get_cls_type_hints)
- [`KWOnlyError`](#KWOnlyError)
- [`FieldError`](#FieldError)
- [`NotSerializableFieldException`](#NotSerializableFieldException)
- [`FieldSerializationError`](#FieldSerializationError)
- [`FieldLoadingError`](#FieldLoadingError)
- [`FieldTypeMismatchError`](#FieldTypeMismatchError)
- [`serializable_dataclass`](#serializable_dataclass)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py)

# `muutils.json_serialize.serializable_dataclass`

save and load objects to and from json or compatible formats in a
recoverable way

`d = dataclasses.asdict(my_obj)` will give you a dict, but if some
fields are not json-serializable, you will get an error when you call
`json.dumps(d)`. This module provides a way around that.

Instead, you define your class:

``` python
@serializable_dataclass
class MyClass(SerializableDataclass):
    a: int
    b: str
```

and then you can call `my_obj.serialize()` to get a dict that can be
serialized to json. So, you can do:

    >>> my_obj = MyClass(a=1, b="q")
    >>> s = json.dumps(my_obj.serialize())
    >>> s
    '{_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}'
    >>> read_obj = MyClass.load(json.loads(s))
    >>> read_obj == my_obj
    True

This isn’t too impressive on its own, but it gets more useful when you
have nested classses, or fields that are not json-serializable by
default:

``` python
@serializable_dataclass
class NestedClass(SerializableDataclass):
    x: str
    y: MyClass
    act_fun: torch.nn.Module = serializable_field(
        default=torch.nn.ReLU(),
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: getattr(torch.nn, x)(),
    )
```

which gives us:

    >>> nc = NestedClass(x="q", y=MyClass(a=1, b="q"), act_fun=torch.nn.Sigmoid())
    >>> s = json.dumps(nc.serialize())
    >>> s
    '{_FORMAT_KEY: "NestedClass(SerializableDataclass)", "x": "q", "y": {_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}, "act_fun": "Sigmoid"}'
    >>> read_nc = NestedClass.load(json.loads(s))
    >>> read_nc == nc
    True

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L0-L904)

### `class CantGetTypeHintsWarning(builtins.UserWarning):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L87-L90)

special warning for when we can’t get type hints

### Inherited Members

- [`UserWarning`](#CantGetTypeHintsWarning.__init__)

- [`with_traceback`](#CantGetTypeHintsWarning.with_traceback)

- [`add_note`](#CantGetTypeHintsWarning.add_note)

- [`args`](#CantGetTypeHintsWarning.args)

### `class ZanjMissingWarning(builtins.UserWarning):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L93-L96)

special warning for when [`ZANJ`](https://github.com/mivanit/ZANJ) is
missing – `register_loader_serializable_dataclass` will not work

### Inherited Members

- [`UserWarning`](#ZanjMissingWarning.__init__)

- [`with_traceback`](#ZanjMissingWarning.with_traceback)

- [`add_note`](#ZanjMissingWarning.add_note)

- [`args`](#ZanjMissingWarning.args)

### `def zanj_register_loader_serializable_dataclass`

``` python
(cls: Type[~T])
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L103-L142)

Register a serializable dataclass with the ZANJ import

this allows `ZANJ().read()` to load the class and not just return plain
dicts

### TODO: there is some duplication here with register_loader_handler

### `class FieldIsNotInitOrSerializeWarning(builtins.UserWarning):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L149-L150)

Base class for warnings generated by user code.

### Inherited Members

- [`UserWarning`](#FieldIsNotInitOrSerializeWarning.__init__)

- [`with_traceback`](#FieldIsNotInitOrSerializeWarning.with_traceback)

- [`add_note`](#FieldIsNotInitOrSerializeWarning.add_note)

- [`args`](#FieldIsNotInitOrSerializeWarning.args)

### `def SerializableDataclass__validate_field_type`

``` python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    field: muutils.json_serialize.serializable_field.SerializableField | str,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L153-L242)

given a dataclass, check the field matches the type hint

this function is written to
`<a href="#SerializableDataclass.validate_field_type">SerializableDataclass.validate_field_type</a>`

### Parameters:

- `self : SerializableDataclass` `SerializableDataclass` instance
- `field : SerializableField | str` field to validate, will get from
  `self.__dataclass_fields__` if an `str`
- `on_typecheck_error : ErrorMode` what to do if type checking throws an
  exception (except, warn, ignore). If `ignore` and an exception is
  thrown, the function will return `False` (defaults to
  `_DEFAULT_ON_TYPECHECK_ERROR`)

### Returns:

- `bool` if the field type is correct. `False` if the field type is
  incorrect or an exception is thrown and `on_typecheck_error` is
  `ignore`

### `def SerializableDataclass__validate_fields_types__dict`

``` python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> dict[str, bool]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L245-L279)

validate the types of all the fields on a `SerializableDataclass`. calls
`SerializableDataclass__validate_field_type` for each field

returns a dict of field names to bools, where the bool is if the field
type is valid

### `def SerializableDataclass__validate_fields_types`

``` python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L282-L291)

validate the types of all the fields on a `SerializableDataclass`. calls
`SerializableDataclass__validate_field_type` for each field

### `class SerializableDataclass(abc.ABC):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L294-L490)

Base class for serializable dataclasses

only for linting and type checking, still need to call
`serializable_dataclass` decorator

### Usage:

``` python
@serializable_dataclass
class MyClass(SerializableDataclass):
    a: int
    b: str
```

and then you can call `my_obj.serialize()` to get a dict that can be
serialized to json. So, you can do:

    >>> my_obj = MyClass(a=1, b="q")
    >>> s = json.dumps(my_obj.serialize())
    >>> s
    '{_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}'
    >>> read_obj = MyClass.load(json.loads(s))
    >>> read_obj == my_obj
    True

This isn’t too impressive on its own, but it gets more useful when you
have nested classses, or fields that are not json-serializable by
default:

``` python
@serializable_dataclass
class NestedClass(SerializableDataclass):
    x: str
    y: MyClass
    act_fun: torch.nn.Module = serializable_field(
        default=torch.nn.ReLU(),
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: getattr(torch.nn, x)(),
    )
```

which gives us:

    >>> nc = NestedClass(x="q", y=MyClass(a=1, b="q"), act_fun=torch.nn.Sigmoid())
    >>> s = json.dumps(nc.serialize())
    >>> s
    '{_FORMAT_KEY: "NestedClass(SerializableDataclass)", "x": "q", "y": {_FORMAT_KEY: "MyClass(SerializableDataclass)", "a": 1, "b": "q"}, "act_fun": "Sigmoid"}'
    >>> read_nc = NestedClass.load(json.loads(s))
    >>> read_nc == nc
    True

### `def serialize`

``` python
(self) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L347-L351)

returns the class as a dict, implemented by using
`@serializable_dataclass` decorator

### `def load`

``` python
(cls: Type[~T], data: Union[dict[str, Any], ~T]) -> ~T
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L353-L356)

takes in an appropriately structured dict and returns an instance of the
class, implemented by using `@serializable_dataclass` decorator

### `def validate_fields_types`

``` python
(
    self,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L358-L364)

validate the types of all the fields on a `SerializableDataclass`. calls
`SerializableDataclass__validate_field_type` for each field

### `def validate_field_type`

``` python
(
    self,
    field: muutils.json_serialize.serializable_field.SerializableField | str,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L366-L374)

given a dataclass, check the field matches the type hint

### `def diff`

``` python
(
    self,
    other: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    of_serialized: bool = False
) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L383-L465)

get a rich and recursive diff between two instances of a serializable
dataclass

``` python
>>> Myclass(a=1, b=2).diff(Myclass(a=1, b=3))
{'b': {'self': 2, 'other': 3}}
>>> NestedClass(x="q1", y=Myclass(a=1, b=2)).diff(NestedClass(x="q2", y=Myclass(a=1, b=3)))
{'x': {'self': 'q1', 'other': 'q2'}, 'y': {'b': {'self': 2, 'other': 3}}}
```

### Parameters:

- `other : SerializableDataclass` other instance to compare against
- `of_serialized : bool` if true, compare serialized data and not raw
  values (defaults to `False`)

### Returns:

- `dict[str, Any]`

### Raises:

- `ValueError` : if the instances are not of the same type
- `ValueError` : if the instances are `dataclasses.dataclass` but not
  `SerializableDataclass`

### `def update_from_nested_dict`

``` python
(self, nested_dict: dict[str, typing.Any])
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L467-L482)

update the instance from a nested dict, useful for configuration from
command line args

### Parameters:

    - `nested_dict : dict[str, Any]`
        nested dict to update the instance with

### `def get_cls_type_hints_cached`

``` python
(cls: Type[~T]) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L495-L498)

cached typing.get_type_hints for a class

### `def get_cls_type_hints`

``` python
(cls: Type[~T]) -> dict[str, typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L501-L519)

helper function to get type hints for a class

### `class KWOnlyError(builtins.NotImplementedError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L522-L525)

kw-only dataclasses are not supported in python \<3.9

### Inherited Members

- [`NotImplementedError`](#KWOnlyError.__init__)

- [`with_traceback`](#KWOnlyError.with_traceback)

- [`add_note`](#KWOnlyError.add_note)

- [`args`](#KWOnlyError.args)

### `class FieldError(builtins.ValueError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L528-L531)

base class for field errors

### Inherited Members

- [`ValueError`](#FieldError.__init__)

- [`with_traceback`](#FieldError.with_traceback)

- [`add_note`](#FieldError.add_note)

- [`args`](#FieldError.args)

### `class NotSerializableFieldException(FieldError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L534-L537)

field is not a `SerializableField`

### Inherited Members

- [`ValueError`](#NotSerializableFieldException.__init__)

- [`with_traceback`](#NotSerializableFieldException.with_traceback)

- [`add_note`](#NotSerializableFieldException.add_note)

- [`args`](#NotSerializableFieldException.args)

### `class FieldSerializationError(FieldError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L540-L543)

error while serializing a field

### Inherited Members

- [`ValueError`](#FieldSerializationError.__init__)

- [`with_traceback`](#FieldSerializationError.with_traceback)

- [`add_note`](#FieldSerializationError.add_note)

- [`args`](#FieldSerializationError.args)

### `class FieldLoadingError(FieldError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L546-L549)

error while loading a field

### Inherited Members

- [`ValueError`](#FieldLoadingError.__init__)

- [`with_traceback`](#FieldLoadingError.with_traceback)

- [`add_note`](#FieldLoadingError.add_note)

- [`args`](#FieldLoadingError.args)

### `class FieldTypeMismatchError(FieldError, builtins.TypeError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L552-L555)

error when a field type does not match the type hint

### Inherited Members

- [`ValueError`](#FieldTypeMismatchError.__init__)

- [`with_traceback`](#FieldTypeMismatchError.with_traceback)

- [`add_note`](#FieldTypeMismatchError.add_note)

- [`args`](#FieldTypeMismatchError.args)

### `def serializable_dataclass`

``` python
(
    _cls=None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    properties_to_serialize: Optional[list[str]] = None,
    register_handler: bool = True,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except,
    on_typecheck_mismatch: muutils.errormode.ErrorMode = ErrorMode.Warn,
    methods_no_override: list[str] | None = None,
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_dataclass.py#L558-L905)

decorator to make a dataclass serializable. **must also make it inherit
from `SerializableDataclass`!!**

types will be validated (like pydantic) unless `on_typecheck_mismatch`
is set to `ErrorMode.IGNORE`

behavior of most kwargs matches that of `dataclasses.dataclass`, but
with some additional kwargs. any kwargs not listed here are passed to
`dataclasses.dataclass`

Returns the same class as was passed in, with dunder methods added based
on the fields defined in the class.

Examines PEP 526 `__annotations__` to determine fields.

If init is true, an `__init__()` method is added to the class. If repr
is true, a `__repr__()` method is added. If order is true, rich
comparison dunder methods are added. If unsafe_hash is true, a
`__hash__()` method function is added. If frozen is true, fields may not
be assigned to after instance creation.

``` python
@serializable_dataclass(kw_only=True)
class Myclass(SerializableDataclass):
    a: int
    b: str
```

``` python
>>> Myclass(a=1, b="q").serialize()
{_FORMAT_KEY: 'Myclass(SerializableDataclass)', 'a': 1, 'b': 'q'}
```

### Parameters:

- `_cls : _type_` class to decorate. don’t pass this arg, just use this
  as a decorator (defaults to `None`)
- `init : bool` whether to add an `__init__` method *(passed to
  dataclasses.dataclass)* (defaults to `True`)
- `repr : bool` whether to add a `__repr__` method *(passed to
  dataclasses.dataclass)* (defaults to `True`)
- `order : bool` whether to add rich comparison methods *(passed to
  dataclasses.dataclass)* (defaults to `False`)
- `unsafe_hash : bool` whether to add a `__hash__` method *(passed to
  dataclasses.dataclass)* (defaults to `False`)
- `frozen : bool` whether to make the class frozen *(passed to
  dataclasses.dataclass)* (defaults to `False`)
- `properties_to_serialize : Optional[list[str]]` which properties to
  add to the serialized data dict **SerializableDataclass only**
  (defaults to `None`)
- `register_handler : bool` if true, register the class with ZANJ for
  loading **SerializableDataclass only** (defaults to `True`)
- `on_typecheck_error : ErrorMode` what to do if type checking throws an
  exception (except, warn, ignore). If `ignore` and an exception is
  thrown, type validation will still return false
  **SerializableDataclass only**
- `on_typecheck_mismatch : ErrorMode` what to do if a type mismatch is
  found (except, warn, ignore). If `ignore`, type validation will return
  `True` **SerializableDataclass only**
- `methods_no_override : list[str]|None` list of methods that should not
  be overridden by the decorator by default, `__eq__`, `serialize`,
  `load`, and `validate_fields_types` are overridden by this function,
  but you can disable this if you’d rather write your own.
  `dataclasses.dataclass` might still overwrite these, and those options
  take precedence **SerializableDataclass only** (defaults to `None`)
- `**kwargs` *(passed to dataclasses.dataclass)*

### Returns:

- `_type_` the decorated class

### Raises:

- `KWOnlyError` : only raised if `kw_only` is `True` and python version
  is \<3.9, since `dataclasses.dataclass` does not support this
- `NotSerializableFieldException` : if a field is not a
  `SerializableField`
- `FieldSerializationError` : if there is an error serializing a field
- `AttributeError` : if a property is not found on the class
- `FieldLoadingError` : if there is an error loading a field

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

extends `dataclasses.Field` for use with `SerializableDataclass`

In particular, instead of using `dataclasses.field`, use
`serializable_field` to define fields in a `SerializableDataclass`. You
provide information on how the field should be serialized and loaded (as
well as anything that goes into `dataclasses.field`) when you define the
field, and the `SerializableDataclass` will automatically use those
functions.

## API Documentation

- [`SerializableField`](#SerializableField)
- [`serializable_field`](#serializable_field)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_field.py)

# `muutils.json_serialize.serializable_field`

extends `dataclasses.Field` for use with `SerializableDataclass`

In particular, instead of using `dataclasses.field`, use
`serializable_field` to define fields in a `SerializableDataclass`. You
provide information on how the field should be serialized and loaded (as
well as anything that goes into `dataclasses.field`) when you define the
field, and the `SerializableDataclass` will automatically use those
functions.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_field.py#L0-L278)

### `class SerializableField(dataclasses.Field):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_field.py#L20-L127)

extension of `dataclasses.Field` with additional serialization
properties

### `SerializableField`

``` python
(
    default: Union[Any, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    default_factory: Union[Callable[[], Any], dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[mappingproxy] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    loading_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[<member 'type' of 'SerializableField' objects>], bool]] = None
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_field.py#L45-L109)

- `serialize: bool`

- `serialization_fn: Optional[Callable[[Any], Any]]`

- `loading_fn: Optional[Callable[[Any], Any]]`

- `deserialize_fn: Optional[Callable[[Any], Any]]`

- `assert_type: bool`

- `custom_typecheck_fn: Optional[Callable[[<member 'type' of 'SerializableField' objects>], bool]]`

### `def from_Field`

``` python
(
    cls,
    field: dataclasses.Field
) -> muutils.json_serialize.serializable_field.SerializableField
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_field.py#L111-L127)

copy all values from a `dataclasses.Field` to new `SerializableField`

- `name`

- `type`

- `default`

- `default_factory`

- `init`

- `repr`

- `hash`

- `compare`

- `metadata`

- `kw_only`

### `def serializable_field`

``` python
(
    *_args,
    default: Union[Any, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    default_factory: Union[Any, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: Optional[mappingproxy] = None,
    kw_only: Union[bool, dataclasses._MISSING_TYPE] = <dataclasses._MISSING_TYPE object>,
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    **kwargs: Any
) -> Any
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/serializable_field.py#L187-L279)

Create a new `SerializableField`

    default: Sfield_T | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    default_factory: Callable[[], Sfield_T]
    | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    metadata: types.MappingProxyType | None = None,
    kw_only: bool | dataclasses._MISSING_TYPE = dataclasses.MISSING,
    ### ----------------------------------------------------------------------
    ### new in `SerializableField`, not in `dataclasses.Field`
    serialize: bool = True,
    serialization_fn: Optional[Callable[[Any], Any]] = None,
    loading_fn: Optional[Callable[[Any], Any]] = None,
    deserialize_fn: Optional[Callable[[Any], Any]] = None,
    assert_type: bool = True,
    custom_typecheck_fn: Optional[Callable[[type], bool]] = None,

### new Parameters:

- `serialize`: whether to serialize this field when serializing the
  class’
- `serialization_fn`: function taking the instance of the field and
  returning a serializable object. If not provided, will iterate through
  the `SerializerHandler`s defined in
  `<a href="json_serialize.html">muutils.json_serialize.json_serialize</a>`
- `loading_fn`: function taking the serialized object and returning the
  instance of the field. If not provided, will take object as-is.
- `deserialize_fn`: new alternative to `loading_fn`. takes only the
  field’s value, not the whole class. if both `loading_fn` and
  `deserialize_fn` are provided, an error will be raised.
- `assert_type`: whether to assert the type of the field when loading.
  if `False`, will not check the type of the field.
- `custom_typecheck_fn`: function taking the type of the field and
  returning whether the type itself is valid. if not provided, will use
  the default type checking.

### Gotchas:

- `loading_fn` takes the dict of the **class**, not the field. if you
  wanted a `loading_fn` that does nothing, you’d write:

``` python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        loading_fn=lambda x["my_field"]: int(x)
    )
```

using `deserialize_fn` instead:

``` python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: int(x)
    )
```

In the above code, `my_field` is an int but will be serialized as a
string.

note that if not using ZANJ, and you have a class inside a container,
you MUST provide `serialization_fn` and `loading_fn` to serialize and
load the container. ZANJ will automatically do this for you.

### TODO: `custom_value_check_fn`: function taking the value of the field and returning whether the value itself is valid. if not provided, any value is valid as long as it passes the type test

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

utilities for json_serialize

## API Documentation

- [`BaseType`](#BaseType)
- [`JSONitem`](#JSONitem)
- [`JSONdict`](#JSONdict)
- [`Hashableitem`](#Hashableitem)
- [`UniversalContainer`](#UniversalContainer)
- [`isinstance_namedtuple`](#isinstance_namedtuple)
- [`try_catch`](#try_catch)
- [`SerializationException`](#SerializationException)
- [`string_as_lines`](#string_as_lines)
- [`safe_getsource`](#safe_getsource)
- [`array_safe_eq`](#array_safe_eq)
- [`dc_eq`](#dc_eq)
- [`MonoTuple`](#MonoTuple)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py)

# `muutils.json_serialize.util`

utilities for json_serialize

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L0-L280)

- `BaseType = typing.Union[bool, int, float, str, NoneType]`

- `JSONitem = typing.Union[bool, int, float, str, NoneType, typing.List[typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]], typing.Dict[str, typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]]]`

- `JSONdict = typing.Dict[str, typing.Union[bool, int, float, str, NoneType, typing.List[typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]], typing.Dict[str, typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]]]]`

- `Hashableitem = typing.Union[bool, int, float, str, tuple]`

### `class UniversalContainer:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L76-L80)

contains everything – `x in UniversalContainer()` is always True

### `def isinstance_namedtuple`

``` python
(x: Any) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L83-L95)

checks if `x` is a `namedtuple`

credit to
https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple

### `def try_catch`

``` python
(func: Callable)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L98-L111)

wraps the function to catch exceptions, returns serialized error message
on exception

returned func will return normal result on success, or error message on
exception

### `class SerializationException(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L128-L129)

Common base class for all non-exit exceptions.

### Inherited Members

- [`Exception`](#SerializationException.__init__)

- [`with_traceback`](#SerializationException.with_traceback)

- [`add_note`](#SerializationException.add_note)

- [`args`](#SerializationException.args)

### `def string_as_lines`

``` python
(s: str | None) -> list[str]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L132-L140)

for easier reading of long strings in json, split up by newlines

sort of like how jupyter notebooks do it

### `def safe_getsource`

``` python
(func) -> list[str]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L143-L147)

### `def array_safe_eq`

``` python
(a: Any, b: Any) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L151-L189)

check if two objects are equal, account for if numpy arrays or torch
tensors

### `def dc_eq`

``` python
(
    dc1,
    dc2,
    except_when_class_mismatch: bool = False,
    false_when_class_mismatch: bool = True,
    except_when_field_mismatch: bool = False
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L192-L281)

checks if two dataclasses which (might) hold numpy arrays are equal

### Parameters:

- `dc1`: the first dataclass
- `dc2`: the second dataclass
- `except_when_class_mismatch: bool` if `True`, will throw `TypeError`
  if the classes are different. if not, will return false by default or
  attempt to compare the fields if `false_when_class_mismatch` is
  `False` (default: `False`)
- `false_when_class_mismatch: bool` only relevant if
  `except_when_class_mismatch` is `False`. if `True`, will return
  `False` if the classes are different. if `False`, will attempt to
  compare the fields.
- `except_when_field_mismatch: bool` only relevant if
  `except_when_class_mismatch` is `False` and
  `false_when_class_mismatch` is `False`. if `True`, will throw
  `TypeError` if the fields are different. (default: `True`)

### Returns:

- `bool`: True if the dataclasses are equal, False otherwise

### Raises:

- `TypeError`: if the dataclasses are of different classes
- `AttributeError`: if the dataclasses have different fields

### TODO: after “except when class mismatch” is False, shouldn’t we then go to “field keys match”?

              [START]
                 ▼
           ┌───────────┐  ┌─────────┐
           │dc1 is dc2?├─►│ classes │
           └──┬────────┘No│ match?  │
      ────    │           ├─────────┤
     (True)◄──┘Yes        │No       │Yes
      ────                ▼         ▼
          ┌────────────────┐ ┌────────────┐
          │ except when    │ │ fields keys│
          │ class mismatch?│ │ match?     │
          ├───────────┬────┘ ├───────┬────┘
          │Yes        │No    │No     │Yes
          ▼           ▼      ▼       ▼
     ───────────  ┌──────────┐  ┌────────┐
    { raise     } │ except   │  │ field  │
    { TypeError } │ when     │  │ values │
     ───────────  │ field    │  │ match? │
                  │ mismatch?│  ├────┬───┘
                  ├───────┬──┘  │    │Yes
                  │Yes    │No   │No  ▼
                  ▼       ▼     │   ────
     ───────────────     ─────  │  (True)
    { raise         }   (False)◄┘   ────
    { AttributeError}    ─────
     ───────────────

### `class MonoTuple:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/json_serialize/util.py#L48-L73)

tuple type hint, but for a tuple of any length with all the same type

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

utilities for reading and writing jsonlines files, including gzip
support

## API Documentation

- [`jsonl_load`](#jsonl_load)
- [`jsonl_load_log`](#jsonl_load_log)
- [`jsonl_write`](#jsonl_write)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/jsonlines.py)

# `muutils.jsonlines`

utilities for reading and writing jsonlines files, including gzip
support

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/jsonlines.py#L0-L76)

### `def jsonl_load`

``` python
(
    path: str,
    /,
    *,
    use_gzip: bool | None = None
) -> list[typing.Union[bool, int, float, str, NoneType, typing.List[typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]], typing.Dict[str, typing.Union[bool, int, float, str, NoneType, typing.List[typing.Any], typing.Dict[str, typing.Any]]]]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/jsonlines.py#L30-L43)

### `def jsonl_load_log`

``` python
(path: str, /, *, use_gzip: bool | None = None) -> list[dict]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/jsonlines.py#L46-L60)

### `def jsonl_write`

``` python
(
    path: str,
    items: Sequence[Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]]],
    use_gzip: bool | None = None,
    gzip_compresslevel: int = 2
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/jsonlines.py#L63-L77)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

anonymous getitem class

util for constructing a class which has a getitem method which just
calls a function

a `lambda` is an anonymous function: kappa is the letter before lambda
in the greek alphabet, hence the name of this class

## API Documentation

- [`Kappa`](#Kappa)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/kappa.py)

# `muutils.kappa`

anonymous getitem class

util for constructing a class which has a getitem method which just
calls a function

a `lambda` is an anonymous function: kappa is the letter before lambda
in the greek alphabet, hence the name of this class

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/kappa.py#L0-L45)

### `class Kappa(typing.Mapping[~_kappa_K, ~_kappa_V]):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/kappa.py#L26-L46)

A Mapping is a generic container for associating key/value pairs.

This class provides concrete generic implementations of all methods
except for **getitem**, **iter**, and **len**.

### `Kappa`

``` python
(func_getitem: Callable[[~_kappa_K], ~_kappa_V])
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/kappa.py#L27-L33)

- `func_getitem`

- `doc`

### Inherited Members

- [`get`](#Kappa.get)
- [`keys`](#Kappa.keys)
- [`items`](#Kappa.items)
- [`values`](#Kappa.values)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

(deprecated) experimenting with logging utilities

## Submodules

- [`exception_context`](#exception_context)
- [`headerfuncs`](#headerfuncs)
- [`log_util`](#log_util)
- [`logger`](#logger)
- [`loggingstream`](#loggingstream)
- [`simplelogger`](#simplelogger)
- [`timing`](#timing)

## API Documentation

- [`Logger`](#Logger)
- [`LoggingStream`](#LoggingStream)
- [`SimpleLogger`](#SimpleLogger)
- [`TimerContext`](#TimerContext)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py)

# `muutils.logger`

(deprecated) experimenting with logging utilities

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L0-L29)

### `class Logger(muutils.logger.simplelogger.SimpleLogger):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L40-L306)

logger with more features, including log levels and streams

### Parameters:

        - `log_path : str | None`
        default log file path
        (defaults to `None`)
        - `log_file : AnyIO | None`
        default log io, should have a `.write()` method (pass only this or `log_path`, not both)
        (defaults to `None`)
        - `timestamp : bool`
        whether to add timestamps to every log message (under the `_timestamp` key)
        (defaults to `True`)
        - `default_level : int`
        default log level for streams/messages that don't specify a level
        (defaults to `0`)
        - `console_print_threshold : int`
        log level at which to print to the console, anything greater will not be printed unless overridden by `console_print`
        (defaults to `50`)
        - `level_header : HeaderFunction`
        function for formatting log messages when printing to console
        (defaults to `HEADER_FUNCTIONS["md"]`)

- `keep_last_msg_time : bool` whether to keep the last message time
  (defaults to `True`)

### Raises:

        - `ValueError` : _description_

### `Logger`

``` python
(
    log_path: str | None = None,
    log_file: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    default_level: int = 0,
    console_print_threshold: int = 50,
    level_header: muutils.logger.headerfuncs.HeaderFunction = <function md_header_function>,
    streams: Union[dict[str | None, muutils.logger.loggingstream.LoggingStream], Sequence[muutils.logger.loggingstream.LoggingStream]] = (),
    keep_last_msg_time: bool = True,
    timestamp: bool = True,
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L71-L147)

### `def log`

``` python
(
    self,
    msg: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]] = None,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = False,
    extra_indent: str = '',
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L158-L267)

logging function

##### Parameters:

- `msg : JSONitem` message (usually string or dict) to be logged
- `lvl : int | None` level of message (lower levels are more important)
  (defaults to `None`)
- `console_print : bool` override `console_print_threshold` setting
  (defaults to `False`)
- `stream : str | None` whether to log to a stream (defaults to `None`),
  which logs to the default `None` stream (defaults to `None`)

### `def log_elapsed_last`

``` python
(
    self,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = True,
    **kwargs
) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L269-L286)

logs the time elapsed since the last message was printed to the console
(in any stream)

### `def flush_all`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L288-L295)

flush all streams

### `class LoggingStream:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L11-L95)

properties of a logging stream

- `name: str` name of the stream
- `aliases: set[str]` aliases for the stream (calls to these names will
  be redirected to this stream. duplicate alises will result in errors)
  TODO: perhaps duplicate alises should result in duplicate writes?
- `file: str|bool|AnyIO|None` file to write to - if `None`, will write
  to standard log - if `True`, will write to `name + ".log"` - if
  `False` will “write” to `NullIO` (throw it away) - if a string, will
  write to that file - if a fileIO type object, will write to that
  object
- `default_level: int|None` default level for this stream
- `default_contents: dict[str, Callable[[], Any]]` default contents for
  this stream
- `last_msg: tuple[float, Any]|None` last message written to this stream
  (timestamp, message)

### `LoggingStream`

``` python
(
    name: str | None,
    aliases: set[str | None] = <factory>,
    file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    default_level: int | None = None,
    default_contents: dict[str, typing.Callable[[], typing.Any]] = <factory>,
    handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None
)
```

- `name: str | None`

- `aliases: set[str | None]`

- `file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`

- `default_level: int | None = None`

- `default_contents: dict[str, typing.Callable[[], typing.Any]]`

- `handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`

### `def make_handler`

``` python
(self) -> Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L40-L76)

### `class SimpleLogger:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L34-L81)

logs training data to a jsonl file

### `SimpleLogger`

``` python
(
    log_path: str | None = None,
    log_file: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    timestamp: bool = True
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L37-L65)

### `def log`

``` python
(
    self,
    msg: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]],
    console_print: bool = False,
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L67-L81)

log a message to the log file, and optionally to the console

### `class TimerContext:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/__init__.py#L7-L22)

context manager for timing code

- `start_time: float`

- `end_time: float`

- `elapsed_time: float`

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`ExceptionContext`](#ExceptionContext)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/exception_context.py)

# `muutils.logger.exception_context`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/exception_context.py#L0-L42)

### `class ExceptionContext:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/exception_context.py#L6-L43)

context manager which catches all exceptions happening while the context
is open, `.write()` the exception trace to the given stream, and then
raises the exception

for example:

``` python
errorfile = open('error.log', 'w')

with ExceptionContext(errorfile):
        # do something that might throw an exception
        # if it does, the exception trace will be written to errorfile
        # and then the exception will be raised
```

### `ExceptionContext`

``` python
(stream)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/exception_context.py#L23-L24)

- `stream`

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`HeaderFunction`](#HeaderFunction)
- [`md_header_function`](#md_header_function)
- [`HEADER_FUNCTIONS`](#HEADER_FUNCTIONS)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/headerfuncs.py)

# `muutils.logger.headerfuncs`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/headerfuncs.py#L0-L67)

### `class HeaderFunction(typing.Protocol):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/headerfuncs.py#L12-L13)

Base class for protocol classes.

Protocol classes are defined as::

    class Proto(Protocol):
        def meth(self) -> int:
            ...

Such classes are primarily used with static type checkers that recognize
structural subtyping (static duck-typing).

For example::

    class C:
        def meth(self) -> int:
            return 0

    def func(x: Proto) -> int:
        return x.meth()

    func(C())  # Passes static type check

See PEP 544 for details. Protocol classes decorated with
@typing.runtime_checkable act as simple-minded runtime protocols that
check only the presence of given attributes, ignoring their type
signatures. Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...

### `HeaderFunction`

``` python
(*args, **kwargs)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/headerfuncs.py#L1766-L1792)

### `def md_header_function`

``` python
(
    msg: Any,
    lvl: int,
    stream: str | None = None,
    indent_lvl: str = '  ',
    extra_indent: str = '',
    **kwargs
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/headerfuncs.py#L16-L63)

standard header function. will output

- `# {msg}`

        for levels in [0, 9]

- `## {msg}`

        for levels in [10, 19], and so on

- `[{stream}] # {msg}`

        for a non-`None` stream, with level headers as before

- `!WARNING! [{stream}] {msg}`

        for level in [-9, -1]

- `!!WARNING!! [{stream}] {msg}`

        for level in [-19, -10] and so on

- `HEADER_FUNCTIONS: dict[str, muutils.logger.headerfuncs.HeaderFunction] = {'md': <function md_header_function>}`

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`get_any_from_stream`](#get_any_from_stream)
- [`gather_log`](#gather_log)
- [`gather_stream`](#gather_stream)
- [`gather_val`](#gather_val)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/log_util.py)

# `muutils.logger.log_util`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/log_util.py#L0-L79)

### `def get_any_from_stream`

``` python
(stream: list[dict], key: str) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/log_util.py#L4-L10)

get the first value of a key from a stream. errors if not found

### `def gather_log`

``` python
(file: str) -> dict[str, list[dict]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/log_util.py#L13-L24)

gathers and sorts all streams from a log

### `def gather_stream`

``` python
(file: str, stream: str) -> list[dict]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/log_util.py#L27-L40)

gets all entries from a specific stream in a log file

### `def gather_val`

``` python
(
    file: str,
    stream: str,
    keys: tuple[str],
    allow_skip: bool = True
) -> list[list]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/log_util.py#L43-L80)

gather specific keys from a specific stream in a log file

example: if “log.jsonl” has contents:

``` jsonl
{"a": 1, "b": 2, "c": 3, "_stream": "s1"}
{"a": 4, "b": 5, "c": 6, "_stream": "s1"}
{"a": 7, "b": 8, "c": 9, "_stream": "s2"}
```

then `gather_val("log.jsonl", "s1", ("a", "b"))` will return

``` python
[
    [1, 2],
    [4, 5]
]
```

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both
  console and a file
- `Logger` class handles levels in a slightly different way than default
  python `logging`, and also has “streams” which allow for different
  sorts of output in the same logger this was mostly made with training
  models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the
  duration of a block of code

## API Documentation

- [`decode_level`](#decode_level)
- [`Logger`](#Logger)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py)

# `muutils.logger.logger`

logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both
  console and a file
- `Logger` class handles levels in a slightly different way than default
  python `logging`, and also has “streams” which allow for different
  sorts of output in the same logger this was mostly made with training
  models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the
  duration of a block of code

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L0-L305)

### `def decode_level`

``` python
(level: int) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L27-L36)

### `class Logger(muutils.logger.simplelogger.SimpleLogger):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L40-L306)

logger with more features, including log levels and streams

### Parameters:

        - `log_path : str | None`
        default log file path
        (defaults to `None`)
        - `log_file : AnyIO | None`
        default log io, should have a `.write()` method (pass only this or `log_path`, not both)
        (defaults to `None`)
        - `timestamp : bool`
        whether to add timestamps to every log message (under the `_timestamp` key)
        (defaults to `True`)
        - `default_level : int`
        default log level for streams/messages that don't specify a level
        (defaults to `0`)
        - `console_print_threshold : int`
        log level at which to print to the console, anything greater will not be printed unless overridden by `console_print`
        (defaults to `50`)
        - `level_header : HeaderFunction`
        function for formatting log messages when printing to console
        (defaults to `HEADER_FUNCTIONS["md"]`)

- `keep_last_msg_time : bool` whether to keep the last message time
  (defaults to `True`)

### Raises:

        - `ValueError` : _description_

### `Logger`

``` python
(
    log_path: str | None = None,
    log_file: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    default_level: int = 0,
    console_print_threshold: int = 50,
    level_header: muutils.logger.headerfuncs.HeaderFunction = <function md_header_function>,
    streams: Union[dict[str | None, muutils.logger.loggingstream.LoggingStream], Sequence[muutils.logger.loggingstream.LoggingStream]] = (),
    keep_last_msg_time: bool = True,
    timestamp: bool = True,
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L71-L147)

### `def log`

``` python
(
    self,
    msg: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]] = None,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = False,
    extra_indent: str = '',
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L158-L267)

logging function

##### Parameters:

- `msg : JSONitem` message (usually string or dict) to be logged
- `lvl : int | None` level of message (lower levels are more important)
  (defaults to `None`)
- `console_print : bool` override `console_print_threshold` setting
  (defaults to `False`)
- `stream : str | None` whether to log to a stream (defaults to `None`),
  which logs to the default `None` stream (defaults to `None`)

### `def log_elapsed_last`

``` python
(
    self,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = True,
    **kwargs
) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L269-L286)

logs the time elapsed since the last message was printed to the console
(in any stream)

### `def flush_all`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/logger.py#L288-L295)

flush all streams

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`LoggingStream`](#LoggingStream)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/loggingstream.py)

# `muutils.logger.loggingstream`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/loggingstream.py#L0-L94)

### `class LoggingStream:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/loggingstream.py#L11-L95)

properties of a logging stream

- `name: str` name of the stream
- `aliases: set[str]` aliases for the stream (calls to these names will
  be redirected to this stream. duplicate alises will result in errors)
  TODO: perhaps duplicate alises should result in duplicate writes?
- `file: str|bool|AnyIO|None` file to write to - if `None`, will write
  to standard log - if `True`, will write to `name + ".log"` - if
  `False` will “write” to `NullIO` (throw it away) - if a string, will
  write to that file - if a fileIO type object, will write to that
  object
- `default_level: int|None` default level for this stream
- `default_contents: dict[str, Callable[[], Any]]` default contents for
  this stream
- `last_msg: tuple[float, Any]|None` last message written to this stream
  (timestamp, message)

### `LoggingStream`

``` python
(
    name: str | None,
    aliases: set[str | None] = <factory>,
    file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    default_level: int | None = None,
    default_contents: dict[str, typing.Callable[[], typing.Any]] = <factory>,
    handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None
)
```

- `name: str | None`

- `aliases: set[str | None]`

- `file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`

- `default_level: int | None = None`

- `default_contents: dict[str, typing.Callable[[], typing.Any]]`

- `handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`

### `def make_handler`

``` python
(self) -> Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/loggingstream.py#L40-L76)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`NullIO`](#NullIO)
- [`AnyIO`](#AnyIO)
- [`SimpleLogger`](#SimpleLogger)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py)

# `muutils.logger.simplelogger`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L0-L80)

### `class NullIO:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L12-L28)

null IO class

### `def write`

``` python
(self, msg: str) -> int
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L18-L20)

write to nothing! this throws away the message

### `def flush`

``` python
(self) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L22-L24)

flush nothing! this is a no-op

### `def close`

``` python
(self) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L26-L28)

close nothing! this is a no-op

- `AnyIO = typing.Union[typing.TextIO, muutils.logger.simplelogger.NullIO]`

### `class SimpleLogger:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L34-L81)

logs training data to a jsonl file

### `SimpleLogger`

``` python
(
    log_path: str | None = None,
    log_file: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    timestamp: bool = True
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L37-L65)

### `def log`

``` python
(
    self,
    msg: Union[bool, int, float, str, NoneType, List[Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]], Dict[str, Union[bool, int, float, str, NoneType, List[Any], Dict[str, Any]]]],
    console_print: bool = False,
    **kwargs
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/simplelogger.py#L67-L81)

log a message to the log file, and optionally to the console

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`TimerContext`](#TimerContext)
- [`filter_time_str`](#filter_time_str)
- [`ProgressEstimator`](#ProgressEstimator)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py)

# `muutils.logger.timing`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L0-L86)

### `class TimerContext:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L7-L22)

context manager for timing code

- `start_time: float`

- `end_time: float`

- `elapsed_time: float`

### `def filter_time_str`

``` python
(time: str) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L25-L30)

assuming format `h:mm:ss`, clips off the hours if its 0

### `class ProgressEstimator:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L33-L87)

estimates progress and can give a progress bar

### `ProgressEstimator`

``` python
(
    n_total: int,
    pbar_fill: str = '█',
    pbar_empty: str = ' ',
    pbar_bounds: tuple[str, str] = ('|', '|')
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L36-L48)

- `n_total: int`

- `starttime: float`

- `pbar_fill: str`

- `pbar_empty: str`

- `pbar_bounds: tuple[str, str]`

- `total_str_len: int`

### `def get_timing_raw`

``` python
(self, i: int) -> dict[str, float]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L50-L59)

returns dict(elapsed, per_iter, remaining, percent)

### `def get_pbar`

``` python
(self, i: int, width: int = 30) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L61-L77)

returns a progress bar

### `def get_progress_default`

``` python
(self, i: int) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/logger/timing.py#L79-L87)

returns a progress string

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Submodules

- [`bins`](#bins)
- [`matrix_powers`](#matrix_powers)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/__init__.py)

# `muutils.math`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/__init__.py#L0-L3)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`Bins`](#Bins)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/bins.py)

# `muutils.math.bins`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/bins.py#L0-L66)

### `class Bins:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/bins.py#L11-L67)

### `Bins`

``` python
(
    n_bins: int = 32,
    start: float = 0,
    stop: float = 1.0,
    scale: Literal['lin', 'log'] = 'log',
    _log_min: float = 0.001,
    _zero_in_small_start_log: bool = True
)
```

- `n_bins: int = 32`

- `start: float = 0`

- `stop: float = 1.0`

- `scale: Literal['lin', 'log'] = 'log'`

- `edges: jaxtyping.Float[ndarray, 'n_bins+1']`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/bins.py#L21-L53)

- `centers: jaxtyping.Float[ndarray, 'n_bins']`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/bins.py#L55-L57)

### `def changed_n_bins_copy`

``` python
(self, n_bins: int) -> muutils.math.bins.Bins
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/bins.py#L59-L67)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`matrix_powers`](#matrix_powers)
- [`matrix_powers_torch`](#matrix_powers_torch)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/matrix_powers.py)

# `muutils.math.matrix_powers`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/matrix_powers.py#L0-L163)

### `def matrix_powers`

``` python
(
    A: jaxtyping.Float[ndarray, 'n n'],
    powers: Sequence[int]
) -> jaxtyping.Float[ndarray, 'n_powers n n']
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/matrix_powers.py#L12-L80)

Compute multiple powers of a matrix efficiently.

Uses binary exponentiation to compute powers in O(log max(powers))
matrix multiplications, avoiding redundant calculations when computing
multiple powers.

### Parameters:

- `A : Float[np.ndarray, "n n"]` Square matrix to exponentiate
- `powers : Sequence[int]` List of powers to compute (non-negative
  integers)

### Returns:

- `dict[int, Float[np.ndarray, "n n"]]` Dictionary mapping each
  requested power to the corresponding matrix power

### `def matrix_powers_torch`

``` python
(A, powers: Sequence[int])
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/math/matrix_powers.py#L85-L164)

Compute multiple powers of a matrix efficiently.

Uses binary exponentiation to compute powers in O(log max(powers))
matrix multiplications, avoiding redundant calculations when computing
multiple powers.

### Parameters:

- `A : Float[torch.Tensor, "n n"]` Square matrix to exponentiate
- `powers : Sequence[int]` List of powers to compute (non-negative
  integers)

### Returns:

- `Float[torch.Tensor, "n_powers n n"]` Tensor containing the requested
  matrix powers stacked along the first dimension

### Raises:

- `ValueError` : If no powers are requested or if A is not a square
  matrix

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

miscellaneous utilities

- `stable_hash` for hashing that is stable across runs
- `muutils.misc.sequence` for sequence manipulation, applying mappings,
  and string-like operations on lists
- `muutils.misc.string` for sanitizing things for filenames, adjusting
  docstrings, and converting dicts to filenames
- `muutils.misc.numerical` for turning numbers into nice strings and
  back
- `muutils.misc.freezing` for freezing things
- `muutils.misc.classes` for some weird class utilities

## Submodules

- [`classes`](#classes)
- [`freezing`](#freezing)
- [`func`](#func)
- [`hashing`](#hashing)
- [`numerical`](#numerical)
- [`sequence`](#sequence)
- [`string`](#string)

## API Documentation

- [`stable_hash`](#stable_hash)
- [`WhenMissing`](#WhenMissing)
- [`empty_sequence_if_attr_false`](#empty_sequence_if_attr_false)
- [`flatten`](#flatten)
- [`list_split`](#list_split)
- [`list_join`](#list_join)
- [`apply_mapping`](#apply_mapping)
- [`apply_mapping_chain`](#apply_mapping_chain)
- [`sanitize_name`](#sanitize_name)
- [`sanitize_fname`](#sanitize_fname)
- [`sanitize_identifier`](#sanitize_identifier)
- [`dict_to_filename`](#dict_to_filename)
- [`dynamic_docstring`](#dynamic_docstring)
- [`shorten_numerical_to_str`](#shorten_numerical_to_str)
- [`str_to_numeric`](#str_to_numeric)
- [`_SHORTEN_MAP`](#_SHORTEN_MAP)
- [`FrozenDict`](#FrozenDict)
- [`FrozenList`](#FrozenList)
- [`freeze`](#freeze)
- [`is_abstract`](#is_abstract)
- [`get_all_subclasses`](#get_all_subclasses)
- [`isinstance_by_type_name`](#isinstance_by_type_name)
- [`IsDataclass`](#IsDataclass)
- [`get_hashable_eq_attrs`](#get_hashable_eq_attrs)
- [`dataclass_set_equals`](#dataclass_set_equals)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py)

# `muutils.misc`

miscellaneous utilities

- `stable_hash` for hashing that is stable across runs
- `<a href="misc/sequence.html">muutils.misc.sequence</a>` for sequence
  manipulation, applying mappings, and string-like operations on lists
- `<a href="misc/string.html">muutils.misc.string</a>` for sanitizing
  things for filenames, adjusting docstrings, and converting dicts to
  filenames
- `<a href="misc/numerical.html">muutils.misc.numerical</a>` for turning
  numbers into nice strings and back
- `<a href="misc/freezing.html">muutils.misc.freezing</a>` for freezing
  things
- `<a href="misc/classes.html">muutils.misc.classes</a>` for some weird
  class utilities

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L0-L82)

### `def stable_hash`

``` python
(s: str | bytes) -> int
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L8-L18)

Returns a stable hash of the given string. not cryptographically secure,
but stable between runs

- `WhenMissing = typing.Literal['except', 'skip', 'include']`

### `def empty_sequence_if_attr_false`

``` python
(itr: Iterable[Any], attr_owner: Any, attr_name: str) -> Iterable[Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L21-L42)

Returns `itr` if `attr_owner` has the attribute `attr_name` and it
boolean casts to `True`. Returns an empty sequence otherwise.

Particularly useful for optionally inserting delimiters into a sequence
depending on an `TokenizerElement` attribute.

### Parameters:

- `itr: Iterable[Any]` The iterable to return if the attribute is
  `True`.
- `attr_owner: Any` The object to check for the attribute.
- `attr_name: str` The name of the attribute to check.

### Returns:

- `itr: Iterable` if `attr_owner` has the attribute `attr_name` and it
  boolean casts to `True`, otherwise an empty sequence.
- `()` an empty sequence if the attribute is `False` or not present.

### `def flatten`

``` python
(it: Iterable[Any], levels_to_flatten: int | None = None) -> Generator
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L45-L68)

Flattens an arbitrarily nested iterable. Flattens all iterable data
types except for `str` and `bytes`.

### Returns

Generator over the flattened sequence.

### Parameters

- `it`: Any arbitrarily nested iterable.
- `levels_to_flatten`: Number of levels to flatten by, starting at the
  outermost layer. If `None`, performs full flattening.

### `def list_split`

``` python
(lst: list, val: Any) -> list[list]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L75-L103)

split a list into sublists by `val`. similar to “a_b_c”.split(“\_“)

``` python
>>> list_split([1,2,3,0,4,5,0,6], 0)
[[1, 2, 3], [4, 5], [6]]
>>> list_split([0,1,2,3], 0)
[[], [1, 2, 3]]
>>> list_split([1,2,3], 0)
[[1, 2, 3]]
>>> list_split([], 0)
[[]]
```

### `def list_join`

``` python
(lst: list, factory: Callable) -> list
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L106-L128)

add a *new* instance of `factory()` between each element of `lst`

``` python
>>> list_join([1,2,3], lambda : 0)
[1,0,2,0,3]
>>> list_join([1,2,3], lambda: [time.sleep(0.1), time.time()][1])
[1, 1600000000.0, 2, 1600000000.1, 3]
```

### `def apply_mapping`

``` python
(
    mapping: Mapping[~_AM_K, ~_AM_V],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L138-L184)

Given an iterable and a mapping, apply the mapping to the iterable with
certain options

Gotcha: if `when_missing` is invalid, this is totally fine until a
missing key is actually encountered.

Note: you can use this with
`<a href="kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to pass
a function instead of a dict

### Parameters:

- `mapping : Mapping[_AM_K, _AM_V]` must have `__contains__` and
  `__getitem__`, both of which take `_AM_K` and the latter returns
  `_AM_V`
- `iter : Iterable[_AM_K]` the iterable to apply the mapping to
- `when_missing : WhenMissing` what to do when a key is missing from the
  mapping – this is what distinguishes this function from `map` you can
  choose from `"skip"`, `"include"` (without converting), and `"except"`
  (defaults to `"skip"`)

### Returns:

return type is one of: - `list[_AM_V]` if `when_missing` is `"skip"` or
`"except"` - `list[Union[_AM_K, _AM_V]]` if `when_missing` is
`"include"`

### Raises:

- `KeyError` : if the item is missing from the mapping and
  `when_missing` is `"except"`
- `ValueError` : if `when_missing` is invalid

### `def apply_mapping_chain`

``` python
(
    mapping: Mapping[~_AM_K, Iterable[~_AM_V]],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L187-L234)

Given an iterable and a mapping, chain the mappings together

Gotcha: if `when_missing` is invalid, this is totally fine until a
missing key is actually encountered.

Note: you can use this with
`<a href="kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to pass
a function instead of a dict

### Parameters:

- `mapping : Mapping[_AM_K, Iterable[_AM_V]]` must have `__contains__`
  and `__getitem__`, both of which take `_AM_K` and the latter returns
  `Iterable[_AM_V]`
- `iter : Iterable[_AM_K]` the iterable to apply the mapping to
- `when_missing : WhenMissing` what to do when a key is missing from the
  mapping – this is what distinguishes this function from `map` you can
  choose from `"skip"`, `"include"` (without converting), and `"except"`
  (defaults to `"skip"`)

### Returns:

return type is one of: - `list[_AM_V]` if `when_missing` is `"skip"` or
`"except"` - `list[Union[_AM_K, _AM_V]]` if `when_missing` is
`"include"`

### Raises:

- `KeyError` : if the item is missing from the mapping and
  `when_missing` is `"except"`
- `ValueError` : if `when_missing` is invalid

### `def sanitize_name`

``` python
(
    name: str | None,
    additional_allowed_chars: str = '',
    replace_invalid: str = '',
    when_none: str | None = '_None_',
    leading_digit_prefix: str = ''
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L7-L55)

sanitize a string, leaving only alphanumerics and
`additional_allowed_chars`

### Parameters:

- `name : str | None` input string
- `additional_allowed_chars : str` additional characters to allow, none
  by default (defaults to `""`)
- `replace_invalid : str` character to replace invalid characters with
  (defaults to `""`)
- `when_none : str | None` string to return if `name` is `None`. if
  `None`, raises an exception (defaults to `"_None_"`)
- `leading_digit_prefix : str` character to prefix the string with if it
  starts with a digit (defaults to `""`)

### Returns:

- `str` sanitized string

### `def sanitize_fname`

``` python
(fname: str | None, **kwargs) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L58-L63)

sanitize a filename to posix standards

- leave only alphanumerics, `_` (underscore), ‘-’ (dash) and `.`
  (period)

### `def sanitize_identifier`

``` python
(fname: str | None, **kwargs) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L66-L74)

sanitize an identifier (variable or function name)

- leave only alphanumerics and `_` (underscore)
- prefix with `_` if it starts with a digit

### `def dict_to_filename`

``` python
(
    data: dict,
    format_str: str = '{key}_{val}',
    separator: str = '.',
    max_length: int = 255
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L77-L99)

### `def dynamic_docstring`

``` python
(**doc_params)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L102-L108)

### `def shorten_numerical_to_str`

``` python
(
    num: int | float,
    small_as_decimal: bool = True,
    precision: int = 1
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L22-L46)

shorten a large numerical value to a string 1234 -\> 1K

precision guaranteed to 1 in 10, but can be higher. reverse of
`str_to_numeric`

### `def str_to_numeric`

``` python
(
    quantity: str,
    mapping: None | bool | dict[str, int | float] = True
) -> int | float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L49-L165)

Convert a string representing a quantity to a numeric value.

The string can represent an integer, python float, fraction, or
shortened via `shorten_numerical_to_str`.

### Examples:

    >>> str_to_numeric("5")
    5
    >>> str_to_numeric("0.1")
    0.1
    >>> str_to_numeric("1/5")
    0.2
    >>> str_to_numeric("-1K")
    -1000.0
    >>> str_to_numeric("1.5M")
    1500000.0
    >>> str_to_numeric("1.2e2")
    120.0

- `_SHORTEN_MAP = {1000.0: 'K', 1000000.0: 'M', 1000000000.0: 'B', 1000000000000.0: 't', 1000000000000000.0: 'q', 1e+18: 'Q'}`

### `class FrozenDict(builtins.dict):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L5-L10)

### Inherited Members

- [`get`](#FrozenDict.get)
- [`setdefault`](#FrozenDict.setdefault)
- [`pop`](#FrozenDict.pop)
- [`popitem`](#FrozenDict.popitem)
- [`keys`](#FrozenDict.keys)
- [`items`](#FrozenDict.items)
- [`values`](#FrozenDict.values)
- [`update`](#FrozenDict.update)
- [`fromkeys`](#FrozenDict.fromkeys)
- [`clear`](#FrozenDict.clear)
- [`copy`](#FrozenDict.copy)

### `class FrozenList(builtins.list):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L13-L36)

Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list. The
argument must be an iterable if specified.

### `def append`

``` python
(self, value)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L20-L21)

Append object to the end of the list.

### `def extend`

``` python
(self, iterable)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L23-L24)

Extend list by appending elements from the iterable.

### `def insert`

``` python
(self, index, value)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L26-L27)

Insert object before index.

### `def remove`

``` python
(self, value)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L29-L30)

Remove first occurrence of value.

Raises ValueError if the value is not present.

### `def pop`

``` python
(self, index=-1)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L32-L33)

Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.

### `def clear`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L35-L36)

Remove all items from list.

### Inherited Members

- [`list`](#FrozenList.__init__)
- [`copy`](#FrozenList.copy)
- [`index`](#FrozenList.index)
- [`count`](#FrozenList.count)
- [`reverse`](#FrozenList.reverse)
- [`sort`](#FrozenList.sort)

### `def freeze`

``` python
(instance: Any) -> Any
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L52-L121)

recursively freeze an object in-place so that its attributes and
elements cannot be changed

messy in the sense that sometimes the object is modified in place, but
you can’t rely on that. always use the return value.

the [gelidum](https://github.com/diegojromerolopez/gelidum/) package is
a more complete implementation of this idea

### `def is_abstract`

``` python
(cls: type) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L14-L23)

Returns if a class is abstract.

### `def get_all_subclasses`

``` python
(class_: type, include_self=False) -> set[type]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L26-L48)

Returns a set containing all child classes in the subclass graph of
`class_`. I.e., includes subclasses of subclasses, etc.

### Parameters

- `include_self`: Whether to include `class_` itself in the returned set
- `class_`: Superclass

### Development

Since most class hierarchies are small, the inefficiencies of the
existing recursive implementation aren’t problematic. It might be
valuable to refactor with memoization if the need arises to use this
function on a very large class hierarchy.

### `def isinstance_by_type_name`

``` python
(o: object, type_name: str)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L51-L61)

Behaves like stdlib `isinstance` except it accepts a string
representation of the type rather than the type itself. This is a hacky
function intended to circumvent the need to import a type into a module.
It is susceptible to type name collisions.

### Parameters

`o`: Object (not the type itself) whose type to interrogate `type_name`:
The string returned by `type_.__name__`. Generic types are not
supported, only types that would appear in `type_.__mro__`.

### `class IsDataclass(typing.Protocol):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L68-L72)

Base class for protocol classes.

Protocol classes are defined as::

    class Proto(Protocol):
        def meth(self) -> int:
            ...

Such classes are primarily used with static type checkers that recognize
structural subtyping (static duck-typing).

For example::

    class C:
        def meth(self) -> int:
            return 0

    def func(x: Proto) -> int:
        return x.meth()

    func(C())  # Passes static type check

See PEP 544 for details. Protocol classes decorated with
@typing.runtime_checkable act as simple-minded runtime protocols that
check only the presence of given attributes, ignoring their type
signatures. Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...

### `IsDataclass`

``` python
(*args, **kwargs)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L1766-L1792)

### `def get_hashable_eq_attrs`

``` python
(dc: muutils.misc.classes.IsDataclass) -> tuple[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L75-L83)

Returns a tuple of all fields used for equality comparison, including
the type of the dataclass itself. The type is included to preserve the
unequal equality behavior of instances of different dataclasses whose
fields are identical. Essentially used to generate a hashable dataclass
representation for equality comparison even if it’s not frozen.

### `def dataclass_set_equals`

``` python
(
    coll1: Iterable[muutils.misc.classes.IsDataclass],
    coll2: Iterable[muutils.misc.classes.IsDataclass]
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/__init__.py#L86-L97)

Compares 2 collections of dataclass instances as if they were sets.
Duplicates are ignored in the same manner as a set. Unfrozen dataclasses
can’t be placed in sets since they’re not hashable. Collections of them
may be compared using this function.

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`is_abstract`](#is_abstract)
- [`get_all_subclasses`](#get_all_subclasses)
- [`isinstance_by_type_name`](#isinstance_by_type_name)
- [`IsDataclass`](#IsDataclass)
- [`get_hashable_eq_attrs`](#get_hashable_eq_attrs)
- [`dataclass_set_equals`](#dataclass_set_equals)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py)

# `muutils.misc.classes`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L0-L96)

### `def is_abstract`

``` python
(cls: type) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L14-L23)

Returns if a class is abstract.

### `def get_all_subclasses`

``` python
(class_: type, include_self=False) -> set[type]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L26-L48)

Returns a set containing all child classes in the subclass graph of
`class_`. I.e., includes subclasses of subclasses, etc.

### Parameters

- `include_self`: Whether to include `class_` itself in the returned set
- `class_`: Superclass

### Development

Since most class hierarchies are small, the inefficiencies of the
existing recursive implementation aren’t problematic. It might be
valuable to refactor with memoization if the need arises to use this
function on a very large class hierarchy.

### `def isinstance_by_type_name`

``` python
(o: object, type_name: str)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L51-L61)

Behaves like stdlib `isinstance` except it accepts a string
representation of the type rather than the type itself. This is a hacky
function intended to circumvent the need to import a type into a module.
It is susceptible to type name collisions.

### Parameters

`o`: Object (not the type itself) whose type to interrogate `type_name`:
The string returned by `type_.__name__`. Generic types are not
supported, only types that would appear in `type_.__mro__`.

### `class IsDataclass(typing.Protocol):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L68-L72)

Base class for protocol classes.

Protocol classes are defined as::

    class Proto(Protocol):
        def meth(self) -> int:
            ...

Such classes are primarily used with static type checkers that recognize
structural subtyping (static duck-typing).

For example::

    class C:
        def meth(self) -> int:
            return 0

    def func(x: Proto) -> int:
        return x.meth()

    func(C())  # Passes static type check

See PEP 544 for details. Protocol classes decorated with
@typing.runtime_checkable act as simple-minded runtime protocols that
check only the presence of given attributes, ignoring their type
signatures. Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...

### `IsDataclass`

``` python
(*args, **kwargs)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L1766-L1792)

### `def get_hashable_eq_attrs`

``` python
(dc: muutils.misc.classes.IsDataclass) -> tuple[typing.Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L75-L83)

Returns a tuple of all fields used for equality comparison, including
the type of the dataclass itself. The type is included to preserve the
unequal equality behavior of instances of different dataclasses whose
fields are identical. Essentially used to generate a hashable dataclass
representation for equality comparison even if it’s not frozen.

### `def dataclass_set_equals`

``` python
(
    coll1: Iterable[muutils.misc.classes.IsDataclass],
    coll2: Iterable[muutils.misc.classes.IsDataclass]
) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/classes.py#L86-L97)

Compares 2 collections of dataclass instances as if they were sets.
Duplicates are ignored in the same manner as a set. Unfrozen dataclasses
can’t be placed in sets since they’re not hashable. Collections of them
may be compared using this function.

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`FrozenDict`](#FrozenDict)
- [`FrozenList`](#FrozenList)
- [`freeze`](#freeze)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py)

# `muutils.misc.freezing`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L0-L120)

### `class FrozenDict(builtins.dict):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L5-L10)

### Inherited Members

- [`get`](#FrozenDict.get)
- [`setdefault`](#FrozenDict.setdefault)
- [`pop`](#FrozenDict.pop)
- [`popitem`](#FrozenDict.popitem)
- [`keys`](#FrozenDict.keys)
- [`items`](#FrozenDict.items)
- [`values`](#FrozenDict.values)
- [`update`](#FrozenDict.update)
- [`fromkeys`](#FrozenDict.fromkeys)
- [`clear`](#FrozenDict.clear)
- [`copy`](#FrozenDict.copy)

### `class FrozenList(builtins.list):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L13-L36)

Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list. The
argument must be an iterable if specified.

### `def append`

``` python
(self, value)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L20-L21)

Append object to the end of the list.

### `def extend`

``` python
(self, iterable)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L23-L24)

Extend list by appending elements from the iterable.

### `def insert`

``` python
(self, index, value)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L26-L27)

Insert object before index.

### `def remove`

``` python
(self, value)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L29-L30)

Remove first occurrence of value.

Raises ValueError if the value is not present.

### `def pop`

``` python
(self, index=-1)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L32-L33)

Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.

### `def clear`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L35-L36)

Remove all items from list.

### Inherited Members

- [`list`](#FrozenList.__init__)
- [`copy`](#FrozenList.copy)
- [`index`](#FrozenList.index)
- [`count`](#FrozenList.count)
- [`reverse`](#FrozenList.reverse)
- [`sort`](#FrozenList.sort)

### `def freeze`

``` python
(instance: Any) -> Any
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/freezing.py#L52-L121)

recursively freeze an object in-place so that its attributes and
elements cannot be changed

messy in the sense that sometimes the object is modified in place, but
you can’t rely on that. always use the return value.

the [gelidum](https://github.com/diegojromerolopez/gelidum/) package is
a more complete implementation of this idea

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`FuncParams`](#FuncParams)
- [`FuncParamsPreWrap`](#FuncParamsPreWrap)
- [`process_kwarg`](#process_kwarg)
- [`validate_kwarg`](#validate_kwarg)
- [`replace_kwarg`](#replace_kwarg)
- [`is_none`](#is_none)
- [`always_true`](#always_true)
- [`always_false`](#always_false)
- [`format_docstring`](#format_docstring)
- [`LambdaArgs`](#LambdaArgs)
- [`typed_lambda`](#typed_lambda)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py)

# `muutils.misc.func`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L0-L276)

- `FuncParams = ~FuncParams`

- `FuncParamsPreWrap = ~FuncParamsPreWrap`

### `def process_kwarg`

``` python
(
    kwarg_name: str,
    processor: Callable[[~T_process_in], ~T_process_out]
) -> Callable[[Callable[~FuncParamsPreWrap, ~ReturnType]], Callable[~FuncParams, ~ReturnType]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L37-L74)

Decorator that applies a processor to a keyword argument.

The underlying function is expected to have a keyword argument (with
name `kwarg_name`) of type `T_out`, but the caller provides a value of
type `T_in` that is converted via `processor`.

### Parameters:

- `kwarg_name : str` The name of the keyword argument to process.
- `processor : Callable[[T_in], T_out]` A callable that converts the
  input value (`T_in`) into the type expected by the function (`T_out`).

### Returns:

- A decorator that converts a function of type
  `Callable[OutputParams, ReturnType]` (expecting `kwarg_name` of type
  `T_out`) into one of type `Callable[InputParams, ReturnType]`
  (accepting `kwarg_name` of type `T_in`).

### `def validate_kwarg`

``` python
(
    kwarg_name: str,
    validator: Callable[[~T_kwarg], bool],
    description: str | None = None,
    action: muutils.errormode.ErrorMode = ErrorMode.Except
) -> Callable[[Callable[~FuncParams, ~ReturnType]], Callable[~FuncParams, ~ReturnType]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L77-L139)

Decorator that validates a specific keyword argument.

### Parameters:

- `kwarg_name : str` The name of the keyword argument to validate.
- `validator : Callable[[Any], bool]` A callable that returns True if
  the keyword argument is valid.
- `description : str | None` A message template if validation fails.
- `action : str` Either `"raise"` (default) or `"warn"`.

### Returns:

- `Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]`
  A decorator that validates the keyword argument.

### Modifies:

- If validation fails and `action=="warn"`, emits a warning. Otherwise,
  raises a ValueError.

### Usage:

``` python
@validate_kwarg("x", lambda val: val > 0, "Invalid {kwarg_name}: {value}")
def my_func(x: int) -> int:
    return x

assert my_func(x=1) == 1
```

### Raises:

- `ValueError` if validation fails and `action == "raise"`.

### `def replace_kwarg`

``` python
(
    kwarg_name: str,
    check: Callable[[~T_kwarg], bool],
    replacement_value: ~T_kwarg,
    replace_if_missing: bool = False
) -> Callable[[Callable[~FuncParams, ~ReturnType]], Callable[~FuncParams, ~ReturnType]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L142-L193)

Decorator that replaces a specific keyword argument value by identity
comparison.

### Parameters:

- `kwarg_name : str` The name of the keyword argument to replace.
- `check : Callable[[T_kwarg], bool]` A callable that returns True if
  the keyword argument should be replaced.
- `replacement_value : T_kwarg` The value to replace with.
- `replace_if_missing : bool` If True, replaces the keyword argument
  even if it’s missing.

### Returns:

- `Callable[[Callable[FuncParams, ReturnType]], Callable[FuncParams, ReturnType]]`
  A decorator that replaces the keyword argument value.

### Modifies:

- Updates `kwargs[kwarg_name]` if its value is `default_value`.

### Usage:

``` python
@replace_kwarg("x", None, "default_string")
def my_func(*, x: str | None = None) -> str:
    return x

assert my_func(x=None) == "default_string"
```

### `def is_none`

``` python
(value: Any) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L196-L197)

### `def always_true`

``` python
(value: Any) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L200-L201)

### `def always_false`

``` python
(value: Any) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L204-L205)

### `def format_docstring`

``` python
(
    **fmt_kwargs: Any
) -> Callable[[Callable[~FuncParams, ~ReturnType]], Callable[~FuncParams, ~ReturnType]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L208-L220)

Decorator that formats a function’s docstring with the provided keyword
arguments.

- `LambdaArgs = LambdaArgs`

### `def typed_lambda`

``` python
(
    fn: Callable[[Unpack[LambdaArgs]], ~ReturnType],
    in_types: ~LambdaArgsTypes,
    out_type: type[~ReturnType]
) -> Callable[[Unpack[LambdaArgs]], ~ReturnType]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/func.py#L228-L277)

Wraps a lambda function with type hints.

### Parameters:

- `fn : Callable[[Unpack[LambdaArgs]], ReturnType]` The lambda function
  to wrap.
- `in_types : tuple[type, ...]` Tuple of input types.
- `out_type : type[ReturnType]` The output type.

### Returns:

- `Callable[..., ReturnType]` A new function with annotations matching
  the given signature.

### Usage:

``` python
add = typed_lambda(lambda x, y: x + y, (int, int), int)
assert add(1, 2) == 3
```

### Raises:

- `ValueError` if the number of input types doesn’t match the lambda’s
  parameters.

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`stable_hash`](#stable_hash)
- [`stable_json_dumps`](#stable_json_dumps)
- [`base64_hash`](#base64_hash)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/hashing.py)

# `muutils.misc.hashing`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/hashing.py#L0-L37)

### `def stable_hash`

``` python
(s: str | bytes) -> int
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/hashing.py#L8-L18)

Returns a stable hash of the given string. not cryptographically secure,
but stable between runs

### `def stable_json_dumps`

``` python
(d) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/hashing.py#L21-L26)

### `def base64_hash`

``` python
(s: str | bytes) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/hashing.py#L29-L38)

Returns a base64 representation of the hash of the given string. not
cryptographically secure

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`shorten_numerical_to_str`](#shorten_numerical_to_str)
- [`str_to_numeric`](#str_to_numeric)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/numerical.py)

# `muutils.misc.numerical`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/numerical.py#L0-L164)

### `def shorten_numerical_to_str`

``` python
(
    num: int | float,
    small_as_decimal: bool = True,
    precision: int = 1
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/numerical.py#L22-L46)

shorten a large numerical value to a string 1234 -\> 1K

precision guaranteed to 1 in 10, but can be higher. reverse of
`str_to_numeric`

### `def str_to_numeric`

``` python
(
    quantity: str,
    mapping: None | bool | dict[str, int | float] = True
) -> int | float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/numerical.py#L49-L165)

Convert a string representing a quantity to a numeric value.

The string can represent an integer, python float, fraction, or
shortened via `shorten_numerical_to_str`.

### Examples:

    >>> str_to_numeric("5")
    5
    >>> str_to_numeric("0.1")
    0.1
    >>> str_to_numeric("1/5")
    0.2
    >>> str_to_numeric("-1K")
    -1000.0
    >>> str_to_numeric("1.5M")
    1500000.0
    >>> str_to_numeric("1.2e2")
    120.0

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`WhenMissing`](#WhenMissing)
- [`empty_sequence_if_attr_false`](#empty_sequence_if_attr_false)
- [`flatten`](#flatten)
- [`list_split`](#list_split)
- [`list_join`](#list_join)
- [`apply_mapping`](#apply_mapping)
- [`apply_mapping_chain`](#apply_mapping_chain)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py)

# `muutils.misc.sequence`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L0-L233)

- `WhenMissing = typing.Literal['except', 'skip', 'include']`

### `def empty_sequence_if_attr_false`

``` python
(itr: Iterable[Any], attr_owner: Any, attr_name: str) -> Iterable[Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L21-L42)

Returns `itr` if `attr_owner` has the attribute `attr_name` and it
boolean casts to `True`. Returns an empty sequence otherwise.

Particularly useful for optionally inserting delimiters into a sequence
depending on an `TokenizerElement` attribute.

### Parameters:

- `itr: Iterable[Any]` The iterable to return if the attribute is
  `True`.
- `attr_owner: Any` The object to check for the attribute.
- `attr_name: str` The name of the attribute to check.

### Returns:

- `itr: Iterable` if `attr_owner` has the attribute `attr_name` and it
  boolean casts to `True`, otherwise an empty sequence.
- `()` an empty sequence if the attribute is `False` or not present.

### `def flatten`

``` python
(it: Iterable[Any], levels_to_flatten: int | None = None) -> Generator
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L45-L68)

Flattens an arbitrarily nested iterable. Flattens all iterable data
types except for `str` and `bytes`.

### Returns

Generator over the flattened sequence.

### Parameters

- `it`: Any arbitrarily nested iterable.
- `levels_to_flatten`: Number of levels to flatten by, starting at the
  outermost layer. If `None`, performs full flattening.

### `def list_split`

``` python
(lst: list, val: Any) -> list[list]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L75-L103)

split a list into sublists by `val`. similar to “a_b_c”.split(“\_“)

``` python
>>> list_split([1,2,3,0,4,5,0,6], 0)
[[1, 2, 3], [4, 5], [6]]
>>> list_split([0,1,2,3], 0)
[[], [1, 2, 3]]
>>> list_split([1,2,3], 0)
[[1, 2, 3]]
>>> list_split([], 0)
[[]]
```

### `def list_join`

``` python
(lst: list, factory: Callable) -> list
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L106-L128)

add a *new* instance of `factory()` between each element of `lst`

``` python
>>> list_join([1,2,3], lambda : 0)
[1,0,2,0,3]
>>> list_join([1,2,3], lambda: [time.sleep(0.1), time.time()][1])
[1, 1600000000.0, 2, 1600000000.1, 3]
```

### `def apply_mapping`

``` python
(
    mapping: Mapping[~_AM_K, ~_AM_V],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L138-L184)

Given an iterable and a mapping, apply the mapping to the iterable with
certain options

Gotcha: if `when_missing` is invalid, this is totally fine until a
missing key is actually encountered.

Note: you can use this with
`<a href="../kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to
pass a function instead of a dict

### Parameters:

- `mapping : Mapping[_AM_K, _AM_V]` must have `__contains__` and
  `__getitem__`, both of which take `_AM_K` and the latter returns
  `_AM_V`
- `iter : Iterable[_AM_K]` the iterable to apply the mapping to
- `when_missing : WhenMissing` what to do when a key is missing from the
  mapping – this is what distinguishes this function from `map` you can
  choose from `"skip"`, `"include"` (without converting), and `"except"`
  (defaults to `"skip"`)

### Returns:

return type is one of: - `list[_AM_V]` if `when_missing` is `"skip"` or
`"except"` - `list[Union[_AM_K, _AM_V]]` if `when_missing` is
`"include"`

### Raises:

- `KeyError` : if the item is missing from the mapping and
  `when_missing` is `"except"`
- `ValueError` : if `when_missing` is invalid

### `def apply_mapping_chain`

``` python
(
    mapping: Mapping[~_AM_K, Iterable[~_AM_V]],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/sequence.py#L187-L234)

Given an iterable and a mapping, chain the mappings together

Gotcha: if `when_missing` is invalid, this is totally fine until a
missing key is actually encountered.

Note: you can use this with
`<a href="../kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to
pass a function instead of a dict

### Parameters:

- `mapping : Mapping[_AM_K, Iterable[_AM_V]]` must have `__contains__`
  and `__getitem__`, both of which take `_AM_K` and the latter returns
  `Iterable[_AM_V]`
- `iter : Iterable[_AM_K]` the iterable to apply the mapping to
- `when_missing : WhenMissing` what to do when a key is missing from the
  mapping – this is what distinguishes this function from `map` you can
  choose from `"skip"`, `"include"` (without converting), and `"except"`
  (defaults to `"skip"`)

### Returns:

return type is one of: - `list[_AM_V]` if `when_missing` is `"skip"` or
`"except"` - `list[Union[_AM_K, _AM_V]]` if `when_missing` is
`"include"`

### Raises:

- `KeyError` : if the item is missing from the mapping and
  `when_missing` is `"except"`
- `ValueError` : if `when_missing` is invalid

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## API Documentation

- [`sanitize_name`](#sanitize_name)
- [`sanitize_fname`](#sanitize_fname)
- [`sanitize_identifier`](#sanitize_identifier)
- [`dict_to_filename`](#dict_to_filename)
- [`dynamic_docstring`](#dynamic_docstring)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py)

# `muutils.misc.string`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py#L0-L107)

### `def sanitize_name`

``` python
(
    name: str | None,
    additional_allowed_chars: str = '',
    replace_invalid: str = '',
    when_none: str | None = '_None_',
    leading_digit_prefix: str = ''
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py#L7-L55)

sanitize a string, leaving only alphanumerics and
`additional_allowed_chars`

### Parameters:

- `name : str | None` input string
- `additional_allowed_chars : str` additional characters to allow, none
  by default (defaults to `""`)
- `replace_invalid : str` character to replace invalid characters with
  (defaults to `""`)
- `when_none : str | None` string to return if `name` is `None`. if
  `None`, raises an exception (defaults to `"_None_"`)
- `leading_digit_prefix : str` character to prefix the string with if it
  starts with a digit (defaults to `""`)

### Returns:

- `str` sanitized string

### `def sanitize_fname`

``` python
(fname: str | None, **kwargs) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py#L58-L63)

sanitize a filename to posix standards

- leave only alphanumerics, `_` (underscore), ‘-’ (dash) and `.`
  (period)

### `def sanitize_identifier`

``` python
(fname: str | None, **kwargs) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py#L66-L74)

sanitize an identifier (variable or function name)

- leave only alphanumerics and `_` (underscore)
- prefix with `_` if it starts with a digit

### `def dict_to_filename`

``` python
(
    data: dict,
    format_str: str = '{key}_{val}',
    separator: str = '.',
    max_length: int = 255
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py#L77-L99)

### `def dynamic_docstring`

``` python
(**doc_params)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/misc/string.py#L102-L108)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

miscellaneous utilities for ML pipelines

## API Documentation

- [`ARRAY_IMPORTS`](#ARRAY_IMPORTS)
- [`DEFAULT_SEED`](#DEFAULT_SEED)
- [`GLOBAL_SEED`](#GLOBAL_SEED)
- [`get_device`](#get_device)
- [`set_reproducibility`](#set_reproducibility)
- [`chunks`](#chunks)
- [`get_checkpoint_paths_for_run`](#get_checkpoint_paths_for_run)
- [`register_method`](#register_method)
- [`pprint_summary`](#pprint_summary)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py)

# `muutils.mlutils`

miscellaneous utilities for ML pipelines

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L0-L164)

- `ARRAY_IMPORTS: bool = True`

- `DEFAULT_SEED: int = 42`

- `GLOBAL_SEED: int = 42`

### `def get_device`

``` python
(device: Union[str, torch.device, NoneType] = None) -> torch.device
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L30-L74)

Get the torch.device instance on which `torch.Tensor`s should be
allocated.

### `def set_reproducibility`

``` python
(seed: int = 42)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L77-L97)

Improve model reproducibility. See
https://github.com/NVIDIA/framework-determinism for more information.

Deterministic operations tend to have worse performance than
nondeterministic operations, so this method trades off performance for
reproducibility. Set use_deterministic_algorithms to True to improve
performance.

### `def chunks`

``` python
(it, chunk_size)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L100-L105)

Yield successive chunks from an iterator.

### `def get_checkpoint_paths_for_run`

``` python
(
    run_path: pathlib.Path,
    extension: Literal['pt', 'zanj'],
    checkpoints_format: str = 'checkpoints/model.iter_*.{extension}'
) -> list[tuple[int, pathlib.Path]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L108-L127)

get checkpoints of the format from the run_path

note that `checkpoints_format` should contain a glob pattern with: -
unresolved “{extension}” format term for the extension - a wildcard for
the iteration number

### `def register_method`

``` python
(
    method_dict: dict[str, typing.Callable[..., typing.Any]],
    custom_name: Optional[str] = None
) -> Callable[[~F], ~F]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L133-L161)

Decorator to add a method to the method_dict

### `def pprint_summary`

``` python
(summary: dict)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/mlutils.py#L164-L165)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

utilities for working with notebooks

- configuring figures mdoes and torch devices: `configure_notebook`
- converting them to scripts: `convert_ipynb_to_script`
- running them as tests: `run_notebook_tests`
- and working with diagrams/LaTeX: `mermaid`, `print_tex`

## Submodules

- [`configure_notebook`](#configure_notebook)
- [`convert_ipynb_to_script`](#convert_ipynb_to_script)
- [`mermaid`](#mermaid)
- [`print_tex`](#print_tex)
- [`run_notebook_tests`](#run_notebook_tests)

## API Documentation

- [`mm`](#mm)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/__init__.py)

# `muutils.nbutils`

utilities for working with notebooks

- configuring figures mdoes and torch devices: `configure_notebook`
- converting them to scripts: `convert_ipynb_to_script`
- running them as tests: `run_notebook_tests`
- and working with diagrams/LaTeX: `mermaid`, `print_tex`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/__init__.py#L0-L20)

### `def mm`

``` python
(graph)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/__init__.py#L15-L20)

for plotting mermaid.js diagrams

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

shared utilities for setting up a notebook

## API Documentation

- [`PlotlyNotInstalledWarning`](#PlotlyNotInstalledWarning)
- [`PLOTLY_IMPORTED`](#PLOTLY_IMPORTED)
- [`PlottingMode`](#PlottingMode)
- [`PLOT_MODE`](#PLOT_MODE)
- [`CONVERSION_PLOTMODE_OVERRIDE`](#CONVERSION_PLOTMODE_OVERRIDE)
- [`FIG_COUNTER`](#FIG_COUNTER)
- [`FIG_OUTPUT_FMT`](#FIG_OUTPUT_FMT)
- [`FIG_NUMBERED_FNAME`](#FIG_NUMBERED_FNAME)
- [`FIG_CONFIG`](#FIG_CONFIG)
- [`FIG_BASEPATH`](#FIG_BASEPATH)
- [`CLOSE_AFTER_PLOTSHOW`](#CLOSE_AFTER_PLOTSHOW)
- [`MATPLOTLIB_FORMATS`](#MATPLOTLIB_FORMATS)
- [`TIKZPLOTLIB_FORMATS`](#TIKZPLOTLIB_FORMATS)
- [`UnknownFigureFormatWarning`](#UnknownFigureFormatWarning)
- [`universal_savefig`](#universal_savefig)
- [`setup_plots`](#setup_plots)
- [`configure_notebook`](#configure_notebook)
- [`plotshow`](#plotshow)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py)

# `muutils.nbutils.configure_notebook`

shared utilities for setting up a notebook

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L0-L319)

### `class PlotlyNotInstalledWarning(builtins.UserWarning):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L12-L13)

Base class for warnings generated by user code.

### Inherited Members

- [`UserWarning`](#PlotlyNotInstalledWarning.__init__)

- [`with_traceback`](#PlotlyNotInstalledWarning.with_traceback)

- [`add_note`](#PlotlyNotInstalledWarning.add_note)

- [`args`](#PlotlyNotInstalledWarning.args)

- `PLOTLY_IMPORTED: bool = True`

- `PlottingMode = typing.Literal['ignore', 'inline', 'widget', 'save']`

- `PLOT_MODE: Literal['ignore', 'inline', 'widget', 'save'] = 'inline'`

- `CONVERSION_PLOTMODE_OVERRIDE: Optional[Literal['ignore', 'inline', 'widget', 'save']] = None`

- `FIG_COUNTER: int = 0`

- `FIG_OUTPUT_FMT: str | None = None`

- `FIG_NUMBERED_FNAME: str = 'figure-{num}'`

- `FIG_CONFIG: dict | None = None`

- `FIG_BASEPATH: str | None = None`

- `CLOSE_AFTER_PLOTSHOW: bool = False`

- `MATPLOTLIB_FORMATS = ['pdf', 'png', 'jpg', 'jpeg', 'svg', 'eps', 'ps', 'tif', 'tiff']`

- `TIKZPLOTLIB_FORMATS = ['tex', 'tikz']`

### `class UnknownFigureFormatWarning(builtins.UserWarning):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L55-L56)

Base class for warnings generated by user code.

### Inherited Members

- [`UserWarning`](#UnknownFigureFormatWarning.__init__)

- [`with_traceback`](#UnknownFigureFormatWarning.with_traceback)

- [`add_note`](#UnknownFigureFormatWarning.add_note)

- [`args`](#UnknownFigureFormatWarning.args)

### `def universal_savefig`

``` python
(fname: str, fmt: str | None = None) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L59-L83)

### `def setup_plots`

``` python
(
    plot_mode: Literal['ignore', 'inline', 'widget', 'save'] = 'inline',
    fig_output_fmt: str | None = 'pdf',
    fig_numbered_fname: str = 'figure-{num}',
    fig_config: dict | None = None,
    fig_basepath: str | None = None,
    close_after_plotshow: bool = False
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L86-L189)

Set up plot saving/rendering options

### `def configure_notebook`

``` python
(
    *args,
    seed: int = 42,
    device: Any = None,
    dark_mode: bool = True,
    plot_mode: Literal['ignore', 'inline', 'widget', 'save'] = 'inline',
    fig_output_fmt: str | None = 'pdf',
    fig_numbered_fname: str = 'figure-{num}',
    fig_config: dict | None = None,
    fig_basepath: str | None = None,
    close_after_plotshow: bool = False
) -> torch.device | None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L192-L284)

Shared Jupyter notebook setup steps

- Set random seeds and library reproducibility settings
- Set device based on availability
- Set module reloading before code execution
- Set plot formatting
- Set plot saving/rendering options

### Parameters:

- `seed : int` random seed across libraries including torch, numpy, and
  random (defaults to `42`) (defaults to `42`)
- `device : typing.Any` pytorch device to use (defaults to `None`)
- `dark_mode : bool` figures in dark mode (defaults to `True`)
- `plot_mode : PlottingMode` how to display plots, one of `PlottingMode`
  or `["ignore", "inline", "widget", "save"]` (defaults to `"inline"`)
- `fig_output_fmt : str | None` format for saving figures (defaults to
  `"pdf"`)
- `fig_numbered_fname : str` format for saving figures with numbers (if
  they aren’t named) (defaults to `"figure-{num}"`)
- `fig_config : dict | None` metadata to save with the figures (defaults
  to `None`)
- `fig_basepath : str | None` base path for saving figures (defaults to
  `None`)
- `close_after_plotshow : bool` close figures after showing them
  (defaults to `False`)

### Returns:

- `torch.device|None` the device set, if torch is installed

### `def plotshow`

``` python
(
    fname: str | None = None,
    plot_mode: Optional[Literal['ignore', 'inline', 'widget', 'save']] = None,
    fmt: str | None = None
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/configure_notebook.py#L287-L320)

Show the active plot, depending on global configs

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

fast conversion of Jupyter Notebooks to scripts, with some basic and
hacky filtering and formatting.

## API Documentation

- [`DISABLE_PLOTS`](#DISABLE_PLOTS)
- [`DISABLE_PLOTS_WARNING`](#DISABLE_PLOTS_WARNING)
- [`disable_plots_in_script`](#disable_plots_in_script)
- [`convert_ipynb`](#convert_ipynb)
- [`process_file`](#process_file)
- [`process_dir`](#process_dir)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/convert_ipynb_to_script.py)

# `muutils.nbutils.convert_ipynb_to_script`

fast conversion of Jupyter Notebooks to scripts, with some basic and
hacky filtering and formatting.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/convert_ipynb_to_script.py#L0-L373)

- `DISABLE_PLOTS: dict[str, list[str]] = {'matplotlib': ['\n# ------------------------------------------------------------\n# Disable matplotlib plots, done during processing by`convert_ipynb_to_script.py`\nimport matplotlib.pyplot as plt\nplt.show = lambda: None\n# ------------------------------------------------------------\n'], 'circuitsvis': ['\n# ------------------------------------------------------------\n# Disable circuitsvis plots, done during processing by`convert_ipynb_to_script.py`\nfrom circuitsvis.utils.convert_props import PythonProperty, convert_props\nfrom circuitsvis.utils.render import RenderedHTML, render, render_cdn, render_local\n\ndef new_render(\n    react_element_name: str,\n    **kwargs: PythonProperty\n) -> RenderedHTML:\n    "return a visualization as raw HTML"\n    local_src = render_local(react_element_name, **kwargs)\n    cdn_src = render_cdn(react_element_name, **kwargs)\n    # return as string instead of RenderedHTML for CI\n    return str(RenderedHTML(local_src, cdn_src))\n\nrender = new_render\n# ------------------------------------------------------------\n'], 'muutils': ['import muutils.nbutils.configure_notebook as nb_conf\nnb_conf.CONVERSION_PLOTMODE_OVERRIDE = "ignore"\n']}`

- `DISABLE_PLOTS_WARNING: list[str] = ["# ------------------------------------------------------------\n# WARNING: this script is auto-generated by`convert_ipynb_to_script.py`\n# showing plots has been disabled, so this is presumably in a temp dict for CI or something\n# so don't modify this code, it will be overwritten!\n# ------------------------------------------------------------\n"]`

### `def disable_plots_in_script`

``` python
(script_lines: list[str]) -> list[str]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/convert_ipynb_to_script.py#L64-L148)

Disable plots in a script by adding cursed things after the import
statements

### `def convert_ipynb`

``` python
(
    notebook: dict,
    strip_md_cells: bool = False,
    header_comment: str = '#%%',
    disable_plots: bool = False,
    filter_out_lines: Union[str, Sequence[str]] = ('%', '!')
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/convert_ipynb_to_script.py#L151-L208)

Convert Jupyter Notebook to a script, doing some basic filtering and
formatting.

### Arguments

    - `notebook: dict`: Jupyter Notebook loaded as json.
    - `strip_md_cells: bool = False`: Remove markdown cells from the output script.
    - `header_comment: str = r'#%%'`: Comment string to separate cells in the output script.
    - `disable_plots: bool = False`: Disable plots in the output script.
    - `filter_out_lines: str|typing.Sequence[str] = ('%', '!')`: comment out lines starting with these strings (in code blocks).
        if a string is passed, it will be split by char and each char will be treated as a separate filter.

### Returns

    - `str`: Converted script.

### `def process_file`

``` python
(
    in_file: str,
    out_file: str | None = None,
    strip_md_cells: bool = False,
    header_comment: str = '#%%',
    disable_plots: bool = False,
    filter_out_lines: Union[str, Sequence[str]] = ('%', '!')
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/convert_ipynb_to_script.py#L211-L243)

### `def process_dir`

``` python
(
    input_dir: Union[str, pathlib.Path],
    output_dir: Union[str, pathlib.Path],
    strip_md_cells: bool = False,
    header_comment: str = '#%%',
    disable_plots: bool = False,
    filter_out_lines: Union[str, Sequence[str]] = ('%', '!')
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/convert_ipynb_to_script.py#L246-L307)

Convert all Jupyter Notebooks in a directory to scripts.

### Arguments

    - `input_dir: str`: Input directory.
    - `output_dir: str`: Output directory.
    - `strip_md_cells: bool = False`: Remove markdown cells from the output script.
    - `header_comment: str = r'#%%'`: Comment string to separate cells in the output script.
    - `disable_plots: bool = False`: Disable plots in the output script.
    - `filter_out_lines: str|typing.Sequence[str] = ('%', '!')`: comment out lines starting with these strings (in code blocks).
        if a string is passed, it will be split by char and each char will be treated as a separate filter.

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

display mermaid.js diagrams in jupyter notebooks by the
`mermaid.ink/img` service

## API Documentation

- [`mm`](#mm)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/mermaid.py)

# `muutils.nbutils.mermaid`

display mermaid.js diagrams in jupyter notebooks by the
`mermaid.ink/img` service

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/mermaid.py#L0-L19)

### `def mm`

``` python
(graph)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/mermaid.py#L15-L20)

for plotting mermaid.js diagrams

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

quickly print a sympy expression in latex

## API Documentation

- [`print_tex`](#print_tex)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/print_tex.py)

# `muutils.nbutils.print_tex`

quickly print a sympy expression in latex

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/print_tex.py#L0-L20)

### `def print_tex`

``` python
(
    expr: sympy.core.expr.Expr,
    name: str | None = None,
    plain: bool = False,
    rendered: bool = True
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/print_tex.py#L7-L21)

function for easily rendering a sympy expression in latex

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

turn a folder of notebooks into scripts, run them, and make sure they
work.

made to be called as

``` bash
python -m muutils.nbutils.run_notebook_tests --notebooks-dir <notebooks_dir> --converted-notebooks-temp-dir <converted_notebooks_temp_dir>
```

## API Documentation

- [`NotebookTestError`](#NotebookTestError)
- [`SUCCESS_STR`](#SUCCESS_STR)
- [`FAILURE_STR`](#FAILURE_STR)
- [`run_notebook_tests`](#run_notebook_tests)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/run_notebook_tests.py)

# `muutils.nbutils.run_notebook_tests`

turn a folder of notebooks into scripts, run them, and make sure they
work.

made to be called as

``` bash
python -m <a href="">muutils.nbutils.run_notebook_tests</a> --notebooks-dir <notebooks_dir> --converted-notebooks-temp-dir <converted_notebooks_temp_dir>
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/run_notebook_tests.py#L0-L254)

### `class NotebookTestError(builtins.Exception):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/run_notebook_tests.py#L21-L22)

Common base class for all non-exit exceptions.

### Inherited Members

- [`Exception`](#NotebookTestError.__init__)

- [`with_traceback`](#NotebookTestError.with_traceback)

- [`add_note`](#NotebookTestError.add_note)

- [`args`](#NotebookTestError.args)

- `SUCCESS_STR: str = '✅'`

- `FAILURE_STR: str = '❌'`

### `def run_notebook_tests`

``` python
(
    notebooks_dir: pathlib.Path,
    converted_notebooks_temp_dir: pathlib.Path,
    CI_output_suffix: str = '.CI-output.txt',
    run_python_cmd: Optional[str] = None,
    run_python_cmd_fmt: str = '{python_tool} run python',
    python_tool: str = 'poetry',
    exit_on_first_fail: bool = False
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/nbutils/run_notebook_tests.py#L29-L217)

Run converted Jupyter notebooks as Python scripts and verify they
execute successfully.

Takes a directory of notebooks and their corresponding converted Python
scripts, executes each script, and captures the output. Failures are
collected and reported, with optional early exit on first failure.

### Parameters:

- `notebooks_dir : Path` Directory containing the original .ipynb
  notebook files
- `converted_notebooks_temp_dir : Path` Directory containing the
  corresponding converted .py files
- `CI_output_suffix : str` Suffix to append to output files capturing
  execution results (defaults to `".CI-output.txt"`)
- `run_python_cmd : str | None` Custom command to run Python scripts.
  Overrides python_tool and run_python_cmd_fmt if provided (defaults to
  `None`)
- `run_python_cmd_fmt : str` Format string for constructing the Python
  run command (defaults to `"{python_tool} run python"`)
- `python_tool : str` Tool used to run Python (e.g. poetry, uv)
  (defaults to `"poetry"`)
- `exit_on_first_fail : bool` Whether to raise exception immediately on
  first notebook failure (defaults to `False`)

### Returns:

- `None`

### Modifies:

- Working directory: Temporarily changes to notebooks_dir during
  execution
- Filesystem: Creates output files with CI_output_suffix for each
  notebook

### Raises:

- `NotebookTestError`: If any notebooks fail to execute, or if input
  directories are invalid
- `TypeError`: If run_python_cmd is provided but not a string

### Usage:

``` python
>>> run_notebook_tests(
...     notebooks_dir=Path("notebooks"),
...     converted_notebooks_temp_dir=Path("temp/converted"),
...     python_tool="poetry"
... )
### testing notebooks in 'notebooks'
### reading converted notebooks from 'temp/converted'
Running 1/2: temp/converted/notebook1.py
    Output in temp/converted/notebook1.CI-output.txt
    {SUCCESS_STR} Run completed with return code 0
```

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

parallel processing utilities, chiefly `run_maybe_parallel`

## API Documentation

- [`ProgressBarFunction`](#ProgressBarFunction)
- [`ProgressBarOption`](#ProgressBarOption)
- [`DEFAULT_PBAR_FN`](#DEFAULT_PBAR_FN)
- [`spinner_fn_wrap`](#spinner_fn_wrap)
- [`map_kwargs_for_tqdm`](#map_kwargs_for_tqdm)
- [`no_progress_fn_wrap`](#no_progress_fn_wrap)
- [`set_up_progress_bar_fn`](#set_up_progress_bar_fn)
- [`run_maybe_parallel`](#run_maybe_parallel)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py)

# `muutils.parallel`

parallel processing utilities, chiefly `run_maybe_parallel`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L0-L278)

### `class ProgressBarFunction(typing.Protocol):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L31-L34)

a protocol for a progress bar function

### `ProgressBarFunction`

``` python
(*args, **kwargs)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L1766-L1792)

- `ProgressBarOption = typing.Literal['tqdm', 'spinner', 'none', None]`

- `DEFAULT_PBAR_FN: Literal['tqdm', 'spinner', 'none', None] = 'tqdm'`

### `def spinner_fn_wrap`

``` python
(x: Iterable, **kwargs) -> List
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L55-L72)

spinner wrapper

### `def map_kwargs_for_tqdm`

``` python
(kwargs: dict) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L75-L86)

map kwargs for tqdm, cant wrap because the pbar dissapears?

### `def no_progress_fn_wrap`

``` python
(x: Iterable, **kwargs) -> Iterable
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L89-L91)

fallback to no progress bar

### `def set_up_progress_bar_fn`

``` python
(
    pbar: Union[muutils.parallel.ProgressBarFunction, Literal['tqdm', 'spinner', 'none', None]],
    pbar_kwargs: Optional[Dict[str, Any]] = None,
    **extra_kwargs
) -> Tuple[muutils.parallel.ProgressBarFunction, dict]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L94-L142)

set up the progress bar function and its kwargs

### Parameters:

- `pbar : Union[ProgressBarFunction, ProgressBarOption]` progress bar
  function or option. if a function, we return as-is. if a string, we
  figure out which progress bar to use
- `pbar_kwargs : Optional[Dict[str, Any]]` kwargs passed to the progress
  bar function (default to `None`) (defaults to `None`)

### Returns:

- `Tuple[ProgressBarFunction, dict]` a tuple of the progress bar
  function and its kwargs

### Raises:

- `ValueError` : if `pbar` is not one of the valid options

### `def run_maybe_parallel`

``` python
(
    func: Callable[[~InputType], ~OutputType],
    iterable: Iterable[~InputType],
    parallel: Union[bool, int],
    pbar_kwargs: Optional[Dict[str, Any]] = None,
    chunksize: Optional[int] = None,
    keep_ordered: bool = True,
    use_multiprocess: bool = False,
    pbar: Union[muutils.parallel.ProgressBarFunction, Literal['tqdm', 'spinner', 'none', None]] = 'tqdm'
) -> List[~OutputType]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/parallel.py#L146-L279)

a function to make it easier to sometimes parallelize an operation

- if `parallel` is `False`, then the function will run in serial,
  running `map(func, iterable)`
- if `parallel` is `True`, then the function will run in parallel,
  running in parallel with the maximum number of processes
- if `parallel` is an `int`, it must be greater than 1, and the function
  will run in parallel with the number of processes specified by
  `parallel`

the maximum number of processes is given by the
`min(len(iterable), multiprocessing.cpu_count())`

### Parameters:

- `func : Callable[[InputType], OutputType]` function passed to either
  `map` or `Pool.imap`
- `iterable : Iterable[InputType]` iterable passed to either `map` or
  `Pool.imap`
- `parallel : bool | int` whether to run in parallel, and how many
  processes to use
- `pbar_kwargs : Dict[str, Any]` kwargs passed to the progress bar
  function

### Returns:

- `List[OutputType]` a list of the output of `func` for each element in
  `iterable`

### Raises:

- `ValueError` : if `parallel` is not a boolean or an integer greater
  than 1
- `ValueError` : if `use_multiprocess=True` and `parallel=False`
- `ImportError` : if `use_multiprocess=True` and `multiprocess` is not
  available

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

decorator `spinner_decorator` and context manager `SpinnerContext` to
display a spinner

using the base `Spinner` class while some code is running.

## API Documentation

- [`DecoratedFunction`](#DecoratedFunction)
- [`SpinnerConfig`](#SpinnerConfig)
- [`SpinnerConfigArg`](#SpinnerConfigArg)
- [`SPINNERS`](#SPINNERS)
- [`Spinner`](#Spinner)
- [`NoOpContextManager`](#NoOpContextManager)
- [`SpinnerContext`](#SpinnerContext)
- [`spinner_decorator`](#spinner_decorator)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py)

# `muutils.spinner`

decorator `spinner_decorator` and context manager `SpinnerContext` to
display a spinner

using the base `Spinner` class while some code is running.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L0-L510)

- `DecoratedFunction = ~DecoratedFunction`

Define a generic type for the decorated function

### `class SpinnerConfig:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L31-L80)

### `SpinnerConfig`

``` python
(working: List[str] = <factory>, success: str = '✔️', fail: str = '❌')
```

- `working: List[str]`

- `success: str = '✔️'`

- `fail: str = '❌'`

### `def is_ascii`

``` python
(self) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L37-L39)

whether all characters are ascii

### `def eq_lens`

``` python
(self) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L41-L49)

whether all working characters are the same length

### `def is_valid`

``` python
(self) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L51-L61)

whether the spinner config is valid

### `def from_any`

``` python
(
    cls,
    arg: Union[str, List[str], muutils.spinner.SpinnerConfig, dict]
) -> muutils.spinner.SpinnerConfig
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L67-L80)

- `SpinnerConfigArg = typing.Union[str, typing.List[str], muutils.spinner.SpinnerConfig, dict]`

- `SPINNERS: Dict[str, muutils.spinner.SpinnerConfig] = {'default': SpinnerConfig(working=['|', '/', '-', '\\'], success='#', fail='X'), 'dots': SpinnerConfig(working=['.  ', '.. ', '...'], success='***', fail='xxx'), 'bars': SpinnerConfig(working=['|  ', '|| ', '|||'], success='|||', fail='///'), 'arrows': SpinnerConfig(working=['<', '^', '>', 'v'], success='►', fail='✖'), 'arrows_2': SpinnerConfig(working=['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'], success='→', fail='↯'), 'bouncing_bar': SpinnerConfig(working=['[    ]', '[=   ]', '[==  ]', '[=== ]', '[ ===]', '[  ==]', '[   =]'], success='[====]', fail='[XXXX]'), 'bar': SpinnerConfig(working=['[  ]', '[- ]', '[--]', '[ -]'], success='[==]', fail='[xx]'), 'bouncing_ball': SpinnerConfig(working=['( ●    )', '(  ●   )', '(   ●  )', '(    ● )', '(     ●)', '(    ● )', '(   ●  )', '(  ●   )', '( ●    )', '(●     )'], success='(●●●●●●)', fail='(  ✖  )'), 'ooo': SpinnerConfig(working=['.', 'o', 'O', 'o'], success='O', fail='x'), 'braille': SpinnerConfig(working=['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'], success='⣿', fail='X'), 'clock': SpinnerConfig(working=['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚'], success='✔️', fail='❌'), 'hourglass': SpinnerConfig(working=['⏳', '⌛'], success='✔️', fail='❌'), 'square_corners': SpinnerConfig(working=['◰', '◳', '◲', '◱'], success='◼', fail='✖'), 'triangle': SpinnerConfig(working=['◢', '◣', '◤', '◥'], success='◆', fail='✖'), 'square_dot': SpinnerConfig(working=['⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽', '⣾'], success='⣿', fail='❌'), 'box_bounce': SpinnerConfig(working=['▌', '▀', '▐', '▄'], success='■', fail='✖'), 'hamburger': SpinnerConfig(working=['☱', '☲', '☴'], success='☰', fail='✖'), 'earth': SpinnerConfig(working=['🌍', '🌎', '🌏'], success='✔️', fail='❌'), 'growing_dots': SpinnerConfig(working=['⣀', '⣄', '⣤', '⣦', '⣶', '⣷', '⣿'], success='⣿', fail='✖'), 'dice': SpinnerConfig(working=['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'], success='🎲', fail='✖'), 'wifi': SpinnerConfig(working=['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'], success='✔️', fail='❌'), 'bounce': SpinnerConfig(working=['⠁', '⠂', '⠄', '⠂'], success='⠿', fail='⢿'), 'arc': SpinnerConfig(working=['◜', '◠', '◝', '◞', '◡', '◟'], success='○', fail='✖'), 'toggle': SpinnerConfig(working=['⊶', '⊷'], success='⊷', fail='⊗'), 'toggle2': SpinnerConfig(working=['▫', '▪'], success='▪', fail='✖'), 'toggle3': SpinnerConfig(working=['□', '■'], success='■', fail='✖'), 'toggle4': SpinnerConfig(working=['■', '□', '▪', '▫'], success='■', fail='✖'), 'toggle5': SpinnerConfig(working=['▮', '▯'], success='▮', fail='✖'), 'toggle7': SpinnerConfig(working=['⦾', '⦿'], success='⦿', fail='✖'), 'toggle8': SpinnerConfig(working=['◍', '◌'], success='◍', fail='✖'), 'toggle9': SpinnerConfig(working=['◉', '◎'], success='◉', fail='✖'), 'arrow2': SpinnerConfig(working=['⬆️ ', '↗️ ', '➡️ ', '↘️ ', '⬇️ ', '↙️ ', '⬅️ ', '↖️ '], success='➡️', fail='❌'), 'point': SpinnerConfig(working=['∙∙∙', '●∙∙', '∙●∙', '∙∙●', '∙∙∙'], success='●●●', fail='xxx'), 'layer': SpinnerConfig(working=['-', '=', '≡'], success='≡', fail='✖'), 'speaker': SpinnerConfig(working=['🔈 ', '🔉 ', '🔊 ', '🔉 '], success='🔊', fail='🔇'), 'orangePulse': SpinnerConfig(working=['🔸 ', '🔶 ', '🟠 ', '🟠 ', '🔷 '], success='🟠', fail='❌'), 'bluePulse': SpinnerConfig(working=['🔹 ', '🔷 ', '🔵 ', '🔵 ', '🔷 '], success='🔵', fail='❌'), 'satellite_signal': SpinnerConfig(working=['📡   ', '📡·  ', '📡·· ', '📡···', '📡 ··', '📡  ·'], success='📡 ✔️ ', fail='📡 ❌ '), 'rocket_orbit': SpinnerConfig(working=['🌍🚀  ', '🌏 🚀 ', '🌎  🚀'], success='🌍  ✨', fail='🌍  💥'), 'ogham': SpinnerConfig(working=['ᚁ ', 'ᚂ ', 'ᚃ ', 'ᚄ', 'ᚅ'], success='᚛᚜', fail='✖'), 'eth': SpinnerConfig(working=['᛫', '፡', '፥', '፤', '፧', '።', '፨'], success='፠', fail='✖')}`

### `class Spinner:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L201-L410)

displays a spinner, and optionally elapsed time and a mutable value
while a function is running.

### Parameters:

- `update_interval : float` how often to update the spinner display in
  seconds (defaults to `0.1`)
- `initial_value : str` initial value to display with the spinner
  (defaults to `""`)
- `message : str` message to display with the spinner (defaults to `""`)
- `format_string : str` string to format the spinner with. must have
  `"\r"` prepended to clear the line. allowed keys are `spinner`,
  `elapsed_time`, `message`, and `value` (defaults to
  `"\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
- `output_stream : TextIO` stream to write the spinner to (defaults to
  `sys.stdout`)
- `format_string_when_updated : Union[bool,str]` whether to use a
  different format string when the value is updated. if `True`, use the
  default format string with a newline appended. if a string, use that
  string. this is useful if you want update_value to print to console
  and be preserved. (defaults to `False`)

### Deprecated Parameters:

- `spinner_chars : Union[str, Sequence[str]]` sequence of strings, or
  key to look up in `SPINNER_CHARS`, to use as the spinner characters
  (defaults to `"default"`)
- `spinner_complete : str` string to display when the spinner is
  complete (defaults to looking up `spinner_chars` in `SPINNER_COMPLETE`
  or `"#"`)

### Methods:

- `update_value(value: Any) -> None` update the current value displayed
  by the spinner

### Usage:

#### As a context manager:

``` python
with SpinnerContext() as sp:
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
```

#### As a decorator:

``` python
@spinner_decorator
def long_running_function():
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
    return "Function completed"
```

### `Spinner`

``` python
(
    *args,
    config: Union[str, List[str], muutils.spinner.SpinnerConfig, dict] = 'default',
    update_interval: float = 0.1,
    initial_value: str = '',
    message: str = '',
    format_string: str = '\r{spinner} ({elapsed_time:.2f}s) {message}{value}',
    output_stream: <class 'TextIO'> = <_io.StringIO object>,
    format_string_when_updated: Union[str, bool] = False,
    spinner_chars: Union[str, Sequence[str], NoneType] = None,
    spinner_complete: Optional[str] = None,
    **kwargs: Any
)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L262-L350)

- `config: muutils.spinner.SpinnerConfig`

- `format_string_when_updated: Optional[str]`

format string to use when the value is updated

- `update_interval: float`

- `message: str`

- `current_value: Any`

- `format_string: str`

- `output_stream: <class 'TextIO'>`

- `start_time: float`

for measuring elapsed time

- `stop_spinner: threading.Event`

to stop the spinner

- `spinner_thread: Optional[threading.Thread]`

the thread running the spinner

- `value_changed: bool`

whether the value has been updated since the last display

- `term_width: int`

width of the terminal, for padding with spaces

- `state: Literal['initialized', 'running', 'success', 'fail']`

### `def spin`

``` python
(self) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L352-L380)

Function to run in a separate thread, displaying the spinner and
optional information

### `def update_value`

``` python
(self, value: Any) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L382-L385)

Update the current value displayed by the spinner

### `def start`

``` python
(self) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L387-L392)

Start the spinner

### `def stop`

``` python
(self, failed: bool = False) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L394-L410)

Stop the spinner

### `class NoOpContextManager(typing.ContextManager):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L413-L423)

A context manager that does nothing.

### `NoOpContextManager`

``` python
(*args, **kwargs)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L416-L417)

### `class SpinnerContext(Spinner, typing.ContextManager):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L426-L434)

displays a spinner, and optionally elapsed time and a mutable value
while a function is running.

### Parameters:

- `update_interval : float` how often to update the spinner display in
  seconds (defaults to `0.1`)
- `initial_value : str` initial value to display with the spinner
  (defaults to `""`)
- `message : str` message to display with the spinner (defaults to `""`)
- `format_string : str` string to format the spinner with. must have
  `"\r"` prepended to clear the line. allowed keys are `spinner`,
  `elapsed_time`, `message`, and `value` (defaults to
  `"\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
- `output_stream : TextIO` stream to write the spinner to (defaults to
  `sys.stdout`)
- `format_string_when_updated : Union[bool,str]` whether to use a
  different format string when the value is updated. if `True`, use the
  default format string with a newline appended. if a string, use that
  string. this is useful if you want update_value to print to console
  and be preserved. (defaults to `False`)

### Deprecated Parameters:

- `spinner_chars : Union[str, Sequence[str]]` sequence of strings, or
  key to look up in `SPINNER_CHARS`, to use as the spinner characters
  (defaults to `"default"`)
- `spinner_complete : str` string to display when the spinner is
  complete (defaults to looking up `spinner_chars` in `SPINNER_COMPLETE`
  or `"#"`)

### Methods:

- `update_value(value: Any) -> None` update the current value displayed
  by the spinner

### Usage:

#### As a context manager:

``` python
with SpinnerContext() as sp:
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
```

#### As a decorator:

``` python
@spinner_decorator
def long_running_function():
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
    return "Function completed"
```

### Inherited Members

- [`Spinner`](#SpinnerContext.__init__)
- [`config`](#SpinnerContext.config)
- [`format_string_when_updated`](#SpinnerContext.format_string_when_updated)
- [`update_interval`](#SpinnerContext.update_interval)
- [`message`](#SpinnerContext.message)
- [`current_value`](#SpinnerContext.current_value)
- [`format_string`](#SpinnerContext.format_string)
- [`output_stream`](#SpinnerContext.output_stream)
- [`start_time`](#SpinnerContext.start_time)
- [`stop_spinner`](#SpinnerContext.stop_spinner)
- [`spinner_thread`](#SpinnerContext.spinner_thread)
- [`value_changed`](#SpinnerContext.value_changed)
- [`term_width`](#SpinnerContext.term_width)
- [`state`](#SpinnerContext.state)
- [`spin`](#SpinnerContext.spin)
- [`update_value`](#SpinnerContext.update_value)
- [`start`](#SpinnerContext.start)
- [`stop`](#SpinnerContext.stop)

### `def spinner_decorator`

``` python
(
    *args,
    config: Union[str, List[str], muutils.spinner.SpinnerConfig, dict] = 'default',
    update_interval: float = 0.1,
    initial_value: str = '',
    message: str = '',
    format_string: str = '{spinner} ({elapsed_time:.2f}s) {message}{value}',
    output_stream: <class 'TextIO'> = <_io.StringIO object>,
    mutable_kwarg_key: Optional[str] = None,
    spinner_chars: Union[str, Sequence[str], NoneType] = None,
    spinner_complete: Optional[str] = None,
    **kwargs
) -> Callable[[~DecoratedFunction], ~DecoratedFunction]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/spinner.py#L441-L508)

displays a spinner, and optionally elapsed time and a mutable value
while a function is running.

### Parameters:

- `update_interval : float` how often to update the spinner display in
  seconds (defaults to `0.1`)
- `initial_value : str` initial value to display with the spinner
  (defaults to `""`)
- `message : str` message to display with the spinner (defaults to `""`)
- `format_string : str` string to format the spinner with. must have
  `"\r"` prepended to clear the line. allowed keys are `spinner`,
  `elapsed_time`, `message`, and `value` (defaults to
  `"\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
- `output_stream : TextIO` stream to write the spinner to (defaults to
  `sys.stdout`)
- `format_string_when_updated : Union[bool,str]` whether to use a
  different format string when the value is updated. if `True`, use the
  default format string with a newline appended. if a string, use that
  string. this is useful if you want update_value to print to console
  and be preserved. (defaults to `False`)

### Deprecated Parameters:

- `spinner_chars : Union[str, Sequence[str]]` sequence of strings, or
  key to look up in `SPINNER_CHARS`, to use as the spinner characters
  (defaults to `"default"`)
- `spinner_complete : str` string to display when the spinner is
  complete (defaults to looking up `spinner_chars` in `SPINNER_COMPLETE`
  or `"#"`)

### Methods:

- `update_value(value: Any) -> None` update the current value displayed
  by the spinner

### Usage:

#### As a context manager:

``` python
with SpinnerContext() as sp:
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
```

#### As a decorator:

``` python
@spinner_decorator
def long_running_function():
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
    return "Function completed"
```

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

`StatCounter` class for counting and calculating statistics on numbers

cleaner and more efficient than just using a `Counter` or array

## API Documentation

- [`NumericSequence`](#NumericSequence)
- [`universal_flatten`](#universal_flatten)
- [`StatCounter`](#StatCounter)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py)

# `muutils.statcounter`

`StatCounter` class for counting and calculating statistics on numbers

cleaner and more efficient than just using a `Counter` or array

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L0-L230)

- `NumericSequence = typing.Sequence[typing.Union[float, int, ForwardRef('NumericSequence')]]`

### `def universal_flatten`

``` python
(
    arr: Union[Sequence[Union[float, int, Sequence[Union[float, int, ForwardRef('NumericSequence')]]]], float, int],
    require_rectangular: bool = True
) -> Sequence[Union[float, int, ForwardRef('NumericSequence')]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L24-L41)

flattens any iterable

### `class StatCounter(collections.Counter):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L48-L231)

`Counter`, but with some stat calculation methods which assume the keys
are numerical

works best when the keys are `int`s

### `def validate`

``` python
(self) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L54-L56)

validate the counter as being all floats or ints

### `def min`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L58-L60)

minimum value

### `def max`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L62-L64)

maximum value

### `def total`

``` python
(self)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L66-L68)

Sum of the counts

- `keys_sorted: list`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L70-L73)

return the keys

### `def percentile`

``` python
(self, p: float)
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L75-L122)

return the value at the given percentile

this could be log time if we did binary search, but that would be a lot
of added complexity

### `def median`

``` python
(self) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L124-L125)

### `def mean`

``` python
(self) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L127-L129)

return the mean of the values

### `def mode`

``` python
(self) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L131-L132)

### `def std`

``` python
(self) -> float
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L134-L139)

return the standard deviation of the values

### `def summary`

``` python
(
    self,
    typecast: Callable = <function StatCounter.<lambda>>,
    *,
    extra_percentiles: Optional[list[float]] = None
) -> dict[str, typing.Union[float, int]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L141-L179)

return a summary of the stats, without the raw data. human readable and
small

### `def serialize`

``` python
(
    self,
    typecast: Callable = <function StatCounter.<lambda>>,
    *,
    extra_percentiles: Optional[list[float]] = None
) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L181-L205)

return a json-serializable version of the counter

includes both the output of `summary` and the raw data:

``` json
{
    "StatCounter": { <keys, values from raw data> },
    "summary": self.summary(typecast, extra_percentiles=extra_percentiles),
}


### `def load` { #StatCounter.load }
```python
(cls, data: dict) -> muutils.statcounter.StatCounter
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L214-L222)

load from a the output of
`<a href="#StatCounter.serialize">StatCounter.serialize</a>`

### `def from_list_arrays`

``` python
(
    cls,
    arr,
    map_func: Callable = <class 'float'>
) -> muutils.statcounter.StatCounter
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/statcounter.py#L224-L231)

calls `map_func` on each element of `universal_flatten(arr)`

### Inherited Members

- [`Counter`](#StatCounter.__init__)

- [`most_common`](#StatCounter.most_common)

- [`elements`](#StatCounter.elements)

- [`fromkeys`](#StatCounter.fromkeys)

- [`update`](#StatCounter.update)

- [`subtract`](#StatCounter.subtract)

- [`copy`](#StatCounter.copy)

- [`get`](#StatCounter.get)

- [`setdefault`](#StatCounter.setdefault)

- [`pop`](#StatCounter.pop)

- [`popitem`](#StatCounter.popitem)

- [`keys`](#StatCounter.keys)

- [`items`](#StatCounter.items)

- [`values`](#StatCounter.values)

- [`clear`](#StatCounter.clear)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

utilities for getting information about the system, see `SysInfo` class

## API Documentation

- [`SysInfo`](#SysInfo)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py)

# `muutils.sysinfo`

utilities for getting information about the system, see `SysInfo` class

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L0-L199)

### `class SysInfo:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L34-L194)

getters for various information about the system

### `def python`

``` python
() -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L37-L49)

details about python version

### `def pip`

``` python
() -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L51-L59)

installed packages info

### `def pytorch`

``` python
() -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L61-L124)

pytorch and cuda information

### `def platform`

``` python
() -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L126-L145)

### `def git_info`

``` python
(with_log: bool = False) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L147-L168)

### `def get_all`

``` python
(
    cls,
    include: Optional[tuple[str, ...]] = None,
    exclude: tuple[str, ...] = ()
) -> dict
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/sysinfo.py#L170-L194)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

get metadata about a tensor, mostly for `muutils.dbg`

## API Documentation

- [`COLORS`](#COLORS)
- [`OutputFormat`](#OutputFormat)
- [`SYMBOLS`](#SYMBOLS)
- [`SPARK_CHARS`](#SPARK_CHARS)
- [`array_info`](#array_info)
- [`generate_sparkline`](#generate_sparkline)
- [`DEFAULT_SETTINGS`](#DEFAULT_SETTINGS)
- [`apply_color`](#apply_color)
- [`colorize_dtype`](#colorize_dtype)
- [`format_shape_colored`](#format_shape_colored)
- [`format_device_colored`](#format_device_colored)
- [`array_summary`](#array_summary)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py)

# `muutils.tensor_info`

get metadata about a tensor, mostly for
`<a href="dbg.html">muutils.dbg</a>`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L0-L647)

- `COLORS: Dict[str, Dict[str, str]] = {'latex': {'range': '\\textcolor{purple}', 'mean': '\\textcolor{teal}', 'std': '\\textcolor{orange}', 'median': '\\textcolor{green}', 'warning': '\\textcolor{red}', 'shape': '\\textcolor{magenta}', 'dtype': '\\textcolor{gray}', 'device': '\\textcolor{gray}', 'requires_grad': '\\textcolor{gray}', 'sparkline': '\\textcolor{blue}', 'torch': '\\textcolor{orange}', 'dtype_bool': '\\textcolor{gray}', 'dtype_int': '\\textcolor{blue}', 'dtype_float': '\\textcolor{red!70}', 'dtype_str': '\\textcolor{red}', 'device_cuda': '\\textcolor{green}', 'reset': ''}, 'terminal': {'range': '\x1b[35m', 'mean': '\x1b[36m', 'std': '\x1b[33m', 'median': '\x1b[32m', 'warning': '\x1b[31m', 'shape': '\x1b[95m', 'dtype': '\x1b[90m', 'device': '\x1b[90m', 'requires_grad': '\x1b[90m', 'sparkline': '\x1b[34m', 'torch': '\x1b[38;5;208m', 'dtype_bool': '\x1b[38;5;245m', 'dtype_int': '\x1b[38;5;39m', 'dtype_float': '\x1b[38;5;167m', 'device_cuda': '\x1b[38;5;76m', 'reset': '\x1b[0m'}, 'none': {'range': '', 'mean': '', 'std': '', 'median': '', 'warning': '', 'shape': '', 'dtype': '', 'device': '', 'requires_grad': '', 'sparkline': '', 'torch': '', 'dtype_bool': '', 'dtype_int': '', 'dtype_float': '', 'dtype_str': '', 'device_cuda': '', 'reset': ''}}`

- `OutputFormat = typing.Literal['unicode', 'latex', 'ascii']`

- `SYMBOLS: Dict[Literal['unicode', 'latex', 'ascii'], Dict[str, str]] = {'latex': {'range': '\\mathcal{R}', 'mean': '\\mu', 'std': '\\sigma', 'median': '\\tilde{x}', 'distribution': '\\mathbb{P}', 'distribution_log': '\\mathbb{P}_L', 'nan_values': '\\text{NANvals}', 'warning': '!!!', 'requires_grad': '\\nabla', 'true': '\\checkmark', 'false': '\\times'}, 'unicode': {'range': 'R', 'mean': 'μ', 'std': 'σ', 'median': 'x̃', 'distribution': 'ℙ', 'distribution_log': 'ℙ˪', 'nan_values': 'NANvals', 'warning': '🚨', 'requires_grad': '∇', 'true': '✓', 'false': '✗'}, 'ascii': {'range': 'range', 'mean': 'mean', 'std': 'std', 'median': 'med', 'distribution': 'dist', 'distribution_log': 'dist_log', 'nan_values': 'NANvals', 'warning': '!!!', 'requires_grad': 'requires_grad', 'true': '1', 'false': '0'}}`

Symbols for different formats

- `SPARK_CHARS: Dict[Literal['unicode', 'latex', 'ascii'], List[str]] = {'unicode': [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'], 'ascii': [' ', '_', '.', '-', '~', '=', '#'], 'latex': [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']}`

characters for sparklines in different formats

### `def array_info`

``` python
(A: Any, hist_bins: int = 5) -> Dict[str, Any]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L121-L274)

Extract statistical information from an array-like object.

### Parameters:

- `A : array-like` Array to analyze (numpy array or torch tensor)

### Returns:

- `Dict[str, Any]` Dictionary containing raw statistical information
  with numeric values

### `def generate_sparkline`

``` python
(
    histogram: numpy.ndarray,
    format: Literal['unicode', 'latex', 'ascii'] = 'unicode',
    log_y: Optional[bool] = None
) -> tuple[str, bool]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L277-L337)

Generate a sparkline visualization of the histogram.

### Parameters:

- `histogram : np.ndarray` Histogram data
- `format : Literal["unicode", "latex", "ascii"]` Output format
  (defaults to `"unicode"`)
- `log_y : bool|None` Whether to use logarithmic y-scale. `None` for
  automatic detection (defaults to `None`)

### Returns:

- `tuple[str, bool]` Sparkline visualization and whether log scale was
  used

- `DEFAULT_SETTINGS: Dict[str, Any] = {'fmt': 'unicode', 'precision': 2, 'stats': True, 'shape': True, 'dtype': True, 'device': True, 'requires_grad': True, 'sparkline': False, 'sparkline_bins': 5, 'sparkline_logy': None, 'colored': False, 'as_list': False, 'eq_char': '='}`

### `def apply_color`

``` python
(
    text: str,
    color_key: str,
    colors: Dict[str, str],
    using_tex: bool
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L357-L365)

### `def colorize_dtype`

``` python
(dtype_str: str, colors: Dict[str, str], using_tex: bool) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L368-L394)

Colorize dtype string with specific colors for torch and type names.

### `def format_shape_colored`

``` python
(shape_val, colors: Dict[str, str], using_tex: bool) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L397-L415)

Format shape with proper coloring for both 1D and multi-D arrays.

### `def format_device_colored`

``` python
(device_str: str, colors: Dict[str, str], using_tex: bool) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L418-L436)

Format device string with CUDA highlighting.

### `def array_summary`

``` python
(
    array,
    fmt: Literal['unicode', 'latex', 'ascii'] = <muutils.tensor_info._UseDefaultType object>,
    precision: int = <muutils.tensor_info._UseDefaultType object>,
    stats: bool = <muutils.tensor_info._UseDefaultType object>,
    shape: bool = <muutils.tensor_info._UseDefaultType object>,
    dtype: bool = <muutils.tensor_info._UseDefaultType object>,
    device: bool = <muutils.tensor_info._UseDefaultType object>,
    requires_grad: bool = <muutils.tensor_info._UseDefaultType object>,
    sparkline: bool = <muutils.tensor_info._UseDefaultType object>,
    sparkline_bins: int = <muutils.tensor_info._UseDefaultType object>,
    sparkline_logy: Optional[bool] = <muutils.tensor_info._UseDefaultType object>,
    colored: bool = <muutils.tensor_info._UseDefaultType object>,
    eq_char: str = <muutils.tensor_info._UseDefaultType object>,
    as_list: bool = <muutils.tensor_info._UseDefaultType object>
) -> Union[str, List[str]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_info.py#L456-L648)

Format array information into a readable summary.

### Parameters:

- `array` array-like object (numpy array or torch tensor)
- `precision : int` Decimal places (defaults to `2`)
- `format : Literal["unicode", "latex", "ascii"]` Output format
  (defaults to `{default_fmt}`)
- `stats : bool` Whether to include statistical info (μ, σ, x̃) (defaults
  to `True`)
- `shape : bool` Whether to include shape info (defaults to `True`)
- `dtype : bool` Whether to include dtype info (defaults to `True`)
- `device : bool` Whether to include device info for torch tensors
  (defaults to `True`)
- `requires_grad : bool` Whether to include requires_grad info for torch
  tensors (defaults to `True`)
- `sparkline : bool` Whether to include a sparkline visualization
  (defaults to `False`)
- `sparkline_width : int` Width of the sparkline (defaults to `20`)
- `sparkline_logy : bool|None` Whether to use logarithmic y-scale for
  sparkline (defaults to `None`)
- `colored : bool` Whether to add color to output (defaults to `False`)
- `as_list : bool` Whether to return as list of strings instead of
  joined string (defaults to `False`)

### Returns:

- `Union[str, List[str]]` Formatted statistical summary, either as
  string or list of strings

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

utilities for working with tensors and arrays.

notably:

- `TYPE_TO_JAX_DTYPE` : a mapping from python, numpy, and torch types to
  `jaxtyping` types
- `DTYPE_MAP` mapping string representations of types to their type
- `TORCH_DTYPE_MAP` mapping string representations of types to torch
  types
- `compare_state_dicts` for comparing two state dicts and giving a
  detailed error message on whether if was keys, shapes, or values that
  didn’t match

## API Documentation

- [`TYPE_TO_JAX_DTYPE`](#TYPE_TO_JAX_DTYPE)
- [`jaxtype_factory`](#jaxtype_factory)
- [`ATensor`](#ATensor)
- [`NDArray`](#NDArray)
- [`numpy_to_torch_dtype`](#numpy_to_torch_dtype)
- [`DTYPE_LIST`](#DTYPE_LIST)
- [`DTYPE_MAP`](#DTYPE_MAP)
- [`TORCH_DTYPE_MAP`](#TORCH_DTYPE_MAP)
- [`TORCH_OPTIMIZERS_MAP`](#TORCH_OPTIMIZERS_MAP)
- [`pad_tensor`](#pad_tensor)
- [`lpad_tensor`](#lpad_tensor)
- [`rpad_tensor`](#rpad_tensor)
- [`pad_array`](#pad_array)
- [`lpad_array`](#lpad_array)
- [`rpad_array`](#rpad_array)
- [`get_dict_shapes`](#get_dict_shapes)
- [`string_dict_shapes`](#string_dict_shapes)
- [`StateDictCompareError`](#StateDictCompareError)
- [`StateDictKeysError`](#StateDictKeysError)
- [`StateDictShapeError`](#StateDictShapeError)
- [`StateDictValueError`](#StateDictValueError)
- [`compare_state_dicts`](#compare_state_dicts)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py)

# `muutils.tensor_utils`

utilities for working with tensors and arrays.

notably:

- `TYPE_TO_JAX_DTYPE` : a mapping from python, numpy, and torch types to
  `jaxtyping` types
- `DTYPE_MAP` mapping string representations of types to their type
- `TORCH_DTYPE_MAP` mapping string representations of types to torch
  types
- `compare_state_dicts` for comparing two state dicts and giving a
  detailed error message on whether if was keys, shapes, or values that
  didn’t match

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L0-L494)

- `TYPE_TO_JAX_DTYPE: dict = {<class 'float'>: <class 'jaxtyping.Float'>, <class 'int'>: <class 'jaxtyping.Int'>, <class 'jaxtyping.Float'>: <class 'jaxtyping.Float'>, <class 'jaxtyping.Int'>: <class 'jaxtyping.Int'>, <class 'bool'>: <class 'jaxtyping.Bool'>, <class 'jaxtyping.Bool'>: <class 'jaxtyping.Bool'>, <class 'numpy.bool_'>: <class 'jaxtyping.Bool'>, torch.bool: <class 'jaxtyping.Bool'>, <class 'numpy.float16'>: <class 'jaxtyping.Float'>, <class 'numpy.float32'>: <class 'jaxtyping.Float'>, <class 'numpy.float64'>: <class 'jaxtyping.Float'>, <class 'numpy.int8'>: <class 'jaxtyping.Int'>, <class 'numpy.int16'>: <class 'jaxtyping.Int'>, <class 'numpy.int32'>: <class 'jaxtyping.Int'>, <class 'numpy.int64'>: <class 'jaxtyping.Int'>, <class 'numpy.longlong'>: <class 'jaxtyping.Int'>, <class 'numpy.uint8'>: <class 'jaxtyping.Int'>, torch.float32: <class 'jaxtyping.Float'>, torch.float16: <class 'jaxtyping.Float'>, torch.float64: <class 'jaxtyping.Float'>, torch.bfloat16: <class 'jaxtyping.Float'>, torch.int32: <class 'jaxtyping.Int'>, torch.int8: <class 'jaxtyping.Int'>, torch.int16: <class 'jaxtyping.Int'>, torch.int64: <class 'jaxtyping.Int'>}`

dict mapping python, numpy, and torch types to `jaxtyping` types

### `def jaxtype_factory`

``` python
(
    name: str,
    array_type: type,
    default_jax_dtype=<class 'jaxtyping.Float'>,
    legacy_mode: Union[muutils.errormode.ErrorMode, str] = ErrorMode.Warn
) -> type
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L78-L172)

usage:

    ATensor = jaxtype_factory("ATensor", torch.Tensor, jaxtyping.Float)
    x: ATensor["dim1 dim2", np.float32]

- `ATensor = <class 'muutils.tensor_utils.jaxtype_factory.<locals>._BaseArray'>`

- `NDArray = <class 'muutils.tensor_utils.jaxtype_factory.<locals>._BaseArray'>`

### `def numpy_to_torch_dtype`

``` python
(dtype: Union[numpy.dtype, torch.dtype]) -> torch.dtype
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L195-L200)

convert numpy dtype to torch dtype

- `DTYPE_LIST: list = [<class 'bool'>, <class 'int'>, <class 'float'>, torch.float32, torch.float32, torch.float64, torch.float16, torch.float64, torch.bfloat16, torch.complex64, torch.complex128, torch.int32, torch.int8, torch.int16, torch.int32, torch.int64, torch.int64, torch.int16, torch.uint8, torch.bool, <class 'numpy.float16'>, <class 'numpy.float32'>, <class 'numpy.float64'>, <class 'numpy.float16'>, <class 'numpy.float32'>, <class 'numpy.float64'>, <class 'numpy.complex64'>, <class 'numpy.complex128'>, <class 'numpy.int8'>, <class 'numpy.int16'>, <class 'numpy.int32'>, <class 'numpy.int64'>, <class 'numpy.longlong'>, <class 'numpy.int16'>, <class 'numpy.uint8'>, <class 'numpy.bool_'>, <class 'numpy.float64'>, <class 'numpy.int64'>]`

list of all the python, numpy, and torch numerical types I could think
of

- `DTYPE_MAP: dict = {"<class 'bool'>": <class 'bool'>, "<class 'int'>": <class 'int'>, "<class 'float'>": <class 'float'>, 'torch.float32': torch.float32, 'torch.float64': torch.float64, 'torch.float16': torch.float16, 'torch.bfloat16': torch.bfloat16, 'torch.complex64': torch.complex64, 'torch.complex128': torch.complex128, 'torch.int32': torch.int32, 'torch.int8': torch.int8, 'torch.int16': torch.int16, 'torch.int64': torch.int64, 'torch.uint8': torch.uint8, 'torch.bool': torch.bool, "<class 'numpy.float16'>": <class 'numpy.float16'>, "<class 'numpy.float32'>": <class 'numpy.float32'>, "<class 'numpy.float64'>": <class 'numpy.float64'>, "<class 'numpy.complex64'>": <class 'numpy.complex64'>, "<class 'numpy.complex128'>": <class 'numpy.complex128'>, "<class 'numpy.int8'>": <class 'numpy.int8'>, "<class 'numpy.int16'>": <class 'numpy.int16'>, "<class 'numpy.int32'>": <class 'numpy.int32'>, "<class 'numpy.int64'>": <class 'numpy.int64'>, "<class 'numpy.longlong'>": <class 'numpy.longlong'>, "<class 'numpy.uint8'>": <class 'numpy.uint8'>, "<class 'numpy.bool_'>": <class 'numpy.bool_'>, 'float16': <class 'numpy.float16'>, 'float32': <class 'numpy.float32'>, 'float64': <class 'numpy.float64'>, 'complex64': <class 'numpy.complex64'>, 'complex128': <class 'numpy.complex128'>, 'int8': <class 'numpy.int8'>, 'int16': <class 'numpy.int16'>, 'int32': <class 'numpy.int32'>, 'int64': <class 'numpy.int64'>, 'longlong': <class 'numpy.longlong'>, 'uint8': <class 'numpy.uint8'>, 'bool_': <class 'numpy.bool_'>, 'bool': <class 'numpy.bool_'>}`

mapping from string representations of types to their type

- `TORCH_DTYPE_MAP: dict = {"<class 'bool'>": torch.bool, "<class 'int'>": torch.int64, "<class 'float'>": torch.float64, 'torch.float32': torch.float32, 'torch.float64': torch.float64, 'torch.float16': torch.float16, 'torch.bfloat16': torch.bfloat16, 'torch.complex64': torch.complex64, 'torch.complex128': torch.complex128, 'torch.int32': torch.int32, 'torch.int8': torch.int8, 'torch.int16': torch.int16, 'torch.int64': torch.int64, 'torch.uint8': torch.uint8, 'torch.bool': torch.bool, "<class 'numpy.float16'>": torch.float16, "<class 'numpy.float32'>": torch.float32, "<class 'numpy.float64'>": torch.float64, "<class 'numpy.complex64'>": torch.complex64, "<class 'numpy.complex128'>": torch.complex128, "<class 'numpy.int8'>": torch.int8, "<class 'numpy.int16'>": torch.int16, "<class 'numpy.int32'>": torch.int32, "<class 'numpy.int64'>": torch.int64, "<class 'numpy.longlong'>": torch.int64, "<class 'numpy.uint8'>": torch.uint8, "<class 'numpy.bool_'>": torch.bool, 'float16': torch.float16, 'float32': torch.float32, 'float64': torch.float64, 'complex64': torch.complex64, 'complex128': torch.complex128, 'int8': torch.int8, 'int16': torch.int16, 'int32': torch.int32, 'int64': torch.int64, 'longlong': torch.int64, 'uint8': torch.uint8, 'bool_': torch.bool, 'bool': torch.bool}`

mapping from string representations of types to specifically torch types

- `TORCH_OPTIMIZERS_MAP: dict[str, typing.Type[torch.optim.optimizer.Optimizer]] = {'Adagrad': <class 'torch.optim.adagrad.Adagrad'>, 'Adam': <class 'torch.optim.adam.Adam'>, 'AdamW': <class 'torch.optim.adamw.AdamW'>, 'SparseAdam': <class 'torch.optim.sparse_adam.SparseAdam'>, 'Adamax': <class 'torch.optim.adamax.Adamax'>, 'ASGD': <class 'torch.optim.asgd.ASGD'>, 'LBFGS': <class 'torch.optim.lbfgs.LBFGS'>, 'NAdam': <class 'torch.optim.nadam.NAdam'>, 'RAdam': <class 'torch.optim.radam.RAdam'>, 'RMSprop': <class 'torch.optim.rmsprop.RMSprop'>, 'Rprop': <class 'torch.optim.rprop.Rprop'>, 'SGD': <class 'torch.optim.sgd.SGD'>}`

### `def pad_tensor`

``` python
(
    tensor: jaxtyping.Shaped[Tensor, 'dim1'],
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False
) -> jaxtyping.Shaped[Tensor, 'padded_length']
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L298-L321)

pad a 1-d tensor on the left with pad_value to length `padded_length`

set `rpad = True` to pad on the right instead

### `def lpad_tensor`

``` python
(
    tensor: torch.Tensor,
    padded_length: int,
    pad_value: float = 0.0
) -> torch.Tensor
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L324-L328)

pad a 1-d tensor on the left with pad_value to length `padded_length`

### `def rpad_tensor`

``` python
(
    tensor: torch.Tensor,
    pad_length: int,
    pad_value: float = 0.0
) -> torch.Tensor
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L331-L335)

pad a 1-d tensor on the right with pad_value to length `pad_length`

### `def pad_array`

``` python
(
    array: jaxtyping.Shaped[ndarray, 'dim1'],
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False
) -> jaxtyping.Shaped[ndarray, 'padded_length']
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L338-L360)

pad a 1-d array on the left with pad_value to length `padded_length`

set `rpad = True` to pad on the right instead

### `def lpad_array`

``` python
(
    array: numpy.ndarray,
    padded_length: int,
    pad_value: float = 0.0
) -> numpy.ndarray
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L363-L367)

pad a 1-d array on the left with pad_value to length `padded_length`

### `def rpad_array`

``` python
(
    array: numpy.ndarray,
    pad_length: int,
    pad_value: float = 0.0
) -> numpy.ndarray
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L370-L374)

pad a 1-d array on the right with pad_value to length `pad_length`

### `def get_dict_shapes`

``` python
(d: dict[str, torch.Tensor]) -> dict[str, tuple[int, ...]]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L377-L379)

given a state dict or cache dict, compute the shapes and put them in a
nested dict

### `def string_dict_shapes`

``` python
(d: dict[str, torch.Tensor]) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L382-L394)

printable version of get_dict_shapes

### `class StateDictCompareError(builtins.AssertionError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L397-L400)

raised when state dicts don’t match

### Inherited Members

- [`AssertionError`](#StateDictCompareError.__init__)

- [`with_traceback`](#StateDictCompareError.with_traceback)

- [`add_note`](#StateDictCompareError.add_note)

- [`args`](#StateDictCompareError.args)

### `class StateDictKeysError(StateDictCompareError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L403-L406)

raised when state dict keys don’t match

### Inherited Members

- [`AssertionError`](#StateDictKeysError.__init__)

- [`with_traceback`](#StateDictKeysError.with_traceback)

- [`add_note`](#StateDictKeysError.add_note)

- [`args`](#StateDictKeysError.args)

### `class StateDictShapeError(StateDictCompareError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L409-L412)

raised when state dict shapes don’t match

### Inherited Members

- [`AssertionError`](#StateDictShapeError.__init__)

- [`with_traceback`](#StateDictShapeError.with_traceback)

- [`add_note`](#StateDictShapeError.add_note)

- [`args`](#StateDictShapeError.args)

### `class StateDictValueError(StateDictCompareError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L415-L418)

raised when state dict values don’t match

### Inherited Members

- [`AssertionError`](#StateDictValueError.__init__)

- [`with_traceback`](#StateDictValueError.with_traceback)

- [`add_note`](#StateDictValueError.add_note)

- [`args`](#StateDictValueError.args)

### `def compare_state_dicts`

``` python
(
    d1: dict,
    d2: dict,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    verbose: bool = True
) -> None
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/tensor_utils.py#L421-L495)

compare two dicts of tensors

### Parameters:

- `d1 : dict`
- `d2 : dict`
- `rtol : float` (defaults to `1e-5`)
- `atol : float` (defaults to `1e-8`)
- `verbose : bool` (defaults to `True`)

### Raises:

- `StateDictKeysError` : keys don’t match
- `StateDictShapeError` : shapes don’t match (but keys do)
- `StateDictValueError` : values don’t match (but keys and shapes do)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

`timeit_fancy` is just a fancier version of timeit with more options

## API Documentation

- [`FancyTimeitResult`](#FancyTimeitResult)
- [`timeit_fancy`](#timeit_fancy)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/timeit_fancy.py)

# `muutils.timeit_fancy`

`timeit_fancy` is just a fancier version of timeit with more options

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/timeit_fancy.py#L0-L106)

### `class FancyTimeitResult(typing.NamedTuple):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/timeit_fancy.py#L16-L21)

return type of `timeit_fancy`

### `FancyTimeitResult`

``` python
(
    timings: ForwardRef('StatCounter'),
    return_value: ForwardRef('T_return'),
    profile: ForwardRef('Union[pstats.Stats, None]')
)
```

Create new instance of FancyTimeitResult(timings, return_value, profile)

- `timings: muutils.statcounter.StatCounter`

Alias for field number 0

- `return_value: ~T_return`

Alias for field number 1

- `profile: Optional[pstats.Stats]`

Alias for field number 2

### Inherited Members

- [`index`](#FancyTimeitResult.index)
- [`count`](#FancyTimeitResult.count)

### `def timeit_fancy`

``` python
(
    cmd: Union[Callable[[], ~T_return], str],
    setup: Union[str, Callable[[], Any]] = <function <lambda>>,
    repeats: int = 5,
    namespace: Optional[dict[str, Any]] = None,
    get_return: bool = True,
    do_profiling: bool = False
) -> muutils.timeit_fancy.FancyTimeitResult
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/timeit_fancy.py#L24-L107)

Wrapper for `timeit` to get the fastest run of a callable with more
customization options.

Approximates the functionality of the %timeit magic or command line
interface in a Python callable.

### Parameters

- `cmd: Callable[[], T_return] | str` The callable to time. If a string,
  it will be passed to `timeit.Timer` as the `stmt` argument.
- `setup: str` The setup code to run before `cmd`. If a string, it will
  be passed to `timeit.Timer` as the `setup` argument.
- `repeats: int` The number of times to run `cmd` to get a reliable
  measurement.
- `namespace: dict[str, Any]` Passed to `timeit.Timer` constructor. If
  `cmd` or `setup` use local or global variables, they must be passed
  here. See `timeit` documentation for details.
- `get_return: bool` Whether to pass the value returned from `cmd`. If
  True, the return value will be appended in a tuple with execution
  time. This is for speed and convenience so that `cmd` doesn’t need to
  be run again in the calling scope if the return values are needed.
  (default: `False`)
- `do_profiling: bool` Whether to return a `pstats.Stats` object in
  addition to the time and return value. (default: `False`)

### Returns

`FancyTimeitResult`, which is a NamedTuple with the following fields:

- `time: float` The time in seconds it took to run `cmd` the minimum
  number of times to get a reliable measurement.
- `return_value: T|None` The return value of `cmd` if `get_return` is
  `True`, otherwise `None`.
- `profile: pstats.Stats|None` A `pstats.Stats` object if `do_profiling`
  is `True`, otherwise `None`.

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

experimental utility for validating types in python, see `validate_type`

## API Documentation

- [`GenericAliasTypes`](#GenericAliasTypes)
- [`IncorrectTypeException`](#IncorrectTypeException)
- [`TypeHintNotImplementedError`](#TypeHintNotImplementedError)
- [`InvalidGenericAliasError`](#InvalidGenericAliasError)
- [`validate_type`](#validate_type)
- [`get_fn_allowed_kwargs`](#get_fn_allowed_kwargs)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py)

# `muutils.validate_type`

experimental utility for validating types in python, see `validate_type`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py#L0-L236)

- `GenericAliasTypes: tuple = (<class 'types.GenericAlias'>, <class 'typing._GenericAlias'>, <class 'typing._UnionGenericAlias'>, <class 'typing._BaseGenericAlias'>)`

### `class IncorrectTypeException(builtins.TypeError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py#L25-L26)

Inappropriate argument type.

### Inherited Members

- [`TypeError`](#IncorrectTypeException.__init__)

- [`with_traceback`](#IncorrectTypeException.with_traceback)

- [`add_note`](#IncorrectTypeException.add_note)

- [`args`](#IncorrectTypeException.args)

### `class TypeHintNotImplementedError(builtins.NotImplementedError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py#L29-L30)

Method or function hasn’t been implemented yet.

### Inherited Members

- [`NotImplementedError`](#TypeHintNotImplementedError.__init__)

- [`with_traceback`](#TypeHintNotImplementedError.with_traceback)

- [`add_note`](#TypeHintNotImplementedError.add_note)

- [`args`](#TypeHintNotImplementedError.args)

### `class InvalidGenericAliasError(builtins.TypeError):`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py#L33-L34)

Inappropriate argument type.

### Inherited Members

- [`TypeError`](#InvalidGenericAliasError.__init__)

- [`with_traceback`](#InvalidGenericAliasError.with_traceback)

- [`add_note`](#InvalidGenericAliasError.add_note)

- [`args`](#InvalidGenericAliasError.args)

### `def validate_type`

``` python
(value: Any, expected_type: Any, do_except: bool = False) -> bool
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py#L58-L220)

Validate that a `value` is of the `expected_type`

### Parameters

- `value`: the value to check the type of
- `expected_type`: the type to check against. Not all types are
  supported
- `do_except`: if `True`, raise an exception if the type is incorrect
  (instead of returning `False`) (default: `False`)

### Returns

- `bool`: `True` if the value is of the expected type, `False`
  otherwise.

### Raises

- `IncorrectTypeException(TypeError)`: if the type is incorrect and
  `do_except` is `True`
- `TypeHintNotImplementedError(NotImplementedError)`: if the type hint
  is not implemented
- `InvalidGenericAliasError(TypeError)`: if the generic alias is invalid

use `typeguard` for a more robust solution:
https://github.com/agronholm/typeguard

### `def get_fn_allowed_kwargs`

``` python
(fn: Callable) -> Set[str]
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/validate_type.py#L223-L237)

Get the allowed kwargs for a function, raising an exception if the
signature cannot be determined.

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Submodules

- [`bundle_html`](#bundle_html)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/__init__.py)

# `muutils.web`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/__init__.py#L0-L2)

> docs for [`muutils`](https://github.com/mivanit/muutils) v0.8.11

## Contents

Inline / bundle external assets (CSS, JS, SVG, PNG) into an HTML
document.

Default mode uses **zero external dependencies** and a few well-targeted
regular expressions. If you install *beautifulsoup4* you can enable the
far more robust BS4 mode by passing `InlineConfig(use_bs4=True)`.

## API Documentation

- [`AssetExt`](#AssetExt)
- [`DEFAULT_ALLOWED_EXTENSIONS`](#DEFAULT_ALLOWED_EXTENSIONS)
- [`DEFAULT_TAG_ATTR`](#DEFAULT_TAG_ATTR)
- [`MIME_BY_EXT`](#MIME_BY_EXT)
- [`InlineConfig`](#InlineConfig)
- [`inline_html_assets`](#inline_html_assets)
- [`inline_html_file`](#inline_html_file)

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/bundle_html.py)

# `muutils.web.bundle_html`

Inline / bundle external assets (CSS, JS, SVG, PNG) into an HTML
document.

Default mode uses **zero external dependencies** and a few well-targeted
regular expressions. If you install *beautifulsoup4* you can enable the
far more robust BS4 mode by passing `InlineConfig(use_bs4=True)`.

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/bundle_html.py#L0-L387)

- `AssetExt = typing.Literal['.css', '.js', '.svg', '.png']`

- `DEFAULT_ALLOWED_EXTENSIONS: Final[set[Literal['.css', '.js', '.svg', '.png']]] = {'.png', '.svg', '.css', '.js'}`

- `DEFAULT_TAG_ATTR: Final[dict[str, str]] = {'link': 'href', 'script': 'src', 'img': 'src', 'use': 'xlink:href'}`

- `MIME_BY_EXT: Final[dict[Literal['.css', '.js', '.svg', '.png'], str]] = {'.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.png': 'image/png'}`

### `class InlineConfig:`

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/bundle_html.py#L46-L76)

High-level configuration for the inliner.

### Parameters

- `allowed_extensions : set[AssetExt]` Extensions that may be inlined.
- `tag_attr : dict[str, str]` Mapping *tag -\> attribute* that holds the
  asset reference.
- `max_bytes : int` Assets larger than this are ignored.
- `local : bool` Allow local filesystem assets.
- `remote : bool` Allow remote http/https assets.
- `include_filename_comments : bool` Surround every replacement with
  `<!-- begin '...' -->` and `<!-- end '...' -->`.
- `use_bs4 : bool` Parse the document with BeautifulSoup if available.

### `InlineConfig`

``` python
(
    allowed_extensions: set[typing.Literal['.css', '.js', '.svg', '.png']] = <factory>,
    tag_attr: dict[str, str] = <factory>,
    max_bytes: int = 131072,
    local: bool = True,
    remote: bool = False,
    include_filename_comments: bool = True,
    use_bs4: bool = False
)
```

- `allowed_extensions: set[typing.Literal['.css', '.js', '.svg', '.png']]`

- `tag_attr: dict[str, str]`

- `max_bytes: int = 131072`

- `local: bool = True`

- `remote: bool = False`

- `include_filename_comments: bool = True`

- `use_bs4: bool = False`

### `def inline_html_assets`

``` python
(
    html: str,
    *,
    base_path: pathlib.Path,
    config: muutils.web.bundle_html.InlineConfig | None = None,
    prettify: bool = False
) -> str
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/bundle_html.py#L235-L269)

Inline permitted external assets inside *html*.

### Parameters

- `html : str` Raw HTML text.
- `base_path : Path` Directory used to resolve relative asset paths.
- `config : InlineConfig | None` Inlining options (see `InlineConfig`).
- `prettify : bool` Pretty-print output (only effective in BS4 mode).

### Returns

- `str` Modified HTML.

### `def inline_html_file`

``` python
(
    html_path: pathlib.Path,
    output_path: pathlib.Path,
    base_path: pathlib.Path | None = None,
    config: muutils.web.bundle_html.InlineConfig | None = None,
    prettify: bool = False
) -> pathlib.Path
```

[View Source on
GitHub](https://github.com/mivanit/muutils/blob/0.8.11/web/bundle_html.py#L272-L313)

Read *html_path*, inline its assets, and write the result.

### Parameters

- `html_path : Path` Source HTML file.
- `output_path : Path` Destination path to write the modified HTML.
- `base_path : Path | None` Directory used to resolve relative asset
  paths (defaults to the HTML file’s directory). If `None`, uses the
  directory of *html_path*. (default: `None` -\> use `html_path.parent`)
- `config : InlineConfig | None` Inlining options. If `None`, uses
  default configuration. (default: `None` -\> use `InlineConfig()`)
- `prettify : bool` Pretty-print when `use_bs4=True`. (default: `False`)

### Returns

- `Path` Path actually written.
