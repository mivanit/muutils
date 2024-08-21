from __future__ import annotations

import argparse
import json
import os
import sys
import typing
import warnings

from muutils.spinner import SpinnerContext

DISABLE_PLOTS: dict[str, list[str]] = {
    "matplotlib": [
        """
# ------------------------------------------------------------
# Disable matplotlib plots, done during processing by `convert_ipynb_to_script.py`
import matplotlib.pyplot as plt
plt.show = lambda: None
# ------------------------------------------------------------
"""
    ],
    "circuitsvis": [
        """
# ------------------------------------------------------------
# Disable circuitsvis plots, done during processing by `convert_ipynb_to_script.py`
from circuitsvis.utils.convert_props import PythonProperty, convert_props
from circuitsvis.utils.render import RenderedHTML, render, render_cdn, render_local

def new_render(
    react_element_name: str,
    **kwargs: PythonProperty
) -> RenderedHTML:
    "return a visualization as raw HTML"
    local_src = render_local(react_element_name, **kwargs)
    cdn_src = render_cdn(react_element_name, **kwargs)
    # return as string instead of RenderedHTML for CI
    return str(RenderedHTML(local_src, cdn_src))

render = new_render
# ------------------------------------------------------------
"""
    ],
    "muutils": [
        """import muutils.nbutils.configure_notebook as nb_conf
nb_conf.CONVERSION_PLOTMODE_OVERRIDE = "ignore"
"""
    ],
}

DISABLE_PLOTS_WARNING: list[str] = [
    """
# ------------------------------------------------------------
# WARNING: this script is auto-generated by `convert_ipynb_to_script.py`
# showing plots has been disabled, so this is presumably in a temp dict for CI or something
# so don't modify this code, it will be overwritten!
# ------------------------------------------------------------
""".lstrip()
]


def disable_plots_in_script(script_lines: list[str]) -> list[str]:
    """Disable plots in a script by adding cursed things after the import statements"""
    result_str_TEMP: str = "\n\n".join(script_lines)
    script_lines_new: list[str] = script_lines

    if "muutils" in result_str_TEMP:
        script_lines_new = DISABLE_PLOTS["muutils"] + script_lines_new

    if "matplotlib" in result_str_TEMP:
        assert (
            "import matplotlib.pyplot as plt" in result_str_TEMP
        ), "matplotlib.pyplot must be imported as plt"

        # find the last import statement involving matplotlib, and the first line that uses plt
        mpl_last_import_index: int = -1
        mpl_first_usage_index: int = -1
        for i, line in enumerate(script_lines_new):
            if "matplotlib" in line and (("import" in line) or ("from" in line)):
                mpl_last_import_index = i

            if "configure_notebook" in line:
                mpl_last_import_index = i

            if "plt." in line:
                mpl_first_usage_index = i

        assert (
            mpl_last_import_index != -1
        ), f"matplotlib imports not found! see line {mpl_last_import_index}"
        if mpl_first_usage_index != -1:
            assert (
                mpl_first_usage_index > mpl_last_import_index
            ), f"matplotlib plots created before import! see lines {mpl_first_usage_index}, {mpl_last_import_index}"
        else:
            warnings.warn(
                "could not find where matplotlib is used, plot disabling might not work!"
            )

        # insert the cursed things
        script_lines_new = (
            script_lines_new[: mpl_last_import_index + 1]
            + DISABLE_PLOTS["matplotlib"]
            + script_lines_new[mpl_last_import_index + 1 :]
        )
        result_str_TEMP = "\n\n".join(script_lines_new)

    if "circuitsvis" in result_str_TEMP:
        # find the last import statement involving circuitsvis, and the first line that uses it
        cirv_last_import_index: int = -1
        cirv_first_usage_index: int = -1

        for i, line in enumerate(script_lines_new):
            if "circuitsvis" in line:
                if (("import" in line) or ("from" in line)) and "circuitsvis" in line:
                    cirv_last_import_index = i
                else:
                    cirv_first_usage_index = i

                if "configure_notebook" in line:
                    mpl_last_import_index = i

                if "render" in line:
                    cirv_first_usage_index = i

        assert (
            cirv_last_import_index != -1
        ), f"circuitsvis imports not found! see line {cirv_last_import_index}"
        if cirv_first_usage_index != -1:
            assert (
                cirv_first_usage_index > cirv_last_import_index
            ), f"circuitsvis plots created before import! see lines {cirv_first_usage_index}, {cirv_last_import_index}"
        else:
            warnings.warn(
                "could not find where circuitsvis is used, plot disabling might not work!"
            )

        # insert the cursed things
        script_lines_new = (
            script_lines_new[: cirv_last_import_index + 1]
            + DISABLE_PLOTS["circuitsvis"]
            + script_lines_new[cirv_last_import_index + 1 :]
        )
        result_str_TEMP = "\n\n".join(script_lines_new)

    return script_lines_new


def convert_ipynb(
    notebook: dict,
    strip_md_cells: bool = False,
    header_comment: str = r"#%%",
    disable_plots: bool = False,
    filter_out_lines: str | typing.Sequence[str] = (
        "%",
        "!",
    ),  # ignore notebook magic commands and shell commands
) -> str:
    """Convert Jupyter Notebook to a script, doing some basic filtering and formatting.

    # Arguments
        - `notebook: dict`: Jupyter Notebook loaded as json.
        - `strip_md_cells: bool = False`: Remove markdown cells from the output script.
        - `header_comment: str = r'#%%'`: Comment string to separate cells in the output script.
        - `disable_plots: bool = False`: Disable plots in the output script.
        - `filter_out_lines: str|typing.Sequence[str] = ('%', '!')`: comment out lines starting with these strings (in code blocks).
            if a string is passed, it will be split by char and each char will be treated as a separate filter.

    # Returns
        - `str`: Converted script.
    """

    if isinstance(filter_out_lines, str):
        filter_out_lines = tuple(filter_out_lines)
    filter_out_lines_set: set = set(filter_out_lines)

    result: list[str] = []

    all_cells: list[dict] = notebook["cells"]

    for cell in all_cells:
        cell_type: str = cell["cell_type"]

        if not strip_md_cells and cell_type == "markdown":
            result.append(f'{header_comment}\n"""\n{"".join(cell["source"])}\n"""')
        elif cell_type == "code":
            source: list[str] = cell["source"]
            if filter_out_lines:
                source = [
                    (
                        f"#{line}"
                        if any(
                            line.startswith(filter_prefix)
                            for filter_prefix in filter_out_lines_set
                        )
                        else line
                    )
                    for line in source
                ]
            result.append(f'{header_comment}\n{"".join(source)}')

    if disable_plots:
        result = disable_plots_in_script(result)
        result = DISABLE_PLOTS_WARNING + result

    return "\n\n".join(result)


def process_file(
    in_file: str,
    out_file: str | None = None,
    strip_md_cells: bool = False,
    header_comment: str = r"#%%",
    disable_plots: bool = False,
    filter_out_lines: str | typing.Sequence[str] = ("%", "!"),
):
    print(f"\tProcessing {in_file}...", file=sys.stderr)
    assert os.path.exists(in_file), f"File {in_file} does not exist."
    assert os.path.isfile(in_file), f"Path {in_file} is not a file."
    assert in_file.endswith(".ipynb"), f"File {in_file} is not a Jupyter Notebook."

    with open(in_file, "r") as file:
        notebook: dict = json.load(file)

    try:
        converted_script: str = convert_ipynb(
            notebook=notebook,
            strip_md_cells=strip_md_cells,
            header_comment=header_comment,
            disable_plots=disable_plots,
            filter_out_lines=filter_out_lines,
        )
    except AssertionError as e:
        print(f"Error converting {in_file}: {e}", file=sys.stderr)
        raise e

    if out_file:
        with open(out_file, "w") as file:
            file.write(converted_script)
    else:
        print(converted_script)


def process_dir(
    input_dir: str,
    output_dir: str,
    strip_md_cells: bool = False,
    header_comment: str = r"#%%",
    disable_plots: bool = False,
    filter_out_lines: str | typing.Sequence[str] = ("%", "!"),
):
    """Convert all Jupyter Notebooks in a directory to scripts.

    # Arguments
        - `input_dir: str`: Input directory.
        - `output_dir: str`: Output directory.
        - `strip_md_cells: bool = False`: Remove markdown cells from the output script.
        - `header_comment: str = r'#%%'`: Comment string to separate cells in the output script.
        - `disable_plots: bool = False`: Disable plots in the output script.
        - `filter_out_lines: str|typing.Sequence[str] = ('%', '!')`: comment out lines starting with these strings (in code blocks).
            if a string is passed, it will be split by char and each char will be treated as a separate filter.
    """

    assert os.path.exists(input_dir), f"Directory {input_dir} does not exist."
    assert os.path.isdir(input_dir), f"Path {input_dir} is not a directory."

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    filenames: list[str] = [
        fname for fname in os.listdir(input_dir) if fname.endswith(".ipynb")
    ]

    assert filenames, f"Directory {input_dir} does not contain any Jupyter Notebooks."
    n_files: int = len(filenames)
    print(f"Converting {n_files} notebooks:", file=sys.stderr)

    with SpinnerContext(
        spinner_chars="braille",
        update_interval=0.01,
        format_string_when_updated=True,
        output_stream=sys.stderr,
    ) as spinner:
        for idx, fname in enumerate(filenames):
            spinner.update_value(f"\tConverting {idx+1}/{n_files}: {fname}")
            in_file: str = os.path.join(input_dir, fname)
            out_file: str = os.path.join(output_dir, fname.replace(".ipynb", ".py"))

            with open(in_file, "r", encoding="utf-8") as file_in:
                notebook: dict = json.load(file_in)

            try:
                converted_script: str = convert_ipynb(
                    notebook=notebook,
                    strip_md_cells=strip_md_cells,
                    header_comment=header_comment,
                    disable_plots=disable_plots,
                    filter_out_lines=filter_out_lines,
                )
            except AssertionError as e:
                spinner.stop()
                raise Exception(f"Error converting {in_file}") from e

            with open(out_file, "w", encoding="utf-8") as file_out:
                file_out.write(converted_script)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Jupyter Notebook to a script with cell separators."
    )
    parser.add_argument(
        "in_path",
        type=str,
        help="Input Jupyter Notebook file (.ipynb) or directory of files.",
    )
    parser.add_argument(
        "--out_file",
        type=str,
        help="Output script file. If not specified, the result will be printed to stdout.",
    )
    parser.add_argument(
        "--output_dir", type=str, help="Output directory for converted script files."
    )
    parser.add_argument(
        "--strip_md_cells",
        action="store_true",
        help="Remove markdown cells from the output script.",
    )
    parser.add_argument(
        "--header_comment",
        type=str,
        default=r"#%%",
        help="Comment string to separate cells in the output script.",
    )
    parser.add_argument(
        "--disable_plots",
        action="store_true",
        help="Disable plots in the output script. Useful for testing in CI.",
    )
    parser.add_argument(
        "--filter_out_lines",
        type=str,
        default="%",
        help="Comment out lines starting with these characters.",
    )

    args = parser.parse_args()

    if args.output_dir:
        assert not args.out_file, "Cannot specify both --out_file and --output_dir."
        process_dir(
            input_dir=args.in_path,
            output_dir=args.output_dir,
            strip_md_cells=args.strip_md_cells,
            header_comment=args.header_comment,
            disable_plots=args.disable_plots,
            filter_out_lines=args.filter_out_lines,
        )

    else:
        process_file(
            in_file=args.in_path,
            out_file=args.out_file,
            strip_md_cells=args.strip_md_cells,
            header_comment=args.header_comment,
            disable_plots=args.disable_plots,
            filter_out_lines=args.filter_out_lines,
        )
