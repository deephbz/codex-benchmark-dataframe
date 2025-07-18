#!/usr/bin/env bash
set -euo pipefail

# Optional second argument can specify space separated row sizes
# e.g. ./run_bench.sh benchmark_results "1000 10000 100000"

OUT_DIR="${1:-benchmark_results}"
ROWS_INPUT="${2:-}"
RESULT_MD="results.md"

export PYTHONPATH="$(pwd)/src"
export ROWS_INPUT

# Run benchmarks
uv run python - <<PY
from pathlib import Path
from run_bench import run_benchmarks, ROW_SIZES
import os

rows_str = os.environ.get("ROWS_INPUT")
rows = [int(r) for r in rows_str.split()] if rows_str else ROW_SIZES

out_dir = Path("$OUT_DIR")
results = run_benchmarks(out_dir, rows)
results.write_csv(out_dir / "summary.csv")
with open("$RESULT_MD", "w") as f:
    f.write(results.to_pandas().to_markdown(index=False))
PY

# Copy plot to project root for convenience
cp "$OUT_DIR/benchmark.png" ./benchmark.png

echo "Benchmark complete. Results saved to $OUT_DIR and $RESULT_MD"

