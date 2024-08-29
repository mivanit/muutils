[![PyPI](https://img.shields.io/pypi/v/muutils)](https://pypi.org/project/muutils/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/muutils)
[![docs](https://img.shields.io/badge/docs-latest-blue)](https://miv.name/muutils)

[![Checks](https://github.com/mivanit/muutils/actions/workflows/checks.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/checks.yml)
[![Checks](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml/badge.svg)](https://github.com/mivanit/muutils/actions/workflows/make-docs.yml)
[![Coverage](docs/coverage/coverage.svg)](docs/coverage/html/)

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

[**hosted html docs:**](https://miv.name/muutils) https://miv.name/muutils

- [single-page html docs](https://miv.name/muutils/combined/muutils.html) [(absolute source link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.html)
- [single-page markdown docs](https://miv.name/muutils/combined/muutils.md) [(absolute source link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.md)
- Test coverage: [![Test Coverage](https://miv.name/muutils/coverage/coverage.svg)](https://miv.name/muutils/coverage/html/) [webpage](https://miv.name/muutils/coverage/html/) [(absolute source link)](https://github.com/mivanit/muutils/tree/main/docs/coverage/html/) [(plain text)](https://github.com/mivanit/muutils/tree/main/docs/coverage/coverage.txt)

# modules

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
