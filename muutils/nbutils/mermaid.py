"""display mermaid.js diagrams in jupyter notebooks by the `mermaid.ink/img` service"""

import base64

try:
    from IPython.display import Image, display
except ImportError:
    import warnings

    warnings.warn(
        "IPython.display could not be imported, mermaid will not work", ImportWarning
    )


def mm(graph):
    """for plotting mermaid.js diagrams"""
    graphbytes = graph.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    display(Image(url="https://mermaid.ink/img/" + base64_string))
