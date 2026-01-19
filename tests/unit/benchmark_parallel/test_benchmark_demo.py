"""Simple demo of using the benchmark script."""

from pathlib import Path

from .benchmark_parallel import io_bound_task, light_cpu_task, main


def test_main():
    """Test the main function of the benchmark script."""
    _ = main(
        data_sizes=(1, 2),
        base_path=Path("tests/_temp/benchmark_demo"),
        plot=True,
        task_funcs={
            "io_bound": io_bound_task,
            "light_cpu": light_cpu_task,
        },
    )
