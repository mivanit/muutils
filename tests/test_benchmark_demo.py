#!/usr/bin/env python3
"""Simple demo of using the benchmark script."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.benchmark_parallel import (
    BenchmarkRunner,
    cpu_bound_task,
    io_bound_task,
    light_cpu_task,
    print_summary_stats,
)


def quick_benchmark():
    """Run a quick benchmark with small data sizes."""
    print("Running quick benchmark demo...\n")

    # Small data sizes for quick demo
    data_sizes = [100, 500, 1000]
    task_funcs = {
        "cpu_bound": cpu_bound_task,
        "io_bound": io_bound_task,
        "light_cpu": light_cpu_task,
    }

    # Run benchmarks
    runner = BenchmarkRunner()
    df = runner.run_benchmark_suite(data_sizes, task_funcs, runs_per_method=2)

    # Print results
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS DATAFRAME")
    print("=" * 60)
    print(df.to_string())

    print("\n" + "=" * 60)
    print_summary_stats(df)

    # Show example of filtering data
    print("\n" + "=" * 60)
    print("EXAMPLE: CPU-bound tasks only")
    print("=" * 60)
    cpu_df = df[df["task"] == "cpu_bound"]
    print(cpu_df[["method", "data_size", "mean_time", "speedup"]].to_string())

    return df


if __name__ == "__main__":
    df = quick_benchmark()
