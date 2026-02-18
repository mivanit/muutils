# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Export dependencies to requirements.txt files based on pyproject.toml configuration.

Reads [tool.makefile.uv-exports] from pyproject.toml and generates uv export
commands for each configured export. Output is shell commands printed to stdout.

Usage: python export_requirements.py <pyproject_path> <output_dir>
"""

from __future__ import annotations

import sys
import warnings

try:
	import tomllib  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
except ImportError:
	import tomli as tomllib  # type: ignore[import-not-found,no-redef,import-untyped] # pyright: ignore[reportMissingImports]
from functools import reduce
from pathlib import Path
from typing import Any, cast

TOOL_PATH: str = "tool.makefile.uv-exports"


def deep_get(
	d: dict[str, Any],
	path: str,
	default: Any = None,  # noqa: ANN401
	sep: str = ".",
) -> Any:  # noqa: ANN401
	"get a value from a nested dictionary"
	return reduce(
		lambda x, y: x.get(y, default) if isinstance(x, dict) else default,  # function
		path.split(sep) if isinstance(path, str) else path,  # sequence
		d,  # initial
	)


def export_configuration(
	export: dict[str, Any],
	all_groups: list[str],
	all_extras: list[str],
	export_opts: dict[str, Any],
	output_dir: Path,
) -> None:
	"print to console a uv command for make which will export a requirements.txt file"
	# get name and validate
	name = export.get("name")
	if not name or not name.isalnum():
		warnings.warn(
			f"Export configuration missing valid 'name' field {export}",
		)
		return

	# get other options with default fallbacks
	filename: str = export.get("filename") or f"requirements-{name}.txt"
	groups: list[str] | bool | None = export.get("groups")
	extras: list[str] | bool = export.get("extras", [])
	options: list[str] = export.get("options", [])

	# init command
	cmd: list[str] = ["uv", "export", *export_opts.get("args", [])]

	# handle groups
	if groups is not None:
		groups_list: list[str] = []
		if isinstance(groups, bool):
			if groups:
				groups_list = all_groups.copy()
		else:
			groups_list = groups

		for group in all_groups:
			if group in groups_list:
				cmd.extend(["--group", group])
			else:
				cmd.extend(["--no-group", group])

	# handle extras
	extras_list: list[str] = []
	if isinstance(extras, bool):
		if extras:
			extras_list = all_extras.copy()
	else:
		extras_list = extras

	for extra in extras_list:
		cmd.extend(["--extra", extra])

	# add extra options
	cmd.extend(options)

	# assemble the command and print to console -- makefile will run it
	output_path = output_dir / filename
	print(f"{' '.join(cmd)} > {output_path.as_posix()}")


def main(
	pyproject_path: Path,
	output_dir: Path,
) -> None:
	"export to requirements.txt files based on pyproject.toml configuration"
	# read pyproject.toml
	with open(pyproject_path, "rb") as f:
		pyproject_data: dict[str, Any] = cast("dict[str, Any]", tomllib.load(f))  # pyright: ignore[reportUnknownMemberType]

	# all available groups
	all_groups: list[str] = list(pyproject_data.get("dependency-groups", {}).keys())
	all_extras: list[str] = list(
		deep_get(pyproject_data, "project.optional-dependencies", {}).keys(),
	)

	# options for exporting
	export_opts: dict[str, Any] = deep_get(pyproject_data, TOOL_PATH, {})

	# what are we exporting?
	exports: list[dict[str, Any]] = export_opts.get("exports", [])
	if not exports:
		exports = [{"name": "all", "groups": [], "extras": [], "options": []}]

	# export each configuration
	for export in exports:
		export_configuration(
			export=export,
			all_groups=all_groups,
			all_extras=all_extras,
			export_opts=export_opts,
			output_dir=output_dir,
		)


if __name__ == "__main__":
	main(
		pyproject_path=Path(sys.argv[1]),
		output_dir=Path(sys.argv[2]),
	)
