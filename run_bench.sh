#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-benchmark_results}"
RESULT_MD="results.md"

export PYTHONPATH="$(pwd)/src"

# Run benchmarks
uv run python - <<PY
from pathlib import Path
from run_bench import run_benchmarks

out_dir = Path("$OUT_DIR")
results = run_benchmarks(out_dir, repeats=3)
results.write_csv(out_dir / "summary.csv")
with open("$RESULT_MD", "w") as f:
    f.write(results.to_pandas().to_markdown(index=False))
PY

# Copy plot to project root for convenience
cp "$OUT_DIR/benchmark.png" ./benchmark.png

echo "Benchmark complete. Results saved to $OUT_DIR and $RESULT_MD"

