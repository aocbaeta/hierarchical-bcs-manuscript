"""Parameter sweeps for the finite BCS hierarchy benchmark."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from bcs_core import bcs_gap_iteration, default_model, exact_ground_state, hierarchy_residual


def run_sweep(levels_values: list[int], g_values: np.ndarray) -> list[dict]:
    rows: list[dict] = []
    for levels in levels_values:
        for g in g_values:
            model = default_model(n_levels=levels, g=float(g))
            exact = exact_ground_state(model)
            closure = bcs_gap_iteration(model)
            residual = hierarchy_residual(model, exact["state"])
            rows.append(
                {
                    "levels": levels,
                    "qubits": model.n_modes,
                    "g": float(g),
                    "exact_energy": exact["energy"],
                    "bcs_energy": closure["energy_mean_field"],
                    "energy_error": closure["energy_mean_field"] - exact["energy"],
                    "gap": closure["delta"],
                    "leading_pair_density_eigenvalue": residual["leading_pair_density_eigenvalue"],
                    "relative_pair_density_residual": residual["relative_pair_density_residual"],
                }
            )
    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_by_levels(rows: list[dict], output_dir: Path) -> None:
    levels_values = sorted({row["levels"] for row in rows})

    def arr(levels: int, key: str) -> np.ndarray:
        subset = [row for row in rows if row["levels"] == levels]
        subset.sort(key=lambda item: item["g"])
        return np.array([row[key] for row in subset], dtype=float)

    for ylabel, key, filename in [
        ("Energy error: E_BCS - E_exact", "energy_error", "energy_error_vs_g.png"),
        ("BCS gap Delta", "gap", "gap_vs_g.png"),
        ("Relative pair-density residual", "relative_pair_density_residual", "pair_residual_vs_g.png"),
        ("Leading pair-density eigenvalue", "leading_pair_density_eigenvalue", "pair_eigenvalue_vs_g.png"),
    ]:
        plt.figure(figsize=(7.0, 4.6))
        for levels in levels_values:
            plt.plot(arr(levels, "g"), arr(levels, key), marker="o", linewidth=1.8, label=f"N={levels}")
        plt.xlabel("pairing strength g")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend(title="levels")
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=180)
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="3,4,5", help="comma-separated level counts")
    parser.add_argument("--g-min", type=float, default=0.1)
    parser.add_argument("--g-max", type=float, default=1.4)
    parser.add_argument("--points", type=int, default=14)
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    levels_values = [int(item.strip()) for item in args.levels.split(",") if item.strip()]
    g_values = np.linspace(args.g_min, args.g_max, args.points)
    rows = run_sweep(levels_values, g_values)

    save_csv(rows, output_dir / "sweep_results.csv")
    plot_by_levels(rows, output_dir)

    print(f"Wrote {len(rows)} rows to {output_dir / 'sweep_results.csv'}")
    print(f"Wrote figures to {output_dir}")


if __name__ == "__main__":
    main()
