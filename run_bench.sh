#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-benchmark_results}"
RESULT_MD="results.md"

# Run benchmarks
uv pip run python - <<PY
from pathlib import Path
import polars as pl
from run_bench import run_benchmarks

out_dir = Path("$OUT_DIR")
results = run_benchmarks(out_dir)
results.write_csv(out_dir / "summary.csv")
with open("$RESULT_MD", "w") as f:
    f.write(results.to_markdown())

PY

# Copy plot to project root for convenience
cp "$OUT_DIR/benchmark.png" ./benchmark.png

echo "Benchmark complete. Results saved to $OUT_DIR and $RESULT_MD"

