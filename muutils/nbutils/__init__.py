"""utilities for working with notebooks

- configuring figures mdoes and torch devices: `configure_notebook`
- converting them to scripts: `convert_ipynb_to_script`
- running them as tests: `run_notebook_tests`
- and working with diagrams/LaTeX: `mermaid`, `print_tex`

"""

from muutils.nbutils.mermaid import mm

__all__ = [
    # sub-modules
    "configure_notebook",
    "convert_ipynb_to_script",
    "mermaid",
    "print_tex",
    "run_notebook_tests",
    # functions
    "mm",
]
