import os
import subprocess
import sys
import typing

from pip._internal.operations.freeze import freeze as pip_freeze


def _popen(cmd: list[str], split_out: bool = False) -> dict[str, typing.Any]:
    p: subprocess.Popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    p_out: str | list[str] | None
    if p.stdout is not None:
        p_out = p.stdout.read().decode("utf-8")
        if split_out:
            assert isinstance(p_out, str)
            p_out = p_out.strip().split("\n")
    else:
        p_out = None

    return {
        "stdout": p_out,
        "stderr": (None if p.stderr is None else p.stderr.read().decode("utf-8")),
        "returncode": p.returncode if p.returncode is None else int(p.returncode),
    }


class SysInfo:
    """getters for various information about the system"""

    @staticmethod
    def python() -> dict:
        """details about python version"""
        ver_tup = sys.version_info
        return {
            "version": sys.version,
            "major": ver_tup[0],
            "minor": ver_tup[1],
            "micro": ver_tup[2],
            "releaselevel": ver_tup[3],
            "serial": ver_tup[4],
        }

    @staticmethod
    def pip() -> dict:
        """installed packages info"""
        pckgs: list[str] = [x for x in pip_freeze(local_only=True)]
        return {
            "n_packages": len(pckgs),
            "packages": pckgs,
        }

    @staticmethod
    def pytorch() -> dict:
        """pytorch and cuda information"""
        try:
            import torch
        except Exception as e:
            return {
                "importable": False,
                "error": str(e),
            }

        output: dict = {"importable": True}

        output["torch.__version__"] = torch.__version__
        output["torch.version.cuda"] = torch.version.cuda
        output["torch.version.debug"] = torch.version.debug
        output["torch.version.git_version"] = torch.version.git_version
        output["torch.version.hip"] = torch.version.hip
        output["torch.cuda.is_available()"] = torch.cuda.is_available()
        output["torch.cuda.device_count()"] = torch.cuda.device_count()
        output["torch.cuda.is_initialized()"] = torch.cuda.is_initialized()

        if torch.cuda.is_available():
            import os

            cuda_version_nvcc: str = os.popen("nvcc --version").read()
            output["nvcc --version"] = cuda_version_nvcc.split("\n")

            if torch.cuda.device_count() > 0:
                n_devices: int = torch.cuda.device_count()
                output["torch.cuda.current_device()"] = torch.cuda.current_device()
                output["torch devices"] = []
                for current_device in range(n_devices):
                    try:
                        # print(f'checking current device {current_device} of {torch.cuda.device_count()} devices')
                        # print(f'\tdevice {current_device}')
                        # dev_prop = torch.cuda.get_device_properties(torch.device(0))
                        # print(f'\t    name:                   {dev_prop.name}')
                        # print(f'\t    version:                {dev_prop.major}.{dev_prop.minor}')
                        # print(f'\t    total_memory:           {dev_prop.total_memory}')
                        # print(f'\t    multi_processor_count:  {dev_prop.multi_processor_count}')
                        # print(f'\t')
                        dev_prop = torch.cuda.get_device_properties(current_device)
                        output["torch devices"].append(
                            {
                                "device": current_device,
                                "name": dev_prop.name,
                                "version": {
                                    f"major": dev_prop.major,
                                    "minor": dev_prop.minor,
                                },
                                "total_memory": dev_prop.total_memory,
                                "multi_processor_count": dev_prop.multi_processor_count,
                            }
                        )
                    except Exception as e:
                        output["torch devices"].append(
                            {
                                "device": current_device,
                                "error": str(e),
                            }
                        )
        return output

    @staticmethod
    def platform() -> dict:
        import platform

        items = [
            "platform",
            "machine",
            "processor",
            "system",
            "version",
            "architecture",
            "uname",
            "node",
            "python_branch",
            "python_build",
            "python_compiler",
            "python_implementation",
        ]

        return {x: getattr(platform, x)() for x in items}

    @staticmethod
    def git_info() -> dict:
        git_version: dict = _popen(["git", "version"])
        git_status: dict = _popen(["git", "status"])
        if git_status["stderr"].startswith("fatal: not a git repository"):
            return {
                "git version": git_version["stdout"],
                "git status": git_status,
            }
        else:
            return {
                "git version": git_version["stdout"],
                "git status": git_status,
                "git branch": _popen(["git", "branch"], split_out=True),
                "git remote -v": _popen(["git", "remote", "-v"], split_out=True),
                "git log": _popen(["git", "log"]),
            }

    @classmethod
    def get_all(
        cls,
        include: tuple[str, ...] | None = None,
        exclude: tuple[str, ...] = tuple(),
    ) -> dict:
        include_meta: tuple[str, ...]
        if include is None:
            include_meta = tuple(cls.__dict__.keys())
        else:
            include_meta = include

        return {
            x: getattr(cls, x)()
            for x in include_meta
            if all(
                [
                    not x.startswith("_"),
                    x not in exclude,
                    callable(getattr(cls, x)),
                    x != "get_all",
                    x in include if include is not None else True,
                ]
            )
        }
