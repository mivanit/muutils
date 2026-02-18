# python project makefile template
# https://github.com/mivanit/python-project-makefile-template
# version: 0.5.1
# license: https://creativecommons.org/licenses/by-sa/4.0/

"""Print info about current python, torch, cuda, and devices.

Useful for debugging environment issues and verifying GPU availability.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
	from collections.abc import Mapping


def print_info_dict(
	info: Mapping[str, str | int | Mapping[str, Any]],
	indent: str = "  ",
	level: int = 1,
) -> None:
	"pretty print the info"
	indent_str: str = indent * level
	longest_key_len: int = max(map(len, info.keys()))
	for key, value in info.items():
		if isinstance(value, dict):
			print(f"{indent_str}{key:<{longest_key_len}}:")
			print_info_dict(value, indent, level + 1)
		else:
			print(f"{indent_str}{key:<{longest_key_len}} = {value}")


def get_nvcc_info() -> dict[str, str]:
	"get info about cuda from nvcc --version"
	# Run the nvcc command.
	try:
		result: subprocess.CompletedProcess[str] = subprocess.run(
			["nvcc", "--version"],  # noqa: S607
			check=True,
			capture_output=True,
			text=True,
		)
	except Exception as e:
		return {"Failed to run 'nvcc --version'": str(e)}

	output: str = result.stdout
	lines: list[str] = [line.strip() for line in output.splitlines() if line.strip()]

	# Ensure there are exactly 5 lines in the output.
	if len(lines) != 5:
		msg = f"Expected exactly 5 lines from nvcc --version, got {len(lines)} lines:\n{output}"
		raise ValueError(msg)

	# Compile shared regex for release info.
	release_regex: re.Pattern[str] = re.compile(
		r"Cuda compilation tools,\s*release\s*([^,]+),\s*(V.+)",
	)

	# Define a mapping for each desired field:
	# key -> (line index, regex pattern, group index, transformation function)
	patterns: dict[str, tuple[int, re.Pattern[str], int, Callable[[str], str]]] = {
		"build_time": (
			2,
			re.compile(r"Built on (.+)"),
			1,
			lambda s: s.replace("_", " "),
		),
		"release": (3, release_regex, 1, str.strip),
		"release_V": (3, release_regex, 2, str.strip),
		"build": (4, re.compile(r"Build (.+)"), 1, str.strip),
	}

	info: dict[str, str] = {}
	for key, (line_index, pattern, group_index, transform) in patterns.items():
		match: re.Match[str] | None = pattern.search(lines[line_index])
		if not match:
			err_msg: str = (
				f"Unable to parse {key} from nvcc output: {lines[line_index]}"
			)
			raise ValueError(err_msg)
		info[key] = transform(match.group(group_index))

	info["release_short"] = info["release"].replace(".", "").strip()

	return info


def get_torch_info() -> tuple[list[Exception], dict[str, Any]]:
	"get info about pytorch and cuda devices"
	exceptions: list[Exception] = []
	info: dict[str, Any] = {}

	try:
		import torch  # type: ignore[import-not-found] # noqa: PLC0415
	except ImportError as e:
		info["torch.__version__"] = "not available"
		exceptions.append(e)
		return exceptions, info

	try:
		info["torch.__version__"] = torch.__version__
		info["torch.cuda.is_available()"] = torch.cuda.is_available()

		if torch.cuda.is_available():
			info["torch.version.cuda"] = torch.version.cuda  # pyright: ignore[reportAttributeAccessIssue,reportUnknownMemberType]  # ty: ignore[possibly-missing-attribute]
			info["torch.cuda.device_count()"] = torch.cuda.device_count()

			if torch.cuda.device_count() > 0:
				info["torch.cuda.current_device()"] = torch.cuda.current_device()
				n_devices: int = torch.cuda.device_count()
				info["n_devices"] = n_devices
				for current_device in range(n_devices):
					try:
						current_device_info: dict[str, str | int] = {}

						dev_prop = torch.cuda.get_device_properties(  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
							torch.device(f"cuda:{current_device}"),
						)

						current_device_info["name"] = dev_prop.name  # pyright: ignore[reportUnknownMemberType]
						current_device_info["version"] = (
							f"{dev_prop.major}.{dev_prop.minor}"  # pyright: ignore[reportUnknownMemberType]
						)
						current_device_info["total_memory"] = (
							f"{dev_prop.total_memory} ({dev_prop.total_memory:.1e})"  # pyright: ignore[reportUnknownMemberType]
						)
						current_device_info["multi_processor_count"] = (
							dev_prop.multi_processor_count  # pyright: ignore[reportUnknownMemberType]
						)
						current_device_info["is_integrated"] = dev_prop.is_integrated  # pyright: ignore[reportUnknownMemberType]
						current_device_info["is_multi_gpu_board"] = (
							dev_prop.is_multi_gpu_board  # pyright: ignore[reportUnknownMemberType]
						)

						info[f"device cuda:{current_device}"] = current_device_info

					except Exception as e:  # noqa: PERF203
						exceptions.append(e)
			else:
				err_msg_nodevice: str = (
					f"{torch.cuda.device_count() = } devices detected, invalid"
				)
				raise ValueError(err_msg_nodevice)  # noqa: TRY301

		else:
			err_msg_nocuda: str = (
				f"CUDA is NOT available in torch: {torch.cuda.is_available() = }"
			)
			raise ValueError(err_msg_nocuda)  # noqa: TRY301

	except Exception as e:
		exceptions.append(e)

	return exceptions, info


if __name__ == "__main__":
	print(f"python: {sys.version}")
	print_info_dict(
		{
			"python executable path: sys.executable": str(sys.executable),
			"sys.platform": sys.platform,
			"current working directory: os.getcwd()": os.getcwd(),
			"Host name: os.name": os.name,
			"CPU count: os.cpu_count()": str(os.cpu_count()),
		},
	)

	nvcc_info: dict[str, Any] = get_nvcc_info()
	print("nvcc:")
	print_info_dict(nvcc_info)

	torch_exceptions, torch_info = get_torch_info()
	print("torch:")
	print_info_dict(torch_info)

	if torch_exceptions:
		print("torch_exceptions:")
		for e in torch_exceptions:
			print(f"  {e}")
