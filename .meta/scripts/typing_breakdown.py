# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Parse type checker outputs and generate detailed breakdown of errors by type and file.

Usage:
    python typing_breakdown.py [OPTIONS]

Examples:
    python typing_breakdown.py
    python typing_breakdown.py --error-dir .meta/.type-errors
    python typing_breakdown.py --output .meta/typing-summary.toml --checkers mypy,basedpyright,ty

"""

from __future__ import annotations

import argparse
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal


def strip_cwd(path: str) -> str:
	"""Strip the current working directory from a file path to make it relative.

	Args:
		path: File path (absolute or relative)

	Returns:
		Relative path with CWD stripped, or original path if not under CWD

	"""
	cwd: str = os.getcwd()
	# Normalize both paths to handle different separators and resolve symlinks
	abs_path: str = os.path.abspath(path)
	abs_cwd: str = os.path.abspath(cwd)

	# Ensure CWD ends with separator for proper prefix matching
	if not abs_cwd.endswith(os.sep):
		abs_cwd += os.sep

	# Strip CWD prefix if present
	if abs_path.startswith(abs_cwd):
		return abs_path[len(abs_cwd) :]

	return path


@dataclass
class TypeCheckResult:
	"results from parsing a type checker output"

	type_checker: Literal["mypy", "basedpyright", "ty"]
	by_type: dict[str, int] = field(default_factory=lambda: defaultdict(int))
	by_file: dict[str, int] = field(default_factory=lambda: defaultdict(int))
	# Separate tracking for warnings (used by basedpyright)
	warnings_by_type: dict[str, int] = field(default_factory=lambda: defaultdict(int))
	warnings_by_file: dict[str, int] = field(default_factory=lambda: defaultdict(int))

	@property
	def total_errors(self) -> int:
		"total number of errors across all types, validates they match between type and file dicts"
		total_by_type: int = sum(self.by_type.values())
		total_by_file: int = sum(self.by_file.values())

		if total_by_type != total_by_file:
			err_msg: str = f"Error count mismatch for {self.type_checker}: by_type={total_by_type}, by_file={total_by_file}"
			raise ValueError(err_msg)

		return total_by_type

	@property
	def total_warnings(self) -> int:
		"total number of warnings across all types"
		total_by_type: int = sum(self.warnings_by_type.values())
		total_by_file: int = sum(self.warnings_by_file.values())

		if total_by_type != total_by_file:
			err_msg: str = f"Warning count mismatch for {self.type_checker}: by_type={total_by_type}, by_file={total_by_file}"
			raise ValueError(err_msg)

		return total_by_type

	def sorted_results(self) -> TypeCheckResult:
		"return a copy with errors sorted by count (descending)"
		# Sort by count (descending)
		sorted_by_type: list[tuple[str, int]] = sorted(
			self.by_type.items(),
			key=lambda x: x[1],
			reverse=True,
		)
		sorted_by_file: list[tuple[str, int]] = sorted(
			self.by_file.items(),
			key=lambda x: x[1],
			reverse=True,
		)
		sorted_warnings_by_type: list[tuple[str, int]] = sorted(
			self.warnings_by_type.items(),
			key=lambda x: x[1],
			reverse=True,
		)
		sorted_warnings_by_file: list[tuple[str, int]] = sorted(
			self.warnings_by_file.items(),
			key=lambda x: x[1],
			reverse=True,
		)

		# Create new instance with sorted data (dicts maintain insertion order in Python 3.7+)
		result: TypeCheckResult = TypeCheckResult(type_checker=self.type_checker)
		result.by_type = dict(sorted_by_type)
		result.by_file = dict(sorted_by_file)
		result.warnings_by_type = dict(sorted_warnings_by_type)
		result.warnings_by_file = dict(sorted_warnings_by_file)

		return result

	def to_toml(self) -> str:
		"format as TOML output"
		lines: list[str] = []

		# Main section with total
		lines.append(f"[type_errors.{self.type_checker}]")
		try:
			lines.append(f"total_errors = {self.total_errors}")
		except ValueError:
			lines.append(f"total_errors_by_type = {sum(self.by_type.values())}")
			lines.append(f"total_errors_by_file = {sum(self.by_file.values())}")
		lines.append("")

		# by_type section
		lines.append(f"[type_errors.{self.type_checker}.by_type]")
		error_type: str
		count: int
		for error_type, count in self.by_type.items():
			# Always quote keys
			lines.append(f'"{error_type}" = {count}')

		lines.append("")

		# by_file section
		lines.append(f"[type_errors.{self.type_checker}.by_file]")
		file_path: str
		for file_path, count in self.by_file.items():
			# Always quote file paths
			lines.append(f'"{file_path}" = {count}')

		# Add warnings sections if there are any warnings
		if self.warnings_by_type or self.warnings_by_file:
			lines.append("")
			lines.append(f"[type_warnings.{self.type_checker}]")
			try:
				lines.append(f"total_warnings = {self.total_warnings}")
			except ValueError:
				lines.append(
					f"total_warnings_by_type = {sum(self.warnings_by_type.values())}"
				)
				lines.append(
					f"total_warnings_by_file = {sum(self.warnings_by_file.values())}"
				)
			lines.append("")

			# warnings by_type section
			lines.append(f"[type_warnings.{self.type_checker}.by_type]")
			warning_type: str
			for warning_type, count in self.warnings_by_type.items():
				lines.append(f'"{warning_type}" = {count}')

			lines.append("")

			# warnings by_file section
			lines.append(f"[type_warnings.{self.type_checker}.by_file]")
			for file_path, count in self.warnings_by_file.items():
				lines.append(f'"{file_path}" = {count}')

		return "\n".join(lines)


def parse_mypy(content: str) -> TypeCheckResult:
	"parse mypy output: file.py:line: error: message [error-code]"
	result: TypeCheckResult = TypeCheckResult(type_checker="mypy")

	pattern: re.Pattern[str] = re.compile(
		r"^(.+?):\d+: error: .+ \[(.+?)\]", re.MULTILINE
	)
	match: re.Match[str]
	for match in pattern.finditer(content):
		file_path: str = match.group(1)
		error_code: str = match.group(2)
		result.by_type[error_code] += 1
		result.by_file[file_path] += 1

	return result


def parse_basedpyright(content: str) -> TypeCheckResult:
	"parse basedpyright output: path on line, then indented errors with (code)"
	result: TypeCheckResult = TypeCheckResult(type_checker="basedpyright")

	# Pattern for file paths (lines that start with /)
	# Pattern for errors: indented line with - error/warning: message (code)
	# Some diagnostics span multiple lines with (reportCode) on a continuation line
	current_file: str = ""
	pending_diagnostic_type: str | None = None  # "error" or "warning" waiting for code

	line: str
	for line in content.splitlines():
		# Check if this is a file path line (starts with / and no leading space)
		if line and not line.startswith(" ") and line.startswith("/"):
			current_file = strip_cwd(line.strip())
			pending_diagnostic_type = None

		elif line.strip() and current_file:
			# Try to match single-line format: "  path:line:col - warning: message (reportCode)"
			match: re.Match[str] | None = re.search(
				r"\s+.+:\d+:\d+ - (error|warning): .+ \((\w+)\)", line
			)
			if match:
				diagnostic_type: str = match.group(1)
				error_code: str = match.group(2)
				if diagnostic_type == "warning":
					result.warnings_by_type[error_code] += 1
					result.warnings_by_file[current_file] += 1
				else:
					result.by_type[error_code] += 1
					result.by_file[current_file] += 1
				pending_diagnostic_type = None
			else:
				# Check if this is a diagnostic line without code (multi-line format start)
				diag_match: re.Match[str] | None = re.search(
					r"\s+.+:\d+:\d+ - (error|warning): ", line
				)
				if diag_match:
					pending_diagnostic_type = diag_match.group(1)
				# Check if this is a continuation line with the code
				elif pending_diagnostic_type:
					code_match: re.Match[str] | None = re.search(r"\((\w+)\)\s*$", line)
					if code_match:
						error_code = code_match.group(1)
						if pending_diagnostic_type == "warning":
							result.warnings_by_type[error_code] += 1
							result.warnings_by_file[current_file] += 1
						else:
							result.by_type[error_code] += 1
							result.by_file[current_file] += 1
						pending_diagnostic_type = None

	return result


def parse_ty(content: str) -> TypeCheckResult:
	"parse ty output: error[error-code]: message then --> file:line:col"
	result: TypeCheckResult = TypeCheckResult(type_checker="ty")

	# Pattern for error type: error[code]: or warning[code]:
	error_pattern: re.Pattern[str] = re.compile(
		r"^(error|warning)\[(.+?)\]:", re.MULTILINE
	)
	# Pattern for location: --> file:line:col
	location_pattern: re.Pattern[str] = re.compile(
		r"^\s+-->\s+(.+?):\d+:\d+", re.MULTILINE
	)

	# Find all errors and their locations
	errors: list[re.Match[str]] = list(error_pattern.finditer(content))
	locations: list[re.Match[str]] = list(location_pattern.finditer(content))

	# Match errors with locations (they should be in order)
	error_match: re.Match[str]
	for error_match in errors:
		error_code: str = error_match.group(2)
		result.by_type[error_code] += 1

		# Find the next location after this error
		error_pos: int = error_match.end()
		loc_match: re.Match[str]
		for loc_match in locations:
			if loc_match.start() > error_pos:
				file_path: str = loc_match.group(1)
				result.by_file[file_path] += 1
				break

	return result


def extract_summary_line(file_path: Path) -> str:
	"extract the last non-empty line from a file (typically the summary line)"
	content: str = file_path.read_text(encoding="utf-8")
	lines: list[str] = [line.strip() for line in content.splitlines() if line.strip()]
	if not lines:
		return "(empty output)"
	return lines[-1]


def main(error_dir: str, output_file: str, checkers: list[str]) -> None:
	"parse all type checker outputs and generate breakdown"
	error_path: Path = Path(error_dir)
	output_path: Path = Path(output_file)

	output_lines: list[str] = []

	# Checker info lookup (filename, parser function)
	checkers_info: dict[str, tuple[str, Callable[[str], TypeCheckResult]]] = {
		"mypy": ("mypy.txt", parse_mypy),
		"basedpyright": ("basedpyright.txt", parse_basedpyright),
		"ty": ("ty.txt", parse_ty),
	}

	# Add summary comments (in order specified by checkers argument)
	name: str
	for name in checkers:
		if name not in checkers_info:
			continue
		filename, _ = checkers_info[name]
		file_path: Path = error_path / filename
		if not file_path.exists():
			output_lines.append(f"# {name}: (not run or file not found)")
		else:
			summary: str = extract_summary_line(file_path)
			output_lines.append(f"# {name}: {summary}")

	output_lines.append("")

	# Parse each type checker (in order specified by checkers argument)
	for name in checkers:
		if name not in checkers_info:
			continue
		filename, parser_fn = checkers_info[name]
		file_path_: Path = error_path / filename
		if not file_path_.exists():
			continue
		content: str = file_path_.read_text(encoding="utf-8")
		result: TypeCheckResult = parser_fn(content)
		# Sort the results
		sorted_result: TypeCheckResult = result.sorted_results()
		# Convert to TOML
		breakdown: str = sorted_result.to_toml()
		output_lines.append(breakdown)
		output_lines.append("")  # Add blank line between checkers

	# Write to output file
	final_output: str = "\n".join(output_lines)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	_ = output_path.write_text(final_output, encoding="utf-8")

	# Also print to stdout
	print(final_output)


if __name__ == "__main__":
	parser: argparse.ArgumentParser = argparse.ArgumentParser(
		description="Parse type checker outputs and generate detailed breakdown of errors by type and file",
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	_ = parser.add_argument(
		"--error-dir",
		type=str,
		default=".meta/.type-errors",
		help="Directory containing type checker output files (default: .meta/.type-errors)",
	)
	_ = parser.add_argument(
		"--output",
		"-o",
		type=str,
		default=".meta/typing-summary.toml",
		help="Output file to write summary to (default: .meta/typing-summary.toml)",
	)
	_ = parser.add_argument(
		"--checkers",
		"-c",
		type=str,
		default="mypy,basedpyright,ty",
		help="Comma-separated list of checkers to process (default: mypy,basedpyright,ty)",
	)

	args: argparse.Namespace = parser.parse_args()

	# Parse checkers list
	checkers_list: list[str] = [c.strip() for c in args.checkers.split(",")]

	main(error_dir=args.error_dir, output_file=args.output, checkers=checkers_list)
