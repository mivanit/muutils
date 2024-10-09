from __future__ import annotations

import itertools
import os

import pytest

from muutils.nbutils.convert_ipynb_to_script import process_dir, process_file
from muutils.nbutils.run_notebook_tests import run_notebook_tests

notebooks_input_dir: str = "tests/input_data/notebooks"
notebooks_converted_input_dir: str = "tests/input_data/notebooks_converted/"
nb_test_dir: str = "tests/_temp/run_notebook_tests"
nb_conversion_dir: str = "tests/_temp/test_file_conversion"


def test_run_notebook_tests():
    os.makedirs(nb_test_dir, exist_ok=True)
    print(os.listdir(notebooks_input_dir))
    print(os.listdir(notebooks_converted_input_dir))

    # convert the notebooks
    process_dir(
        input_dir=notebooks_input_dir,
        output_dir=nb_test_dir,
        disable_plots=True,
    )

    # run the notebooks
    run_notebook_tests(
        notebooks_dir=notebooks_input_dir,
        converted_notebooks_temp_dir=nb_test_dir,
        run_python_cmd="python",
    )

    # assert output directory contents are identical
    output_files: list = sorted(os.listdir(notebooks_converted_input_dir))
    assert sorted(os.listdir(nb_test_dir)) == output_files

    for fname in output_files:
        with open(os.path.join(notebooks_converted_input_dir, fname), "r") as f:
            expected = f.read()
        with open(os.path.join(nb_test_dir, fname), "r") as f:
            actual = f.read()
        assert expected == actual


@pytest.mark.parametrize(
    "idx, args",
    enumerate(
        itertools.product(
            [True, False],
            [r"#%%", "#" + "=" * 50],
            [True, False],
            ["%", ("!", "#"), ("import", "return")],
        )
    ),
)
def test_file_conversion(idx, args):
    os.makedirs(nb_conversion_dir, exist_ok=True)
    process_file(
        in_file=os.path.join(notebooks_input_dir, "dummy_notebook.ipynb"),
        out_file=os.path.join(nb_conversion_dir, f"dn-test-{idx}.py"),
        strip_md_cells=args[0],
        header_comment=args[1],
        disable_plots=args[2],
        filter_out_lines=args[3],
    )
