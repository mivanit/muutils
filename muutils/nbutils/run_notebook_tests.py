"""turn a folder of notebooks into scripts, run them, and make sure they work.

made to be called as

```bash
python -m muutils.nbutils.run_notebook_tests --notebooks-dir <notebooks_dir> --converted-notebooks-temp-dir <converted_notebooks_temp_dir>
```
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional
import warnings

from muutils.console_unicode import get_console_safe_str
from muutils.spinner import SpinnerContext


class NotebookTestError(Exception):
    pass


SUCCESS_STR: str = get_console_safe_str("✅", "[OK]")
FAILURE_STR: str = get_console_safe_str("❌", "[!!]")


def run_notebook_tests(
    notebooks_dir: Path,
    converted_notebooks_temp_dir: Path,
    CI_output_suffix: str = ".CI-output.txt",
    run_python_cmd: Optional[str] = None,
    run_python_cmd_fmt: str = "{python_tool} run python",
    python_tool: str = "poetry",
    exit_on_first_fail: bool = False,
):
    """Run converted Jupyter notebooks as Python scripts and verify they execute successfully.

    Takes a directory of notebooks and their corresponding converted Python scripts,
    executes each script, and captures the output. Failures are collected and reported,
    with optional early exit on first failure.

    # Parameters:
     - `notebooks_dir : Path`
        Directory containing the original .ipynb notebook files
     - `converted_notebooks_temp_dir : Path`
        Directory containing the corresponding converted .py files
     - `CI_output_suffix : str`
        Suffix to append to output files capturing execution results
        (defaults to `".CI-output.txt"`)
     - `run_python_cmd : str | None`
        Custom command to run Python scripts. Overrides python_tool and run_python_cmd_fmt if provided
        (defaults to `None`)
     - `run_python_cmd_fmt : str`
        Format string for constructing the Python run command
        (defaults to `"{python_tool} run python"`)
     - `python_tool : str`
        Tool used to run Python (e.g. poetry, uv)
        (defaults to `"poetry"`)
     - `exit_on_first_fail : bool`
        Whether to raise exception immediately on first notebook failure
        (defaults to `False`)

    # Returns:
     - `None`

    # Modifies:
     - Working directory: Temporarily changes to notebooks_dir during execution
     - Filesystem: Creates output files with CI_output_suffix for each notebook

    # Raises:
     - `NotebookTestError`: If any notebooks fail to execute, or if input directories are invalid
     - `TypeError`: If run_python_cmd is provided but not a string

    # Usage:
    ```python
    >>> run_notebook_tests(
    ...     notebooks_dir=Path("notebooks"),
    ...     converted_notebooks_temp_dir=Path("temp/converted"),
    ...     python_tool="poetry"
    ... )
    # testing notebooks in 'notebooks'
    # reading converted notebooks from 'temp/converted'
    Running 1/2: temp/converted/notebook1.py
        Output in temp/converted/notebook1.CI-output.txt
        {SUCCESS_STR} Run completed with return code 0
    ```
    """

    run_python_cmd_: str
    if run_python_cmd is None:
        run_python_cmd_ = run_python_cmd_fmt.format(python_tool=python_tool)
    elif isinstance(run_python_cmd, str):
        run_python_cmd_ = run_python_cmd
        warnings.warn(
            "You have specified a custom run_python_cmd, this will override the `python_tool` parameter and `run_python_cmd_fmt` parameter. This will be removed in a future version.",
            DeprecationWarning,
        )
    else:
        raise TypeError(
            f"run_python_cmd must be a string or None, got {run_python_cmd =}, {type(run_python_cmd) =}"
        )

    original_cwd: Path = Path.cwd()
    # get paths
    notebooks_dir = Path(notebooks_dir)
    converted_notebooks_temp_dir = Path(converted_notebooks_temp_dir)
    root_relative_to_notebooks: Path = Path(os.path.relpath(".", notebooks_dir))

    term_width: int
    try:
        term_width = os.get_terminal_size().columns
    except OSError:
        term_width = 80

    exceptions: dict[str, str] = dict()

    print(f"# testing notebooks in '{notebooks_dir}'")
    print(
        f"# reading converted notebooks from '{converted_notebooks_temp_dir.as_posix()}'"
    )

    try:
        # check things exist
        if not notebooks_dir.exists():
            raise NotebookTestError(f"Notebooks dir '{notebooks_dir}' does not exist")
        if not notebooks_dir.is_dir():
            raise NotebookTestError(
                f"Notebooks dir '{notebooks_dir}' is not a directory"
            )
        if not converted_notebooks_temp_dir.exists():
            raise NotebookTestError(
                f"Converted notebooks dir '{converted_notebooks_temp_dir}' does not exist"
            )
        if not converted_notebooks_temp_dir.is_dir():
            raise NotebookTestError(
                f"Converted notebooks dir '{converted_notebooks_temp_dir}' is not a directory"
            )

        notebooks: list[Path] = list(notebooks_dir.glob("*.ipynb"))
        if not notebooks:
            raise NotebookTestError(f"No notebooks found in '{notebooks_dir}'")

        converted_notebooks: list[Path] = list()
        for nb in notebooks:
            converted_file: Path = (
                converted_notebooks_temp_dir / nb.with_suffix(".py").name
            )
            if not converted_file.exists():
                raise NotebookTestError(
                    f"Did not find converted notebook '{converted_file}' for '{nb}'"
                )
            converted_notebooks.append(converted_file)

        del converted_file

        # the location of this line is important
        os.chdir(notebooks_dir)

        n_notebooks: int = len(converted_notebooks)
        for idx, file in enumerate(converted_notebooks):
            # run the file
            print(f"Running {idx+1}/{n_notebooks}: {file.as_posix()}")
            output_file: Path = file.with_suffix(CI_output_suffix)
            print(f"    Output in {output_file.as_posix()}")
            with SpinnerContext(
                spinner_chars="braille",
                update_interval=0.5,
                format_string="\r    {spinner} ({elapsed_time:.2f}s) {message}{value}",
            ):
                command: str = f"{run_python_cmd_} {root_relative_to_notebooks / file} > {root_relative_to_notebooks / output_file} 2>&1"
                process: subprocess.CompletedProcess = subprocess.run(
                    command,
                    shell=True,
                    text=True,
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                )

            if process.returncode == 0:
                print(
                    f"    {SUCCESS_STR} Run completed with return code {process.returncode}"
                )
            else:
                print(
                    f"    {FAILURE_STR} Run failed with return code {process.returncode}!!! Check {output_file.as_posix()}"
                )

            # print the output of the file to the console if it failed
            if process.returncode != 0:
                with open(root_relative_to_notebooks / output_file, "r") as f:
                    file_output: str = f.read()
                err: str = f"Error in {file}:\n{'-'*term_width}\n{file_output}"
                exceptions[file.as_posix()] = err
                if exit_on_first_fail:
                    raise NotebookTestError(err)

            del process

        if len(exceptions) > 0:
            exceptions_str: str = ("\n" + "=" * term_width + "\n").join(
                list(exceptions.values())
            )
            raise NotebookTestError(
                exceptions_str
                + "=" * term_width
                + f"\n{FAILURE_STR} {len(exceptions)}/{n_notebooks} notebooks failed:\n{list(exceptions.keys())}"
            )

    except NotebookTestError as e:
        print("!" * term_width, file=sys.stderr)
        print(e, file=sys.stderr)
        print("!" * term_width, file=sys.stderr)
        raise e
    finally:
        # return to original cwd
        os.chdir(original_cwd)


if __name__ == "__main__":
    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument(
        "--notebooks-dir",
        type=str,
        help="The directory from which to run the notebooks",
    )
    parser.add_argument(
        "--converted-notebooks-temp-dir",
        type=str,
        help="The directory containing the converted notebooks to test",
    )
    parser.add_argument(
        "--python-tool",
        type=str,
        default="poetry",
        help="The python tool to use to run the notebooks (usually uv or poetry)",
    )
    parser.add_argument(
        "--run-python-cmd-fmt",
        type=str,
        default="{python_tool} run python",
        help="The command to run python with the python tool. if you don't want to use poetry or uv, you can just set this to 'python'",
    )

    args: argparse.Namespace = parser.parse_args()

    run_notebook_tests(
        notebooks_dir=Path(args.notebooks_dir),
        converted_notebooks_temp_dir=Path(args.converted_notebooks_temp_dir),
        python_tool=args.python_tool,
        run_python_cmd_fmt=args.run_python_cmd_fmt,
    )
