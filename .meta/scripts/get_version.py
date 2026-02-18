# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Extract version from pyproject.toml and print to stdout.

Usage: python get_version.py <pyproject_path>
Prints 'v<version>' on success, 'NULL' on failure.
"""

from __future__ import annotations

import sys
from typing import Any, cast

try:
	try:
		import tomllib  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
	except ImportError:
		import tomli as tomllib  # type: ignore[import-untyped,import-not-found,no-redef] # pyright: ignore[reportMissingImports]

	pyproject_path: str = sys.argv[1].strip()

	with open(pyproject_path, "rb") as f:
		pyproject_data: dict[str, Any] = cast("dict[str, Any]", tomllib.load(f))  # pyright: ignore[reportUnknownMemberType]

	print("v" + pyproject_data["project"]["version"], end="")
except Exception:
	print("NULL", end="")
	sys.exit(1)
