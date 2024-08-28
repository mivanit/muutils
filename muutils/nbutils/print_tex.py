"""quickly print a sympy expression in latex"""

import sympy as sp  # type: ignore
from IPython.display import Math, display  # type: ignore


def print_tex(
    expr: sp.Expr,
    name: str | None = None,
    plain: bool = False,
    rendered: bool = True,
):
    """function for easily rendering a sympy expression in latex"""
    out: str = sp.latex(expr)
    if name is not None:
        out = f"{name} = {out}"

    if plain:
        print(out)
    if rendered:
        display(Math(out))
