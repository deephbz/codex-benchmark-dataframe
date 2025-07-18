import numpy as np
import polars as pl


def generate_float32_df(
    rows: int,
    cols: int = 50,
    *,
    chunk_size: int | None = None,
    lazy: bool = False,
) -> pl.DataFrame | pl.LazyFrame:
    """Generate a DataFrame with the given number of rows and float32 columns.

    Parameters
    ----------
    rows:
        Number of rows in the resulting frame.
    cols:
        Number of `float32` columns to create.
    chunk_size:
        Optional chunk size used when ``rows`` is very large. If provided, data
        is generated in smaller pieces and concatenated which can help reduce
        peak memory usage during creation.
    lazy:
        Return a ``LazyFrame`` instead of a ``DataFrame``.
    """

    if chunk_size is None or rows <= chunk_size:
        data = {
            f"col_{i}": np.random.rand(rows).astype(np.float32) for i in range(cols)
        }
        df = pl.DataFrame(data)
    else:
        dfs = []
        for start in range(0, rows, chunk_size):
            end = min(start + chunk_size, rows)
            data = {
                f"col_{i}": np.random.rand(end - start).astype(np.float32)
                for i in range(cols)
            }
            dfs.append(pl.DataFrame(data))
        df = pl.concat(dfs, how="vertical")

    return df.lazy() if lazy else df
