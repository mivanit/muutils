from __future__ import annotations

import os
import subprocess

import pytest

from muutils.cli.command import Command


def test_Command_init():
    """Test Command initialization with list and string cmds."""
    # Valid: list cmd with shell=False (default)
    cmd1 = Command(cmd=["echo", "hello"])
    assert cmd1.cmd == ["echo", "hello"]
    assert cmd1.shell is False

    # Valid: string cmd with shell=True
    cmd2 = Command(cmd="echo hello", shell=True)
    assert cmd2.cmd == "echo hello"
    assert cmd2.shell is True

    # Invalid: string cmd with shell=False should raise ValueError
    with pytest.raises(
        ValueError, match="cmd must be List\\[str\\] when shell is False"
    ):
        Command(cmd="echo hello", shell=False)

    # Valid: list cmd with shell=True is allowed (will be joined)
    cmd3 = Command(cmd=["echo", "hello"], shell=True)
    assert cmd3.cmd == ["echo", "hello"]
    assert cmd3.shell is True


def test_Command_properties():
    """Test cmd_joined and cmd_for_subprocess properties in both shell modes."""
    # Test with shell=False (list cmd)
    cmd_list = Command(cmd=["echo", "hello", "world"])
    assert cmd_list.cmd_joined == "echo hello world"
    assert cmd_list.cmd_for_subprocess == ["echo", "hello", "world"]

    # Test with shell=True and string cmd
    cmd_str = Command(cmd="echo hello world", shell=True)
    assert cmd_str.cmd_joined == "echo hello world"
    assert cmd_str.cmd_for_subprocess == "echo hello world"

    # Test with shell=True and list cmd (should be joined for subprocess)
    cmd_list_shell = Command(cmd=["echo", "hello", "world"], shell=True)
    assert cmd_list_shell.cmd_joined == "echo hello world"
    assert cmd_list_shell.cmd_for_subprocess == "echo hello world"


def test_Command_script_line():
    """Test script_line with env vars formatting."""
    # No env vars
    cmd1 = Command(cmd=["echo", "hello"])
    assert cmd1.script_line() == "echo hello"

    # With env vars
    cmd2 = Command(cmd=["echo", "hello"], env={"FOO": "bar", "BAZ": "qux"})
    script = cmd2.script_line()
    # env vars can be in any order, so check both are present
    assert "FOO=bar" in script
    assert "BAZ=qux" in script
    assert "echo hello" in script
    # Verify format: env vars come before command
    assert script.endswith("echo hello")

    # With shell=True
    cmd3 = Command(cmd="echo $FOO", shell=True, env={"FOO": "bar"})
    assert cmd3.script_line() == "FOO=bar echo $FOO"


def test_Command_env_final():
    """Test env_final with inherit_env=True and inherit_env=False."""
    # Set a test environment variable
    os.environ["TEST_VAR_COMMAND"] = "original"

    try:
        # inherit_env=True (default) should merge with os.environ
        cmd1 = Command(cmd=["echo", "test"], env={"FOO": "bar"})
        env1 = cmd1.env_final
        assert env1["FOO"] == "bar"
        assert env1["TEST_VAR_COMMAND"] == "original"

        # inherit_env=False should only include provided env
        cmd2 = Command(cmd=["echo", "test"], env={"FOO": "bar"}, inherit_env=False)
        env2 = cmd2.env_final
        assert env2["FOO"] == "bar"
        assert "TEST_VAR_COMMAND" not in env2

        # Custom env should override inherited env
        os.environ["OVERRIDE_TEST"] = "old"
        cmd3 = Command(cmd=["echo", "test"], env={"OVERRIDE_TEST": "new"})
        env3 = cmd3.env_final
        assert env3["OVERRIDE_TEST"] == "new"

    finally:
        # Clean up test env vars
        os.environ.pop("TEST_VAR_COMMAND", None)
        os.environ.pop("OVERRIDE_TEST", None)


def test_Command_run():
    """Test running a simple command and capturing output."""
    # Simple successful command
    cmd = Command(cmd=["echo", "hello"])
    result = cmd.run(capture_output=True, text=True)
    assert result.returncode == 0
    assert "hello" in result.stdout

    # Command with env vars
    cmd2 = Command(cmd=["sh", "-c", "echo $TEST_VAR"], env={"TEST_VAR": "test_value"})
    result2 = cmd2.run(capture_output=True, text=True)
    assert result2.returncode == 0
    assert "test_value" in result2.stdout

    # Shell command
    cmd3 = Command(cmd="echo shell test", shell=True)
    result3 = cmd3.run(capture_output=True, text=True)
    assert result3.returncode == 0
    assert "shell test" in result3.stdout

    # Test that CalledProcessError is properly raised and handled
    cmd4 = Command(cmd=["sh", "-c", "exit 1"])
    result4 = cmd4.run(capture_output=True)
    assert result4.returncode == 1  # Should not raise by default

    # When check=True is passed, it should raise CalledProcessError
    cmd5 = Command(cmd=["sh", "-c", "exit 1"])
    with pytest.raises(subprocess.CalledProcessError):
        cmd5.run(check=True, capture_output=True)
