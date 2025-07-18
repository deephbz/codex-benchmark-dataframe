from __future__ import annotations
from pathlib import Path
import polars as pl
from benchmark.data_gen import generate_float32_df
from benchmark.io_bench import IOBenchmark
from benchmark.plotting import plot_results

ROW_SIZES = [1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]


def run_benchmarks(out_dir: Path, rows: list[int] = ROW_SIZES) -> pl.DataFrame:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bench = IOBenchmark(out_dir)
    records = []
    for n in rows:
        df = generate_float32_df(n)
        tag = f"df_{n}"
        records.append({
            "rows": n,
            "write_ipc": bench.bench_write_ipc(df, tag),
            "read_ipc": bench.bench_read_ipc(tag),
            "write_parquet": bench.bench_write_parquet(df, tag),
            "read_parquet": bench.bench_read_parquet(tag),
        })
    results = pl.DataFrame(records)
    plot_results({
        "write_ipc": results.get_column("write_ipc").to_list(),
        "read_ipc": results.get_column("read_ipc").to_list(),
        "write_parquet": results.get_column("write_parquet").to_list(),
        "read_parquet": results.get_column("read_parquet").to_list(),
    }, rows, str(out_dir / "benchmark.png"))
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Polars I/O benchmarks")
    parser.add_argument("--output", type=Path, default=Path("./benchmark_data"))
    parser.add_argument("--rows", type=int, nargs="*", default=ROW_SIZES)
    args = parser.parse_args()
    df = run_benchmarks(args.output, args.rows)
    print(df)
