# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""CLI to convert markdown files to HTML using pdoc's markdown2.

Usage: python pdoc_markdown2_cli.py <input.md> <output.html> [--safe-mode escape|replace]
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from pdoc.markdown2 import (  # type: ignore[import-untyped,import-not-found,attr-defined] # pyright: ignore[reportMissingImports]
	Markdown,  # pyright: ignore[reportUnknownVariableType]
)


def convert_file(
	input_path: Path,
	output_path: Path,
	safe_mode: str | None = None,
	encoding: str = "utf-8",
) -> None:
	"""Convert a markdown file to HTML"""
	# Read markdown input
	text: str = input_path.read_text(encoding=encoding)

	# Convert to HTML using markdown2
	markdown: Any = Markdown(  # pyright: ignore[reportUnknownVariableType]
		extras=["fenced-code-blocks", "header-ids", "markdown-in-html", "tables"],
		safe_mode=safe_mode,  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]
	)
	html: str = str(markdown.convert(text))  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]

	# Write HTML output
	output_path.write_text(html, encoding=encoding)


def main() -> None:
	"cli entry point"
	parser: argparse.ArgumentParser = argparse.ArgumentParser(
		description="Convert markdown files to HTML using pdoc's markdown2",
	)
	parser.add_argument("input", type=Path, help="Input markdown file path")
	parser.add_argument("output", type=Path, help="Output HTML file path")
	parser.add_argument(
		"--safe-mode",
		choices=["escape", "replace"],
		help="Sanitize literal HTML: 'escape' escapes HTML meta chars, 'replace' replaces with [HTML_REMOVED]",
	)
	parser.add_argument(
		"--encoding",
		default="utf-8",
		help="Character encoding for reading/writing files (default: utf-8)",
	)

	args: argparse.Namespace = parser.parse_args()

	convert_file(
		args.input,
		args.output,
		safe_mode=args.safe_mode,
		encoding=args.encoding,
	)


if __name__ == "__main__":
	main()
