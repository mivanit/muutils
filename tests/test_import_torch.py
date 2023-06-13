import json
import os
import random
import typing
import warnings
from itertools import islice
from pathlib import Path
from typing import Any, Callable, TypeVar

import numpy as np

def test_import_torch():
    import torch

    print(f"torch version: {torch.__version__}")
    print(f"torch cuda available: {torch.cuda.is_available()}")
