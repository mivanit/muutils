import os

from muutils.nbutils.convert_ipynb_to_script import process_dir
from muutils.nbutils.run_notebook_tests import run_notebook_tests

notebooks_input_dir: str = "tests/input_data/notebooks"
notebooks_converted_input_dir: str = "tests/input_data/notebooks_converted/"
test_output_dir: str = "tests/junk_data/test_conversion"


def test_run_notebook_tests():
    os.makedirs(test_output_dir, exist_ok=True)
    print(os.listdir(notebooks_input_dir))
    print(os.listdir(notebooks_converted_input_dir))

    # convert the notebooks
    process_dir(
        input_dir=notebooks_input_dir,
        output_dir=test_output_dir,
        disable_plots=True,
    )

    # run the notebooks
    run_notebook_tests(
        notebooks_dir=notebooks_input_dir,
        converted_notebooks_temp_dir=test_output_dir,
        run_python_cmd="python",
    )

    # assert output directory contents are identical
    output_files: list = sorted(os.listdir(notebooks_converted_input_dir))
    assert sorted(os.listdir(test_output_dir)) == output_files

    for fname in output_files:
        with open(os.path.join(notebooks_converted_input_dir, fname), "r") as f:
            expected = f.read()
        with open(os.path.join(test_output_dir, fname), "r") as f:
            actual = f.read()
        assert expected == actual
