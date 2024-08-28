
## Contents
[![PyPI](https://img.shields.io/pypi/v/muutils)](https://pypi.org/project/muutils/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/muutils)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/muutils)

[![Checks](https://github.com/mivanit/muutils/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/checks.yml)
[![Checks](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTkiIGhlaWdodD0iMjAiPg0KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYiIgeDI9IjAiIHkyPSIxMDAlIj4NCiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+DQogICAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIuMSIvPg0KICAgIDwvbGluZWFyR3JhZGllbnQ+DQogICAgPG1hc2sgaWQ9ImEiPg0KICAgICAgICA8cmVjdCB3aWR0aD0iOTkiIGhlaWdodD0iMjAiIHJ4PSIzIiBmaWxsPSIjZmZmIi8+DQogICAgPC9tYXNrPg0KICAgIDxnIG1hc2s9InVybCgjYSkiPg0KICAgICAgICA8cGF0aCBmaWxsPSIjNTU1IiBkPSJNMCAwaDYzdjIwSDB6Ii8+DQogICAgICAgIDxwYXRoIGZpbGw9IiNhNGE2MWQiIGQ9Ik02MyAwaDM2djIwSDYzeiIvPg0KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+DQogICAgPC9nPg0KICAgIDxnIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyxWZXJkYW5hLEdlbmV2YSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjExIj4NCiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSIzMS41IiB5PSIxNCI+Y292ZXJhZ2U8L3RleHQ+DQogICAgICAgIDx0ZXh0IHg9IjgwIiB5PSIxNSIgZmlsbD0iIzAxMDEwMSIgZmlsbC1vcGFjaXR5PSIuMyI+ODQlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjg0JTwvdGV4dD4NCiAgICA8L2c+DQo8L3N2Zz4NCg==)](docs/coverage/html/)

![GitHub commits](https://img.shields.io/github/commit-activity/t/mivanit/muutils)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/mivanit/muutils)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/mivanit/muutils)
![code size, bytes](https://img.shields.io/github/languages/code-size/mivanit/muutils)
<!-- ![Lines of code](https://img.shields.io/tokei/lines/github.com/mivanit/muutils) -->

`muutils`, stylized as "$\mu$utils" or "μutils", is a collection of miscellaneous python utilities, meant to be small and with no dependencies outside of standard python.

# installation

PyPi: [muutils](https://pypi.org/project/muutils/)

```
pip install muutils
```

Note that for using `mlutils`, `tensor_utils`, `nbutils.configure_notebook`, or the array serialization features of `json_serialize`, you will need to install with optional `array` dependencies:
```
pip install muutils[array]
```

# documentation

- [hosted html docs](https://miv.name/muutils)
- [single-page html docs](docs/combined/muutils.html) [(absolute link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.html)
- [single-page markdown docs](docs/combined/muutils.md) [(absolute link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.md)
- Test coverage: [![Test Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTkiIGhlaWdodD0iMjAiPg0KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYiIgeDI9IjAiIHkyPSIxMDAlIj4NCiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+DQogICAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIuMSIvPg0KICAgIDwvbGluZWFyR3JhZGllbnQ+DQogICAgPG1hc2sgaWQ9ImEiPg0KICAgICAgICA8cmVjdCB3aWR0aD0iOTkiIGhlaWdodD0iMjAiIHJ4PSIzIiBmaWxsPSIjZmZmIi8+DQogICAgPC9tYXNrPg0KICAgIDxnIG1hc2s9InVybCgjYSkiPg0KICAgICAgICA8cGF0aCBmaWxsPSIjNTU1IiBkPSJNMCAwaDYzdjIwSDB6Ii8+DQogICAgICAgIDxwYXRoIGZpbGw9IiNhNGE2MWQiIGQ9Ik02MyAwaDM2djIwSDYzeiIvPg0KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+DQogICAgPC9nPg0KICAgIDxnIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyxWZXJkYW5hLEdlbmV2YSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjExIj4NCiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSIzMS41IiB5PSIxNCI+Y292ZXJhZ2U8L3RleHQ+DQogICAgICAgIDx0ZXh0IHg9IjgwIiB5PSIxNSIgZmlsbD0iIzAxMDEwMSIgZmlsbC1vcGFjaXR5PSIuMyI+ODQlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjg0JTwvdGV4dD4NCiAgICA8L2c+DQo8L3N2Zz4NCg==)](docs/coverage/html/) [(absolute link)](https://github.com/mivanit/muutils/tree/main/docs/coverage/html/) [(plain text)](https://github.com/mivanit/muutils/tree/main/docs/coverage/coverage.txt)



## [`statcounter`](https://github.com/mivanit/muutils/tree/main/muutils/statcounter.py)

an extension of `collections.Counter` that provides "smart" computation of stats (mean, variance, median, other percentiles) from the counter object without using `Counter.elements()`

## [`dictmagic`](https://github.com/mivanit/muutils/tree/main/muutils/dictmagic.py)

has utilities for working with dictionaries, like:

  - converting dotlist-dictionaries to nested dictionaries and back:
      ```python
      >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})
      {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
      >>> nested_dict_to_dotlist({'a': {'b': {'c': 1, 'd': 2}, 'e': 3}})
      {'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}
      ```
  - `DefaulterDict` which works like a `defaultdict` but can generate the default value based on the key
  - `condense_tensor_dict` takes a dict of dotlist-tensors and gives a more human-readable summary:
      ```python
      >>> model = MyGPT()
      >>> print(condense_tensor_dict(model.named_parameters(), 'yaml'))
      ```
      ```yaml
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
	  <...>
      ```

## [`kappa`](https://github.com/mivanit/muutils/tree/main/muutils/kappa.py)

Anonymous gettitem, so you can do things like

```python
>>> k = Kappa(lambda x: x**2)
>>> k[2]
4
```

## [`sysinfo`](https://github.com/mivanit/muutils/tree/main/muutils/sysinfo.py)

utility for getting a bunch of system information. useful for logging.

## `misc`:

contains a few utilities:
    - `stable_hash()` uses `hashlib.sha256` to compute a hash of an object that is stable across runs of python
    - `list_join` and `list_split` which behave like `str.join` and `str.split` but for lists
    - `sanitize_fname` and `dict_to_filename` for simplifying the creation of unique filename
    - `shorten_numerical_to_str()` and `str_to_numeric` turns numbers like `123456789` into `"123M"` and back
    - `freeze`, which prevents an object from being modified. Also see [gelidum](https://github.com/diegojromerolopez/gelidum/)


## [`nbutils`](https://github.com/mivanit/muutils/tree/main/muutils/nbutils)

contains utilities for working with jupyter notebooks, such as:

- quickly converting notebooks to python scripts (and running those scripts) for testing in CI
- configuring notebooks, to make it easier to switch between figure output formats, locations, and more
- shorthand for displaying mermaid diagrams and TeX

## [`json_serialize`](https://github.com/mivanit/muutils/tree/main/muutils/json_serialize.py)

a tool for serializing and loading arbitrary python objects into json. plays nicely with [`ZANJ`](https://github.com/mivanit/ZANJ/)


## [`tensor_utils`]

contains minor utilities for working with pytorch tensors and numpy arrays, mostly for making type conversions easier

## [`group_equiv`](https://github.com/mivanit/muutils/tree/main/muutils/group_equiv.py)

groups elements from a sequence according to a given equivalence relation, without assuming that the equivalence relation obeys the transitive property



## [`jsonlines`](https://github.com/mivanit/muutils/tree/main/muutils/jsonlines.py)

an extremely simple utility for reading/writing `jsonl` files

## [`ZANJ`](https://github.com/mivanit/ZANJ/)

is a human-readable and simple format for ML models, datasets, and arbitrary objects. It's build around having a zip file with `json` and `npy` files, and has been spun off into its [own project](https://github.com/mivanit/ZANJ/).

There are a couple work-in-progress utilities in [`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/) that aren't ready for anything, but nothing in this repo is suitable for production. Use at your own risk!



## Submodules

- [`json_serialize`](#json_serialize)
- [`logger`](#logger)
- [`misc`](#misc)
- [`nbutils`](#nbutils)
- [`dictmagic`](#dictmagic)
- [`errormode`](#errormode)
- [`group_equiv`](#group_equiv)
- [`interval`](#interval)
- [`jsonlines`](#jsonlines)
- [`kappa`](#kappa)
- [`mlutils`](#mlutils)
- [`spinner`](#spinner)
- [`statcounter`](#statcounter)
- [`sysinfo`](#sysinfo)
- [`tensor_utils`](#tensor_utils)
- [`timeit_fancy`](#timeit_fancy)
- [`validate_type`](#validate_type)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/__init__.py)

# `muutils` { #muutils }

[![PyPI](https://img.shields.io/pypi/v/muutils)](https://pypi.org/project/muutils/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/muutils)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/muutils)

[![Checks](https://github.com/mivanit/muutils/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/checks.yml)
[![Checks](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml)
[![Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTkiIGhlaWdodD0iMjAiPg0KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYiIgeDI9IjAiIHkyPSIxMDAlIj4NCiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+DQogICAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIuMSIvPg0KICAgIDwvbGluZWFyR3JhZGllbnQ+DQogICAgPG1hc2sgaWQ9ImEiPg0KICAgICAgICA8cmVjdCB3aWR0aD0iOTkiIGhlaWdodD0iMjAiIHJ4PSIzIiBmaWxsPSIjZmZmIi8+DQogICAgPC9tYXNrPg0KICAgIDxnIG1hc2s9InVybCgjYSkiPg0KICAgICAgICA8cGF0aCBmaWxsPSIjNTU1IiBkPSJNMCAwaDYzdjIwSDB6Ii8+DQogICAgICAgIDxwYXRoIGZpbGw9IiNhNGE2MWQiIGQ9Ik02MyAwaDM2djIwSDYzeiIvPg0KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+DQogICAgPC9nPg0KICAgIDxnIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyxWZXJkYW5hLEdlbmV2YSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjExIj4NCiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSIzMS41IiB5PSIxNCI+Y292ZXJhZ2U8L3RleHQ+DQogICAgICAgIDx0ZXh0IHg9IjgwIiB5PSIxNSIgZmlsbD0iIzAxMDEwMSIgZmlsbC1vcGFjaXR5PSIuMyI+ODQlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjg0JTwvdGV4dD4NCiAgICA8L2c+DQo8L3N2Zz4NCg==)](docs/coverage/html/)

![GitHub commits](https://img.shields.io/github/commit-activity/t/mivanit/muutils)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/mivanit/muutils)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/mivanit/muutils)
![code size, bytes](https://img.shields.io/github/languages/code-size/mivanit/muutils)
<!-- ![Lines of code](https://img.shields.io/tokei/lines/github.com/mivanit/muutils) -->

`muutils`, stylized as "$\mu$utils" or "μutils", is a collection of miscellaneous python utilities, meant to be small and with no dependencies outside of standard python.

### installation

PyPi: [muutils](https://pypi.org/project/muutils/)

```
pip install muutils
```

Note that for using `mlutils`, `tensor_utils`, `nbutils.configure_notebook`, or the array serialization features of `json_serialize`, you will need to install with optional `array` dependencies:
```
pip install muutils[array]
```

### documentation

- [hosted html docs](https://miv.name/muutils)
- [single-page html docs](docs/combined/muutils.html) [(absolute link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.html)
- [single-page markdown docs](docs/combined/muutils.md) [(absolute link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.md)
- Test coverage: [![Test Coverage](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iOTkiIGhlaWdodD0iMjAiPg0KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYiIgeDI9IjAiIHkyPSIxMDAlIj4NCiAgICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjYmJiIiBzdG9wLW9wYWNpdHk9Ii4xIi8+DQogICAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIuMSIvPg0KICAgIDwvbGluZWFyR3JhZGllbnQ+DQogICAgPG1hc2sgaWQ9ImEiPg0KICAgICAgICA8cmVjdCB3aWR0aD0iOTkiIGhlaWdodD0iMjAiIHJ4PSIzIiBmaWxsPSIjZmZmIi8+DQogICAgPC9tYXNrPg0KICAgIDxnIG1hc2s9InVybCgjYSkiPg0KICAgICAgICA8cGF0aCBmaWxsPSIjNTU1IiBkPSJNMCAwaDYzdjIwSDB6Ii8+DQogICAgICAgIDxwYXRoIGZpbGw9IiNhNGE2MWQiIGQ9Ik02MyAwaDM2djIwSDYzeiIvPg0KICAgICAgICA8cGF0aCBmaWxsPSJ1cmwoI2IpIiBkPSJNMCAwaDk5djIwSDB6Ii8+DQogICAgPC9nPg0KICAgIDxnIGZpbGw9IiNmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJEZWphVnUgU2FucyxWZXJkYW5hLEdlbmV2YSxzYW5zLXNlcmlmIiBmb250LXNpemU9IjExIj4NCiAgICAgICAgPHRleHQgeD0iMzEuNSIgeT0iMTUiIGZpbGw9IiMwMTAxMDEiIGZpbGwtb3BhY2l0eT0iLjMiPmNvdmVyYWdlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSIzMS41IiB5PSIxNCI+Y292ZXJhZ2U8L3RleHQ+DQogICAgICAgIDx0ZXh0IHg9IjgwIiB5PSIxNSIgZmlsbD0iIzAxMDEwMSIgZmlsbC1vcGFjaXR5PSIuMyI+ODQlPC90ZXh0Pg0KICAgICAgICA8dGV4dCB4PSI4MCIgeT0iMTQiPjg0JTwvdGV4dD4NCiAgICA8L2c+DQo8L3N2Zz4NCg==)](docs/coverage/html/) [(absolute link)](https://github.com/mivanit/muutils/tree/main/docs/coverage/html/) [(plain text)](https://github.com/mivanit/muutils/tree/main/docs/coverage/coverage.txt)



#### [`statcounter`](https://github.com/mivanit/muutils/tree/main/muutils/statcounter.py)

an extension of `collections.Counter` that provides "smart" computation of stats (mean, variance, median, other percentiles) from the counter object without using `Counter.elements()`

#### [`dictmagic`](https://github.com/mivanit/muutils/tree/main/muutils/dictmagic.py)

has utilities for working with dictionaries, like:

  - converting dotlist-dictionaries to nested dictionaries and back:
      ```python
      >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})
      {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
      >>> nested_dict_to_dotlist({'a': {'b': {'c': 1, 'd': 2}, 'e': 3}})
      {'a.b.c': 1, 'a.b.d': 2, 'a.e': 3}
      ```
  - `DefaulterDict` which works like a `defaultdict` but can generate the default value based on the key
  - `condense_tensor_dict` takes a dict of dotlist-tensors and gives a more human-readable summary:
      ```python
      >>> model = MyGPT()
      >>> print(condense_tensor_dict(model.named_parameters(), 'yaml'))
      ```
      ```yaml
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
	  <...>
      ```

#### [`kappa`](https://github.com/mivanit/muutils/tree/main/muutils/kappa.py)

Anonymous gettitem, so you can do things like

```python
>>> k = Kappa(lambda x: x**2)
>>> k[2]
4
```

#### [`sysinfo`](https://github.com/mivanit/muutils/tree/main/muutils/sysinfo.py)

utility for getting a bunch of system information. useful for logging.

#### `misc`:

contains a few utilities:
    - `stable_hash()` uses `hashlib.sha256` to compute a hash of an object that is stable across runs of python
    - `list_join` and `list_split` which behave like `str.join` and `str.split` but for lists
    - `sanitize_fname` and `dict_to_filename` for simplifying the creation of unique filename
    - `shorten_numerical_to_str()` and `str_to_numeric` turns numbers like `123456789` into `"123M"` and back
    - `freeze`, which prevents an object from being modified. Also see [gelidum](https://github.com/diegojromerolopez/gelidum/)


#### [`nbutils`](https://github.com/mivanit/muutils/tree/main/muutils/nbutils)

contains utilities for working with jupyter notebooks, such as:

- quickly converting notebooks to python scripts (and running those scripts) for testing in CI
- configuring notebooks, to make it easier to switch between figure output formats, locations, and more
- shorthand for displaying mermaid diagrams and TeX

#### [`json_serialize`](https://github.com/mivanit/muutils/tree/main/muutils/json_serialize.py)

a tool for serializing and loading arbitrary python objects into json. plays nicely with [`ZANJ`](https://github.com/mivanit/ZANJ/)


#### [`tensor_utils`]

contains minor utilities for working with pytorch tensors and numpy arrays, mostly for making type conversions easier

#### [`group_equiv`](https://github.com/mivanit/muutils/tree/main/muutils/group_equiv.py)

groups elements from a sequence according to a given equivalence relation, without assuming that the equivalence relation obeys the transitive property



#### [`jsonlines`](https://github.com/mivanit/muutils/tree/main/muutils/jsonlines.py)

an extremely simple utility for reading/writing `jsonl` files

#### [`ZANJ`](https://github.com/mivanit/ZANJ/)

is a human-readable and simple format for ML models, datasets, and arbitrary objects. It's build around having a zip file with `json` and `npy` files, and has been spun off into its [own project](https://github.com/mivanit/ZANJ/).

There are a couple work-in-progress utilities in [`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/) that aren't ready for anything, but nothing in this repo is suitable for production. Use at your own risk!



[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/__init__.py#L0-L26)








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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py)

# `muutils.dictmagic` { #muutils.dictmagic }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L0-L512)



### `class DefaulterDict(typing.Dict[~_KT, ~_VT], typing.Generic[~_KT, ~_VT]):` { #DefaulterDict }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L24-L41)


like a defaultdict, but default_factory is passed the key as an argument


- `default_factory: Callable[[~_KT], ~_VT] `




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


### `def defaultdict_to_dict_recursive` { #defaultdict_to_dict_recursive }
```python
(
    dd: Union[collections.defaultdict, muutils.dictmagic.DefaulterDict]
) -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L48-L57)


Convert a defaultdict or DefaulterDict to a normal dict, recursively


### `def dotlist_to_nested_dict` { #dotlist_to_nested_dict }
```python
(dot_dict: Dict[str, Any], sep: str = '.') -> Dict[str, Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L60-L80)


Convert a dict with dot-separated keys to a nested dict

Example:

    >>> dotlist_to_nested_dict({'a.b.c': 1, 'a.b.d': 2, 'a.e': 3})
    {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}


### `def nested_dict_to_dotlist` { #nested_dict_to_dotlist }
```python
(
    nested_dict: Dict[str, Any],
    sep: str = '.',
    allow_lists: bool = False
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L83-L113)




### `def update_with_nested_dict` { #update_with_nested_dict }
```python
(
    original: dict[str, typing.Any],
    update: dict[str, typing.Any]
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L116-L145)


Update a dict with a nested dict

Example:
>>> update_with_nested_dict({'a': {'b': 1}, "c": -1}, {'a': {"b": 2}})
{'a': {'b': 2}, 'c': -1}

### Arguments
- `original: dict[str, Any]`
    the dict to update (will be modified in-place)
- `update: dict[str, Any]`
    the dict to update with

### Returns
- `dict`
    the updated dict


### `def kwargs_to_nested_dict` { #kwargs_to_nested_dict }
```python
(
    kwargs_dict: dict[str, typing.Any],
    sep: str = '.',
    strip_prefix: Optional[str] = None,
    when_unknown_prefix: muutils.errormode.ErrorMode = ErrorMode.Warn,
    transform_key: Optional[Callable[[str], str]] = None
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L148-L202)


given kwargs from fire, convert them to a nested dict

if strip_prefix is not None, then all keys must start with the prefix. by default,
will warn if an unknown prefix is found, but can be set to raise an error or ignore it:
`when_unknown_prefix: ErrorMode`

Example:
```python
def main(**kwargs):
    print(kwargs_to_nested_dict(kwargs))
fire.Fire(main)
```
running the above script will give:
```bash
$ python test.py --a.b.c=1 --a.b.d=2 --a.e=3
{'a': {'b': {'c': 1, 'd': 2}, 'e': 3}}
```

### Arguments
- `kwargs_dict: dict[str, Any]`
    the kwargs dict to convert
- `sep: str = "."`
    the separator to use for nested keys
- `strip_prefix: Optional[str] = None`
    if not None, then all keys must start with this prefix
- `when_unknown_prefix: ErrorMode = ErrorMode.WARN`
    what to do when an unknown prefix is found
- `transform_key: Callable[[str], str] | None = None`
    a function to apply to each key before adding it to the dict (applied after stripping the prefix)


### `def is_numeric_consecutive` { #is_numeric_consecutive }
```python
(lst: list[str]) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L205-L211)


Check if the list of keys is numeric and consecutive.


### `def condense_nested_dicts_numeric_keys` { #condense_nested_dicts_numeric_keys }
```python
(data: dict[str, typing.Any]) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L214-L258)


condense a nested dict, by condensing numeric keys with matching values to ranges

### Examples:
```python
>>> condense_nested_dicts_numeric_keys({'1': 1, '2': 1, '3': 1, '4': 2, '5': 2, '6': 2})
{'[1-3]': 1, '[4-6]': 2}
>>> condense_nested_dicts_numeric_keys({'1': {'1': 'a', '2': 'a'}, '2': 'b'})
{"1": {"[1-2]": "a"}, "2": "b"}
```


### `def condense_nested_dicts_matching_values` { #condense_nested_dicts_matching_values }
```python
(
    data: dict[str, typing.Any],
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L261-L312)


condense a nested dict, by condensing keys with matching values

### Examples: TODO

### Parameters:
 - `data : dict[str, Any]`
    data to process
 - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
    a function to apply to each value before adding it to the dict (if it's not hashable)
    (defaults to `None`)


### `def condense_nested_dicts` { #condense_nested_dicts }
```python
(
    data: dict[str, typing.Any],
    condense_numeric_keys: bool = True,
    condense_matching_values: bool = True,
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L315-L350)


condense a nested dict, by condensing numeric or matching keys with matching values to ranges

combines the functionality of `condense_nested_dicts_numeric_keys()` and `condense_nested_dicts_matching_values()`

### NOTE: this process is not meant to be reversible, and is intended for pretty-printing and visualization purposes
it's not reversible because types are lost to make the printing pretty

### Parameters:
 - `data : dict[str, Any]`
    data to process
 - `condense_numeric_keys : bool`
    whether to condense numeric keys (e.g. "1", "2", "3") to ranges (e.g. "[1-3]")
   (defaults to `True`)
 - `condense_matching_values : bool`
    whether to condense keys with matching values
   (defaults to `True`)
 - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
    a function to apply to each value before adding it to the dict (if it's not hashable)
   (defaults to `None`)


### `def tuple_dims_replace` { #tuple_dims_replace }
```python
(
    t: tuple[int, ...],
    dims_names_map: Optional[dict[int, str]] = None
) -> tuple[typing.Union[int, str], ...]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L353-L359)




- `TensorDict = typing.Dict[str, ForwardRef('torch.Tensor|np.ndarray')]`




- `TensorIterable = typing.Iterable[typing.Tuple[str, ForwardRef('torch.Tensor|np.ndarray')]]`




- `TensorDictFormats = typing.Literal['dict', 'json', 'yaml', 'yml']`




### `def condense_tensor_dict` { #condense_tensor_dict }
```python
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


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L371-L513)


Convert a dictionary of tensors to a dictionary of shapes.

by default, values are converted to strings of their shapes (for nice printing).
If you want the actual shapes, set `shapes_convert = lambda x: x` or `shapes_convert = None`.

### Parameters:
 - `data : dict[str, "torch.Tensor|np.ndarray"] | Iterable[tuple[str, "torch.Tensor|np.ndarray"]]`
    a either a `TensorDict` dict from strings to tensors, or an `TensorIterable` iterable of (key, tensor) pairs (like you might get from a `dict().items())` )
 - `fmt : TensorDictFormats`
    format to return the result in -- either a dict, or dump to json/yaml directly for pretty printing. will crash if yaml is not installed.
    (defaults to `'dict'`)
 - `shapes_convert : Callable[[tuple], Any]`
    conversion of a shape tuple to a string or other format (defaults to turning it into a string and removing quotes)
    (defaults to `lambdax:str(x).replace('"', '').replace("'", '')`)
 - `drop_batch_dims : int`
    number of leading dimensions to drop from the shape
    (defaults to `0`)
 - `sep : str`
    separator to use for nested keys
    (defaults to `'.'`)
 - `dims_names_map : dict[int, str] | None`
    convert certain dimension values in shape. not perfect, can be buggy
    (defaults to `None`)
 - `condense_numeric_keys : bool`
    whether to condense numeric keys (e.g. "1", "2", "3") to ranges (e.g. "[1-3]"), passed on to `condense_nested_dicts`
    (defaults to `True`)
 - `condense_matching_values : bool`
    whether to condense keys with matching values, passed on to `condense_nested_dicts`
    (defaults to `True`)
 - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
    a function to apply to each value before adding it to the dict (if it's not hashable), passed on to `condense_nested_dicts`
    (defaults to `None`)
 - `return_format : TensorDictFormats | None`
    legacy alias for `fmt` kwarg

### Returns:
 - `str|dict[str, str|tuple[int, ...]]`
    dict if `return_format='dict'`, a string for `json` or `yaml` output

### Examples:
```python
>>> model = transformer_lens.HookedTransformer.from_pretrained("gpt2")
>>> print(condense_tensor_dict(model.named_parameters(), return_format='yaml'))
```
```yaml
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
 - `ValueError` :  if `return_format` is not one of 'dict', 'json', or 'yaml', or if you try to use 'yaml' output without having PyYAML installed







## API Documentation

 - [`WarningFunc`](#WarningFunc)
 - [`LoggingFunc`](#LoggingFunc)
 - [`GLOBAL_WARN_FUNC`](#GLOBAL_WARN_FUNC)
 - [`GLOBAL_LOG_FUNC`](#GLOBAL_LOG_FUNC)
 - [`custom_showwarning`](#custom_showwarning)
 - [`ErrorMode`](#ErrorMode)
 - [`ERROR_MODE_ALIASES`](#ERROR_MODE_ALIASES)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py)

# `muutils.errormode` { #muutils.errormode }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L0-L196)



### `class WarningFunc(typing.Protocol):` { #WarningFunc }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L10-L16)


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
@typing.runtime_checkable act as simple-minded runtime protocols that check
only the presence of given attributes, ignoring their type signatures.
Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...


### `WarningFunc` { #WarningFunc.__init__ }
```python
(*args, **kwargs)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L1757-L1783)




- `LoggingFunc = typing.Callable[[str], NoneType]`




### `def GLOBAL_WARN_FUNC` { #GLOBAL_WARN_FUNC }
```python
(unknown)
```



Issue a warning, or maybe ignore it or raise an exception.

message
  Text of the warning message.
category
  The Warning category subclass. Defaults to UserWarning.
stacklevel
  How far up the call stack to make this warning appear. A value of 2 for
  example attributes the warning to the caller of the code calling warn().
source
  If supplied, the destroyed object which emitted a ResourceWarning
skip_file_prefixes
  An optional tuple of module filename prefixes indicating frames to skip
  during stacklevel computations for stack frame attribution.


### `def GLOBAL_LOG_FUNC` { #GLOBAL_LOG_FUNC }
```python
(*args, sep=' ', end='\n', file=None, flush=False)
```



Prints the values to a stream, or to sys.stdout by default.

sep
  string inserted between values, default a space.
end
  string appended after the last value, default a newline.
file
  a file-like object (stream); defaults to the current sys.stdout.
flush
  whether to forcibly flush the stream.


### `def custom_showwarning` { #custom_showwarning }
```python
(
    message: Warning | str,
    category: Optional[Type[Warning]] = None,
    filename: str | None = None,
    lineno: int | None = None,
    file: Optional[TextIO] = None,
    line: Optional[str] = None
) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L25-L66)




### `class ErrorMode(enum.Enum):` { #ErrorMode }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L69-L169)




- `EXCEPT = ErrorMode.Except`




- `WARN = ErrorMode.Warn`




- `LOG = ErrorMode.Log`




- `IGNORE = ErrorMode.Ignore`




### `def process` { #ErrorMode.process }
```python
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


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L75-L118)




### `def from_any` { #ErrorMode.from_any }
```python
(
    cls,
    mode: str | muutils.errormode.ErrorMode,
    allow_aliases: bool = True,
    allow_prefix: bool = True
) -> muutils.errormode.ErrorMode
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L120-L152)




### `def serialize` { #ErrorMode.serialize }
```python
(self) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L160-L161)




### `def load` { #ErrorMode.load }
```python
(cls, data: str) -> muutils.errormode.ErrorMode
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/errormode.py#L163-L169)




### Inherited Members                                

- [`name`](#ErrorMode.name)
- [`value`](#ErrorMode.value)


- `ERROR_MODE_ALIASES: dict[str, muutils.errormode.ErrorMode] = {'except': ErrorMode.Except, 'warn': ErrorMode.Warn, 'log': ErrorMode.Log, 'ignore': ErrorMode.Ignore, 'e': ErrorMode.Except, 'error': ErrorMode.Except, 'err': ErrorMode.Except, 'raise': ErrorMode.Except, 'w': ErrorMode.Warn, 'warning': ErrorMode.Warn, 'l': ErrorMode.Log, 'print': ErrorMode.Log, 'output': ErrorMode.Log, 'show': ErrorMode.Log, 'display': ErrorMode.Log, 'i': ErrorMode.Ignore, 'silent': ErrorMode.Ignore, 'quiet': ErrorMode.Ignore, 'nothing': ErrorMode.Ignore}`









## API Documentation

 - [`group_by_equivalence`](#group_by_equivalence)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/group_equiv.py)

# `muutils.group_equiv` { #muutils.group_equiv }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/group_equiv.py#L0-L63)



### `def group_by_equivalence` { #group_by_equivalence }
```python
(
    items_in: Sequence[~T],
    eq_func: Callable[[~T, ~T], bool]
) -> list[list[~T]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/group_equiv.py#L9-L64)


group items by assuming that `eq_func` implies an equivalence relation but might not be transitive

so, if f(a,b) and f(b,c) then f(a,c) might be false, but we still want to put [a,b,c] in the same class

note that lists are used to avoid the need for hashable items, and to allow for duplicates

### Arguments
 - `items_in: Sequence[T]` the items to group
 - `eq_func: Callable[[T, T], bool]` a function that returns true if two items are equivalent. need not be transitive







## API Documentation

 - [`Number`](#Number)
 - [`Interval`](#Interval)
 - [`ClosedInterval`](#ClosedInterval)
 - [`OpenInterval`](#OpenInterval)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py)

# `muutils.interval` { #muutils.interval }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L0-L527)



- `Number = typing.Union[float, int]`




### `class Interval:` { #Interval }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L22-L514)


Represents a mathematical interval, open by default.

The Interval class can represent both open and closed intervals, as well as half-open intervals.
It supports various initialization methods and provides containment checks.

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


### `Interval` { #Interval.__init__ }
```python
(
    *args: Union[Sequence[Union[float, int]], float, int],
    is_closed: Optional[bool] = None,
    closed_L: Optional[bool] = None,
    closed_R: Optional[bool] = None
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L47-L152)




- `lower: Union[float, int] `




- `upper: Union[float, int] `




- `closed_L: bool `




- `closed_R: bool `




- `singleton_set: Optional[set[Union[float, int]]] `




- `is_closed: bool `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L154-L160)




- `is_open: bool `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L162-L168)




- `is_half_open: bool `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L170-L174)




- `is_singleton: bool `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L176-L178)




- `is_empty: bool `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L180-L182)




- `is_finite: bool `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L184-L186)




- `singleton: Union[float, int] `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L188-L192)




### `def get_empty` { #Interval.get_empty }
```python
() -> muutils.interval.Interval
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L194-L196)




### `def get_singleton` { #Interval.get_singleton }
```python
(value: Union[float, int]) -> muutils.interval.Interval
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L198-L202)




### `def numerical_contained` { #Interval.numerical_contained }
```python
(self, item: Union[float, int]) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L204-L213)




### `def interval_contained` { #Interval.interval_contained }
```python
(self, item: muutils.interval.Interval) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L215-L241)




### `def from_str` { #Interval.from_str }
```python
(cls, input_str: str) -> muutils.interval.Interval
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L261-L309)




### `def copy` { #Interval.copy }
```python
(self) -> muutils.interval.Interval
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L353-L360)




### `def size` { #Interval.size }
```python
(self) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L362-L374)


Returns the size of the interval.

### Returns:

 - `float`
    the size of the interval


### `def clamp` { #Interval.clamp }
```python
(self, value: Union[int, float], epsilon: float = 1e-10) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L376-L436)


Clamp the given value to the interval bounds.

For open bounds, the clamped value will be slightly inside the interval (by epsilon).

### Parameters:

 - `value : Union[int, float]`
   the value to clamp.
 - `epsilon : float`
   margin for open bounds
   (defaults to `_EPSILON`)

### Returns:

 - `float`
    the clamped value

### Raises:

 - `ValueError` : If the input value is NaN.


### `def intersection` { #Interval.intersection }
```python
(
    self,
    other: muutils.interval.Interval
) -> Optional[muutils.interval.Interval]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L438-L465)




### `def union` { #Interval.union }
```python
(self, other: muutils.interval.Interval) -> muutils.interval.Interval
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L467-L514)




### `class ClosedInterval(Interval):` { #ClosedInterval }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L517-L521)


Represents a mathematical interval, open by default.

The Interval class can represent both open and closed intervals, as well as half-open intervals.
It supports various initialization methods and provides containment checks.

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


### `ClosedInterval` { #ClosedInterval.__init__ }
```python
(*args: Union[Sequence[float], float], **kwargs: Any)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L518-L521)




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


### `class OpenInterval(Interval):` { #OpenInterval }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L524-L528)


Represents a mathematical interval, open by default.

The Interval class can represent both open and closed intervals, as well as half-open intervals.
It supports various initialization methods and provides containment checks.

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


### `OpenInterval` { #OpenInterval.__init__ }
```python
(*args: Union[Sequence[float], float], **kwargs: Any)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/interval.py#L525-L528)




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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py)

# `muutils.json_serialize` { #muutils.json_serialize }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L0-L35)



### `def json_serialize` { #json_serialize }
```python
(
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, list, Dict[str, Any], NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L319-L321)


serialize object to json-serializable object with default config


### `def serializable_dataclass` { #serializable_dataclass }
```python
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
    **kwargs
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L395-L668)


decorator to make a dataclass serializable. must also make it inherit from `SerializableDataclass`

types will be validated (like pydantic) unless `on_typecheck_mismatch` is set to `ErrorMode.IGNORE`

behavior of most kwargs matches that of `dataclasses.dataclass`, but with some additional kwargs

Returns the same class as was passed in, with dunder methods added based on the fields defined in the class.

Examines PEP 526 __annotations__ to determine fields.

If init is true, an __init__() method is added to the class. If repr is true, a __repr__() method is added. If order is true, rich comparison dunder methods are added. If unsafe_hash is true, a __hash__() method function is added. If frozen is true, fields may not be assigned to after instance creation.

```python
@serializable_dataclass(kw_only=True)
class Myclass(SerializableDataclass):
    a: int
    b: str
```
```python
>>> Myclass(a=1, b="q").serialize()
{'__format__': 'Myclass(SerializableDataclass)', 'a': 1, 'b': 'q'}
```

### Parameters:
 - `_cls : _type_`
   class to decorate. don't pass this arg, just use this as a decorator
   (defaults to `None`)
 - `init : bool`
   (defaults to `True`)
 - `repr : bool`
   (defaults to `True`)
 - `order : bool`
   (defaults to `False`)
 - `unsafe_hash : bool`
   (defaults to `False`)
 - `frozen : bool`
   (defaults to `False`)
 - `properties_to_serialize : Optional[list[str]]`
   **SerializableDataclass only:** which properties to add to the serialized data dict
   (defaults to `None`)
 - `register_handler : bool`
    **SerializableDataclass only:** if true, register the class with ZANJ for loading
   (defaults to `True`)
 - `on_typecheck_error : ErrorMode`
    **SerializableDataclass only:** what to do if type checking throws an exception (except, warn, ignore). If `ignore` and an exception is thrown, type validation will still return false
 - `on_typecheck_mismatch : ErrorMode`
    **SerializableDataclass only:** what to do if a type mismatch is found (except, warn, ignore). If `ignore`, type validation will return `True`

### Returns:
 - `_type_`
   _description_

### Raises:
 - `ValueError` : _description_
 - `ValueError` : _description_
 - `ValueError` : _description_
 - `AttributeError` : _description_
 - `ValueError` : _description_


### `def serializable_field` { #serializable_field }
```python
(*args, **kwargs)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L123-L179)


Create a new `SerializableField`. type hinting this func confuses mypy, so scroll down

```
default: Any | dataclasses._MISSING_TYPE = dataclasses.MISSING,
default_factory: Callable[[], Any]
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
```

### new Parameters:
- `serialize`: whether to serialize this field when serializing the class'
- `serialization_fn`: function taking the instance of the field and returning a serializable object. If not provided, will iterate through the `SerializerHandler`s defined in `<a href="json_serialize/json_serialize.html">muutils.json_serialize.json_serialize</a>`
- `loading_fn`: function taking the serialized object and returning the instance of the field. If not provided, will take object as-is.
- `deserialize_fn`: new alternative to `loading_fn`. takes only the field's value, not the whole class. if both `loading_fn` and `deserialize_fn` are provided, an error will be raised.

### Gotchas:
- `loading_fn` takes the dict of the **class**, not the field. if you wanted a `loading_fn` that does nothing, you'd write:

```python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        loading_fn=lambda x["my_field"]: int(x)
    )
```

using `deserialize_fn` instead:

```python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: int(x)
    )
```

In the above code, `my_field` is an int but will be serialized as a string.

note that if not using ZANJ, and you have a class inside a container, you MUST provide
`serialization_fn` and `loading_fn` to serialize and load the container.
ZANJ will automatically do this for you.


### `def arr_metadata` { #arr_metadata }
```python
(arr) -> dict[str, list[int] | str | int]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L34-L42)


get metadata for a numpy array


### `def load_array` { #load_array }
```python
(
    arr: Union[bool, int, float, str, list, Dict[str, Any], NoneType],
    array_mode: Optional[Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']] = None
) -> Any
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L153-L216)


load a json-serialized array, infer the mode if not specified


- `BASE_HANDLERS = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'))`




- `JSONitem = typing.Union[bool, int, float, str, list, typing.Dict[str, typing.Any], NoneType]`




### `class JsonSerializer:` { #JsonSerializer }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L223-L313)


Json serialization class (holds configs)

### Parameters:
- `array_mode : ArrayMode`
how to write arrays
(defaults to `"array_list_meta"`)
- `error_mode : ErrorMode`
what to do when we can't serialize an object (will use repr as fallback if "ignore" or "warn")
(defaults to `"except"`)
- `handlers_pre : MonoTuple[SerializerHandler]`
handlers to use before the default handlers
(defaults to `tuple()`)
- `handlers_default : MonoTuple[SerializerHandler]`
default handlers to use
(defaults to `DEFAULT_HANDLERS`)
- `write_only_format : bool`
changes "__format__" keys in output to "__write_format__" (when you want to serialize something in a way that zanj won't try to recover the object when loading)
(defaults to `False`)

### Raises:
- `ValueError`: on init, if `args` is not empty
- `SerializationException`: on `json_serialize()`, if any error occurs when trying to serialize an object and `error_mode` is set to `ErrorMode.EXCEPT"`


### `JsonSerializer` { #JsonSerializer.__init__ }
```python
(
    *args,
    array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim'] = 'array_list_meta',
    error_mode: muutils.errormode.ErrorMode = ErrorMode.Except,
    handlers_pre: None = (),
    handlers_default: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function _serialize_override_serialize_func>, uid='.serialize override', desc='objects with .serialize method'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='namedtuple -> dict', desc='namedtuples as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dataclass -> dict', desc='dataclasses as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='path -> str', desc='Path objects as posix strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='obj -> str(obj)', desc='directly serialize objects in `SERIALIZE_DIRECT_AS_STR` to strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='numpy.ndarray', desc='numpy arrays'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='torch.Tensor', desc='pytorch tensors'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='pandas.DataFrame', desc='pandas DataFrames'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(set, list, tuple, Iterable) -> list', desc='sets, lists, tuples, and Iterables as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='fallback', desc='fallback handler -- serialize object attributes and special functions as strings')),
    write_only_format: bool = False
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L249-L269)




- `array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim'] `




- `error_mode: muutils.errormode.ErrorMode `




- `write_only_format: bool `




- `handlers: None `




### `def json_serialize` { #JsonSerializer.json_serialize }
```python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, list, Dict[str, Any], NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L271-L301)




### `def hashify` { #JsonSerializer.hashify }
```python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = (),
    force: bool = True
) -> Union[bool, int, float, str, tuple]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L303-L313)


try to turn any object into something hashable


### `def try_catch` { #try_catch }
```python
(func: Callable)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L80-L93)


wraps the function to catch exceptions, returns serialized error message on exception

returned func will return normal result on success, or error message on exception


### `def dc_eq` { #dc_eq }
```python
(
    dc1,
    dc2,
    except_when_class_mismatch: bool = False,
    false_when_class_mismatch: bool = True,
    except_when_field_mismatch: bool = False
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L174-L260)


checks if two dataclasses which (might) hold numpy arrays are equal

    # Parameters:
    - `dc1`: the first dataclass
    - `dc2`: the second dataclass
    - `except_when_class_mismatch: bool`
        if `True`, will throw `TypeError` if the classes are different.
        if not, will return false by default or attempt to compare the fields if `false_when_class_mismatch` is `False`
        (default: `False`)
    - `false_when_class_mismatch: bool`
        only relevant if `except_when_class_mismatch` is `False`.
        if `True`, will return `False` if the classes are different.
        if `False`, will attempt to compare the fields.
    - `except_when_field_mismatch: bool`
        only relevant if `except_when_class_mismatch` is `False` and `false_when_class_mismatch` is `False`.
        if `True`, will throw `TypeError` if the fields are different.
        (default: `True`)

    # Returns:
    - `bool`: True if the dataclasses are equal, False otherwise

    # Raises:
    - `TypeError`: if the dataclasses are of different classes
    - `AttributeError`: if the dataclasses have different fields

```
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
```


### `class SerializableDataclass(abc.ABC):` { #SerializableDataclass }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L222-L363)


Base class for serializable dataclasses

only for linting and type checking, still need to call `serializable_dataclass` decorator


### `def serialize` { #SerializableDataclass.serialize }
```python
(self) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L228-L231)




### `def load` { #SerializableDataclass.load }
```python
(cls: Type[~T], data: Union[dict[str, Any], ~T]) -> ~T
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L233-L235)




### `def validate_fields_types` { #SerializableDataclass.validate_fields_types }
```python
(
    self,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L237-L242)




### `def validate_field_type` { #SerializableDataclass.validate_field_type }
```python
(
    self,
    field: muutils.json_serialize.serializable_field.SerializableField | str,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L244-L251)




### `def diff` { #SerializableDataclass.diff }
```python
(
    self,
    other: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    of_serialized: bool = False
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L259-L338)


get a rich and recursive diff between two instances of a serializable dataclass

```python
>>> Myclass(a=1, b=2).diff(Myclass(a=1, b=3))
{'b': {'self': 2, 'other': 3}}
>>> NestedClass(x="q1", y=Myclass(a=1, b=2)).diff(NestedClass(x="q2", y=Myclass(a=1, b=3)))
{'x': {'self': 'q1', 'other': 'q2'}, 'y': {'b': {'self': 2, 'other': 3}}}
```

### Parameters:
 - `other : SerializableDataclass`
   other instance to compare against
 - `of_serialized : bool`
   if true, compare serialized data and not raw values
   (defaults to `False`)

### Returns:
 - `dict[str, Any]`


### Raises:
 - `ValueError` : if the instances are not of the same type
 - `ValueError` : if the instances are `dataclasses.dataclass` but not `SerializableDataclass`


### `def update_from_nested_dict` { #SerializableDataclass.update_from_nested_dict }
```python
(self, nested_dict: dict[str, typing.Any])
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/__init__.py#L340-L355)


update the instance from a nested dict, useful for configuration from command line args

### Parameters:
    - `nested_dict : dict[str, Any]`
        nested dict to update the instance with







## API Documentation

 - [`ArrayMode`](#ArrayMode)
 - [`array_n_elements`](#array_n_elements)
 - [`arr_metadata`](#arr_metadata)
 - [`serialize_array`](#serialize_array)
 - [`infer_array_mode`](#infer_array_mode)
 - [`load_array`](#load_array)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py)

# `muutils.json_serialize.array` { #muutils.json_serialize.array }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py#L0-L215)



- `ArrayMode = typing.Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']`




### `def array_n_elements` { #array_n_elements }
```python
(arr) -> int
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py#L24-L31)


get the number of elements in an array


### `def arr_metadata` { #arr_metadata }
```python
(arr) -> dict[str, list[int] | str | int]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py#L34-L42)


get metadata for a numpy array


### `def serialize_array` { #serialize_array }
```python
(
    jser: "'JsonSerializer'",
    arr: numpy.ndarray,
    path: Union[str, Sequence[str | int]],
    array_mode: Optional[Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']] = None
) -> Union[bool, int, float, str, list, Dict[str, Any], NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py#L45-L119)


serialize a numpy or pytorch array in one of several modes

if the object is zero-dimensional, simply get the unique item

`array_mode: ArrayMode` can be one of:
- `list`: serialize as a list of values, no metadata (equivalent to `arr.tolist()`)
- `array_list_meta`: serialize dict with metadata, actual list under the key `data`
- `array_hex_meta`: serialize dict with metadata, actual hex string under the key `data`
- `array_b64_meta`: serialize dict with metadata, actual base64 string under the key `data`

for `array_list_meta`, `array_hex_meta`, and `array_b64_meta`, the serialized object is:
```
{
    "__format__": <array_list_meta|array_hex_meta>,
    "shape": arr.shape,
    "dtype": str(arr.dtype),
    "data": <arr.tolist()|arr.tobytes().hex()|base64.b64encode(arr.tobytes()).decode()>,
}
```

### Parameters:
 - `arr : Any` array to serialize
 - `array_mode : ArrayMode` mode in which to serialize the array
   (defaults to `None` and inheriting from `jser: JsonSerializer`)

### Returns:
 - `JSONitem`
   json serialized array

### Raises:
 - `KeyError` : if the array mode is not valid


### `def infer_array_mode` { #infer_array_mode }
```python
(
    arr: Union[bool, int, float, str, list, Dict[str, Any], NoneType]
) -> Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py#L122-L150)


given a serialized array, infer the mode

assumes the array was serialized via `serialize_array()`


### `def load_array` { #load_array }
```python
(
    arr: Union[bool, int, float, str, list, Dict[str, Any], NoneType],
    array_mode: Optional[Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim']] = None
) -> Any
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/array.py#L153-L216)


load a json-serialized array, infer the mode if not specified







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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py)

# `muutils.json_serialize.json_serialize` { #muutils.json_serialize.json_serialize }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L0-L320)



- `SERIALIZER_SPECIAL_KEYS: None = ('__name__', '__doc__', '__module__', '__class__', '__dict__', '__annotations__')`




- `SERIALIZER_SPECIAL_FUNCS: dict[str, typing.Callable] = {'str': <class 'str'>, 'dir': <built-in function dir>, 'type': <function <lambda>>, 'repr': <function <lambda>>, 'code': <function <lambda>>, 'sourcefile': <function <lambda>>}`




- `SERIALIZE_DIRECT_AS_STR: Set[str] = {"<class 'torch.dtype'>", "<class 'torch.device'>"}`




- `ObjectPath = tuple[typing.Union[str, int], ...]`




### `class SerializerHandler:` { #SerializerHandler }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L61-L98)


a handler for a specific type of object

### Parameters:
    - `check : Callable[[JsonSerializer, Any], bool]` takes a JsonSerializer and an object, returns whether to use this handler
    - `serialize : Callable[[JsonSerializer, Any, ObjectPath], JSONitem]` takes a JsonSerializer, an object, and the current path, returns the serialized object
    - `desc : str` description of the handler (optional)


### `SerializerHandler` { #SerializerHandler.__init__ }
```python
(
    check: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], bool],
    serialize_func: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], Union[bool, int, float, str, list, Dict[str, Any], NoneType]],
    uid: str,
    desc: str
)
```




- `check: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], bool] `




- `serialize_func: Callable[[muutils.json_serialize.json_serialize.JsonSerializer, Any, tuple[Union[str, int], ...]], Union[bool, int, float, str, list, Dict[str, Any], NoneType]] `




- `uid: str `




- `desc: str `




### `def serialize` { #SerializerHandler.serialize }
```python
(self) -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L80-L98)


serialize the handler info


- `BASE_HANDLERS: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'))`




- `DEFAULT_HANDLERS: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function _serialize_override_serialize_func>, uid='.serialize override', desc='objects with .serialize method'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='namedtuple -> dict', desc='namedtuples as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dataclass -> dict', desc='dataclasses as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='path -> str', desc='Path objects as posix strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='obj -> str(obj)', desc='directly serialize objects in `SERIALIZE_DIRECT_AS_STR` to strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='numpy.ndarray', desc='numpy arrays'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='torch.Tensor', desc='pytorch tensors'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='pandas.DataFrame', desc='pandas DataFrames'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(set, list, tuple, Iterable) -> list', desc='sets, lists, tuples, and Iterables as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='fallback', desc='fallback handler -- serialize object attributes and special functions as strings'))`




### `class JsonSerializer:` { #JsonSerializer }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L223-L313)


Json serialization class (holds configs)

### Parameters:
- `array_mode : ArrayMode`
how to write arrays
(defaults to `"array_list_meta"`)
- `error_mode : ErrorMode`
what to do when we can't serialize an object (will use repr as fallback if "ignore" or "warn")
(defaults to `"except"`)
- `handlers_pre : MonoTuple[SerializerHandler]`
handlers to use before the default handlers
(defaults to `tuple()`)
- `handlers_default : MonoTuple[SerializerHandler]`
default handlers to use
(defaults to `DEFAULT_HANDLERS`)
- `write_only_format : bool`
changes "__format__" keys in output to "__write_format__" (when you want to serialize something in a way that zanj won't try to recover the object when loading)
(defaults to `False`)

### Raises:
- `ValueError`: on init, if `args` is not empty
- `SerializationException`: on `json_serialize()`, if any error occurs when trying to serialize an object and `error_mode` is set to `ErrorMode.EXCEPT"`


### `JsonSerializer` { #JsonSerializer.__init__ }
```python
(
    *args,
    array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim'] = 'array_list_meta',
    error_mode: muutils.errormode.ErrorMode = ErrorMode.Except,
    handlers_pre: None = (),
    handlers_default: None = (SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='base types', desc='base types (bool, int, float, str, None)'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dictionaries', desc='dictionaries'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(list, tuple) -> list', desc='lists and tuples as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function _serialize_override_serialize_func>, uid='.serialize override', desc='objects with .serialize method'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='namedtuple -> dict', desc='namedtuples as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='dataclass -> dict', desc='dataclasses as dicts'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='path -> str', desc='Path objects as posix strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='obj -> str(obj)', desc='directly serialize objects in `SERIALIZE_DIRECT_AS_STR` to strings'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='numpy.ndarray', desc='numpy arrays'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='torch.Tensor', desc='pytorch tensors'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='pandas.DataFrame', desc='pandas DataFrames'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='(set, list, tuple, Iterable) -> list', desc='sets, lists, tuples, and Iterables as lists'), SerializerHandler(check=<function <lambda>>, serialize_func=<function <lambda>>, uid='fallback', desc='fallback handler -- serialize object attributes and special functions as strings')),
    write_only_format: bool = False
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L249-L269)




- `array_mode: Literal['list', 'array_list_meta', 'array_hex_meta', 'array_b64_meta', 'external', 'zero_dim'] `




- `error_mode: muutils.errormode.ErrorMode `




- `write_only_format: bool `




- `handlers: None `




### `def json_serialize` { #JsonSerializer.json_serialize }
```python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, list, Dict[str, Any], NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L271-L301)




### `def hashify` { #JsonSerializer.hashify }
```python
(
    self,
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = (),
    force: bool = True
) -> Union[bool, int, float, str, tuple]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L303-L313)


try to turn any object into something hashable


- `GLOBAL_JSON_SERIALIZER: muutils.json_serialize.json_serialize.JsonSerializer = <muutils.json_serialize.json_serialize.JsonSerializer object>`




### `def json_serialize` { #json_serialize }
```python
(
    obj: Any,
    path: tuple[typing.Union[str, int], ...] = ()
) -> Union[bool, int, float, str, list, Dict[str, Any], NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L319-L321)


serialize object to json-serializable object with default config







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
 - [`serializable_dataclass`](#serializable_dataclass)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py)

# `muutils.json_serialize.serializable_dataclass` { #muutils.json_serialize.serializable_dataclass }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L0-L667)



### `class CantGetTypeHintsWarning(builtins.UserWarning):` { #CantGetTypeHintsWarning }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L25-L26)


Base class for warnings generated by user code.


### Inherited Members                                

- [`UserWarning`](#CantGetTypeHintsWarning.__init__)

- [`with_traceback`](#CantGetTypeHintsWarning.with_traceback)
- [`add_note`](#CantGetTypeHintsWarning.add_note)
- [`args`](#CantGetTypeHintsWarning.args)


### `class ZanjMissingWarning(builtins.UserWarning):` { #ZanjMissingWarning }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L29-L30)


Base class for warnings generated by user code.


### Inherited Members                                

- [`UserWarning`](#ZanjMissingWarning.__init__)

- [`with_traceback`](#ZanjMissingWarning.with_traceback)
- [`add_note`](#ZanjMissingWarning.add_note)
- [`args`](#ZanjMissingWarning.args)


### `def zanj_register_loader_serializable_dataclass` { #zanj_register_loader_serializable_dataclass }
```python
(cls: Type[~T])
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L36-L72)


Register a serializable dataclass with the ZANJ backport


### TODO: there is some duplication here with register_loader_handler


### `class FieldIsNotInitOrSerializeWarning(builtins.UserWarning):` { #FieldIsNotInitOrSerializeWarning }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L79-L80)


Base class for warnings generated by user code.


### Inherited Members                                

- [`UserWarning`](#FieldIsNotInitOrSerializeWarning.__init__)

- [`with_traceback`](#FieldIsNotInitOrSerializeWarning.with_traceback)
- [`add_note`](#FieldIsNotInitOrSerializeWarning.add_note)
- [`args`](#FieldIsNotInitOrSerializeWarning.args)


### `def SerializableDataclass__validate_field_type` { #SerializableDataclass__validate_field_type }
```python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    field: muutils.json_serialize.serializable_field.SerializableField | str,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L83-L170)


given a dataclass, check the field matches the type hint

### Parameters:
 - `self : SerializableDataclass`
   `SerializableDataclass` instance
 - `field : SerializableField | str`
    field to validate, will get from `self.__dataclass_fields__` if an `str`
 - `on_typecheck_error : ErrorMode`
    what to do if type checking throws an exception (except, warn, ignore). If `ignore` and an exception is thrown, the function will return `False`
   (defaults to `_DEFAULT_ON_TYPECHECK_ERROR`)

### Returns:
 - `bool`
    if the field type is correct. `False` if the field type is incorrect or an exception is thrown and `on_typecheck_error` is `ignore`


### `def SerializableDataclass__validate_fields_types__dict` { #SerializableDataclass__validate_fields_types__dict }
```python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> dict[str, bool]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L173-L207)


validate the types of all the fields on a SerializableDataclass. calls `SerializableDataclass__validate_field_type` for each field

returns a dict of field names to bools, where the bool is if the field type is valid


### `def SerializableDataclass__validate_fields_types` { #SerializableDataclass__validate_fields_types }
```python
(
    self: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L210-L219)


validate the types of all the fields on a SerializableDataclass. calls `SerializableDataclass__validate_field_type` for each field


### `class SerializableDataclass(abc.ABC):` { #SerializableDataclass }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L222-L363)


Base class for serializable dataclasses

only for linting and type checking, still need to call `serializable_dataclass` decorator


### `def serialize` { #SerializableDataclass.serialize }
```python
(self) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L228-L231)




### `def load` { #SerializableDataclass.load }
```python
(cls: Type[~T], data: Union[dict[str, Any], ~T]) -> ~T
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L233-L235)




### `def validate_fields_types` { #SerializableDataclass.validate_fields_types }
```python
(
    self,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L237-L242)




### `def validate_field_type` { #SerializableDataclass.validate_field_type }
```python
(
    self,
    field: muutils.json_serialize.serializable_field.SerializableField | str,
    on_typecheck_error: muutils.errormode.ErrorMode = ErrorMode.Except
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L244-L251)




### `def diff` { #SerializableDataclass.diff }
```python
(
    self,
    other: muutils.json_serialize.serializable_dataclass.SerializableDataclass,
    of_serialized: bool = False
) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L259-L338)


get a rich and recursive diff between two instances of a serializable dataclass

```python
>>> Myclass(a=1, b=2).diff(Myclass(a=1, b=3))
{'b': {'self': 2, 'other': 3}}
>>> NestedClass(x="q1", y=Myclass(a=1, b=2)).diff(NestedClass(x="q2", y=Myclass(a=1, b=3)))
{'x': {'self': 'q1', 'other': 'q2'}, 'y': {'b': {'self': 2, 'other': 3}}}
```

### Parameters:
 - `other : SerializableDataclass`
   other instance to compare against
 - `of_serialized : bool`
   if true, compare serialized data and not raw values
   (defaults to `False`)

### Returns:
 - `dict[str, Any]`


### Raises:
 - `ValueError` : if the instances are not of the same type
 - `ValueError` : if the instances are `dataclasses.dataclass` but not `SerializableDataclass`


### `def update_from_nested_dict` { #SerializableDataclass.update_from_nested_dict }
```python
(self, nested_dict: dict[str, typing.Any])
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L340-L355)


update the instance from a nested dict, useful for configuration from command line args

### Parameters:
    - `nested_dict : dict[str, Any]`
        nested dict to update the instance with


### `def get_cls_type_hints_cached` { #get_cls_type_hints_cached }
```python
(cls: Type[~T]) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L368-L371)


cached typing.get_type_hints for a class


### `def get_cls_type_hints` { #get_cls_type_hints }
```python
(cls: Type[~T]) -> dict[str, typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L374-L391)




### `def serializable_dataclass` { #serializable_dataclass }
```python
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
    **kwargs
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L395-L668)


decorator to make a dataclass serializable. must also make it inherit from `SerializableDataclass`

types will be validated (like pydantic) unless `on_typecheck_mismatch` is set to `ErrorMode.IGNORE`

behavior of most kwargs matches that of `dataclasses.dataclass`, but with some additional kwargs

Returns the same class as was passed in, with dunder methods added based on the fields defined in the class.

Examines PEP 526 __annotations__ to determine fields.

If init is true, an __init__() method is added to the class. If repr is true, a __repr__() method is added. If order is true, rich comparison dunder methods are added. If unsafe_hash is true, a __hash__() method function is added. If frozen is true, fields may not be assigned to after instance creation.

```python
@serializable_dataclass(kw_only=True)
class Myclass(SerializableDataclass):
    a: int
    b: str
```
```python
>>> Myclass(a=1, b="q").serialize()
{'__format__': 'Myclass(SerializableDataclass)', 'a': 1, 'b': 'q'}
```

### Parameters:
 - `_cls : _type_`
   class to decorate. don't pass this arg, just use this as a decorator
   (defaults to `None`)
 - `init : bool`
   (defaults to `True`)
 - `repr : bool`
   (defaults to `True`)
 - `order : bool`
   (defaults to `False`)
 - `unsafe_hash : bool`
   (defaults to `False`)
 - `frozen : bool`
   (defaults to `False`)
 - `properties_to_serialize : Optional[list[str]]`
   **SerializableDataclass only:** which properties to add to the serialized data dict
   (defaults to `None`)
 - `register_handler : bool`
    **SerializableDataclass only:** if true, register the class with ZANJ for loading
   (defaults to `True`)
 - `on_typecheck_error : ErrorMode`
    **SerializableDataclass only:** what to do if type checking throws an exception (except, warn, ignore). If `ignore` and an exception is thrown, type validation will still return false
 - `on_typecheck_mismatch : ErrorMode`
    **SerializableDataclass only:** what to do if a type mismatch is found (except, warn, ignore). If `ignore`, type validation will return `True`

### Returns:
 - `_type_`
   _description_

### Raises:
 - `ValueError` : _description_
 - `ValueError` : _description_
 - `ValueError` : _description_
 - `AttributeError` : _description_
 - `ValueError` : _description_







## API Documentation

 - [`SerializableField`](#SerializableField)
 - [`serializable_field`](#serializable_field)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py)

# `muutils.json_serialize.serializable_field` { #muutils.json_serialize.serializable_field }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L0-L178)



### `class SerializableField(dataclasses.Field):` { #SerializableField }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L12-L119)


extension of `dataclasses.Field` with additional serialization properties


### `SerializableField` { #SerializableField.__init__ }
```python
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

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L37-L101)




- `serialize: bool `




- `serialization_fn: Optional[Callable[[Any], Any]] `




- `loading_fn: Optional[Callable[[Any], Any]] `




- `deserialize_fn: Optional[Callable[[Any], Any]] `




- `assert_type: bool `




- `custom_typecheck_fn: Optional[Callable[[<member 'type' of 'SerializableField' objects>], bool]] `




### `def from_Field` { #SerializableField.from_Field }
```python
(
    cls,
    field: dataclasses.Field
) -> muutils.json_serialize.serializable_field.SerializableField
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L103-L119)


copy all values from a `dataclasses.Field` to new `SerializableField`


- `name `




- `type `




- `default `




- `default_factory `




- `init `




- `repr `




- `hash `




- `compare `




- `metadata `




- `kw_only `




### `def serializable_field` { #serializable_field }
```python
(*args, **kwargs)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L123-L179)


Create a new `SerializableField`. type hinting this func confuses mypy, so scroll down

```
default: Any | dataclasses._MISSING_TYPE = dataclasses.MISSING,
default_factory: Callable[[], Any]
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
```

### new Parameters:
- `serialize`: whether to serialize this field when serializing the class'
- `serialization_fn`: function taking the instance of the field and returning a serializable object. If not provided, will iterate through the `SerializerHandler`s defined in `<a href="json_serialize.html">muutils.json_serialize.json_serialize</a>`
- `loading_fn`: function taking the serialized object and returning the instance of the field. If not provided, will take object as-is.
- `deserialize_fn`: new alternative to `loading_fn`. takes only the field's value, not the whole class. if both `loading_fn` and `deserialize_fn` are provided, an error will be raised.

### Gotchas:
- `loading_fn` takes the dict of the **class**, not the field. if you wanted a `loading_fn` that does nothing, you'd write:

```python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        loading_fn=lambda x["my_field"]: int(x)
    )
```

using `deserialize_fn` instead:

```python
class MyClass:
    my_field: int = serializable_field(
        serialization_fn=lambda x: str(x),
        deserialize_fn=lambda x: int(x)
    )
```

In the above code, `my_field` is an int but will be serialized as a string.

note that if not using ZANJ, and you have a class inside a container, you MUST provide
`serialization_fn` and `loading_fn` to serialize and load the container.
ZANJ will automatically do this for you.





## Contents
utilities for json_serialize


## API Documentation

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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py)

# `muutils.json_serialize.util` { #muutils.json_serialize.util }

utilities for json_serialize

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L0-L259)



- `JSONitem = typing.Union[bool, int, float, str, list, typing.Dict[str, typing.Any], NoneType]`




- `JSONdict = typing.Dict[str, typing.Union[bool, int, float, str, list, typing.Dict[str, typing.Any], NoneType]]`




- `Hashableitem = typing.Union[bool, int, float, str, tuple]`




### `class UniversalContainer:` { #UniversalContainer }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L58-L62)


contains everything -- `x in UniversalContainer()` is always True


### `def isinstance_namedtuple` { #isinstance_namedtuple }
```python
(x: Any) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L65-L77)


checks if `x` is a `namedtuple`

credit to https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple


### `def try_catch` { #try_catch }
```python
(func: Callable)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L80-L93)


wraps the function to catch exceptions, returns serialized error message on exception

returned func will return normal result on success, or error message on exception


### `class SerializationException(builtins.Exception):` { #SerializationException }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L110-L111)


Common base class for all non-exit exceptions.


### Inherited Members                                

- [`Exception`](#SerializationException.__init__)

- [`with_traceback`](#SerializationException.with_traceback)
- [`add_note`](#SerializationException.add_note)
- [`args`](#SerializationException.args)


### `def string_as_lines` { #string_as_lines }
```python
(s: str | None) -> list[str]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L114-L122)


for easier reading of long strings in json, split up by newlines

sort of like how jupyter notebooks do it


### `def safe_getsource` { #safe_getsource }
```python
(func) -> list[str]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L125-L129)




### `def array_safe_eq` { #array_safe_eq }
```python
(a: Any, b: Any) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L133-L171)


check if two objects are equal, account for if numpy arrays or torch tensors


### `def dc_eq` { #dc_eq }
```python
(
    dc1,
    dc2,
    except_when_class_mismatch: bool = False,
    false_when_class_mismatch: bool = True,
    except_when_field_mismatch: bool = False
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L174-L260)


checks if two dataclasses which (might) hold numpy arrays are equal

    # Parameters:
    - `dc1`: the first dataclass
    - `dc2`: the second dataclass
    - `except_when_class_mismatch: bool`
        if `True`, will throw `TypeError` if the classes are different.
        if not, will return false by default or attempt to compare the fields if `false_when_class_mismatch` is `False`
        (default: `False`)
    - `false_when_class_mismatch: bool`
        only relevant if `except_when_class_mismatch` is `False`.
        if `True`, will return `False` if the classes are different.
        if `False`, will attempt to compare the fields.
    - `except_when_field_mismatch: bool`
        only relevant if `except_when_class_mismatch` is `False` and `false_when_class_mismatch` is `False`.
        if `True`, will throw `TypeError` if the fields are different.
        (default: `True`)

    # Returns:
    - `bool`: True if the dataclasses are equal, False otherwise

    # Raises:
    - `TypeError`: if the dataclasses are of different classes
    - `AttributeError`: if the dataclasses have different fields

```
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
```


### `class MonoTuple:` { #MonoTuple }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L30-L55)


tuple type hint, but for a tuple of any length with all the same type







## API Documentation

 - [`jsonl_load`](#jsonl_load)
 - [`jsonl_load_log`](#jsonl_load_log)
 - [`jsonl_write`](#jsonl_write)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/jsonlines.py)

# `muutils.jsonlines` { #muutils.jsonlines }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/jsonlines.py#L0-L74)



### `def jsonl_load` { #jsonl_load }
```python
(
    path: str,
    /,
    *,
    use_gzip: bool | None = None
) -> list[typing.Union[bool, int, float, str, list, typing.Dict[str, typing.Any], NoneType]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/jsonlines.py#L28-L41)




### `def jsonl_load_log` { #jsonl_load_log }
```python
(path: str, /, *, use_gzip: bool | None = None) -> list[dict]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/jsonlines.py#L44-L58)




### `def jsonl_write` { #jsonl_write }
```python
(
    path: str,
    items: Sequence[Union[bool, int, float, str, list, Dict[str, Any], NoneType]],
    use_gzip: bool | None = None,
    gzip_compresslevel: int = 2
) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/jsonlines.py#L61-L75)







## Contents
anonymous getitem class

util for constructing a class which has a getitem method which just calls a function

a `lambda` is an anonymous function: kappa is the letter before lambda in the greek alphabet,
hence the name of this class


## API Documentation

 - [`Kappa`](#Kappa)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/kappa.py)

# `muutils.kappa` { #muutils.kappa }

anonymous getitem class

util for constructing a class which has a getitem method which just calls a function

a `lambda` is an anonymous function: kappa is the letter before lambda in the greek alphabet,
hence the name of this class

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/kappa.py#L0-L45)



### `class Kappa(typing.Mapping[~_kappa_K, ~_kappa_V]):` { #Kappa }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/kappa.py#L26-L46)


A Mapping is a generic container for associating key/value
pairs.

This class provides concrete generic implementations of all
methods except for __getitem__, __iter__, and __len__.


### `Kappa` { #Kappa.__init__ }
```python
(func_getitem: Callable[[~_kappa_K], ~_kappa_V])
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/kappa.py#L27-L33)




- `func_getitem `




- `doc `




### Inherited Members                                

- [`get`](#Kappa.get)
- [`keys`](#Kappa.keys)
- [`items`](#Kappa.items)
- [`values`](#Kappa.values)






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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py)

# `muutils.logger` { #muutils.logger }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L0-L19)



### `class Logger(muutils.logger.simplelogger.SimpleLogger):` { #Logger }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L40-L306)


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
- `keep_last_msg_time : bool`
        whether to keep the last message time
        (defaults to `True`)


### Raises:
        - `ValueError` : _description_


### `Logger` { #Logger.__init__ }
```python
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

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L71-L147)




### `def log` { #Logger.log }
```python
(
    self,
    msg: Union[bool, int, float, str, list, Dict[str, Any], NoneType] = None,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = False,
    extra_indent: str = '',
    **kwargs
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L158-L267)


logging function

##### Parameters:
 - `msg : JSONitem`
   message (usually string or dict) to be logged
 - `lvl : int | None`
   level of message (lower levels are more important)
   (defaults to `None`)
 - `console_print : bool`
   override `console_print_threshold` setting
   (defaults to `False`)
 - `stream : str | None`
   whether to log to a stream (defaults to `None`), which logs to the default `None` stream
   (defaults to `None`)


### `def log_elapsed_last` { #Logger.log_elapsed_last }
```python
(
    self,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = True,
    **kwargs
) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L269-L286)


logs the time elapsed since the last message was printed to the console (in any stream)


### `def flush_all` { #Logger.flush_all }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L288-L295)


flush all streams


### `class LoggingStream:` { #LoggingStream }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L11-L95)


properties of a logging stream

- `name: str` name of the stream
- `aliases: set[str]` aliases for the stream
        (calls to these names will be redirected to this stream. duplicate alises will result in errors)
        TODO: perhaps duplicate alises should result in duplicate writes?
- `file: str|bool|AnyIO|None` file to write to
        - if `None`, will write to standard log
        - if `True`, will write to `name + ".log"`
        - if `False` will "write" to `NullIO` (throw it away)
        - if a string, will write to that file
        - if a fileIO type object, will write to that object
- `default_level: int|None` default level for this stream
- `default_contents: dict[str, Callable[[], Any]]` default contents for this stream
- `last_msg: tuple[float, Any]|None` last message written to this stream (timestamp, message)


### `LoggingStream` { #LoggingStream.__init__ }
```python
(
    name: str | None,
    aliases: set[str | None] = <factory>,
    file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    default_level: int | None = None,
    default_contents: dict[str, typing.Callable[[], typing.Any]] = <factory>,
    handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None
)
```




- `name: str | None `




- `aliases: set[str | None] `




- `file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`




- `default_level: int | None = None`




- `default_contents: dict[str, typing.Callable[[], typing.Any]] `




- `handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`




### `def make_handler` { #LoggingStream.make_handler }
```python
(self) -> Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L40-L76)




### `class SimpleLogger:` { #SimpleLogger }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L34-L81)


logs training data to a jsonl file


### `SimpleLogger` { #SimpleLogger.__init__ }
```python
(
    log_path: str | None = None,
    log_file: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    timestamp: bool = True
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L37-L65)




### `def log` { #SimpleLogger.log }
```python
(
    self,
    msg: Union[bool, int, float, str, list, Dict[str, Any], NoneType],
    console_print: bool = False,
    **kwargs
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L67-L81)


log a message to the log file, and optionally to the console


### `class TimerContext:` { #TimerContext }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/__init__.py#L7-L22)


context manager for timing code


- `start_time: float `




- `end_time: float `




- `elapsed_time: float `









## API Documentation

 - [`ExceptionContext`](#ExceptionContext)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/exception_context.py)

# `muutils.logger.exception_context` { #muutils.logger.exception_context }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/exception_context.py#L0-L42)



### `class ExceptionContext:` { #ExceptionContext }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/exception_context.py#L6-L43)


context manager which catches all exceptions happening while the context is open, `.write()` the exception trace to the given stream, and then raises the exception


for example:

```python
errorfile = open('error.log', 'w')

with ExceptionContext(errorfile):
        # do something that might throw an exception
        # if it does, the exception trace will be written to errorfile
        # and then the exception will be raised
```


### `ExceptionContext` { #ExceptionContext.__init__ }
```python
(stream)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/exception_context.py#L23-L24)




- `stream `









## API Documentation

 - [`HeaderFunction`](#HeaderFunction)
 - [`md_header_function`](#md_header_function)
 - [`HEADER_FUNCTIONS`](#HEADER_FUNCTIONS)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/headerfuncs.py)

# `muutils.logger.headerfuncs` { #muutils.logger.headerfuncs }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/headerfuncs.py#L0-L67)



### `class HeaderFunction(typing.Protocol):` { #HeaderFunction }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/headerfuncs.py#L12-L13)


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
@typing.runtime_checkable act as simple-minded runtime protocols that check
only the presence of given attributes, ignoring their type signatures.
Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...


### `HeaderFunction` { #HeaderFunction.__init__ }
```python
(*args, **kwargs)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/headerfuncs.py#L1757-L1783)




### `def md_header_function` { #md_header_function }
```python
(
    msg: Any,
    lvl: int,
    stream: str | None = None,
    indent_lvl: str = '  ',
    extra_indent: str = '',
    **kwargs
) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/headerfuncs.py#L16-L63)


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









## API Documentation

 - [`get_any_from_stream`](#get_any_from_stream)
 - [`gather_log`](#gather_log)
 - [`gather_stream`](#gather_stream)
 - [`gather_val`](#gather_val)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/log_util.py)

# `muutils.logger.log_util` { #muutils.logger.log_util }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/log_util.py#L0-L79)



### `def get_any_from_stream` { #get_any_from_stream }
```python
(stream: list[dict], key: str) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/log_util.py#L4-L10)


get the first value of a key from a stream. errors if not found


### `def gather_log` { #gather_log }
```python
(file: str) -> dict[str, list[dict]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/log_util.py#L13-L24)


gathers and sorts all streams from a log


### `def gather_stream` { #gather_stream }
```python
(file: str, stream: str) -> list[dict]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/log_util.py#L27-L40)


gets all entries from a specific stream in a log file


### `def gather_val` { #gather_val }
```python
(
    file: str,
    stream: str,
    keys: tuple[str],
    allow_skip: bool = True
) -> list[list]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/log_util.py#L43-L80)


gather specific keys from a specific stream in a log file

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





## Contents
logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both console and a file
- `Logger` class handles levels in a slightly different way than default python `logging`,
        and also has "streams" which allow for different sorts of output in the same logger
        this was mostly made with training models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the duration of a block of code


## API Documentation

 - [`decode_level`](#decode_level)
 - [`Logger`](#Logger)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py)

# `muutils.logger.logger` { #muutils.logger.logger }

logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both console and a file
- `Logger` class handles levels in a slightly different way than default python `logging`,
        and also has "streams" which allow for different sorts of output in the same logger
        this was mostly made with training models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the duration of a block of code

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L0-L305)



### `def decode_level` { #decode_level }
```python
(level: int) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L27-L36)




### `class Logger(muutils.logger.simplelogger.SimpleLogger):` { #Logger }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L40-L306)


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
- `keep_last_msg_time : bool`
        whether to keep the last message time
        (defaults to `True`)


### Raises:
        - `ValueError` : _description_


### `Logger` { #Logger.__init__ }
```python
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

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L71-L147)




### `def log` { #Logger.log }
```python
(
    self,
    msg: Union[bool, int, float, str, list, Dict[str, Any], NoneType] = None,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = False,
    extra_indent: str = '',
    **kwargs
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L158-L267)


logging function

##### Parameters:
 - `msg : JSONitem`
   message (usually string or dict) to be logged
 - `lvl : int | None`
   level of message (lower levels are more important)
   (defaults to `None`)
 - `console_print : bool`
   override `console_print_threshold` setting
   (defaults to `False`)
 - `stream : str | None`
   whether to log to a stream (defaults to `None`), which logs to the default `None` stream
   (defaults to `None`)


### `def log_elapsed_last` { #Logger.log_elapsed_last }
```python
(
    self,
    lvl: int | None = None,
    stream: str | None = None,
    console_print: bool = True,
    **kwargs
) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L269-L286)


logs the time elapsed since the last message was printed to the console (in any stream)


### `def flush_all` { #Logger.flush_all }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L288-L295)


flush all streams







## API Documentation

 - [`LoggingStream`](#LoggingStream)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py)

# `muutils.logger.loggingstream` { #muutils.logger.loggingstream }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py#L0-L94)



### `class LoggingStream:` { #LoggingStream }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py#L11-L95)


properties of a logging stream

- `name: str` name of the stream
- `aliases: set[str]` aliases for the stream
        (calls to these names will be redirected to this stream. duplicate alises will result in errors)
        TODO: perhaps duplicate alises should result in duplicate writes?
- `file: str|bool|AnyIO|None` file to write to
        - if `None`, will write to standard log
        - if `True`, will write to `name + ".log"`
        - if `False` will "write" to `NullIO` (throw it away)
        - if a string, will write to that file
        - if a fileIO type object, will write to that object
- `default_level: int|None` default level for this stream
- `default_contents: dict[str, Callable[[], Any]]` default contents for this stream
- `last_msg: tuple[float, Any]|None` last message written to this stream (timestamp, message)


### `LoggingStream` { #LoggingStream.__init__ }
```python
(
    name: str | None,
    aliases: set[str | None] = <factory>,
    file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    default_level: int | None = None,
    default_contents: dict[str, typing.Callable[[], typing.Any]] = <factory>,
    handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None
)
```




- `name: str | None `




- `aliases: set[str | None] `




- `file: Union[str, bool, TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`




- `default_level: int | None = None`




- `default_contents: dict[str, typing.Callable[[], typing.Any]] `




- `handler: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None`




### `def make_handler` { #LoggingStream.make_handler }
```python
(self) -> Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py#L40-L76)









## API Documentation

 - [`NullIO`](#NullIO)
 - [`AnyIO`](#AnyIO)
 - [`SimpleLogger`](#SimpleLogger)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py)

# `muutils.logger.simplelogger` { #muutils.logger.simplelogger }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L0-L80)



### `class NullIO:` { #NullIO }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L12-L28)


null IO class


### `def write` { #NullIO.write }
```python
(self, msg: str) -> int
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L18-L20)


write to nothing! this throws away the message


### `def flush` { #NullIO.flush }
```python
(self) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L22-L24)


flush nothing! this is a no-op


### `def close` { #NullIO.close }
```python
(self) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L26-L28)


close nothing! this is a no-op


- `AnyIO = typing.Union[typing.TextIO, muutils.logger.simplelogger.NullIO]`




### `class SimpleLogger:` { #SimpleLogger }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L34-L81)


logs training data to a jsonl file


### `SimpleLogger` { #SimpleLogger.__init__ }
```python
(
    log_path: str | None = None,
    log_file: Union[TextIO, muutils.logger.simplelogger.NullIO, NoneType] = None,
    timestamp: bool = True
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L37-L65)




### `def log` { #SimpleLogger.log }
```python
(
    self,
    msg: Union[bool, int, float, str, list, Dict[str, Any], NoneType],
    console_print: bool = False,
    **kwargs
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/simplelogger.py#L67-L81)


log a message to the log file, and optionally to the console







## API Documentation

 - [`TimerContext`](#TimerContext)
 - [`filter_time_str`](#filter_time_str)
 - [`ProgressEstimator`](#ProgressEstimator)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py)

# `muutils.logger.timing` { #muutils.logger.timing }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L0-L86)



### `class TimerContext:` { #TimerContext }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L7-L22)


context manager for timing code


- `start_time: float `




- `end_time: float `




- `elapsed_time: float `




### `def filter_time_str` { #filter_time_str }
```python
(time: str) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L25-L30)


assuming format `h:mm:ss`, clips off the hours if its 0


### `class ProgressEstimator:` { #ProgressEstimator }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L33-L87)


estimates progress and can give a progress bar


### `ProgressEstimator` { #ProgressEstimator.__init__ }
```python
(
    n_total: int,
    pbar_fill: str = '█',
    pbar_empty: str = ' ',
    pbar_bounds: tuple[str, str] = ('|', '|')
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L36-L48)




- `n_total: int `




- `starttime: float `




- `pbar_fill: str `




- `pbar_empty: str `




- `pbar_bounds: tuple[str, str] `




- `total_str_len: int `




### `def get_timing_raw` { #ProgressEstimator.get_timing_raw }
```python
(self, i: int) -> dict[str, float]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L50-L59)


returns dict(elapsed, per_iter, remaining, percent)


### `def get_pbar` { #ProgressEstimator.get_pbar }
```python
(self, i: int, width: int = 30) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L61-L77)


returns a progress bar


### `def get_progress_default` { #ProgressEstimator.get_progress_default }
```python
(self, i: int) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L79-L87)


returns a progress string






## Submodules

- [`classes`](#classes)
- [`freezing`](#freezing)
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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py)

# `muutils.misc` { #muutils.misc }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L0-L71)



### `def stable_hash` { #stable_hash }
```python
(s: str) -> int
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L6-L12)


Returns a stable hash of the given string. not cryptographically secure, but stable between runs


- `WhenMissing = typing.Literal['except', 'skip', 'include']`




### `def empty_sequence_if_attr_false` { #empty_sequence_if_attr_false }
```python
(itr: Iterable[Any], attr_owner: Any, attr_name: str) -> Iterable[Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L21-L42)


Returns `itr` if `attr_owner` has the attribute `attr_name` and it boolean casts to `True`. Returns an empty sequence otherwise.

Particularly useful for optionally inserting delimiters into a sequence depending on an `TokenizerElement` attribute.

### Parameters:
- `itr: Iterable[Any]`
    The iterable to return if the attribute is `True`.
- `attr_owner: Any`
    The object to check for the attribute.
- `attr_name: str`
    The name of the attribute to check.

### Returns:
- `itr: Iterable` if `attr_owner` has the attribute `attr_name` and it boolean casts to `True`, otherwise an empty sequence.
- `()` an empty sequence if the attribute is `False` or not present.


### `def flatten` { #flatten }
```python
(it: Iterable[Any], levels_to_flatten: int | None = None) -> Generator
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L45-L68)


Flattens an arbitrarily nested iterable.
Flattens all iterable data types except for `str` and `bytes`.

### Returns
Generator over the flattened sequence.

### Parameters
- `it`: Any arbitrarily nested iterable.
- `levels_to_flatten`: Number of levels to flatten by, starting at the outermost layer. If `None`, performs full flattening.


### `def list_split` { #list_split }
```python
(lst: list, val: Any) -> list[list]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L75-L103)


split a list into sublists by `val`. similar to "a_b_c".split("_")

```python
>>> list_split([1,2,3,0,4,5,0,6], 0)
[[1, 2, 3], [4, 5], [6]]
>>> list_split([0,1,2,3], 0)
[[], [1, 2, 3]]
>>> list_split([1,2,3], 0)
[[1, 2, 3]]
>>> list_split([], 0)
[[]]
```


### `def list_join` { #list_join }
```python
(lst: list, factory: Callable) -> list
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L106-L128)


add a *new* instance of `factory()` between each element of `lst`

```python
>>> list_join([1,2,3], lambda : 0)
[1,0,2,0,3]
>>> list_join([1,2,3], lambda: [time.sleep(0.1), time.time()][1])
[1, 1600000000.0, 2, 1600000000.1, 3]
```


### `def apply_mapping` { #apply_mapping }
```python
(
    mapping: Mapping[~_AM_K, ~_AM_V],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L138-L184)


Given an iterable and a mapping, apply the mapping to the iterable with certain options

Gotcha: if `when_missing` is invalid, this is totally fine until a missing key is actually encountered.

Note: you can use this with `<a href="kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to pass a function instead of a dict

### Parameters:
 - `mapping : Mapping[_AM_K, _AM_V]`
    must have `__contains__` and `__getitem__`, both of which take `_AM_K` and the latter returns `_AM_V`
 - `iter : Iterable[_AM_K]`
    the iterable to apply the mapping to
 - `when_missing : WhenMissing`
    what to do when a key is missing from the mapping -- this is what distinguishes this function from `map`
    you can choose from `"skip"`, `"include"` (without converting), and `"except"`
   (defaults to `"skip"`)

### Returns:
return type is one of:
 - `list[_AM_V]` if `when_missing` is `"skip"` or `"except"`
 - `list[Union[_AM_K, _AM_V]]` if `when_missing` is `"include"`

### Raises:
 - `KeyError` : if the item is missing from the mapping and `when_missing` is `"except"`
 - `ValueError` : if `when_missing` is invalid


### `def apply_mapping_chain` { #apply_mapping_chain }
```python
(
    mapping: Mapping[~_AM_K, Iterable[~_AM_V]],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L187-L234)


Given an iterable and a mapping, chain the mappings together

Gotcha: if `when_missing` is invalid, this is totally fine until a missing key is actually encountered.

Note: you can use this with `<a href="kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to pass a function instead of a dict

### Parameters:
- `mapping : Mapping[_AM_K, Iterable[_AM_V]]`
    must have `__contains__` and `__getitem__`, both of which take `_AM_K` and the latter returns `Iterable[_AM_V]`
- `iter : Iterable[_AM_K]`
    the iterable to apply the mapping to
- `when_missing : WhenMissing`
    what to do when a key is missing from the mapping -- this is what distinguishes this function from `map`
    you can choose from `"skip"`, `"include"` (without converting), and `"except"`
(defaults to `"skip"`)

### Returns:
return type is one of:
 - `list[_AM_V]` if `when_missing` is `"skip"` or `"except"`
 - `list[Union[_AM_K, _AM_V]]` if `when_missing` is `"include"`

### Raises:
- `KeyError` : if the item is missing from the mapping and `when_missing` is `"except"`
- `ValueError` : if `when_missing` is invalid


### `def sanitize_name` { #sanitize_name }
```python
(
    name: str | None,
    additional_allowed_chars: str = '',
    replace_invalid: str = '',
    when_none: str | None = '_None_',
    leading_digit_prefix: str = ''
) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L7-L55)


sanitize a string, leaving only alphanumerics and `additional_allowed_chars`

### Parameters:
 - `name : str | None`
   input string
 - `additional_allowed_chars : str`
   additional characters to allow, none by default
   (defaults to `""`)
 - `replace_invalid : str`
    character to replace invalid characters with
   (defaults to `""`)
 - `when_none : str | None`
    string to return if `name` is `None`. if `None`, raises an exception
   (defaults to `"_None_"`)
 - `leading_digit_prefix : str`
    character to prefix the string with if it starts with a digit
   (defaults to `""`)

### Returns:
 - `str`
    sanitized string


### `def sanitize_fname` { #sanitize_fname }
```python
(fname: str | None, **kwargs) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L58-L63)


sanitize a filename to posix standards

- leave only alphanumerics, `_` (underscore), '-' (dash) and `.` (period)


### `def sanitize_identifier` { #sanitize_identifier }
```python
(fname: str | None, **kwargs) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L66-L74)


sanitize an identifier (variable or function name)

- leave only alphanumerics and `_` (underscore)
- prefix with `_` if it starts with a digit


### `def dict_to_filename` { #dict_to_filename }
```python
(
    data: dict,
    format_str: str = '{key}_{val}',
    separator: str = '.',
    max_length: int = 255
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L77-L99)




### `def dynamic_docstring` { #dynamic_docstring }
```python
(**doc_params)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L102-L108)




### `def shorten_numerical_to_str` { #shorten_numerical_to_str }
```python
(
    num: int | float,
    small_as_decimal: bool = True,
    precision: int = 1
) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L22-L46)


shorten a large numerical value to a string
1234 -> 1K

precision guaranteed to 1 in 10, but can be higher. reverse of `str_to_numeric`


### `def str_to_numeric` { #str_to_numeric }
```python
(
    quantity: str,
    mapping: None | bool | dict[str, int | float] = True
) -> int | float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L49-L165)


Convert a string representing a quantity to a numeric value.

The string can represent an integer, python float, fraction, or shortened via `shorten_numerical_to_str`.

### Examples:
```
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
```


- `_SHORTEN_MAP = {1000.0: 'K', 1000000.0: 'M', 1000000000.0: 'B', 1000000000000.0: 't', 1000000000000000.0: 'q', 1e+18: 'Q'}`




### `class FrozenDict(builtins.dict):` { #FrozenDict }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L4-L9)




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


### `class FrozenList(builtins.list):` { #FrozenList }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L12-L35)


Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.


### `def append` { #FrozenList.append }
```python
(self, value)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L19-L20)


Append object to the end of the list.


### `def extend` { #FrozenList.extend }
```python
(self, iterable)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L22-L23)


Extend list by appending elements from the iterable.


### `def insert` { #FrozenList.insert }
```python
(self, index, value)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L25-L26)


Insert object before index.


### `def remove` { #FrozenList.remove }
```python
(self, value)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L28-L29)


Remove first occurrence of value.

Raises ValueError if the value is not present.


### `def pop` { #FrozenList.pop }
```python
(self, index=-1)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L31-L32)


Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.


### `def clear` { #FrozenList.clear }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L34-L35)


Remove all items from list.


### Inherited Members                                

- [`list`](#FrozenList.__init__)
- [`copy`](#FrozenList.copy)
- [`index`](#FrozenList.index)
- [`count`](#FrozenList.count)
- [`reverse`](#FrozenList.reverse)
- [`sort`](#FrozenList.sort)


### `def freeze` { #freeze }
```python
(instance: object) -> object
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L38-L107)


recursively freeze an object in-place so that its attributes and elements cannot be changed

messy in the sense that sometimes the object is modified in place, but you can't rely on that. always use the return value.

the [gelidum](https://github.com/diegojromerolopez/gelidum/) package is a more complete implementation of this idea


### `def is_abstract` { #is_abstract }
```python
(cls: type) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L14-L23)


Returns if a class is abstract.


### `def get_all_subclasses` { #get_all_subclasses }
```python
(class_: type, include_self=False) -> set[type]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L26-L48)


Returns a set containing all child classes in the subclass graph of `class_`.
I.e., includes subclasses of subclasses, etc.

### Parameters
- `include_self`: Whether to include `class_` itself in the returned set
- `class_`: Superclass

### Development
Since most class hierarchies are small, the inefficiencies of the existing recursive implementation aren't problematic.
It might be valuable to refactor with memoization if the need arises to use this function on a very large class hierarchy.


### `def isinstance_by_type_name` { #isinstance_by_type_name }
```python
(o: object, type_name: str)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L51-L61)


Behaves like stdlib `isinstance` except it accepts a string representation of the type rather than the type itself.
This is a hacky function intended to circumvent the need to import a type into a module.
It is susceptible to type name collisions.

### Parameters
`o`: Object (not the type itself) whose type to interrogate
`type_name`: The string returned by `type_.__name__`.
Generic types are not supported, only types that would appear in `type_.__mro__`.


### `class IsDataclass(typing.Protocol):` { #IsDataclass }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L68-L72)


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
@typing.runtime_checkable act as simple-minded runtime protocols that check
only the presence of given attributes, ignoring their type signatures.
Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...


### `IsDataclass` { #IsDataclass.__init__ }
```python
(*args, **kwargs)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L1757-L1783)




### `def get_hashable_eq_attrs` { #get_hashable_eq_attrs }
```python
(dc: muutils.misc.classes.IsDataclass) -> tuple[typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L75-L83)


Returns a tuple of all fields used for equality comparison, including the type of the dataclass itself.
The type is included to preserve the unequal equality behavior of instances of different dataclasses whose fields are identical.
Essentially used to generate a hashable dataclass representation for equality comparison even if it's not frozen.


### `def dataclass_set_equals` { #dataclass_set_equals }
```python
(
    coll1: Iterable[muutils.misc.classes.IsDataclass],
    coll2: Iterable[muutils.misc.classes.IsDataclass]
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/__init__.py#L86-L97)


Compares 2 collections of dataclass instances as if they were sets.
Duplicates are ignored in the same manner as a set.
Unfrozen dataclasses can't be placed in sets since they're not hashable.
Collections of them may be compared using this function.







## API Documentation

 - [`is_abstract`](#is_abstract)
 - [`get_all_subclasses`](#get_all_subclasses)
 - [`isinstance_by_type_name`](#isinstance_by_type_name)
 - [`IsDataclass`](#IsDataclass)
 - [`get_hashable_eq_attrs`](#get_hashable_eq_attrs)
 - [`dataclass_set_equals`](#dataclass_set_equals)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py)

# `muutils.misc.classes` { #muutils.misc.classes }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L0-L96)



### `def is_abstract` { #is_abstract }
```python
(cls: type) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L14-L23)


Returns if a class is abstract.


### `def get_all_subclasses` { #get_all_subclasses }
```python
(class_: type, include_self=False) -> set[type]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L26-L48)


Returns a set containing all child classes in the subclass graph of `class_`.
I.e., includes subclasses of subclasses, etc.

### Parameters
- `include_self`: Whether to include `class_` itself in the returned set
- `class_`: Superclass

### Development
Since most class hierarchies are small, the inefficiencies of the existing recursive implementation aren't problematic.
It might be valuable to refactor with memoization if the need arises to use this function on a very large class hierarchy.


### `def isinstance_by_type_name` { #isinstance_by_type_name }
```python
(o: object, type_name: str)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L51-L61)


Behaves like stdlib `isinstance` except it accepts a string representation of the type rather than the type itself.
This is a hacky function intended to circumvent the need to import a type into a module.
It is susceptible to type name collisions.

### Parameters
`o`: Object (not the type itself) whose type to interrogate
`type_name`: The string returned by `type_.__name__`.
Generic types are not supported, only types that would appear in `type_.__mro__`.


### `class IsDataclass(typing.Protocol):` { #IsDataclass }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L68-L72)


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
@typing.runtime_checkable act as simple-minded runtime protocols that check
only the presence of given attributes, ignoring their type signatures.
Protocol classes can be generic, they are defined as::

    class GenProto[T](Protocol):
        def meth(self) -> T:
            ...


### `IsDataclass` { #IsDataclass.__init__ }
```python
(*args, **kwargs)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L1757-L1783)




### `def get_hashable_eq_attrs` { #get_hashable_eq_attrs }
```python
(dc: muutils.misc.classes.IsDataclass) -> tuple[typing.Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L75-L83)


Returns a tuple of all fields used for equality comparison, including the type of the dataclass itself.
The type is included to preserve the unequal equality behavior of instances of different dataclasses whose fields are identical.
Essentially used to generate a hashable dataclass representation for equality comparison even if it's not frozen.


### `def dataclass_set_equals` { #dataclass_set_equals }
```python
(
    coll1: Iterable[muutils.misc.classes.IsDataclass],
    coll2: Iterable[muutils.misc.classes.IsDataclass]
) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/classes.py#L86-L97)


Compares 2 collections of dataclass instances as if they were sets.
Duplicates are ignored in the same manner as a set.
Unfrozen dataclasses can't be placed in sets since they're not hashable.
Collections of them may be compared using this function.







## API Documentation

 - [`FrozenDict`](#FrozenDict)
 - [`FrozenList`](#FrozenList)
 - [`freeze`](#freeze)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py)

# `muutils.misc.freezing` { #muutils.misc.freezing }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L0-L106)



### `class FrozenDict(builtins.dict):` { #FrozenDict }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L4-L9)




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


### `class FrozenList(builtins.list):` { #FrozenList }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L12-L35)


Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.


### `def append` { #FrozenList.append }
```python
(self, value)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L19-L20)


Append object to the end of the list.


### `def extend` { #FrozenList.extend }
```python
(self, iterable)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L22-L23)


Extend list by appending elements from the iterable.


### `def insert` { #FrozenList.insert }
```python
(self, index, value)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L25-L26)


Insert object before index.


### `def remove` { #FrozenList.remove }
```python
(self, value)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L28-L29)


Remove first occurrence of value.

Raises ValueError if the value is not present.


### `def pop` { #FrozenList.pop }
```python
(self, index=-1)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L31-L32)


Remove and return item at index (default last).

Raises IndexError if list is empty or index is out of range.


### `def clear` { #FrozenList.clear }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L34-L35)


Remove all items from list.


### Inherited Members                                

- [`list`](#FrozenList.__init__)
- [`copy`](#FrozenList.copy)
- [`index`](#FrozenList.index)
- [`count`](#FrozenList.count)
- [`reverse`](#FrozenList.reverse)
- [`sort`](#FrozenList.sort)


### `def freeze` { #freeze }
```python
(instance: object) -> object
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/freezing.py#L38-L107)


recursively freeze an object in-place so that its attributes and elements cannot be changed

messy in the sense that sometimes the object is modified in place, but you can't rely on that. always use the return value.

the [gelidum](https://github.com/diegojromerolopez/gelidum/) package is a more complete implementation of this idea







## API Documentation

 - [`stable_hash`](#stable_hash)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/hashing.py)

# `muutils.misc.hashing` { #muutils.misc.hashing }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/hashing.py#L0-L11)



### `def stable_hash` { #stable_hash }
```python
(s: str) -> int
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/hashing.py#L6-L12)


Returns a stable hash of the given string. not cryptographically secure, but stable between runs







## API Documentation

 - [`shorten_numerical_to_str`](#shorten_numerical_to_str)
 - [`str_to_numeric`](#str_to_numeric)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/numerical.py)

# `muutils.misc.numerical` { #muutils.misc.numerical }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/numerical.py#L0-L164)



### `def shorten_numerical_to_str` { #shorten_numerical_to_str }
```python
(
    num: int | float,
    small_as_decimal: bool = True,
    precision: int = 1
) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/numerical.py#L22-L46)


shorten a large numerical value to a string
1234 -> 1K

precision guaranteed to 1 in 10, but can be higher. reverse of `str_to_numeric`


### `def str_to_numeric` { #str_to_numeric }
```python
(
    quantity: str,
    mapping: None | bool | dict[str, int | float] = True
) -> int | float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/numerical.py#L49-L165)


Convert a string representing a quantity to a numeric value.

The string can represent an integer, python float, fraction, or shortened via `shorten_numerical_to_str`.

### Examples:
```
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
```







## API Documentation

 - [`WhenMissing`](#WhenMissing)
 - [`empty_sequence_if_attr_false`](#empty_sequence_if_attr_false)
 - [`flatten`](#flatten)
 - [`list_split`](#list_split)
 - [`list_join`](#list_join)
 - [`apply_mapping`](#apply_mapping)
 - [`apply_mapping_chain`](#apply_mapping_chain)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py)

# `muutils.misc.sequence` { #muutils.misc.sequence }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L0-L233)



- `WhenMissing = typing.Literal['except', 'skip', 'include']`




### `def empty_sequence_if_attr_false` { #empty_sequence_if_attr_false }
```python
(itr: Iterable[Any], attr_owner: Any, attr_name: str) -> Iterable[Any]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L21-L42)


Returns `itr` if `attr_owner` has the attribute `attr_name` and it boolean casts to `True`. Returns an empty sequence otherwise.

Particularly useful for optionally inserting delimiters into a sequence depending on an `TokenizerElement` attribute.

### Parameters:
- `itr: Iterable[Any]`
    The iterable to return if the attribute is `True`.
- `attr_owner: Any`
    The object to check for the attribute.
- `attr_name: str`
    The name of the attribute to check.

### Returns:
- `itr: Iterable` if `attr_owner` has the attribute `attr_name` and it boolean casts to `True`, otherwise an empty sequence.
- `()` an empty sequence if the attribute is `False` or not present.


### `def flatten` { #flatten }
```python
(it: Iterable[Any], levels_to_flatten: int | None = None) -> Generator
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L45-L68)


Flattens an arbitrarily nested iterable.
Flattens all iterable data types except for `str` and `bytes`.

### Returns
Generator over the flattened sequence.

### Parameters
- `it`: Any arbitrarily nested iterable.
- `levels_to_flatten`: Number of levels to flatten by, starting at the outermost layer. If `None`, performs full flattening.


### `def list_split` { #list_split }
```python
(lst: list, val: Any) -> list[list]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L75-L103)


split a list into sublists by `val`. similar to "a_b_c".split("_")

```python
>>> list_split([1,2,3,0,4,5,0,6], 0)
[[1, 2, 3], [4, 5], [6]]
>>> list_split([0,1,2,3], 0)
[[], [1, 2, 3]]
>>> list_split([1,2,3], 0)
[[1, 2, 3]]
>>> list_split([], 0)
[[]]
```


### `def list_join` { #list_join }
```python
(lst: list, factory: Callable) -> list
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L106-L128)


add a *new* instance of `factory()` between each element of `lst`

```python
>>> list_join([1,2,3], lambda : 0)
[1,0,2,0,3]
>>> list_join([1,2,3], lambda: [time.sleep(0.1), time.time()][1])
[1, 1600000000.0, 2, 1600000000.1, 3]
```


### `def apply_mapping` { #apply_mapping }
```python
(
    mapping: Mapping[~_AM_K, ~_AM_V],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L138-L184)


Given an iterable and a mapping, apply the mapping to the iterable with certain options

Gotcha: if `when_missing` is invalid, this is totally fine until a missing key is actually encountered.

Note: you can use this with `<a href="../kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to pass a function instead of a dict

### Parameters:
 - `mapping : Mapping[_AM_K, _AM_V]`
    must have `__contains__` and `__getitem__`, both of which take `_AM_K` and the latter returns `_AM_V`
 - `iter : Iterable[_AM_K]`
    the iterable to apply the mapping to
 - `when_missing : WhenMissing`
    what to do when a key is missing from the mapping -- this is what distinguishes this function from `map`
    you can choose from `"skip"`, `"include"` (without converting), and `"except"`
   (defaults to `"skip"`)

### Returns:
return type is one of:
 - `list[_AM_V]` if `when_missing` is `"skip"` or `"except"`
 - `list[Union[_AM_K, _AM_V]]` if `when_missing` is `"include"`

### Raises:
 - `KeyError` : if the item is missing from the mapping and `when_missing` is `"except"`
 - `ValueError` : if `when_missing` is invalid


### `def apply_mapping_chain` { #apply_mapping_chain }
```python
(
    mapping: Mapping[~_AM_K, Iterable[~_AM_V]],
    iter: Iterable[~_AM_K],
    when_missing: Literal['except', 'skip', 'include'] = 'skip'
) -> list[typing.Union[~_AM_K, ~_AM_V]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L187-L234)


Given an iterable and a mapping, chain the mappings together

Gotcha: if `when_missing` is invalid, this is totally fine until a missing key is actually encountered.

Note: you can use this with `<a href="../kappa.html#Kappa">muutils.kappa.Kappa</a>` if you want to pass a function instead of a dict

### Parameters:
- `mapping : Mapping[_AM_K, Iterable[_AM_V]]`
    must have `__contains__` and `__getitem__`, both of which take `_AM_K` and the latter returns `Iterable[_AM_V]`
- `iter : Iterable[_AM_K]`
    the iterable to apply the mapping to
- `when_missing : WhenMissing`
    what to do when a key is missing from the mapping -- this is what distinguishes this function from `map`
    you can choose from `"skip"`, `"include"` (without converting), and `"except"`
(defaults to `"skip"`)

### Returns:
return type is one of:
 - `list[_AM_V]` if `when_missing` is `"skip"` or `"except"`
 - `list[Union[_AM_K, _AM_V]]` if `when_missing` is `"include"`

### Raises:
- `KeyError` : if the item is missing from the mapping and `when_missing` is `"except"`
- `ValueError` : if `when_missing` is invalid







## API Documentation

 - [`sanitize_name`](#sanitize_name)
 - [`sanitize_fname`](#sanitize_fname)
 - [`sanitize_identifier`](#sanitize_identifier)
 - [`dict_to_filename`](#dict_to_filename)
 - [`dynamic_docstring`](#dynamic_docstring)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py)

# `muutils.misc.string` { #muutils.misc.string }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py#L0-L107)



### `def sanitize_name` { #sanitize_name }
```python
(
    name: str | None,
    additional_allowed_chars: str = '',
    replace_invalid: str = '',
    when_none: str | None = '_None_',
    leading_digit_prefix: str = ''
) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py#L7-L55)


sanitize a string, leaving only alphanumerics and `additional_allowed_chars`

### Parameters:
 - `name : str | None`
   input string
 - `additional_allowed_chars : str`
   additional characters to allow, none by default
   (defaults to `""`)
 - `replace_invalid : str`
    character to replace invalid characters with
   (defaults to `""`)
 - `when_none : str | None`
    string to return if `name` is `None`. if `None`, raises an exception
   (defaults to `"_None_"`)
 - `leading_digit_prefix : str`
    character to prefix the string with if it starts with a digit
   (defaults to `""`)

### Returns:
 - `str`
    sanitized string


### `def sanitize_fname` { #sanitize_fname }
```python
(fname: str | None, **kwargs) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py#L58-L63)


sanitize a filename to posix standards

- leave only alphanumerics, `_` (underscore), '-' (dash) and `.` (period)


### `def sanitize_identifier` { #sanitize_identifier }
```python
(fname: str | None, **kwargs) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py#L66-L74)


sanitize an identifier (variable or function name)

- leave only alphanumerics and `_` (underscore)
- prefix with `_` if it starts with a digit


### `def dict_to_filename` { #dict_to_filename }
```python
(
    data: dict,
    format_str: str = '{key}_{val}',
    separator: str = '.',
    max_length: int = 255
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py#L77-L99)




### `def dynamic_docstring` { #dynamic_docstring }
```python
(**doc_params)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/misc/string.py#L102-L108)









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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py)

# `muutils.mlutils` { #muutils.mlutils }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L0-L162)



- `ARRAY_IMPORTS: bool = True`




- `DEFAULT_SEED: int = 42`




- `GLOBAL_SEED: int = 42`




### `def get_device` { #get_device }
```python
(device: Union[str, torch.device, NoneType] = None) -> torch.device
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L28-L72)


Get the torch.device instance on which `torch.Tensor`s should be allocated.


### `def set_reproducibility` { #set_reproducibility }
```python
(seed: int = 42)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L75-L95)


Improve model reproducibility. See https://github.com/NVIDIA/framework-determinism for more information.

Deterministic operations tend to have worse performance than nondeterministic operations, so this method trades
off performance for reproducibility. Set use_deterministic_algorithms to True to improve performance.


### `def chunks` { #chunks }
```python
(it, chunk_size)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L98-L103)


Yield successive chunks from an iterator.


### `def get_checkpoint_paths_for_run` { #get_checkpoint_paths_for_run }
```python
(
    run_path: pathlib.Path,
    extension: Literal['pt', 'zanj'],
    checkpoints_format: str = 'checkpoints/model.iter_*.{extension}'
) -> list[tuple[int, pathlib.Path]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L106-L125)


get checkpoints of the format from the run_path

note that `checkpoints_format` should contain a glob pattern with:
 - unresolved "{extension}" format term for the extension
 - a wildcard for the iteration number


### `def register_method` { #register_method }
```python
(
    method_dict: dict[str, typing.Callable[..., typing.Any]],
    custom_name: Optional[str] = None
) -> Callable[[~F], ~F]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L131-L159)


Decorator to add a method to the method_dict


### `def pprint_summary` { #pprint_summary }
```python
(summary: dict)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/mlutils.py#L162-L163)








## Submodules

- [`configure_notebook`](#configure_notebook)
- [`convert_ipynb_to_script`](#convert_ipynb_to_script)
- [`mermaid`](#mermaid)
- [`print_tex`](#print_tex)
- [`run_notebook_tests`](#run_notebook_tests)

## API Documentation

 - [`mm`](#mm)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/__init__.py)

# `muutils.nbutils` { #muutils.nbutils }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/__init__.py#L0-L11)



### `def mm` { #mm }
```python
(graph)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/__init__.py#L13-L18)


for plotting mermaid.js diagrams







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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py)

# `muutils.nbutils.configure_notebook` { #muutils.nbutils.configure_notebook }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L0-L283)



### `class PlotlyNotInstalledWarning(builtins.UserWarning):` { #PlotlyNotInstalledWarning }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L10-L11)


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




### `class UnknownFigureFormatWarning(builtins.UserWarning):` { #UnknownFigureFormatWarning }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L53-L54)


Base class for warnings generated by user code.


### Inherited Members                                

- [`UserWarning`](#UnknownFigureFormatWarning.__init__)

- [`with_traceback`](#UnknownFigureFormatWarning.with_traceback)
- [`add_note`](#UnknownFigureFormatWarning.add_note)
- [`args`](#UnknownFigureFormatWarning.args)


### `def universal_savefig` { #universal_savefig }
```python
(fname: str, fmt: str | None = None) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L57-L81)




### `def setup_plots` { #setup_plots }
```python
(
    plot_mode: Literal['ignore', 'inline', 'widget', 'save'] = 'inline',
    fig_output_fmt: str | None = 'pdf',
    fig_numbered_fname: str = 'figure-{num}',
    fig_config: dict | None = None,
    fig_basepath: str | None = None,
    close_after_plotshow: bool = False
) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L84-L187)


Set up plot saving/rendering options


### `def configure_notebook` { #configure_notebook }
```python
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


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L190-L248)


Shared Jupyter notebook setup steps:
- Set random seeds and library reproducibility settings
- Set device based on availability
- Set module reloading before code execution
- Set plot formatting
- Set plot saving/rendering options


### `def plotshow` { #plotshow }
```python
(
    fname: str | None = None,
    plot_mode: Optional[Literal['ignore', 'inline', 'widget', 'save']] = None,
    fmt: str | None = None
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/configure_notebook.py#L251-L284)


Show the active plot, depending on global configs







## API Documentation

 - [`DISABLE_PLOTS`](#DISABLE_PLOTS)
 - [`DISABLE_PLOTS_WARNING`](#DISABLE_PLOTS_WARNING)
 - [`disable_plots_in_script`](#disable_plots_in_script)
 - [`convert_ipynb`](#convert_ipynb)
 - [`process_file`](#process_file)
 - [`process_dir`](#process_dir)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/convert_ipynb_to_script.py)

# `muutils.nbutils.convert_ipynb_to_script` { #muutils.nbutils.convert_ipynb_to_script }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/convert_ipynb_to_script.py#L0-L370)



- `DISABLE_PLOTS: dict[str, list[str]] = {'matplotlib': ['\n# ------------------------------------------------------------\n# Disable matplotlib plots, done during processing by `convert_ipynb_to_script.py`\nimport matplotlib.pyplot as plt\nplt.show = lambda: None\n# ------------------------------------------------------------\n'], 'circuitsvis': ['\n# ------------------------------------------------------------\n# Disable circuitsvis plots, done during processing by `convert_ipynb_to_script.py`\nfrom circuitsvis.utils.convert_props import PythonProperty, convert_props\nfrom circuitsvis.utils.render import RenderedHTML, render, render_cdn, render_local\n\ndef new_render(\n    react_element_name: str,\n    **kwargs: PythonProperty\n) -> RenderedHTML:\n    "return a visualization as raw HTML"\n    local_src = render_local(react_element_name, **kwargs)\n    cdn_src = render_cdn(react_element_name, **kwargs)\n    # return as string instead of RenderedHTML for CI\n    return str(RenderedHTML(local_src, cdn_src))\n\nrender = new_render\n# ------------------------------------------------------------\n'], 'muutils': ['import muutils.nbutils.configure_notebook as nb_conf\nnb_conf.CONVERSION_PLOTMODE_OVERRIDE = "ignore"\n']}`




- `DISABLE_PLOTS_WARNING: list[str] = ["# ------------------------------------------------------------\n# WARNING: this script is auto-generated by `convert_ipynb_to_script.py`\n# showing plots has been disabled, so this is presumably in a temp dict for CI or something\n# so don't modify this code, it will be overwritten!\n# ------------------------------------------------------------\n"]`




### `def disable_plots_in_script` { #disable_plots_in_script }
```python
(script_lines: list[str]) -> list[str]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/convert_ipynb_to_script.py#L61-L145)


Disable plots in a script by adding cursed things after the import statements


### `def convert_ipynb` { #convert_ipynb }
```python
(
    notebook: dict,
    strip_md_cells: bool = False,
    header_comment: str = '#%%',
    disable_plots: bool = False,
    filter_out_lines: Union[str, Sequence[str]] = ('%', '!')
) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/convert_ipynb_to_script.py#L148-L205)


Convert Jupyter Notebook to a script, doing some basic filtering and formatting.

### Arguments
    - `notebook: dict`: Jupyter Notebook loaded as json.
    - `strip_md_cells: bool = False`: Remove markdown cells from the output script.
    - `header_comment: str = r'#%%'`: Comment string to separate cells in the output script.
    - `disable_plots: bool = False`: Disable plots in the output script.
    - `filter_out_lines: str|typing.Sequence[str] = ('%', '!')`: comment out lines starting with these strings (in code blocks).
        if a string is passed, it will be split by char and each char will be treated as a separate filter.

### Returns
    - `str`: Converted script.


### `def process_file` { #process_file }
```python
(
    in_file: str,
    out_file: str | None = None,
    strip_md_cells: bool = False,
    header_comment: str = '#%%',
    disable_plots: bool = False,
    filter_out_lines: Union[str, Sequence[str]] = ('%', '!')
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/convert_ipynb_to_script.py#L208-L240)




### `def process_dir` { #process_dir }
```python
(
    input_dir: str,
    output_dir: str,
    strip_md_cells: bool = False,
    header_comment: str = '#%%',
    disable_plots: bool = False,
    filter_out_lines: Union[str, Sequence[str]] = ('%', '!')
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/convert_ipynb_to_script.py#L243-L304)


Convert all Jupyter Notebooks in a directory to scripts.

### Arguments
    - `input_dir: str`: Input directory.
    - `output_dir: str`: Output directory.
    - `strip_md_cells: bool = False`: Remove markdown cells from the output script.
    - `header_comment: str = r'#%%'`: Comment string to separate cells in the output script.
    - `disable_plots: bool = False`: Disable plots in the output script.
    - `filter_out_lines: str|typing.Sequence[str] = ('%', '!')`: comment out lines starting with these strings (in code blocks).
        if a string is passed, it will be split by char and each char will be treated as a separate filter.







## API Documentation

 - [`mm`](#mm)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/mermaid.py)

# `muutils.nbutils.mermaid` { #muutils.nbutils.mermaid }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/mermaid.py#L0-L17)



### `def mm` { #mm }
```python
(graph)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/mermaid.py#L13-L18)


for plotting mermaid.js diagrams







## API Documentation

 - [`print_tex`](#print_tex)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/print_tex.py)

# `muutils.nbutils.print_tex` { #muutils.nbutils.print_tex }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/print_tex.py#L0-L18)



### `def print_tex` { #print_tex }
```python
(
    expr: sympy.core.expr.Expr,
    name: str | None = None,
    plain: bool = False,
    rendered: bool = True
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/print_tex.py#L5-L19)


function for easily rendering a sympy expression in latex







## API Documentation

 - [`NotebookTestError`](#NotebookTestError)
 - [`run_notebook_tests`](#run_notebook_tests)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/run_notebook_tests.py)

# `muutils.nbutils.run_notebook_tests` { #muutils.nbutils.run_notebook_tests }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/run_notebook_tests.py#L0-L150)



### `class NotebookTestError(builtins.Exception):` { #NotebookTestError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/run_notebook_tests.py#L9-L10)


Common base class for all non-exit exceptions.


### Inherited Members                                

- [`Exception`](#NotebookTestError.__init__)

- [`with_traceback`](#NotebookTestError.with_traceback)
- [`add_note`](#NotebookTestError.add_note)
- [`args`](#NotebookTestError.args)


### `def run_notebook_tests` { #run_notebook_tests }
```python
(
    notebooks_dir: pathlib.Path,
    converted_notebooks_temp_dir: pathlib.Path,
    CI_output_suffix: str = '.CI-output.txt',
    run_python_cmd: str = 'poetry run python',
    exit_on_first_fail: bool = False
)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/nbutils/run_notebook_tests.py#L13-L127)







## Contents
decorator `spinner_decorator` and context manager `SpinnerContext` to display
a spinner using the base `Spinner` class while some code is running.


## API Documentation

 - [`DecoratedFunction`](#DecoratedFunction)
 - [`SPINNER_CHARS`](#SPINNER_CHARS)
 - [`SPINNER_COMPLETE`](#SPINNER_COMPLETE)
 - [`Spinner`](#Spinner)
 - [`SpinnerContext`](#SpinnerContext)
 - [`spinner_decorator`](#spinner_decorator)
 - [`NoOpContextManager`](#NoOpContextManager)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py)

# `muutils.spinner` { #muutils.spinner }

decorator `spinner_decorator` and context manager `SpinnerContext` to display
a spinner using the base `Spinner` class while some code is running.

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L0-L425)



- `DecoratedFunction = ~DecoratedFunction`


Define a generic type for the decorated function


- `SPINNER_CHARS: Dict[str, Sequence[str]] = {'default': ['|', '/', '-', '\\'], 'dots': ['.  ', '.. ', '...'], 'bars': ['|  ', '|| ', '|||'], 'arrows': ['<', '^', '>', 'v'], 'arrows_2': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'], 'bouncing_bar': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[ ===]', '[  ==]', '[   =]'], 'bouncing_ball': ['( ●    )', '(  ●   )', '(   ●  )', '(    ● )', '(     ●)', '(    ● )', '(   ●  )', '(  ●   )', '( ●    )', '(●     )'], 'ooo': ['.', 'o', 'O', 'o'], 'braille': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'], 'clock': ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚'], 'hourglass': ['⏳', '⌛'], 'square_corners': ['◰', '◳', '◲', '◱'], 'triangle': ['◢', '◣', '◤', '◥'], 'square_dot': ['⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽', '⣾'], 'box_bounce': ['▌', '▀', '▐', '▄'], 'hamburger': ['☱', '☲', '☴'], 'earth': ['🌍', '🌎', '🌏'], 'growing_dots': ['⣀', '⣄', '⣤', '⣦', '⣶', '⣷', '⣿'], 'dice': ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'], 'wifi': ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'], 'bounce': ['⠁', '⠂', '⠄', '⠂'], 'arc': ['◜', '◠', '◝', '◞', '◡', '◟'], 'toggle': ['⊶', '⊷'], 'toggle2': ['▫', '▪'], 'toggle3': ['□', '■'], 'toggle4': ['■', '□', '▪', '▫'], 'toggle5': ['▮', '▯'], 'toggle7': ['⦾', '⦿'], 'toggle8': ['◍', '◌'], 'toggle9': ['◉', '◎'], 'arrow2': ['⬆️ ', '↗️ ', '➡️ ', '↘️ ', '⬇️ ', '↙️ ', '⬅️ ', '↖️ '], 'point': ['∙∙∙', '●∙∙', '∙●∙', '∙∙●', '∙∙∙'], 'layer': ['-', '=', '≡'], 'speaker': ['🔈 ', '🔉 ', '🔊 ', '🔉 '], 'orangePulse': ['🔸 ', '🔶 ', '🟠 ', '🟠 ', '🔷 '], 'bluePulse': ['🔹 ', '🔷 ', '🔵 ', '🔵 ', '🔷 '], 'satellite_signal': ['📡   ', '📡·  ', '📡·· ', '📡···', '📡 ··', '📡  ·'], 'rocket_orbit': ['🌍🚀  ', '🌏 🚀 ', '🌎  🚀'], 'ogham': ['ᚁ ', 'ᚂ ', 'ᚃ ', 'ᚄ', 'ᚅ'], 'eth': ['᛫', '፡', '፥', '፤', '፧', '።', '፨']}`


dict of spinner sequences to show. some from Claude 3.5 Sonnet,
some from [cli-spinners](https://github.com/sindresorhus/cli-spinners)


- `SPINNER_COMPLETE: Dict[str, str] = {'default': '#', 'dots': '***', 'bars': '|||', 'bouncing_bar': '[====]', 'bouncing_ball': '(●●●●●●)', 'braille': '⣿', 'clock': '✔️', 'hourglass': '✔️', 'square_corners': '◼', 'triangle': '◆', 'square_dot': '⣿', 'box_bounce': '■', 'hamburger': '☰', 'earth': '✔️', 'growing_dots': '⣿', 'dice': '🎲', 'wifi': '✔️', 'arc': '○', 'toggle': '-', 'toggle2': '▪', 'toggle3': '■', 'toggle4': '■', 'toggle5': '▮', 'toggle6': '၀', 'toggle7': '⦿', 'toggle8': '◍', 'toggle9': '◉', 'arrow2': '➡️', 'point': '●●●', 'layer': '≡', 'speaker': '🔊', 'orangePulse': '🟠', 'bluePulse': '🔵', 'satellite_signal': '📡 ✔️ ', 'rocket_orbit': '🌍  ✨', 'ogham': '᚛᚜', 'eth': '፠'}`


string to display when the spinner is complete


### `class Spinner:` { #Spinner }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L125-L331)


displays a spinner, and optionally elapsed time and a mutable value while a function is running.

### Parameters:
- `spinner_chars : Union[str, Sequence[str]]`
sequence of strings, or key to look up in `SPINNER_CHARS`, to use as the spinner characters
(defaults to `"default"`)
- `update_interval : float`
how often to update the spinner display in seconds
(defaults to `0.1`)
- `spinner_complete : str`
string to display when the spinner is complete
(defaults to looking up `spinner_chars` in `SPINNER_COMPLETE` or `"#"`)
- `initial_value : str`
initial value to display with the spinner
(defaults to `""`)
- `message : str`
message to display with the spinner
(defaults to `""`)
- `format_string : str`
string to format the spinner with. must have `"\r"` prepended to clear the line.
allowed keys are `spinner`, `elapsed_time`, `message`, and `value`
(defaults to `"\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
- `output_stream : TextIO`
stream to write the spinner to
(defaults to `sys.stdout`)
- `format_string_when_updated : Union[bool,str]`
whether to use a different format string when the value is updated.
if `True`, use the default format string with a newline appended. if a string, use that string.
this is useful if you want update_value to print to console and be preserved.
(defaults to `False`)

### Methods:
- `update_value(value: Any) -> None`
    update the current value displayed by the spinner

### Usage:

#### As a context manager:
```python
with SpinnerContext() as sp:
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
```

#### As a decorator:
```python
@spinner_decorator
def long_running_function():
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
    return "Function completed"
```


### `Spinner` { #Spinner.__init__ }
```python
(
    *args,
    spinner_chars: Union[str, Sequence[str]] = 'default',
    update_interval: float = 0.1,
    spinner_complete: Optional[str] = None,
    initial_value: str = '',
    message: str = '',
    format_string: str = '\r{spinner} ({elapsed_time:.2f}s) {message}{value}',
    output_stream: <class 'TextIO'> = <_io.StringIO object>,
    format_string_when_updated: Union[str, bool] = False,
    **kwargs: Any
)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L182-L274)




- `spinner_complete: str `


string to display when the spinner is complete


- `spinner_chars: Sequence[str] `


sequence of strings to use as the spinner characters


- `format_string_when_updated: Optional[str] `


format string to use when the value is updated


- `update_interval: float `




- `message: str `




- `current_value: Any `




- `format_string: str `




- `output_stream: <class 'TextIO'> `




- `start_time: float `


for measuring elapsed time


- `stop_spinner: threading.Event `


to stop the spinner


- `spinner_thread: Optional[threading.Thread] `


the thread running the spinner


- `value_changed: bool `


whether the value has been updated since the last display


- `term_width: int `


width of the terminal, for padding with spaces


### `def spin` { #Spinner.spin }
```python
(self) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L276-L304)


Function to run in a separate thread, displaying the spinner and optional information


### `def update_value` { #Spinner.update_value }
```python
(self, value: Any) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L306-L309)


Update the current value displayed by the spinner


### `def start` { #Spinner.start }
```python
(self) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L311-L315)


Start the spinner


### `def stop` { #Spinner.stop }
```python
(self) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L317-L331)


Stop the spinner


### `class SpinnerContext(Spinner):` { #SpinnerContext }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L334-L342)


displays a spinner, and optionally elapsed time and a mutable value while a function is running.

### Parameters:
- `spinner_chars : Union[str, Sequence[str]]`
sequence of strings, or key to look up in `SPINNER_CHARS`, to use as the spinner characters
(defaults to `"default"`)
- `update_interval : float`
how often to update the spinner display in seconds
(defaults to `0.1`)
- `spinner_complete : str`
string to display when the spinner is complete
(defaults to looking up `spinner_chars` in `SPINNER_COMPLETE` or `"#"`)
- `initial_value : str`
initial value to display with the spinner
(defaults to `""`)
- `message : str`
message to display with the spinner
(defaults to `""`)
- `format_string : str`
string to format the spinner with. must have `"\r"` prepended to clear the line.
allowed keys are `spinner`, `elapsed_time`, `message`, and `value`
(defaults to `"\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
- `output_stream : TextIO`
stream to write the spinner to
(defaults to `sys.stdout`)
- `format_string_when_updated : Union[bool,str]`
whether to use a different format string when the value is updated.
if `True`, use the default format string with a newline appended. if a string, use that string.
this is useful if you want update_value to print to console and be preserved.
(defaults to `False`)

### Methods:
- `update_value(value: Any) -> None`
    update the current value displayed by the spinner

### Usage:

#### As a context manager:
```python
with SpinnerContext() as sp:
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
```

#### As a decorator:
```python
@spinner_decorator
def long_running_function():
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
    return "Function completed"
```


### Inherited Members                                

- [`Spinner`](#SpinnerContext.__init__)
- [`spinner_complete`](#SpinnerContext.spinner_complete)
- [`spinner_chars`](#SpinnerContext.spinner_chars)
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
- [`spin`](#SpinnerContext.spin)
- [`update_value`](#SpinnerContext.update_value)
- [`start`](#SpinnerContext.start)
- [`stop`](#SpinnerContext.stop)


### `def spinner_decorator` { #spinner_decorator }
```python
(
    *args,
    spinner_chars: Union[str, Sequence[str]] = 'default',
    update_interval: float = 0.1,
    spinner_complete: Optional[str] = None,
    initial_value: str = '',
    message: str = '',
    format_string: str = '{spinner} ({elapsed_time:.2f}s) {message}{value}',
    output_stream: <class 'TextIO'> = <_io.StringIO object>,
    mutable_kwarg_key: Optional[str] = None,
    **kwargs
) -> Callable[[~DecoratedFunction], ~DecoratedFunction]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L348-L410)


displays a spinner, and optionally elapsed time and a mutable value while a function is running.

### Parameters:
- `spinner_chars : Union[str, Sequence[str]]`
sequence of strings, or key to look up in `SPINNER_CHARS`, to use as the spinner characters
(defaults to `"default"`)
- `update_interval : float`
how often to update the spinner display in seconds
(defaults to `0.1`)
- `spinner_complete : str`
string to display when the spinner is complete
(defaults to looking up `spinner_chars` in `SPINNER_COMPLETE` or `"#"`)
- `initial_value : str`
initial value to display with the spinner
(defaults to `""`)
- `message : str`
message to display with the spinner
(defaults to `""`)
- `format_string : str`
string to format the spinner with. must have `"\r"` prepended to clear the line.
allowed keys are `spinner`, `elapsed_time`, `message`, and `value`
(defaults to `"\r{spinner} ({elapsed_time:.2f}s) {message}{value}"`)
- `output_stream : TextIO`
stream to write the spinner to
(defaults to `sys.stdout`)
- `format_string_when_updated : Union[bool,str]`
whether to use a different format string when the value is updated.
if `True`, use the default format string with a newline appended. if a string, use that string.
this is useful if you want update_value to print to console and be preserved.
(defaults to `False`)

### Methods:
- `update_value(value: Any) -> None`
    update the current value displayed by the spinner

### Usage:

#### As a context manager:
```python
with SpinnerContext() as sp:
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
```

#### As a decorator:
```python
@spinner_decorator
def long_running_function():
    for i in range(1):
        time.sleep(0.1)
        spinner.update_value(f"Step {i+1}")
    return "Function completed"
```


### `class NoOpContextManager:` { #NoOpContextManager }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L416-L426)


A context manager that does nothing.


### `NoOpContextManager` { #NoOpContextManager.__init__ }
```python
(*args, **kwargs)
```

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L419-L420)









## API Documentation

 - [`NumericSequence`](#NumericSequence)
 - [`universal_flatten`](#universal_flatten)
 - [`StatCounter`](#StatCounter)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py)

# `muutils.statcounter` { #muutils.statcounter }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L0-L209)



- `NumericSequence = typing.Sequence[typing.Union[float, int, ForwardRef('NumericSequence')]]`




### `def universal_flatten` { #universal_flatten }
```python
(
    arr: Union[Sequence[Union[float, int, Sequence[Union[float, int, ForwardRef('NumericSequence')]]]], float, int],
    require_rectangular: bool = True
) -> Sequence[Union[float, int, ForwardRef('NumericSequence')]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L20-L37)


flattens any iterable


### `class StatCounter(collections.Counter):` { #StatCounter }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L44-L210)


counter, but with some stat calculation methods which assume the keys are numbers

works best when the keys are ints


### `def validate` { #StatCounter.validate }
```python
(self) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L50-L52)


validate the counter as being all floats or ints


### `def min` { #StatCounter.min }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L54-L55)




### `def max` { #StatCounter.max }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L57-L58)




### `def total` { #StatCounter.total }
```python
(self)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L60-L62)


Sum of the counts


- `keys_sorted: list `

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L64-L67)


return the keys


### `def percentile` { #StatCounter.percentile }
```python
(self, p: float)
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L69-L116)


return the value at the given percentile

this could be log time if we did binary search, but that would be a lot of added complexity


### `def median` { #StatCounter.median }
```python
(self) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L118-L119)




### `def mean` { #StatCounter.mean }
```python
(self) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L121-L123)


return the mean of the values


### `def mode` { #StatCounter.mode }
```python
(self) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L125-L126)




### `def std` { #StatCounter.std }
```python
(self) -> float
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L128-L133)


return the standard deviation of the values


### `def summary` { #StatCounter.summary }
```python
(
    self,
    typecast: Callable = <function StatCounter.<lambda>>,
    *,
    extra_percentiles: Optional[list[float]] = None
) -> dict[str, typing.Union[float, int]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L135-L172)




### `def serialize` { #StatCounter.serialize }
```python
(
    self,
    typecast: Callable = <function StatCounter.<lambda>>,
    *,
    extra_percentiles: Optional[list[float]] = None
) -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L174-L186)




### `def load` { #StatCounter.load }
```python
(cls, data: dict) -> muutils.statcounter.StatCounter
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L194-L201)




### `def from_list_arrays` { #StatCounter.from_list_arrays }
```python
(
    cls,
    arr,
    map_func: Callable = <class 'float'>
) -> muutils.statcounter.StatCounter
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/statcounter.py#L203-L210)


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







## API Documentation

 - [`SysInfo`](#SysInfo)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py)

# `muutils.sysinfo` { #muutils.sysinfo }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L0-L196)



### `class SysInfo:` { #SysInfo }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L32-L191)


getters for various information about the system


### `def python` { #SysInfo.python }
```python
() -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L35-L47)


details about python version


### `def pip` { #SysInfo.pip }
```python
() -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L49-L57)


installed packages info


### `def pytorch` { #SysInfo.pytorch }
```python
() -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L59-L121)


pytorch and cuda information


### `def platform` { #SysInfo.platform }
```python
() -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L123-L142)




### `def git_info` { #SysInfo.git_info }
```python
(with_log: bool = False) -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L144-L165)




### `def get_all` { #SysInfo.get_all }
```python
(
    cls,
    include: Optional[tuple[str, ...]] = None,
    exclude: tuple[str, ...] = ()
) -> dict
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/sysinfo.py#L167-L191)









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




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py)

# `muutils.tensor_utils` { #muutils.tensor_utils }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L0-L455)



- `TYPE_TO_JAX_DTYPE: dict = {<class 'float'>: <class 'jaxtyping.Float'>, <class 'int'>: <class 'jaxtyping.Int'>, <class 'jaxtyping.Float'>: <class 'jaxtyping.Float'>, <class 'jaxtyping.Int'>: <class 'jaxtyping.Int'>, <class 'bool'>: <class 'jaxtyping.Bool'>, <class 'jaxtyping.Bool'>: <class 'jaxtyping.Bool'>, <class 'numpy.bool_'>: <class 'jaxtyping.Bool'>, torch.bool: <class 'jaxtyping.Bool'>, <class 'numpy.float64'>: <class 'jaxtyping.Float'>, <class 'numpy.float16'>: <class 'jaxtyping.Float'>, <class 'numpy.float32'>: <class 'jaxtyping.Float'>, <class 'numpy.int32'>: <class 'jaxtyping.Int'>, <class 'numpy.int8'>: <class 'jaxtyping.Int'>, <class 'numpy.int16'>: <class 'jaxtyping.Int'>, <class 'numpy.int64'>: <class 'jaxtyping.Int'>, <class 'numpy.uint8'>: <class 'jaxtyping.Int'>, torch.float32: <class 'jaxtyping.Float'>, torch.float16: <class 'jaxtyping.Float'>, torch.float64: <class 'jaxtyping.Float'>, torch.bfloat16: <class 'jaxtyping.Float'>, torch.int32: <class 'jaxtyping.Int'>, torch.int8: <class 'jaxtyping.Int'>, torch.int16: <class 'jaxtyping.Int'>, torch.int64: <class 'jaxtyping.Int'>}`




### `def jaxtype_factory` { #jaxtype_factory }
```python
(
    name: str,
    array_type: type,
    default_jax_dtype=<class 'jaxtyping.Float'>,
    legacy_mode: muutils.errormode.ErrorMode = ErrorMode.Warn
) -> type
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L63-L157)


usage:
```
ATensor = jaxtype_factory("ATensor", torch.Tensor, jaxtyping.Float)
x: ATensor["dim1 dim2", np.float32]
```


- `ATensor = <class 'muutils.tensor_utils.jaxtype_factory.<locals>._BaseArray'>`




- `NDArray = <class 'muutils.tensor_utils.jaxtype_factory.<locals>._BaseArray'>`




### `def numpy_to_torch_dtype` { #numpy_to_torch_dtype }
```python
(dtype: Union[numpy.dtype, torch.dtype]) -> torch.dtype
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L180-L185)


convert numpy dtype to torch dtype


- `DTYPE_LIST: list = [<class 'bool'>, <class 'int'>, <class 'float'>, torch.float32, torch.float32, torch.float64, torch.float16, torch.float64, torch.bfloat16, torch.complex64, torch.complex128, torch.int32, torch.int8, torch.int16, torch.int32, torch.int64, torch.int64, torch.int16, torch.uint8, torch.bool, <class 'numpy.float64'>, <class 'numpy.float16'>, <class 'numpy.float32'>, <class 'numpy.float64'>, <class 'numpy.float16'>, <class 'numpy.float32'>, <class 'numpy.float64'>, <class 'numpy.complex64'>, <class 'numpy.complex128'>, <class 'numpy.int8'>, <class 'numpy.int16'>, <class 'numpy.int32'>, <class 'numpy.int64'>, <class 'numpy.int32'>, <class 'numpy.int64'>, <class 'numpy.int16'>, <class 'numpy.uint8'>, <class 'numpy.bool_'>]`




- `DTYPE_MAP: dict = {"<class 'bool'>": <class 'bool'>, "<class 'int'>": <class 'int'>, "<class 'float'>": <class 'float'>, 'torch.float32': torch.float32, 'torch.float64': torch.float64, 'torch.float16': torch.float16, 'torch.bfloat16': torch.bfloat16, 'torch.complex64': torch.complex64, 'torch.complex128': torch.complex128, 'torch.int32': torch.int32, 'torch.int8': torch.int8, 'torch.int16': torch.int16, 'torch.int64': torch.int64, 'torch.uint8': torch.uint8, 'torch.bool': torch.bool, "<class 'numpy.float64'>": <class 'numpy.float64'>, "<class 'numpy.float16'>": <class 'numpy.float16'>, "<class 'numpy.float32'>": <class 'numpy.float32'>, "<class 'numpy.complex64'>": <class 'numpy.complex64'>, "<class 'numpy.complex128'>": <class 'numpy.complex128'>, "<class 'numpy.int8'>": <class 'numpy.int8'>, "<class 'numpy.int16'>": <class 'numpy.int16'>, "<class 'numpy.int32'>": <class 'numpy.int32'>, "<class 'numpy.int64'>": <class 'numpy.int64'>, "<class 'numpy.uint8'>": <class 'numpy.uint8'>, "<class 'numpy.bool_'>": <class 'numpy.bool_'>, 'float64': <class 'numpy.float64'>, 'float16': <class 'numpy.float16'>, 'float32': <class 'numpy.float32'>, 'complex64': <class 'numpy.complex64'>, 'complex128': <class 'numpy.complex128'>, 'int8': <class 'numpy.int8'>, 'int16': <class 'numpy.int16'>, 'int32': <class 'numpy.int32'>, 'int64': <class 'numpy.int64'>, 'uint8': <class 'numpy.uint8'>, 'bool_': <class 'numpy.bool_'>, 'bool': <class 'numpy.bool_'>}`




- `TORCH_DTYPE_MAP: dict = {"<class 'bool'>": torch.bool, "<class 'int'>": torch.int32, "<class 'float'>": torch.float64, 'torch.float32': torch.float32, 'torch.float64': torch.float64, 'torch.float16': torch.float16, 'torch.bfloat16': torch.bfloat16, 'torch.complex64': torch.complex64, 'torch.complex128': torch.complex128, 'torch.int32': torch.int32, 'torch.int8': torch.int8, 'torch.int16': torch.int16, 'torch.int64': torch.int64, 'torch.uint8': torch.uint8, 'torch.bool': torch.bool, "<class 'numpy.float64'>": torch.float64, "<class 'numpy.float16'>": torch.float16, "<class 'numpy.float32'>": torch.float32, "<class 'numpy.complex64'>": torch.complex64, "<class 'numpy.complex128'>": torch.complex128, "<class 'numpy.int8'>": torch.int8, "<class 'numpy.int16'>": torch.int16, "<class 'numpy.int32'>": torch.int32, "<class 'numpy.int64'>": torch.int64, "<class 'numpy.uint8'>": torch.uint8, "<class 'numpy.bool_'>": torch.bool, 'float64': torch.float64, 'float16': torch.float16, 'float32': torch.float32, 'complex64': torch.complex64, 'complex128': torch.complex128, 'int8': torch.int8, 'int16': torch.int16, 'int32': torch.int32, 'int64': torch.int64, 'uint8': torch.uint8, 'bool_': torch.bool, 'bool': torch.bool}`




- `TORCH_OPTIMIZERS_MAP: dict[str, typing.Type[torch.optim.optimizer.Optimizer]] = {'Adagrad': <class 'torch.optim.adagrad.Adagrad'>, 'Adam': <class 'torch.optim.adam.Adam'>, 'AdamW': <class 'torch.optim.adamw.AdamW'>, 'SparseAdam': <class 'torch.optim.sparse_adam.SparseAdam'>, 'Adamax': <class 'torch.optim.adamax.Adamax'>, 'ASGD': <class 'torch.optim.asgd.ASGD'>, 'LBFGS': <class 'torch.optim.lbfgs.LBFGS'>, 'NAdam': <class 'torch.optim.nadam.NAdam'>, 'RAdam': <class 'torch.optim.radam.RAdam'>, 'RMSprop': <class 'torch.optim.rmsprop.RMSprop'>, 'Rprop': <class 'torch.optim.rprop.Rprop'>, 'SGD': <class 'torch.optim.sgd.SGD'>}`




### `def pad_tensor` { #pad_tensor }
```python
(
    tensor: jaxtyping.Shaped[Tensor, 'dim1'],
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False
) -> jaxtyping.Shaped[Tensor, 'padded_length']
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L279-L302)


pad a 1-d tensor on the left with pad_value to length `padded_length`

set `rpad = True` to pad on the right instead


### `def lpad_tensor` { #lpad_tensor }
```python
(
    tensor: torch.Tensor,
    padded_length: int,
    pad_value: float = 0.0
) -> torch.Tensor
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L305-L308)




### `def rpad_tensor` { #rpad_tensor }
```python
(
    tensor: torch.Tensor,
    pad_length: int,
    pad_value: float = 0.0
) -> torch.Tensor
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L311-L315)


pad a 1-d tensor on the right with pad_value to length `pad_length`


### `def pad_array` { #pad_array }
```python
(
    array: jaxtyping.Shaped[ndarray, 'dim1'],
    padded_length: int,
    pad_value: float = 0.0,
    rpad: bool = False
) -> jaxtyping.Shaped[ndarray, 'padded_length']
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L318-L340)


pad a 1-d array on the left with pad_value to length `padded_length`

set `rpad = True` to pad on the right instead


### `def lpad_array` { #lpad_array }
```python
(
    array: numpy.ndarray,
    padded_length: int,
    pad_value: float = 0.0
) -> numpy.ndarray
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L343-L347)


pad a 1-d array on the left with pad_value to length `padded_length`


### `def rpad_array` { #rpad_array }
```python
(
    array: numpy.ndarray,
    pad_length: int,
    pad_value: float = 0.0
) -> numpy.ndarray
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L350-L354)


pad a 1-d array on the right with pad_value to length `pad_length`


### `def get_dict_shapes` { #get_dict_shapes }
```python
(d: dict[str, torch.Tensor]) -> dict[str, tuple[int, ...]]
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L357-L359)


given a state dict or cache dict, compute the shapes and put them in a nested dict


### `def string_dict_shapes` { #string_dict_shapes }
```python
(d: dict[str, torch.Tensor]) -> str
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L362-L374)


printable version of get_dict_shapes


### `class StateDictCompareError(builtins.AssertionError):` { #StateDictCompareError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L377-L380)


raised when state dicts don't match


### Inherited Members                                

- [`AssertionError`](#StateDictCompareError.__init__)

- [`with_traceback`](#StateDictCompareError.with_traceback)
- [`add_note`](#StateDictCompareError.add_note)
- [`args`](#StateDictCompareError.args)


### `class StateDictKeysError(StateDictCompareError):` { #StateDictKeysError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L383-L386)


raised when state dict keys don't match


### Inherited Members                                

- [`AssertionError`](#StateDictKeysError.__init__)

- [`with_traceback`](#StateDictKeysError.with_traceback)
- [`add_note`](#StateDictKeysError.add_note)
- [`args`](#StateDictKeysError.args)


### `class StateDictShapeError(StateDictCompareError):` { #StateDictShapeError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L389-L392)


raised when state dict shapes don't match


### Inherited Members                                

- [`AssertionError`](#StateDictShapeError.__init__)

- [`with_traceback`](#StateDictShapeError.with_traceback)
- [`add_note`](#StateDictShapeError.add_note)
- [`args`](#StateDictShapeError.args)


### `class StateDictValueError(StateDictCompareError):` { #StateDictValueError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L395-L398)


raised when state dict values don't match


### Inherited Members                                

- [`AssertionError`](#StateDictValueError.__init__)

- [`with_traceback`](#StateDictValueError.with_traceback)
- [`add_note`](#StateDictValueError.add_note)
- [`args`](#StateDictValueError.args)


### `def compare_state_dicts` { #compare_state_dicts }
```python
(
    d1: dict,
    d2: dict,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    verbose: bool = True
) -> None
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L401-L456)









## API Documentation

 - [`FancyTimeitResult`](#FancyTimeitResult)
 - [`timeit_fancy`](#timeit_fancy)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/timeit_fancy.py)

# `muutils.timeit_fancy` { #muutils.timeit_fancy }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/timeit_fancy.py#L0-L95)



### `class FancyTimeitResult(typing.NamedTuple):` { #FancyTimeitResult }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/timeit_fancy.py#L14-L19)


return type of `timeit_fancy`


### `FancyTimeitResult` { #FancyTimeitResult.__init__ }
```python
(
    timings: ForwardRef('StatCounter'),
    return_value: ForwardRef('T'),
    profile: ForwardRef('Union[pstats.Stats, None]')
)
```


Create new instance of FancyTimeitResult(timings, return_value, profile)


- `timings: muutils.statcounter.StatCounter `


Alias for field number 0


- `return_value: ~T `


Alias for field number 1


- `profile: Optional[pstats.Stats] `


Alias for field number 2


### Inherited Members                                

- [`index`](#FancyTimeitResult.index)
- [`count`](#FancyTimeitResult.count)


### `def timeit_fancy` { #timeit_fancy }
```python
(
    cmd: Callable[[], ~T],
    setup: Union[str, Callable[[], Any]] = <function <lambda>>,
    repeats: int = 5,
    namespace: Optional[dict[str, Any]] = None,
    get_return: bool = True,
    do_profiling: bool = False
) -> muutils.timeit_fancy.FancyTimeitResult
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/timeit_fancy.py#L22-L96)


Wrapper for `timeit` to get the fastest run of a callable with more customization options.

Approximates the functionality of the %timeit magic or command line interface in a Python callable.

### Parameters
- `cmd: Callable[[], T] | str`
    The callable to time. If a string, it will be passed to `timeit.Timer` as the `stmt` argument.
- `setup: str`
    The setup code to run before `cmd`. If a string, it will be passed to `timeit.Timer` as the `setup` argument.
- `repeats: int`
    The number of times to run `cmd` to get a reliable measurement.
- `namespace: dict[str, Any]`
    Passed to `timeit.Timer` constructor.
    If `cmd` or `setup` use local or global variables, they must be passed here. See `timeit` documentation for details.
- `get_return: bool`
    Whether to pass the value returned from `cmd`. If True, the return value will be appended in a tuple with execution time.
    This is for speed and convenience so that `cmd` doesn't need to be run again in the calling scope if the return values are needed.
    (default: `False`)
- `do_profiling: bool`
    Whether to return a `pstats.Stats` object in addition to the time and return value.
    (default: `False`)

### Returns
`FancyTimeitResult`, which is a NamedTuple with the following fields:
- `time: float`
    The time in seconds it took to run `cmd` the minimum number of times to get a reliable measurement.
- `return_value: T|None`
    The return value of `cmd` if `get_return` is `True`, otherwise `None`.
- `profile: pstats.Stats|None`
    A `pstats.Stats` object if `do_profiling` is `True`, otherwise `None`.







## API Documentation

 - [`GenericAliasTypes`](#GenericAliasTypes)
 - [`IncorrectTypeException`](#IncorrectTypeException)
 - [`TypeHintNotImplementedError`](#TypeHintNotImplementedError)
 - [`InvalidGenericAliasError`](#InvalidGenericAliasError)
 - [`validate_type`](#validate_type)




[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py)

# `muutils.validate_type` { #muutils.validate_type }


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py#L0-L216)



- `GenericAliasTypes: tuple = (<class 'types.GenericAlias'>, <class 'typing._GenericAlias'>, <class 'typing._UnionGenericAlias'>, <class 'typing._BaseGenericAlias'>)`




### `class IncorrectTypeException(builtins.TypeError):` { #IncorrectTypeException }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py#L22-L23)


Inappropriate argument type.


### Inherited Members                                

- [`TypeError`](#IncorrectTypeException.__init__)

- [`with_traceback`](#IncorrectTypeException.with_traceback)
- [`add_note`](#IncorrectTypeException.add_note)
- [`args`](#IncorrectTypeException.args)


### `class TypeHintNotImplementedError(builtins.NotImplementedError):` { #TypeHintNotImplementedError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py#L26-L27)


Method or function hasn't been implemented yet.


### Inherited Members                                

- [`NotImplementedError`](#TypeHintNotImplementedError.__init__)

- [`with_traceback`](#TypeHintNotImplementedError.with_traceback)
- [`add_note`](#TypeHintNotImplementedError.add_note)
- [`args`](#TypeHintNotImplementedError.args)


### `class InvalidGenericAliasError(builtins.TypeError):` { #InvalidGenericAliasError }

[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py#L30-L31)


Inappropriate argument type.


### Inherited Members                                

- [`TypeError`](#InvalidGenericAliasError.__init__)

- [`with_traceback`](#InvalidGenericAliasError.with_traceback)
- [`add_note`](#InvalidGenericAliasError.add_note)
- [`args`](#InvalidGenericAliasError.args)


### `def validate_type` { #validate_type }
```python
(value: Any, expected_type: Any, do_except: bool = False) -> bool
```


[View Source on GitHub](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py#L55-L217)


Validate that a `value` is of the `expected_type`

### Parameters
- `value`: the value to check the type of
- `expected_type`: the type to check against. Not all types are supported
- `do_except`: if `True`, raise an exception if the type is incorrect (instead of returning `False`)
    (default: `False`)

### Returns
- `bool`: `True` if the value is of the expected type, `False` otherwise.

### Raises
- `IncorrectTypeException(TypeError)`: if the type is incorrect and `do_except` is `True`
- `TypeHintNotImplementedError(NotImplementedError)`: if the type hint is not implemented
- `InvalidGenericAliasError(TypeError)`: if the generic alias is invalid

use `typeguard` for a more robust solution: https://github.com/agronholm/typeguard



