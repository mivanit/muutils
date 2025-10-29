"""Benchmark test comparing run_maybe_parallel with other parallelization techniques.

Run with: python tests/benchmark_parallel.py
"""

from pathlib import Path
import time
import multiprocessing
from typing import List, Callable, Any, Dict, Optional, Sequence, Tuple, Union
import pandas as pd  # type: ignore[import-untyped]
import numpy as np
from collections import defaultdict

from muutils.parallel import run_maybe_parallel


def cpu_bound_task(x: int) -> int:
    """CPU-intensive task for benchmarking."""
    # Simulate CPU work with a loop
    result = 0
    for i in range(1000):
        result += (x * i) % 1000
    return result


def io_bound_task(x: int) -> int:
    """IO-bound task for benchmarking."""
    time.sleep(0.001)  # Simulate I/O wait
    return x * 2


def light_cpu_task(x: int) -> int:
    """Light CPU task for benchmarking."""
    return x**2 + x * 3 + 7


class BenchmarkRunner:
    """Run benchmarks and collect timing data."""

    def __init__(self):
        self.results = defaultdict(list)
        self.cpu_count = multiprocessing.cpu_count()

    def time_execution(self, func: Callable, *args, **kwargs) -> float:
        """Time a single execution."""
        start = time.perf_counter()
        func(*args, **kwargs)
        return time.perf_counter() - start

    def benchmark_method(
        self,
        method_name: str,
        method_func: Callable,
        task_func: Callable,
        data: List[int],
        runs: int = 3,
    ) -> Dict[str, float]:
        """Benchmark a single method multiple times."""
        times = []
        for _ in range(runs):
            _, duration = method_func(task_func, data)
            times.append(duration)

        return {
            "mean": np.mean(times),
            "std": np.std(times),
            "min": np.min(times),
            "max": np.max(times),
            "median": np.median(times),
        }

    def run_benchmark_suite(
        self,
        data_sizes: List[int],
        task_funcs: Dict[str, Callable],
        runs_per_method: int = 3,
    ) -> pd.DataFrame:
        """Run complete benchmark suite and return results as DataFrame."""

        for data_size in data_sizes:
            test_data = list(range(data_size))

            for task_name, task_func in task_funcs.items():
                print(f"\nBenchmarking {task_name} with {data_size} items...")

                # Sequential baseline
                stats = self.benchmark_method(
                    "sequential",
                    benchmark_sequential,
                    task_func,
                    test_data,
                    runs_per_method,
                )
                self._record_result("sequential", task_name, data_size, stats)

                # Pool.map
                stats = self.benchmark_method(
                    "pool_map",
                    benchmark_pool_map,
                    task_func,
                    test_data,
                    runs_per_method,
                )
                self._record_result("pool_map", task_name, data_size, stats)

                # Pool.imap with optimal chunk size
                chunksize = max(1, data_size // (self.cpu_count * 4))
                imap_func = lambda f, d: benchmark_pool_imap(f, d, chunksize=chunksize)  # noqa: E731
                stats = self.benchmark_method(
                    "pool_imap", imap_func, task_func, test_data, runs_per_method
                )
                self._record_result("pool_imap", task_name, data_size, stats)

                # Pool.imap_unordered
                imap_unord_func = lambda f, d: benchmark_pool_imap_unordered(  # noqa: E731
                    f, d, chunksize=chunksize
                )
                stats = self.benchmark_method(
                    "pool_imap_unordered",
                    imap_unord_func,
                    task_func,
                    test_data,
                    runs_per_method,
                )
                self._record_result("pool_imap_unordered", task_name, data_size, stats)

                # run_maybe_parallel (ordered)
                rmp_func = lambda f, d: benchmark_run_maybe_parallel(  # noqa: E731
                    f, d, parallel=True
                )
                stats = self.benchmark_method(
                    "run_maybe_parallel",
                    rmp_func,
                    task_func,
                    test_data,
                    runs_per_method,
                )
                self._record_result("run_maybe_parallel", task_name, data_size, stats)

                # run_maybe_parallel (unordered)
                rmp_unord_func = lambda f, d: benchmark_run_maybe_parallel(  # noqa: E731
                    f, d, parallel=True, keep_ordered=False
                )
                stats = self.benchmark_method(
                    "run_maybe_parallel_unordered",
                    rmp_unord_func,
                    task_func,
                    test_data,
                    runs_per_method,
                )
                self._record_result(
                    "run_maybe_parallel_unordered", task_name, data_size, stats
                )

        return self._create_dataframe()

    def _record_result(
        self, method: str, task: str, data_size: int, stats: Dict[str, float]
    ):
        """Record benchmark result."""
        self.results["method"].append(method)
        self.results["task"].append(task)
        self.results["data_size"].append(data_size)
        self.results["mean_time"].append(stats["mean"])
        self.results["std_time"].append(stats["std"])
        self.results["min_time"].append(stats["min"])
        self.results["max_time"].append(stats["max"])
        self.results["median_time"].append(stats["median"])

    def _create_dataframe(self) -> pd.DataFrame:
        """Create DataFrame from results."""
        df = pd.DataFrame(self.results)

        # Calculate speedup relative to sequential
        sequential_times = df[df["method"] == "sequential"][
            ["task", "data_size", "mean_time"]
        ]
        sequential_times = sequential_times.rename(
            columns={"mean_time": "sequential_time"}
        )

        df = df.merge(sequential_times, on=["task", "data_size"])
        df["speedup"] = df["sequential_time"] / df["mean_time"]

        return df


def benchmark_sequential(func: Callable, data: List[int]) -> Tuple[List[Any], float]:
    """Benchmark sequential processing."""
    start = time.perf_counter()
    results = [func(x) for x in data]
    end = time.perf_counter()
    return results, end - start


def benchmark_pool_map(
    func: Callable, data: List[int], processes: int = None
) -> Tuple[List[Any], float]:
    """Benchmark using multiprocessing.Pool.map."""
    start = time.perf_counter()
    with multiprocessing.Pool(processes) as pool:
        results = pool.map(func, data)
    end = time.perf_counter()
    return results, end - start


def benchmark_pool_imap(
    func: Callable, data: List[int], processes: int = None, chunksize: int = 1
) -> Tuple[List[Any], float]:
    """Benchmark using multiprocessing.Pool.imap."""
    start = time.perf_counter()
    with multiprocessing.Pool(processes) as pool:
        results = list(pool.imap(func, data, chunksize=chunksize))
    end = time.perf_counter()
    return results, end - start


def benchmark_pool_imap_unordered(
    func: Callable, data: List[int], processes: int = None, chunksize: int = 1
) -> Tuple[List[Any], float]:
    """Benchmark using multiprocessing.Pool.imap_unordered."""
    start = time.perf_counter()
    with multiprocessing.Pool(processes) as pool:
        results = list(pool.imap_unordered(func, data, chunksize=chunksize))
    end = time.perf_counter()
    return results, end - start


def benchmark_run_maybe_parallel(
    func: Callable,
    data: List[int],
    parallel: Union[bool, int],
    keep_ordered: bool = True,
    chunksize: int = None,
) -> Tuple[List[Any], float]:
    """Benchmark using run_maybe_parallel."""
    start = time.perf_counter()
    results = run_maybe_parallel(
        func=func,
        iterable=data,
        parallel=parallel,
        keep_ordered=keep_ordered,
        chunksize=chunksize,
        pbar="none",  # Disable progress bar for fair comparison
    )
    end = time.perf_counter()
    return results, end - start


def plot_speedup_by_data_size(
    df: pd.DataFrame, task_type: str = None, save_path: str = None
):
    """Plot speedup vs data size for different methods."""
    import matplotlib.pyplot as plt  # type: ignore[import-untyped]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Filter by task type if specified
    plot_df = df[df["task"] == task_type] if task_type else df

    # Group by method and plot
    for method in plot_df["method"].unique():
        if method == "sequential":
            continue
        method_df = plot_df[plot_df["method"] == method]
        ax.plot(method_df["data_size"], method_df["speedup"], marker="o", label=method)

    ax.set_xlabel("Data Size")
    ax.set_ylabel("Speedup (vs Sequential)")
    ax.set_title(f"Speedup by Data Size{f' ({task_type} tasks)' if task_type else ''}")
    ax.set_xscale("log")
    ax.axhline(y=1, color="gray", linestyle="--", alpha=0.5)
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def plot_timing_comparison(
    df: pd.DataFrame, data_size: int = None, save_path: str = None
):
    """Plot timing comparison as bar chart."""
    import matplotlib.pyplot as plt  # type: ignore[import-untyped]

    # Filter by data size if specified
    plot_df = df[df["data_size"] == data_size] if data_size else df

    # Pivot for easier plotting
    pivot_df = plot_df.pivot_table(index="task", columns="method", values="mean_time")

    ax = pivot_df.plot(kind="bar", figsize=(12, 6), rot=0)
    ax.set_ylabel("Time (seconds)")
    ax.set_title(
        f"Timing Comparison{f' (Data Size: {data_size})' if data_size else ''}"
    )
    ax.legend(title="Method", bbox_to_anchor=(1.05, 1), loc="upper left")

    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
    else:
        plt.show()


def plot_efficiency_heatmap(df: pd.DataFrame, save_path: str = None):
    """Plot efficiency heatmap (speedup across methods and tasks)."""
    import matplotlib.pyplot as plt  # type: ignore[import-untyped]

    # Create pivot table for heatmap
    pivot_df = df.pivot_table(
        index=["task", "data_size"], columns="method", values="speedup"
    )

    # Create heatmap
    plt.figure(figsize=(12, 8))
    # sns.heatmap(
    #     pivot_df,
    #     annot=True,
    #     fmt=".2f",
    #     cmap="YlOrRd",
    #     vmin=0,
    #     center=1,
    #     cbar_kws={"label": "Speedup"},
    # )
    plt.imshow(pivot_df, aspect="auto", cmap="YlOrRd", vmin=0)
    plt.colorbar(label="Speedup")
    plt.yticks(range(len(pivot_df.index)), [f"{t[0]}-{t[1]}" for t in pivot_df.index])
    plt.xticks(range(len(pivot_df.columns)), pivot_df.columns, rotation=45)
    plt.title("Parallelization Efficiency Heatmap")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def print_summary_stats(df: pd.DataFrame):
    """Print summary statistics from benchmark results."""
    print("\n=== BENCHMARK SUMMARY ===")
    print(f"\nTotal configurations tested: {len(df)}")

    # Best method by task type
    print("\nBest methods by task type (highest average speedup):")
    best_by_task = (
        df[df["method"] != "sequential"]
        .groupby("task")
        .apply(
            lambda x: x.loc[x["speedup"].idxmax()][["method", "speedup", "data_size"]]
        )
    )
    print(best_by_task)

    # Overall best speedups
    print("\nTop 5 speedups achieved:")
    top_speedups = df[df["method"] != "sequential"].nlargest(5, "speedup")[
        ["method", "task", "data_size", "speedup", "mean_time"]
    ]
    print(top_speedups)

    # Method rankings
    print("\nAverage speedup by method:")
    avg_speedup = (
        df[df["method"] != "sequential"]
        .groupby("method")["speedup"]
        .agg(["mean", "std"])
    )
    print(avg_speedup.sort_values("mean", ascending=False))


_DEFAULT_TASK_FUNCS: dict[str, Callable[[int], int]] = {
    "cpu_bound": cpu_bound_task,
    "io_bound": io_bound_task,
    "light_cpu": light_cpu_task,
}


def main(
    data_sizes: Sequence[int] = (100, 1000, 5000, 10000),
    base_path: Path = Path("."),
    plot: bool = True,
    task_funcs: Optional[Dict[str, Callable[[int], int]]] = None,
):
    """Run benchmarks and display results."""
    print("Starting parallelization benchmark...")

    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)

    # Configure benchmark parameters
    if task_funcs is None:
        task_funcs = _DEFAULT_TASK_FUNCS

    # Run benchmarks
    runner = BenchmarkRunner()
    df = runner.run_benchmark_suite(data_sizes, task_funcs, runs_per_method=3)

    # Save results
    df.to_csv(base_path / "benchmark_results.csv", index=False)
    print("\nResults saved to benchmark_results.csv")

    # Display summary
    print_summary_stats(df)

    if plot:
        # Create visualizations
        import matplotlib  # type: ignore[import-untyped]

        matplotlib.use("Agg")  # Use non-interactive backend

        # Plot speedup by data size for each task type
        for task in task_funcs.keys():
            plot_speedup_by_data_size(df, task, base_path / f"speedup_{task}.png")

        # Plot timing comparison for largest data size
        plot_timing_comparison(df, data_sizes[-1], base_path / "timing_comparison.png")

        # Plot efficiency heatmap
        plot_efficiency_heatmap(df, base_path / "efficiency_heatmap.png")

    return df


if __name__ == "__main__":
    df = main()
    print("\nDataFrame columns:", df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head(10))
