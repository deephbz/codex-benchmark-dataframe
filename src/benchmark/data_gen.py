import numpy as np
import polars as pl


def generate_float32_df(rows: int, cols: int = 50) -> pl.DataFrame:
    """Generate a DataFrame with the given number of rows and float32 columns."""
    data = {f"col_{i}": np.random.rand(rows).astype(np.float32) for i in range(cols)}
    return pl.DataFrame(data)
