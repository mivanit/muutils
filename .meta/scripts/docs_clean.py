# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Clean up docs directory based on pyproject.toml configuration.

Removes generated documentation files while preserving resources and
files specified in [tool.makefile.docs.no_clean].

Usage: python docs_clean.py <pyproject_path> <docs_dir> [extra_preserve...]
"""

from __future__ import annotations

import shutil
import sys
from functools import reduce
from pathlib import Path
from typing import Any, cast

try:
	import tomllib  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
except ImportError:
	import tomli as tomllib  # type: ignore[import-untyped,import-not-found,no-redef] # pyright: ignore[reportMissingImports]

TOOL_PATH: str = "tool.makefile.docs"
DEFAULT_DOCS_DIR: str = "docs"


def deep_get(
	d: dict[str, Any],
	path: str,
	default: Any = None,  # noqa: ANN401
	sep: str = ".",
) -> Any:  # noqa: ANN401
	"""Get nested dictionary value via separated path with default."""
	return reduce(
		lambda x, y: x.get(y, default) if isinstance(x, dict) else default,  # function
		path.split(sep) if isinstance(path, str) else path,  # sequence
		d,  # initial
	)


def read_config(pyproject_path: Path) -> tuple[Path, set[Path]]:
	"read configuration from pyproject.toml"
	if not pyproject_path.is_file():
		return Path(DEFAULT_DOCS_DIR), set()

	with pyproject_path.open("rb") as f:
		config: dict[str, Any] = cast("dict[str, Any]", tomllib.load(f))  # pyright: ignore[reportUnknownMemberType]

	preserved: list[str] = deep_get(config, f"{TOOL_PATH}.no_clean", [])
	docs_dir: Path = Path(deep_get(config, f"{TOOL_PATH}.output_dir", DEFAULT_DOCS_DIR))

	# Convert to absolute paths and validate
	preserve_set: set[Path] = set()
	for p in preserved:
		full_path = (docs_dir / p).resolve()
		if not full_path.as_posix().startswith(docs_dir.resolve().as_posix()):
			err_msg: str = f"Preserved path '{p}' must be within docs directory"
			raise ValueError(err_msg)
		preserve_set.add(docs_dir / p)

	return docs_dir, preserve_set


def clean_docs(docs_dir: Path, preserved: set[Path]) -> None:
	"""delete files not in preserved set

	TODO: this is not recursive
	"""
	for path in docs_dir.iterdir():
		if path.is_file() and path not in preserved:
			path.unlink()
		elif path.is_dir() and path not in preserved:
			shutil.rmtree(path)


def main(
	pyproject_path: str,
	docs_dir_cli: str,
	extra_preserve: list[str],
) -> None:
	"Clean up docs directory based on pyproject.toml configuration."
	docs_dir: Path
	preserved: set[Path]
	docs_dir, preserved = read_config(Path(pyproject_path))

	if not docs_dir.is_dir():
		msg = f"Docs directory '{docs_dir}' not found"
		raise FileNotFoundError(msg)
	if docs_dir != Path(docs_dir_cli):
		msg = f"Docs directory mismatch: {docs_dir = } != {docs_dir_cli = }. this is probably because you changed one of `pyproject.toml:{TOOL_PATH}.output_dir` (the former) or `makefile:DOCS_DIR` (the latter) without updating the other."
		raise ValueError(msg)

	for x in extra_preserve:
		preserved.add(Path(x))
	clean_docs(docs_dir, preserved)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3:])
