from __future__ import annotations
from typing import Dict, List
import matplotlib.pyplot as plt


def plot_results(results: Dict[str, List[float]], row_counts: List[int], out_file: str) -> None:
    """Plot benchmark results and save figure."""
    fig, ax = plt.subplots(figsize=(8, 6))

    for label, times in results.items():
        ax.plot(row_counts, times, marker="o", label=label)

    ax.set_xlabel("Rows")
    ax.set_ylabel("Time (s)")
    ax.set_xscale("log")
    ax.set_title("Polars I/O Benchmark")
    ax.legend()
    ax.grid(True, which="both", ls="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out_file)
    plt.close(fig)
