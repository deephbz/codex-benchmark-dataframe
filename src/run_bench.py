from __future__ import annotations
from pathlib import Path
import numpy as np
import polars as pl
from benchmark.data_gen import generate_float32_df
from benchmark.io_bench import IOBenchmark
from benchmark.plotting import plot_results

# Default row sizes keep memory usage reasonable. Adjust if needed.
ROW_SIZES = [1_000, 10_000, 100_000, 1_000_000]


def run_benchmarks(
    out_dir: Path, rows: list[int] = ROW_SIZES, repeats: int = 1
) -> pl.DataFrame:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bench = IOBenchmark(out_dir)
    records = []
    for n in rows:
        df = generate_float32_df(n)
        tag = f"df_{n}"

        write_ipc_times = [bench.bench_write_ipc(df, tag) for _ in range(repeats)]
        read_ipc_times = [bench.bench_read_ipc(tag) for _ in range(repeats)]
        write_parquet_times = [
            bench.bench_write_parquet(df, tag) for _ in range(repeats)
        ]
        read_parquet_times = [
            bench.bench_read_parquet(tag) for _ in range(repeats)
        ]

        records.append({
            "rows": n,
            "write_ipc_mean": float(np.mean(write_ipc_times)),
            "write_ipc_std": float(np.std(write_ipc_times, ddof=0)),
            "read_ipc_mean": float(np.mean(read_ipc_times)),
            "read_ipc_std": float(np.std(read_ipc_times, ddof=0)),
            "write_parquet_mean": float(np.mean(write_parquet_times)),
            "write_parquet_std": float(np.std(write_parquet_times, ddof=0)),
            "read_parquet_mean": float(np.mean(read_parquet_times)),
            "read_parquet_std": float(np.std(read_parquet_times, ddof=0)),
        })
    results = pl.DataFrame(records)
    plot_results(
        {
            "write_ipc": results.get_column("write_ipc_mean").to_list(),
            "read_ipc": results.get_column("read_ipc_mean").to_list(),
            "write_parquet": results.get_column("write_parquet_mean").to_list(),
            "read_parquet": results.get_column("read_parquet_mean").to_list(),
        },
        rows,
        str(out_dir / "benchmark.png"),
    )
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Polars I/O benchmarks")
    parser.add_argument("--output", type=Path, default=Path("./benchmark_data"))
    parser.add_argument("--rows", type=int, nargs="*", default=ROW_SIZES)
    parser.add_argument("--repeats", type=int, default=1, help="Number of repetitions for each benchmark")
    args = parser.parse_args()
    df = run_benchmarks(args.output, args.rows, args.repeats)
    print(df)
