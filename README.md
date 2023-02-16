

`muutils`, stylized as "$\mu$utils" or "μutils", is a collection of miscellaneous python utilities, meant to be small and with ~~no~~ minimal dependencies outside of standard python.


- [`json_serialize`](https://github.com/mivanit/muutils/tree/main/muutils/json_serialize.py) is a tool for serializing and loading arbitrary python objects into json
- [`statcounter`](https://github.com/mivanit/muutils/tree/main/muutils/statcounter.py) is an extension of `collections.Counter` that provides "smart" computation of stats (mean, variance, median, other percentiles) from the counter object without using `Counter.elements()`
- [`group_equiv`](https://github.com/mivanit/muutils/tree/main/muutils/group_equiv.py) groups elements from a sequence according to a given equivalence relation, without assuming that the equivalence relation obeys the transitive property
- [`logger`](https://github.com/mivanit/muutils/tree/main/muutils/logger.py) implements a logger with "streams" and a timer context manager
- [`jsonlines`](https://github.com/mivanit/muutils/tree/main/muutils/jsonlines.py) extremely simple utility for reading/writing `jsonl` files
- [`ZANJ`](https://github.com/mivanit/muutils/tree/main/muutils/zanj/zanj.py) is a WIP hdf5 alternative. This will probably be spun off into its own repo

There are a couple work-in-progress utilities in [`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/) that aren't ready for anything, but nothing in this repo is suitable for production. Use at your own risk!


# installation

```
pip install muutils
```
