#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-benchmark_results}"
IPC_COMP="${2:-zstd}"
PARQUET_COMP="${3:-zstd}"
RESULT_MD="results.md"

export PYTHONPATH="$(pwd)/src"

# Run benchmarks
uv run python - <<PY
from pathlib import Path
from run_bench import run_benchmarks

out_dir = Path("$OUT_DIR")
results = run_benchmarks(
    out_dir,
    ipc_compression="$IPC_COMP",
    parquet_compression="$PARQUET_COMP",
)
results.write_csv(out_dir / "summary.csv")
with open("$RESULT_MD", "w") as f:
    f.write(results.to_pandas().to_markdown(index=False))
PY

# Copy plot to project root for convenience
cp "$OUT_DIR/benchmark.png" ./benchmark.png

echo "Benchmark complete. Results saved to $OUT_DIR and $RESULT_MD"

