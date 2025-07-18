# Polars DataFrame I/O Benchmark

This project benchmarks reading and writing performance of Polars DataFrames
when using Feather (IPC v2) and Parquet formats. The benchmarks generate
random `float32` data with 50 columns and measure performance across a range of
row counts.

## Setup

```bash
uv venv
uv pip install -r requirements.txt
```

## Running

```bash
uv pip run python src/main.py --output benchmark_data --rows 1000 10000 100000 1000000
```

Results are saved in the specified output directory along with a `benchmark.png`
visualization of the timings.
