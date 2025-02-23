import sys
from pathlib import Path

from muutils.mlutils import get_checkpoint_paths_for_run, register_method


def test_get_checkpoint_paths_for_run():
    run_path = Path("tests/_temp/test_get_checkpoint_paths")
    run_path.mkdir(parents=True, exist_ok=True)
    checkpoints_path = run_path / "checkpoints"
    checkpoint1_path = checkpoints_path / "model.iter_123.pt"
    checkpoint2_path = checkpoints_path / "model.iter_456.pt"
    other_path = checkpoints_path / "other_file.txt"

    checkpoints_path.mkdir(exist_ok=True)
    checkpoint1_path.touch()
    checkpoint2_path.touch()
    other_path.touch()

    checkpoint_paths = get_checkpoint_paths_for_run(run_path, "pt")

    assert checkpoint_paths == [(123, checkpoint1_path), (456, checkpoint2_path)]


BELOW_PY_3_10: bool = sys.version_info < (3, 10)


def test_register_method(recwarn):
    class TestEvalsA:
        evals: dict = {}

        @register_method(evals)
        @staticmethod
        def eval_function():
            pass

        @staticmethod
        def other_function():
            pass

    class TestEvalsB:
        evals: dict = {}

        @register_method(evals)
        @staticmethod
        def other_eval_function():
            pass

    if BELOW_PY_3_10:
        assert len(recwarn) == 2
    else:
        assert len(recwarn) == 0

    evalsA = TestEvalsA.evals
    evalsB = TestEvalsB.evals
    if BELOW_PY_3_10:
        assert len(evalsA) == 1
        assert len(evalsB) == 1
    else:
        assert list(evalsA.keys()) == ["eval_function"]
        assert list(evalsB.keys()) == ["other_eval_function"]
