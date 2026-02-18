import sys
from pathlib import Path
import warnings


def pytest_ignore_collect(collection_path: Path, config) -> bool:
    """ignore any test file ending with `_torch.py` on Python 3.14+

    Also ignore tests/unit/validate_type/ on Python < 3.11 (these use modern type syntax)
    """
    path_str: str = str(collection_path).replace("\\", "/")
    # TODO[torch-python-3.14]: remove when torch supports Python 3.14
    # ignore torch tests on Python 3.14+
    if sys.version_info >= (3, 14):
        warnings.warn(
            "Ignoring torch tests on Python 3.14+ as torch does not yet support this version"
        )
        if path_str.endswith("_torch.py"):
            return True

    # ignore validate_type tests on Python < 3.11 (they use | union syntax)
    if sys.version_info < (3, 11):
        warnings.warn(
            "Ignoring tests/unit/validate_type/ tests on Python < 3.11 as they use modern type syntax"
        )
        if "tests/unit/validate_type/" in path_str:
            return True

    return False


# TODO: get beartype working
# from beartype.claw import beartype_all

# beartype_all()
