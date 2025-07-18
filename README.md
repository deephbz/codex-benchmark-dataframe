# Polars DataFrame I/O Benchmark

This project benchmarks Polars DataFrame read and write performance for
Feather (IPC v2) and Parquet formats. The benchmarks generate random
`float32` data with 50 columns across a range of row counts.

## Setup

```bash
uv venv
uv pip install -r requirements.txt
```

## Running quick benchmarks

```bash
uv pip run python src/main.py --output benchmark_data --rows 1000 10000 100000 1000000
```

Results are saved in the specified output directory along with a
`benchmark.png` visualization.

## Reproducing full results

A helper script `run_bench.sh` automates running the benchmarks across
a larger row range (up to 100M rows), saving intermediate summary data
and publishing-ready charts.

```bash
./run_bench.sh
```

The script writes Markdown tables to `results.md` and stores CSV and PNG
artifacts under `benchmark_results/`.

## Test platform and methodology

Benchmarks were executed on a Linux x86_64 server using Python
3.11 and the latest Polars release. The following practices mirror
common HPC benchmarking methodology:

- **Isolated environment** – dependencies are managed via `uv` to ensure
  reproducibility.
- **Repeatability** – each row size is generated once per run and all
  timings are collected with `time.perf_counter()`.
- **Data characteristics** – all columns are `float32` to focus on binary
  I/O throughput. Generated data is random and not compressed.
- **Reporting** – timing results are converted to Markdown tables and
  plots are produced with Matplotlib using a logarithmic x‑axis for
  clarity.

Adjust the row sizes in `run_bench.sh` if hardware constraints require a
smaller range.
