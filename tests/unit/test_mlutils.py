import sys
from pathlib import Path

from muutils.mlutils import get_checkpoint_paths_for_run, register_method


def test_get_checkpoint_paths_for_run():
    run_path = Path("tests/junk_data/test_get_checkpoint_paths")
    run_path.mkdir(parents=True, exist_ok=True)
    checkpoints_path = run_path / "checkpoints"
    checkpoint1_path = checkpoints_path / "model.iter_123.pt"
    checkpoint2_path = checkpoints_path / "model.iter_456.pt"
    other_path = checkpoints_path / "other_file.txt"

    checkpoints_path.mkdir()
    checkpoint1_path.touch()
    checkpoint2_path.touch()
    other_path.touch()

    checkpoint_paths = get_checkpoint_paths_for_run(run_path, "pt")

    assert checkpoint_paths == [(123, checkpoint1_path), (456, checkpoint2_path)]


def test_register_method():
    class TestEvalsA:
        evals = {}

        @register_method(evals)
        @staticmethod
        def eval_function():
            pass

        @staticmethod
        def other_function():
            pass

    class TestEvalsB:
        evals = {}

        @register_method(evals)
        @staticmethod
        def other_eval_function():
            pass

    evalsA = TestEvalsA.evals
    evalsB = TestEvalsB.evals
    if sys.version_info >= (3, 9):
        assert list(evalsA.keys()) == ["eval_function"]
        assert list(evalsB.keys()) == ["other_eval_function"]
    else:
        assert len(evalsA) == 1
        assert len(evalsB) == 1
