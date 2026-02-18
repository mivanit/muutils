# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Generate a formatted commit log and write it to a file.

Usage: python get_commit_log.py <last_version> <output_file>
"""

from __future__ import annotations

import subprocess
import sys


def main(
	last_version: str,
	commit_log_file: str,
) -> None:
	"pretty print a commit log amd wrote it to a file"
	if last_version == "NULL":
		print("!!! ERROR !!!", file=sys.stderr)
		print("LAST_VERSION is NULL, can't get commit log!", file=sys.stderr)
		sys.exit(1)

	try:
		log_cmd: list[str] = [
			"git",
			"log",
			f"{last_version}..HEAD",
			"--pretty=format:- %s (%h)",
		]
		commits: list[str] = (
			subprocess.check_output(log_cmd).decode("utf-8").strip().split("\n")  # noqa: S603
		)
		with open(commit_log_file, "w") as f:
			_ = f.write("\n".join(reversed(commits)))
	except subprocess.CalledProcessError as e:
		print(f"Error: {e}", file=sys.stderr)
		sys.exit(1)


if __name__ == "__main__":
	main(
		last_version=sys.argv[1].strip(),
		commit_log_file=sys.argv[2].strip(),
	)
