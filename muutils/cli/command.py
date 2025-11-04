from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, List, Union


@dataclass
class Command:
    """Simple typed command with shell flag and subprocess helpers."""

    cmd: Union[List[str], str]
    shell: bool = False
    env: dict[str, str] | None = None
    inherit_env: bool = True

    def __post_init__(self) -> None:
        """Enforce cmd type when shell is False."""
        if self.shell is False and isinstance(self.cmd, str):
            raise ValueError("cmd must be List[str] when shell is False")

    def _quote_env(self) -> str:
        """Return KEY=VAL tokens for env values. ignores `inherit_env`."""
        if not self.env:
            return ""

        parts: List[str] = []
        for k, v in self.env.items():
            token: str = f"{k}={v}"
            parts.append(token)
        prefix: str = " ".join(parts)
        return prefix

    @property
    def cmd_joined(self) -> str:
        """Return cmd as a single string, joining with spaces if it's a list. no env included."""
        if isinstance(self.cmd, str):
            return self.cmd
        else:
            return " ".join(self.cmd)

    @property
    def cmd_for_subprocess(self) -> Union[List[str], str]:
        """Return cmd, splitting if shell is True and cmd is a string."""
        if self.shell:
            if isinstance(self.cmd, str):
                return self.cmd
            else:
                return " ".join(self.cmd)
        else:
            assert isinstance(self.cmd, list)
            return self.cmd

    def script_line(self) -> str:
        """Return a single shell string, prefixing KEY=VAL for env if provided."""
        return f"{self._quote_env()} {self.cmd_joined}".strip()

    @property
    def env_final(self) -> dict[str, str]:
        """Return final env dict, merging with os.environ if inherit_env is True."""
        return {
            **(os.environ if self.inherit_env else {}),
            **(self.env or {}),
        }

    def run(
        self,
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[Any]:
        """Call subprocess.run with this command."""
        try:
            return subprocess.run(
                self.cmd_for_subprocess,
                shell=self.shell,
                env=self.env_final,
                **kwargs,
            )
        except subprocess.CalledProcessError as e:
            print(f"Command failed: `{self.script_line()}`", file=sys.stderr)
            raise e

    def Popen(
        self,
        **kwargs: Any,
    ) -> subprocess.Popen[Any]:
        """Call subprocess.Popen with this command."""
        return subprocess.Popen(
            self.cmd_for_subprocess,
            shell=self.shell,
            env=self.env_final,
            **kwargs,
        )
