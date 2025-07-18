from __future__ import annotations
import argparse
from pathlib import Path
from benchmark.data_gen import generate_float32_df
from benchmark.io_bench import IOBenchmark
from benchmark.plotting import plot_results


ROW_SIZES = [1_000, 10_000, 100_000, 1_000_000]


def run_benchmarks(output_dir: Path, rows: list[int]) -> None:
    bench = IOBenchmark(output_dir)
    write_ipc_times = []
    read_ipc_times = []
    write_parquet_times = []
    read_parquet_times = []

    for n in rows:
        df = generate_float32_df(n)
        tag = f"df_{n}"
        write_ipc_times.append(bench.bench_write_ipc(df, tag))
        read_ipc_times.append(bench.bench_read_ipc(tag))
        write_parquet_times.append(bench.bench_write_parquet(df, tag))
        read_parquet_times.append(bench.bench_read_parquet(tag))

    results = {
        "write_ipc": write_ipc_times,
        "read_ipc": read_ipc_times,
        "write_parquet": write_parquet_times,
        "read_parquet": read_parquet_times,
    }
    plot_results(results, rows, str(output_dir / "benchmark.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Polars I/O benchmarks")
    parser.add_argument("--output", type=Path, default=Path("./benchmark_data"))
    parser.add_argument("--rows", type=int, nargs="*", default=ROW_SIZES)
    args = parser.parse_args()

    run_benchmarks(args.output, args.rows)
