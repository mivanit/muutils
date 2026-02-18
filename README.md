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

Optional dependencies:
```
pip install muutils[array]    # numpy, torch, jaxtyping -- for mlutils, tensor_utils, tensor_info, ml, json_serialize array features
pip install muutils[notebook] # ipython -- for nbutils.configure_notebook
pip install muutils[parallel] # multiprocess, tqdm -- for parallel processing with progress
pip install muutils[web]      # weasyprint -- for web/html_to_pdf
```

# documentation

[**hosted html docs:**](https://miv.name/muutils) https://miv.name/muutils

- [single-page html docs](https://miv.name/muutils/combined/muutils.html) [(absolute source link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.html)
- [single-page markdown docs](https://miv.name/muutils/combined/muutils.md) [(absolute source link)](https://github.com/mivanit/muutils/tree/main/docs/combined/muutils.md)
- Test coverage: [![Test Coverage](https://miv.name/muutils/coverage/coverage.svg)](https://miv.name/muutils/coverage/html/) [webpage](https://miv.name/muutils/coverage/html/) [(absolute source link)](https://github.com/mivanit/muutils/tree/main/docs/coverage/html/) [(plain text)](https://github.com/mivanit/muutils/tree/main/docs/coverage/coverage.txt)

# modules

| Module | Description |
|--------|-------------|
| [`statcounter`](https://miv.name/muutils/muutils/statcounter.html) | Extension of `collections.Counter` with smart stats computation (mean, variance, percentiles) |
| [`dictmagic`](https://miv.name/muutils/muutils/dictmagic.html) | Dictionary utilities: dotlist conversion, `DefaulterDict`, tensor dict condensing |
| [`kappa`](https://miv.name/muutils/muutils/kappa.html) | Anonymous getitem (`Kappa(lambda x: x**2)[2]` returns `4`) |
| [`sysinfo`](https://miv.name/muutils/muutils/sysinfo.html) | System information collection for logging |
| [`misc`](https://miv.name/muutils/muutils/misc.html) | Utilities: `stable_hash`, `list_join`/`list_split`, filename sanitization, `freeze` |
| [`interval`](https://miv.name/muutils/muutils/interval.html) | Mathematical intervals (open/closed/half-open) with containment, clamping, set operations |
| [`errormode`](https://miv.name/muutils/muutils/errormode.html) | Enum-based error handling (raise/warn/log/ignore) |
| [`validate_type`](https://miv.name/muutils/muutils/validate_type.html) | Runtime type validation for basic and generic types |
| [`console_unicode`](https://miv.name/muutils/muutils/console_unicode.html) | Safe console output with Unicode/ASCII fallback |
| [`spinner`](https://miv.name/muutils/muutils/spinner.html) | Animated spinners with elapsed time and status updates |
| [`timeit_fancy`](https://miv.name/muutils/muutils/timeit_fancy.html) | Enhanced timing with multiple runs, profiling, and statistics |
| [`dbg`](https://miv.name/muutils/muutils/dbg.html) | Debug printing inspired by Rust's `dbg!` macro |
| [`collect_warnings`](https://miv.name/muutils/muutils/collect_warnings.html) | Context manager to capture and summarize warnings |
| [`parallel`](https://miv.name/muutils/muutils/parallel.html) | Simplified parallel processing with progress bars |
| [`jsonlines`](https://miv.name/muutils/muutils/jsonlines.html) | Simple `jsonl` file reading/writing |
| [`group_equiv`](https://miv.name/muutils/muutils/group_equiv.html) | Group elements by equivalence relation (non-transitive) |
| [`json_serialize`](https://miv.name/muutils/muutils/json_serialize.html) | Serialize arbitrary Python objects to JSON (works with [ZANJ](https://github.com/mivanit/ZANJ/)) |
| [`nbutils`](https://miv.name/muutils/muutils/nbutils.html) | Jupyter utilities: notebook conversion, configuration, mermaid/TeX display |
| [`math`](https://miv.name/muutils/muutils/math.html) | Binning functions and matrix power computation |
| [`cli`](https://miv.name/muutils/muutils/cli.html) | CLI utilities: boolean argument parsing, flag actions |
| [`web`](https://miv.name/muutils/muutils/web.html) | HTML asset inlining for standalone documents |
| [`logger`](https://miv.name/muutils/muutils/logger.html) | *(deprecated)* Logging framework, use [`trnbl`](https://github.com/mivanit/trnbl) instead |
| [`mlutils`](https://miv.name/muutils/muutils/mlutils.html) | ML pipeline: device detection, seeding, checkpoints *(requires `array`)* |
| [`tensor_utils`](https://miv.name/muutils/muutils/tensor_utils.html) | PyTorch/numpy type conversions *(requires `array`)* |
| [`tensor_info`](https://miv.name/muutils/muutils/tensor_info.html) | Tensor metadata extraction and formatting *(requires `array`)* |
| [`ml`](https://miv.name/muutils/muutils/ml.html) | CUDA memory monitoring *(requires `array`)* |

# [`ZANJ`](https://github.com/mivanit/ZANJ/)

ZANJ is a human-readable and simple format for ML models, datasets, and arbitrary objects. It's built around having a zip file with `json` and `npy` files, and has been spun off into its [own project](https://github.com/mivanit/ZANJ/).

There are a couple work-in-progress utilities in [`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/) that aren't ready for anything, but nothing in this repo is suitable for production. Use at your own risk!
