import sys
from pathlib import Path


def pytest_ignore_collect(path: Path, config) -> bool:
    """ignore any test file ending with `_torch.py` on Python 3.14+"""
    if sys.version_info < (3, 14):
        return False

    return str(path).endswith("_torch.py")


# TODO: get beartype working
# from beartype.claw import beartype_all

# beartype_all()
