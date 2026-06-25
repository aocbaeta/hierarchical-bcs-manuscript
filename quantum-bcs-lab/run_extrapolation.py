"""Finite-size extrapolation of pair-source scaling data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: float(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def fit_vs_inverse_n(rows: list[dict], output_dir: Path) -> list[dict]:
    etas = sorted({row["eta"] for row in rows})
    fits = []
    for eta in etas:
        subset = sorted([row for row in rows if row["eta"] == eta], key=lambda row: row["levels"])
        n = np.array([row["levels"] for row in subset], dtype=float)
        x = 1.0 / n
        y = np.array([row["relative_source_profile_error"] for row in subset], dtype=float)
        coeff = np.polyfit(x, y, deg=1)
        intercept, slope = float(coeff[1]), float(coeff[0])
        pred = slope * x + intercept
        ss_res = float(np.sum((y - pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        fits.append({"eta": eta, "error_infinite_n": intercept, "slope_1_over_n": slope, "r2": r2})

    with (output_dir / "extrapolation_fits.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fits[0].keys()))
        writer.writeheader()
        writer.writerows(fits)

    eta_arr = np.array([row["eta"] for row in fits])
    inf_err = np.array([row["error_infinite_n"] for row in fits])
    plt.figure(figsize=(7.2, 4.7))
    plt.semilogx(eta_arr, inf_err, marker="o", linewidth=1.8)
    plt.xlabel("pair source eta")
    plt.ylabel("linear extrapolated error at 1/N -> 0")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "extrapolated_error_vs_eta.png", dpi=180)
    plt.close()

    selected = [etas[0], etas[len(etas) // 2], etas[-1]]
    plt.figure(figsize=(7.2, 4.7))
    for eta in selected:
        subset = sorted([row for row in rows if row["eta"] == eta], key=lambda row: row["levels"])
        n = np.array([row["levels"] for row in subset], dtype=float)
        x = 1.0 / n
        y = np.array([row["relative_source_profile_error"] for row in subset], dtype=float)
        coeff = np.polyfit(x, y, deg=1)
        grid = np.linspace(0.0, max(x), 100)
        plt.plot(x, y, "o", label=f"data eta={eta:.2g}")
        plt.plot(grid, coeff[0] * grid + coeff[1], "-", alpha=0.8)
    plt.xlabel("1/N")
    plt.ylabel("relative source-profile error")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "error_vs_inverse_n_fits.png", dpi=180)
    plt.close()

    return fits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="scaling-results/scaling_sweep_results.csv")
    parser.add_argument("--output-dir", default="extrapolation-results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fits = fit_vs_inverse_n(read_rows(Path(args.input)), output_dir)
    print(f"Wrote {len(fits)} extrapolation rows to {output_dir}")


if __name__ == "__main__":
    main()
