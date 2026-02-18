"""quickly print a sympy expression in latex"""

from __future__ import annotations

import sympy as sp  # type: ignore  # pyright: ignore[reportMissingTypeStubs]
from IPython.display import Math, display  # type: ignore  # pyright: ignore[reportUnknownVariableType]


def print_tex(
    expr: sp.Expr,  # type: ignore
    name: str | None = None,
    plain: bool = False,
    rendered: bool = True,
):
    """function for easily rendering a sympy expression in latex"""
    out: str = sp.latex(expr)  # pyright: ignore[reportUnknownVariableType]
    if name is not None:
        out = f"{name} = {out}"

    if plain:
        print(out)  # pyright: ignore[reportUnknownArgumentType]
    if rendered:
        display(Math(out))  # pyright: ignore[reportUnusedCallResult]
