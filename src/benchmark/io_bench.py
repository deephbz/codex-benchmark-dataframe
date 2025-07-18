from __future__ import annotations
import time
from pathlib import Path
import polars as pl


class IOBenchmark:
    """Benchmark reading and writing DataFrames using Polars."""

    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _time_it(self, func, *args, **kwargs) -> float:
        start = time.perf_counter()
        func(*args, **kwargs)
        return time.perf_counter() - start

    def bench_write_ipc(self, df: pl.DataFrame, filename: str) -> float:
        path = self.base_dir / f"{filename}.feather"
        return self._time_it(df.write_ipc, path)

    def bench_read_ipc(self, filename: str) -> float:
        path = self.base_dir / f"{filename}.feather"
        return self._time_it(pl.read_ipc, path)

    def bench_write_parquet(self, df: pl.DataFrame, filename: str) -> float:
        path = self.base_dir / f"{filename}.parquet"
        return self._time_it(df.write_parquet, path)

    def bench_read_parquet(self, filename: str) -> float:
        path = self.base_dir / f"{filename}.parquet"
        return self._time_it(pl.read_parquet, path)
